// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * build-topical-dataset-chirho.ts
 * Builds training data for topical passage search from two sources:
 *
 * 1. Nave's Topical Bible: (topic_text, verse_text) positive pairs
 *    - Each topic heading becomes a query, matched to its referenced verses
 *    - Creates natural-language topical search pairs
 *
 * 2. TSK Cross-References: (verse_A, verse_B) topically related pairs
 *    - Cross-referenced verses share thematic/topical connections
 *    - Teaches the model that related passages cluster together
 *
 * Uses MultipleNegativesRankingLoss format: {"query_chirho", "positive_chirho"}
 * In-batch negatives mean we only need positive pairs.
 *
 * Target: ~170,000 training pairs, split 80/10/10
 *
 * Output: data-chirho/processed-chirho/{train,val,test}-topical-chirho.jsonl
 */

import { readFile, writeFile, mkdir } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;
const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

const MAX_TRAINING_PAIRS_CHIRHO = 170000;
const TRAIN_SPLIT_CHIRHO = 0.8;
const VAL_SPLIT_CHIRHO = 0.1;
// test is the remainder

interface TopicalPairChirho {
  queryChirho: string;
  positiveChirho: string;
  sourceChirho: string; // "naves" or "crossref"
}

interface NavesDataChirho {
  metaChirho: {
    totalTopicsChirho: number;
    totalReferencesChirho: number;
  };
  topicsChirho: Array<{
    topicChirho: string;
    subtopicChirho: string;
    referencesChirho: string[];
  }>;
}

// ============================================================
// KJV BIBLE LOADING
// ============================================================

