// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * build-glosser-dataset-chirho.ts
 * Builds the interlinear glossing dataset from Macula Hebrew + Greek TSVs.
 *
 * Groups words by verse, then creates:
 *   Input:  "gloss [greek]: Βίβλος γενέσεως Ἰησοῦ Χριστοῦ [MAT 1:1]"
 *   Target: "[The] book | of [the] genealogy | of Jesus | Christ"
 *
 * ~31K verses total (23K OT + 8K NT).
 * Splits 80/10/10 → {train,val,test}-glosser-chirho.jsonl
 */

import { readFile, writeFile, mkdir } from "fs/promises";

const BASE_DIR_CHIRHO = `${import.meta.dir}/../..`;
const RAW_DIR_CHIRHO = `${BASE_DIR_CHIRHO}/data-chirho/raw-chirho`;
const OUTPUT_DIR_CHIRHO = `${BASE_DIR_CHIRHO}/data-chirho/processed-chirho`;

const HEBREW_TSV_PATH_CHIRHO = `${RAW_DIR_CHIRHO}/macula-hebrew-chirho.tsv`;
const GREEK_TSV_PATH_CHIRHO = `${RAW_DIR_CHIRHO}/macula-greek-chirho.tsv`;

interface WordEntryChirho {
  refChirho: string;
  textChirho: string;
  glossChirho: string;
  englishChirho: string;
  afterChirho: string; // whitespace/punctuation after word
  transliterationChirho: string;
}

interface VerseChirho {
  refChirho: string;
  langChirho: string;
  bookChirho: string;
  wordsChirho: WordEntryChirho[];
}

interface GlosserExampleChirho {
  inputChirho: string;
  targetChirho: string;
  refChirho: string;
  langChirho: string;
  bookChirho: string;
  wordCountChirho: number;
}

function parseTsvToWordsChirho(contentChirho: string): WordEntryChirho[] {
  const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());
  if (linesChirho.length < 2) return [];

  const headerChirho = linesChirho[0].split("\t");
  const colIndexChirho: Record<string, number> = {};
  headerChirho.forEach((colChirho, iChirho) => {
    colIndexChirho[colChirho.trim()] = iChirho;
  });

  const getColChirho = (rowChirho: string[], nameChirho: string): string => {
    const idxChirho = colIndexChirho[nameChirho];
    if (idxChirho === undefined) return "";
    return (rowChirho[idxChirho] ?? "").trim();
  };

  const wordsChirho: WordEntryChirho[] = [];

  for (let iChirho = 1; iChirho < linesChirho.length; iChirho++) {
    const fieldsChirho = linesChirho[iChirho].split("\t");
    if (fieldsChirho.length < 10) continue;

    const textChirho = getColChirho(fieldsChirho, "text");
    if (!textChirho) continue;

    wordsChirho.push({
      refChirho: getColChirho(fieldsChirho, "ref"),
      textChirho,
      glossChirho: getColChirho(fieldsChirho, "gloss"),
      englishChirho: getColChirho(fieldsChirho, "english"),
      afterChirho: getColChirho(fieldsChirho, "after"),
      transliterationChirho: getColChirho(fieldsChirho, "transliteration"),
    });
  }

  return wordsChirho;
}

function extractVerseRefChirho(fullRefChirho: string): string {
  // "GEN 1:1!1" → "GEN 1:1" (strip word index)
  return fullRefChirho.replace(/![0-9]+$/, "").trim();
}

function extractBookChirho(refChirho: string): string {
  return refChirho.split(" ")[0] ?? "UNKNOWN";
}

function groupByVerseChirho(
  wordsChirho: WordEntryChirho[],
  langChirho: string
): VerseChirho[] {
  const versesMapChirho = new Map<string, WordEntryChirho[]>();

  for (const wordChirho of wordsChirho) {
    const verseRefChirho = extractVerseRefChirho(wordChirho.refChirho);
    const listChirho = versesMapChirho.get(verseRefChirho) ?? [];
    listChirho.push(wordChirho);
    versesMapChirho.set(verseRefChirho, listChirho);
  }

  const versesChirho: VerseChirho[] = [];
  for (const [refChirho, verseWordsChirho] of versesMapChirho) {
    versesChirho.push({
      refChirho,
      langChirho,
      bookChirho: extractBookChirho(refChirho),
      wordsChirho: verseWordsChirho,
    });
  }

  return versesChirho;
}