/** Book name normalization map: various forms -> canonical short name */
const BOOK_ALIASES_CHIRHO: Record<string, string> = {
  // OT
  genesis: "Gen", gen: "Gen", ge: "Gen",
  exodus: "Exod", exod: "Exod", exo: "Exod", ex: "Exod",
  leviticus: "Lev", lev: "Lev", le: "Lev",
  numbers: "Num", num: "Num", nu: "Num",
  deuteronomy: "Deut", deut: "Deut", de: "Deut", dt: "Deut",
  joshua: "Josh", josh: "Josh", jos: "Josh",
  judges: "Judg", judg: "Judg", jdg: "Judg",
  ruth: "Ruth", ru: "Ruth",
  "1 samuel": "1Sam", "1samuel": "1Sam", "1sam": "1Sam", "1sa": "1Sam", "i samuel": "1Sam",
  "2 samuel": "2Sam", "2samuel": "2Sam", "2sam": "2Sam", "2sa": "2Sam", "ii samuel": "2Sam",
  "1 kings": "1Kgs", "1kings": "1Kgs", "1kgs": "1Kgs", "1ki": "1Kgs", "i kings": "1Kgs",
  "2 kings": "2Kgs", "2kings": "2Kgs", "2kgs": "2Kgs", "2ki": "2Kgs", "ii kings": "2Kgs",
  "1 chronicles": "1Chr", "1chronicles": "1Chr", "1chr": "1Chr", "1ch": "1Chr", "i chronicles": "1Chr",
  "2 chronicles": "2Chr", "2chronicles": "2Chr", "2chr": "2Chr", "2ch": "2Chr", "ii chronicles": "2Chr",
  ezra: "Ezra", ezr: "Ezra",
  nehemiah: "Neh", neh: "Neh", ne: "Neh",
  esther: "Esth", esth: "Esth", est: "Esth", es: "Esth",
  job: "Job", jb: "Job",
  psalms: "Ps", psalm: "Ps", ps: "Ps", psa: "Ps",
  proverbs: "Prov", prov: "Prov", pro: "Prov", pr: "Prov",
  ecclesiastes: "Eccl", eccl: "Eccl", ecc: "Eccl", ec: "Eccl",
  "song of solomon": "Song", "songs": "Song", song: "Song", "sos": "Song", "ss": "Song", "song of songs": "Song",
  isaiah: "Isa", isa: "Isa", is: "Isa",
  jeremiah: "Jer", jer: "Jer", je: "Jer",
  lamentations: "Lam", lam: "Lam", la: "Lam",
  ezekiel: "Ezek", ezek: "Ezek", eze: "Ezek",
  daniel: "Dan", dan: "Dan", da: "Dan",
  hosea: "Hos", hos: "Hos", ho: "Hos",
  joel: "Joel", joe: "Joel",
  amos: "Amos", am: "Amos",
  obadiah: "Obad", obad: "Obad", ob: "Obad",
  jonah: "Jonah", jon: "Jonah",
  micah: "Mic", mic: "Mic",
  nahum: "Nah", nah: "Nah", na: "Nah",
  habakkuk: "Hab", hab: "Hab",
  zephaniah: "Zeph", zeph: "Zeph", zep: "Zeph",
  haggai: "Hag", hag: "Hag",
  zechariah: "Zech", zech: "Zech", zec: "Zech",
  malachi: "Mal", mal: "Mal",
  // NT
  matthew: "Matt", matt: "Matt", mat: "Matt", mt: "Matt",
  mark: "Mark", mar: "Mark", mk: "Mark", mr: "Mark",
  luke: "Luke", luk: "Luke", lu: "Luke",
  john: "John", joh: "John", jn: "John",
  acts: "Acts", act: "Acts", ac: "Acts",
  romans: "Rom", rom: "Rom", ro: "Rom",
  "1 corinthians": "1Cor", "1corinthians": "1Cor", "1cor": "1Cor", "1co": "1Cor", "i corinthians": "1Cor",
  "2 corinthians": "2Cor", "2corinthians": "2Cor", "2cor": "2Cor", "2co": "2Cor", "ii corinthians": "2Cor",
  galatians: "Gal", gal: "Gal", ga: "Gal",
  ephesians: "Eph", eph: "Eph",
  philippians: "Phil", phil: "Phil", php: "Phil",
  colossians: "Col", col: "Col",
  "1 thessalonians": "1Thess", "1thessalonians": "1Thess", "1thess": "1Thess", "1th": "1Thess", "i thessalonians": "1Thess",
  "2 thessalonians": "2Thess", "2thessalonians": "2Thess", "2thess": "2Thess", "2th": "2Thess", "ii thessalonians": "2Thess",
  "1 timothy": "1Tim", "1timothy": "1Tim", "1tim": "1Tim", "1ti": "1Tim", "i timothy": "1Tim",
  "2 timothy": "2Tim", "2timothy": "2Tim", "2tim": "2Tim", "2ti": "2Tim", "ii timothy": "2Tim",
  titus: "Titus", tit: "Titus",
  philemon: "Phlm", phlm: "Phlm", phm: "Phlm",
  hebrews: "Heb", heb: "Heb",
  james: "Jas", jas: "Jas",
  "1 peter": "1Pet", "1peter": "1Pet", "1pet": "1Pet", "1pe": "1Pet", "i peter": "1Pet",
  "2 peter": "2Pet", "2peter": "2Pet", "2pet": "2Pet", "2pe": "2Pet", "ii peter": "2Pet",
  "1 john": "1John", "1john": "1John", "1jn": "1John", "i john": "1John",
  "2 john": "2John", "2john": "2John", "2jn": "2John", "ii john": "2John",
  "3 john": "3John", "3john": "3John", "3jn": "3John", "iii john": "3John",
  jude: "Jude",
  revelation: "Rev", rev: "Rev", re: "Rev",
  revelations: "Rev",
};

function parseCsvLineChirho(lineChirho: string): string[] {
  const fieldsChirho: string[] = [];
  let currentChirho = "";
  let inQuotesChirho = false;

  for (let iChirho = 0; iChirho < lineChirho.length; iChirho++) {
    const charChirho = lineChirho[iChirho];
    if (charChirho === '"') {
      inQuotesChirho = !inQuotesChirho;
    } else if (charChirho === "," && !inQuotesChirho) {
      fieldsChirho.push(currentChirho.trim());
      currentChirho = "";
    } else {
      currentChirho += charChirho;
    }
  }
  fieldsChirho.push(currentChirho.trim());
  return fieldsChirho;
}

/**
 * Normalize a book name to our canonical short form.
 * Handles CSV book names like "Genesis", OSIS like "Gen",
 * and Nave's references like "Ge" or "1 Samuel".
 */
function normalizeBookChirho(rawBookChirho: string): string {
  const cleanedChirho = rawBookChirho
    .replace(/^"|"$/g, "")
    .trim()
    .toLowerCase()
    .replace(/\./g, "");

  if (BOOK_ALIASES_CHIRHO[cleanedChirho]) {
    return BOOK_ALIASES_CHIRHO[cleanedChirho];
  }

  // Try prefix matching for abbreviations
  for (const [aliasChirho, canonicalChirho] of Object.entries(BOOK_ALIASES_CHIRHO)) {
    if (aliasChirho.startsWith(cleanedChirho) || cleanedChirho.startsWith(aliasChirho)) {
      return canonicalChirho;
    }
  }

  return rawBookChirho.trim();
}

/**
 * Load the KJV Bible into a lookup map: "Book.Chapter.Verse" -> text
 * Also creates a secondary map with canonical short book names.
 */
async function loadKjvChirho(): Promise<Map<string, string>> {
  const filePathChirho = `${RAW_DIR_CHIRHO}kjv-chirho.csv`;
  const contentChirho = await readFile(filePathChirho, "utf-8");
  const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());

  const versesChirho = new Map<string, string>();

  for (const lineChirho of linesChirho) {
    const fieldsChirho = parseCsvLineChirho(lineChirho);
    if (fieldsChirho.length < 4) continue;

    const bookRawChirho = fieldsChirho[0]?.replace(/^"|"$/g, "").trim();
    const chapterChirho = fieldsChirho[1]?.trim();
    const verseNumChirho = fieldsChirho[2]?.trim();
    const textChirho = fieldsChirho[3]?.replace(/^"|"$/g, "").trim();

    if (!textChirho || !chapterChirho || isNaN(parseInt(chapterChirho))) continue;

    const canonicalBookChirho = normalizeBookChirho(bookRawChirho);

    // Store under multiple keys for flexible lookup
    const keysChirho = [
      `${canonicalBookChirho}.${chapterChirho}.${verseNumChirho}`,
      `${bookRawChirho}.${chapterChirho}.${verseNumChirho}`,
      `${bookRawChirho.toLowerCase()}.${chapterChirho}.${verseNumChirho}`,
    ];

    for (const keyChirho of keysChirho) {
      versesChirho.set(keyChirho, textChirho);
    }
  }

  return versesChirho;
}

// ============================================================
// REFERENCE PARSING
// ============================================================

/**
 * Parse a Bible reference string into (book, chapter, verse) components.
 * Handles formats like:
 *   "Genesis 1:1", "Gen.1.1", "Gen 1:1", "1 John 3:16",
 *   "Psalm 23:1-3" (returns just verse 1), "Ge 1:1"
 */
function parseReferenceChirho(
  refChirho: string
): { bookChirho: string; chapterChirho: string; verseChirho: string } | null {
  const cleanedChirho = refChirho.trim().replace(/[;,]$/, "");

  // Pattern: "Book Chapter:Verse" or "Book.Chapter.Verse"
  // Handle numbered books: "1 John 3:16", "2 Samuel 7:12"
  const matchChirho = cleanedChirho.match(
    /^(\d?\s*[A-Za-z]+(?:\s+of\s+[A-Za-z]+)?)\s*[.\s]+(\d+)[:.]\s*(\d+)/
  );

  if (matchChirho) {
    const bookChirho = normalizeBookChirho(matchChirho[1]);
    return {
      bookChirho,
      chapterChirho: matchChirho[2],
      verseChirho: matchChirho[3],
    };
  }

  // Try OSIS format: "Gen.1.1"
  const osisMatchChirho = cleanedChirho.match(
    /^(\d?[A-Za-z]+)\.(\d+)\.(\d+)/
  );
  if (osisMatchChirho) {
    const bookChirho = normalizeBookChirho(osisMatchChirho[1]);
    return {
      bookChirho,
      chapterChirho: osisMatchChirho[2],
      verseChirho: osisMatchChirho[3],
    };
  }

  // Try simple format: "Gen 1:1"
  const simpleMatchChirho = cleanedChirho.match(
    /^(\d?\s*[A-Za-z]+)\s+(\d+):(\d+)/
  );
  if (simpleMatchChirho) {
    const bookChirho = normalizeBookChirho(simpleMatchChirho[1]);
    return {
      bookChirho,
      chapterChirho: simpleMatchChirho[2],
      verseChirho: simpleMatchChirho[3],
    };
  }

  return null;
}