function buildGlosserExampleChirho(verseChirho: VerseChirho): GlosserExampleChirho | null {
  if (verseChirho.wordsChirho.length === 0) return null;

  // Build verse text — for Hebrew, include transliteration to help mT5
  // Format: "בְּרֵאשִׁית (bərēʾšiyṯ) בָּרָא (bārāʾ) אֱלֹהִים (ʾĕlōhiym)"
  const isHebrewChirho = verseChirho.langChirho === "hebrew";
  const verseTextChirho = verseChirho.wordsChirho
    .map((wChirho) => {
      if (isHebrewChirho && wChirho.transliterationChirho) {
        return `${wChirho.textChirho} (${wChirho.transliterationChirho})`;
      }
      return wChirho.textChirho;
    })
    .join(" ");

  // Build gloss target: word-by-word glosses joined by " | "
  // Prefer gloss, then english, then [?]
  const glossesChirho = verseChirho.wordsChirho
    .map((wChirho) => {
      const glossChirho = (wChirho.glossChirho || wChirho.englishChirho || "").trim();
      return glossChirho || "[?]";
    })
    .filter((gChirho) => gChirho.trim());

  if (glossesChirho.length === 0) return null;

  // Skip verses where too many glosses are empty/unknown
  const nonEmptyChirho = glossesChirho.filter((gChirho) => gChirho !== "[?]");
  if (nonEmptyChirho.length < verseChirho.wordsChirho.length * 0.5) return null;

  const inputChirho = `gloss [${verseChirho.langChirho}]: ${verseTextChirho} [${verseChirho.refChirho}]`;
  const targetChirho = glossesChirho.join(" | ");

  return {
    inputChirho,
    targetChirho,
    refChirho: verseChirho.refChirho,
    langChirho: verseChirho.langChirho,
    bookChirho: verseChirho.bookChirho,
    wordCountChirho: verseChirho.wordsChirho.length,
  };
}

function splitDatasetChirho(
  examplesChirho: GlosserExampleChirho[]
): {
  trainChirho: GlosserExampleChirho[];
  valChirho: GlosserExampleChirho[];
  testChirho: GlosserExampleChirho[];
} {
  const shuffledChirho = [...examplesChirho].sort(() => Math.random() - 0.5);

  const trainEndChirho = Math.floor(shuffledChirho.length * 0.8);
  const valEndChirho = Math.floor(shuffledChirho.length * 0.9);

  return {
    trainChirho: shuffledChirho.slice(0, trainEndChirho),
    valChirho: shuffledChirho.slice(trainEndChirho, valEndChirho),
    testChirho: shuffledChirho.slice(valEndChirho),
  };
}

async function writeJsonlChirho(
  pathChirho: string,
  examplesChirho: GlosserExampleChirho[]
): Promise<void> {
  const linesChirho = examplesChirho.map((exChirho) =>
    JSON.stringify({
      input_chirho: exChirho.inputChirho,
      target_chirho: exChirho.targetChirho,
      ref_chirho: exChirho.refChirho,
      lang_chirho: exChirho.langChirho,
      word_count_chirho: exChirho.wordCountChirho,
    })
  );
  await writeFile(pathChirho, linesChirho.join("\n") + "\n", "utf-8");
}