/**
 * Look up verse text from the KJV map using a reference string.
 */
function lookupVerseChirho(
  refChirho: string,
  kjvMapChirho: Map<string, string>
): string | null {
  const parsedChirho = parseReferenceChirho(refChirho);
  if (!parsedChirho) return null;

  const keyChirho = `${parsedChirho.bookChirho}.${parsedChirho.chapterChirho}.${parsedChirho.verseChirho}`;
  const textChirho = kjvMapChirho.get(keyChirho);
  if (textChirho) return textChirho;

  // Fallback: try all entries with matching chapter/verse
  for (const [mapKeyChirho, mapValueChirho] of kjvMapChirho) {
    if (
      mapKeyChirho.endsWith(
        `.${parsedChirho.chapterChirho}.${parsedChirho.verseChirho}`
      )
    ) {
      const mapBookChirho = mapKeyChirho.split(".")[0].toLowerCase();
      if (
        parsedChirho.bookChirho.toLowerCase().startsWith(mapBookChirho) ||
        mapBookChirho.startsWith(parsedChirho.bookChirho.toLowerCase())
      ) {
        return mapValueChirho;
      }
    }
  }

  return null;
}

// ============================================================
// NAVE'S TOPICAL PAIRS
// ============================================================

function buildNavesPairsChirho(
  navesDataChirho: NavesDataChirho,
  kjvMapChirho: Map<string, string>
): TopicalPairChirho[] {
  console.log("Building Nave's topical pairs...");
  const pairsChirho: TopicalPairChirho[] = [];
  let resolvedChirho = 0;
  let unresolvedChirho = 0;

  for (const topicEntryChirho of navesDataChirho.topicsChirho) {
    // Build the query from topic + subtopic
    let queryTextChirho = topicEntryChirho.topicChirho;
    if (
      topicEntryChirho.subtopicChirho &&
      topicEntryChirho.subtopicChirho !== topicEntryChirho.topicChirho
    ) {
      queryTextChirho = `${topicEntryChirho.topicChirho}: ${topicEntryChirho.subtopicChirho}`;
    }

    // Make query more natural for search
    const naturalQueryChirho = `What does the Bible say about ${queryTextChirho.toLowerCase()}?`;

    for (const refChirho of topicEntryChirho.referencesChirho) {
      const verseTextChirho = lookupVerseChirho(refChirho, kjvMapChirho);
      if (verseTextChirho && verseTextChirho.length >= 15) {
        // Use both the raw topic and natural question as queries (variety helps)
        pairsChirho.push({
          queryChirho: queryTextChirho,
          positiveChirho: verseTextChirho,
          sourceChirho: "naves",
        });

        // Also add the natural language query form
        pairsChirho.push({
          queryChirho: naturalQueryChirho,
          positiveChirho: verseTextChirho,
          sourceChirho: "naves",
        });

        resolvedChirho++;
      } else {
        unresolvedChirho++;
      }
    }
  }

  console.log(`  Resolved references: ${resolvedChirho}`);
  console.log(`  Unresolved references: ${unresolvedChirho}`);
  console.log(`  Total Nave's pairs: ${pairsChirho.length}`);

  return pairsChirho;
}

// ============================================================
// TSK CROSS-REFERENCE PAIRS
// ============================================================

async function buildCrossrefPairsChirho(
  kjvMapChirho: Map<string, string>
): Promise<TopicalPairChirho[]> {
  console.log("Building cross-reference pairs...");

  const filePathChirho = `${RAW_DIR_CHIRHO}cross-references-chirho.txt`;
  const contentChirho = await readFile(filePathChirho, "utf-8");
  const linesChirho = contentChirho
    .split("\n")
    .filter((lChirho) => lChirho.trim());

  const pairsChirho: TopicalPairChirho[] = [];
  let resolvedChirho = 0;
  let unresolvedChirho = 0;

  for (const lineChirho of linesChirho) {
    // Skip comments and header
    if (lineChirho.startsWith("#") || lineChirho.startsWith("From")) continue;

    const partsChirho = lineChirho.split("\t");
    if (partsChirho.length < 2) continue;

    const sourceRefChirho = partsChirho[0].trim();
    const targetRefChirho = partsChirho[1].trim();

    const sourceTextChirho = lookupVerseChirho(sourceRefChirho, kjvMapChirho);
    const targetTextChirho = lookupVerseChirho(targetRefChirho, kjvMapChirho);

    if (
      sourceTextChirho &&
      targetTextChirho &&
      sourceTextChirho.length >= 15 &&
      targetTextChirho.length >= 15 &&
      sourceTextChirho !== targetTextChirho
    ) {
      pairsChirho.push({
        queryChirho: sourceTextChirho,
        positiveChirho: targetTextChirho,
        sourceChirho: "crossref",
      });
      resolvedChirho++;
    } else {
      unresolvedChirho++;
    }
  }

  console.log(`  Resolved cross-refs: ${resolvedChirho}`);
  console.log(`  Unresolved cross-refs: ${unresolvedChirho}`);
  console.log(`  Total cross-ref pairs: ${pairsChirho.length}`);

  return pairsChirho;
}

// ============================================================
// SHUFFLE + SPLIT
// ============================================================

function shuffleChirho<T>(arrChirho: T[]): T[] {
  const shuffledChirho = [...arrChirho];
  for (let iChirho = shuffledChirho.length - 1; iChirho > 0; iChirho--) {
    const jChirho = Math.floor(Math.random() * (iChirho + 1));
    [shuffledChirho[iChirho], shuffledChirho[jChirho]] = [
      shuffledChirho[jChirho],
      shuffledChirho[iChirho],
    ];
  }
  return shuffledChirho;
}

// ============================================================
// MAIN
// ============================================================