async function mainChirho(): Promise<void> {
  console.log("Glosser Dataset Builder");
  console.log("=======================\n");

  await mkdir(OUTPUT_DIR_CHIRHO, { recursive: true });

  // Load and parse Hebrew
  console.log("Loading Macula Hebrew TSV...");
  let hebrewVersesChirho: VerseChirho[] = [];
  try {
    const hebrewContentChirho = await readFile(HEBREW_TSV_PATH_CHIRHO, "utf-8");
    const hebrewWordsChirho = parseTsvToWordsChirho(hebrewContentChirho);
    console.log(`  Parsed ${hebrewWordsChirho.length} Hebrew words`);
    hebrewVersesChirho = groupByVerseChirho(hebrewWordsChirho, "hebrew");
    console.log(`  Grouped into ${hebrewVersesChirho.length} verses`);
  } catch (errorChirho) {
    console.error(`  Failed to load Hebrew TSV: ${errorChirho}`);
  }

  // Load and parse Greek
  console.log("Loading Macula Greek TSV...");
  let greekVersesChirho: VerseChirho[] = [];
  try {
    const greekContentChirho = await readFile(GREEK_TSV_PATH_CHIRHO, "utf-8");
    const greekWordsChirho = parseTsvToWordsChirho(greekContentChirho);
    console.log(`  Parsed ${greekWordsChirho.length} Greek words`);
    greekVersesChirho = groupByVerseChirho(greekWordsChirho, "greek");
    console.log(`  Grouped into ${greekVersesChirho.length} verses`);
  } catch (errorChirho) {
    console.error(`  Failed to load Greek TSV: ${errorChirho}`);
  }

  if (hebrewVersesChirho.length === 0 && greekVersesChirho.length === 0) {
    console.error("\nNo data loaded. Aborting.");
    process.exit(1);
  }

  // Build glosser examples
  console.log("\nBuilding glosser examples...");
  const allExamplesChirho: GlosserExampleChirho[] = [];

  let hebrewSkippedChirho = 0;
  for (const verseChirho of hebrewVersesChirho) {
    const exampleChirho = buildGlosserExampleChirho(verseChirho);
    if (exampleChirho) {
      allExamplesChirho.push(exampleChirho);
    } else {
      hebrewSkippedChirho++;
    }
  }
  const hebrewCountChirho = allExamplesChirho.length;
  console.log(`  Hebrew verses: ${hebrewCountChirho} (skipped ${hebrewSkippedChirho})`);

  let greekSkippedChirho = 0;
  for (const verseChirho of greekVersesChirho) {
    const exampleChirho = buildGlosserExampleChirho(verseChirho);
    if (exampleChirho) {
      allExamplesChirho.push(exampleChirho);
    } else {
      greekSkippedChirho++;
    }
  }
  const greekCountChirho = allExamplesChirho.length - hebrewCountChirho;
  console.log(`  Greek verses: ${greekCountChirho} (skipped ${greekSkippedChirho})`);
  console.log(`  Total: ${allExamplesChirho.length}`);

  // Split
  const { trainChirho, valChirho, testChirho } = splitDatasetChirho(allExamplesChirho);
  console.log(`\nSplit sizes:`);
  console.log(`  Train: ${trainChirho.length}`);
  console.log(`  Val:   ${valChirho.length}`);
  console.log(`  Test:  ${testChirho.length}`);

  // Write
  await writeJsonlChirho(`${OUTPUT_DIR_CHIRHO}/train-glosser-chirho.jsonl`, trainChirho);
  await writeJsonlChirho(`${OUTPUT_DIR_CHIRHO}/val-glosser-chirho.jsonl`, valChirho);
  await writeJsonlChirho(`${OUTPUT_DIR_CHIRHO}/test-glosser-chirho.jsonl`, testChirho);

  console.log(`\nFiles written to ${OUTPUT_DIR_CHIRHO}/`);

  // Show samples
  console.log("\n--- Sample Entries ---");
  for (const exChirho of trainChirho.slice(0, 3)) {
    console.log(`\n  Input:  ${exChirho.inputChirho.substring(0, 120)}...`);
    console.log(`  Target: ${exChirho.targetChirho.substring(0, 120)}...`);
    console.log(`  Words:  ${exChirho.wordCountChirho}`);
  }

  // Stats
  const avgWordsChirho =
    allExamplesChirho.reduce((sChirho, eChirho) => sChirho + eChirho.wordCountChirho, 0) /
    allExamplesChirho.length;
  console.log(`\nAverage words per verse: ${avgWordsChirho.toFixed(1)}`);
  console.log(`Hebrew verses: ${hebrewCountChirho}`);
  console.log(`Greek verses: ${greekCountChirho}`);

  const bookSetChirho = new Set(allExamplesChirho.map((eChirho) => eChirho.bookChirho));
  console.log(`Books represented: ${bookSetChirho.size}`);

  console.log("\nDone!");
}

mainChirho();