async function mainChirho(): Promise<void> {
  console.log("Topical Passage Dataset Builder");
  console.log("================================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  // 1. Load KJV Bible
  console.log("Loading KJV Bible...");
  const kjvMapChirho = await loadKjvChirho();
  console.log(`  Loaded ${kjvMapChirho.size} verse entries\n`);

  // 2. Load Nave's Topical Bible
  console.log("Loading Nave's Topical Bible...");
  const navesPathChirho = `${RAW_DIR_CHIRHO}naves-topical-chirho.json`;
  const navesRawChirho = await readFile(navesPathChirho, "utf-8");
  const navesDataChirho: NavesDataChirho = JSON.parse(navesRawChirho);
  console.log(`  Topics: ${navesDataChirho.topicsChirho.length}\n`);

  // 3. Build Nave's pairs
  const navesPairsChirho = buildNavesPairsChirho(navesDataChirho, kjvMapChirho);
  console.log();

  // 4. Build cross-reference pairs
  const crossrefPairsChirho = await buildCrossrefPairsChirho(kjvMapChirho);
  console.log();

  // 5. Combine all pairs
  let allPairsChirho = [...navesPairsChirho, ...crossrefPairsChirho];
  console.log(`Combined total: ${allPairsChirho.length} pairs`);

  // 6. Cap at max training pairs
  if (allPairsChirho.length > MAX_TRAINING_PAIRS_CHIRHO) {
    console.log(`  Capping at ${MAX_TRAINING_PAIRS_CHIRHO} pairs...`);

    // Keep a balanced mix: proportional sampling from each source
    const navesCountChirho = navesPairsChirho.length;
    const crossrefCountChirho = crossrefPairsChirho.length;
    const totalCountChirho = navesCountChirho + crossrefCountChirho;

    const navesTargetChirho = Math.floor(
      (navesCountChirho / totalCountChirho) * MAX_TRAINING_PAIRS_CHIRHO
    );
    const crossrefTargetChirho =
      MAX_TRAINING_PAIRS_CHIRHO - navesTargetChirho;

    const sampledNavesChirho = shuffleChirho(navesPairsChirho).slice(
      0,
      navesTargetChirho
    );
    const sampledCrossrefChirho = shuffleChirho(crossrefPairsChirho).slice(
      0,
      crossrefTargetChirho
    );

    allPairsChirho = [...sampledNavesChirho, ...sampledCrossrefChirho];
    console.log(
      `    Nave's: ${sampledNavesChirho.length}, Cross-refs: ${sampledCrossrefChirho.length}`
    );
  }

  // 7. Shuffle and split
  const shuffledChirho = shuffleChirho(allPairsChirho);
  const totalChirho = shuffledChirho.length;
  const trainEndChirho = Math.floor(totalChirho * TRAIN_SPLIT_CHIRHO);
  const valEndChirho = Math.floor(
    totalChirho * (TRAIN_SPLIT_CHIRHO + VAL_SPLIT_CHIRHO)
  );

  const trainChirho = shuffledChirho.slice(0, trainEndChirho);
  const valChirho = shuffledChirho.slice(trainEndChirho, valEndChirho);
  const testChirho = shuffledChirho.slice(valEndChirho);

  // 8. Write JSONL files
  const writeJsonlChirho = async (
    dataChirho: TopicalPairChirho[],
    fileNameChirho: string
  ) => {
    const outputChirho = dataChirho
      .map((pairChirho) =>
        JSON.stringify({
          query_chirho: pairChirho.queryChirho,
          positive_chirho: pairChirho.positiveChirho,
          source_chirho: pairChirho.sourceChirho,
        })
      )
      .join("\n");
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${fileNameChirho}`;
    await writeFile(pathChirho, outputChirho, "utf-8");
    console.log(`  Wrote ${pathChirho}: ${dataChirho.length} examples`);
  };

  console.log("\n================================");
  console.log("Writing dataset splits...");

  await writeJsonlChirho(trainChirho, "train-topical-chirho.jsonl");
  await writeJsonlChirho(valChirho, "val-topical-chirho.jsonl");
  await writeJsonlChirho(testChirho, "test-topical-chirho.jsonl");

  // 9. Compute and display source distribution
  const navesTrainChirho = trainChirho.filter(
    (pChirho) => pChirho.sourceChirho === "naves"
  ).length;
  const crossrefTrainChirho = trainChirho.filter(
    (pChirho) => pChirho.sourceChirho === "crossref"
  ).length;

  console.log("\n================================");
  console.log("Dataset Summary:");
  console.log(`  Total pairs: ${totalChirho}`);
  console.log(
    `  Sources: Nave's=${allPairsChirho.filter((pChirho) => pChirho.sourceChirho === "naves").length}, CrossRefs=${allPairsChirho.filter((pChirho) => pChirho.sourceChirho === "crossref").length}`
  );
  console.log(`  Train: ${trainChirho.length} (Naves: ${navesTrainChirho}, CrossRef: ${crossrefTrainChirho})`);
  console.log(`  Validation: ${valChirho.length}`);
  console.log(`  Test: ${testChirho.length}`);

  // Show a few samples
  console.log("\n  Sample pairs:");
  for (let iChirho = 0; iChirho < Math.min(5, trainChirho.length); iChirho++) {
    const sampleChirho = trainChirho[iChirho];
    console.log(`    [${sampleChirho.sourceChirho}] Q: "${sampleChirho.queryChirho.slice(0, 60)}..."`);
    console.log(`         P: "${sampleChirho.positiveChirho.slice(0, 60)}..."`);
  }

  console.log("\nDone!");
}

mainChirho();
