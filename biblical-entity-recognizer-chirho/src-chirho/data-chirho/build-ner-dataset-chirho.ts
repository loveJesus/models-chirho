// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * build-ner-dataset-chirho.ts
 * Constructs a BIO-tagged NER dataset from KJV verses and TIPNR entity data.
 *
 * Process:
 * 1. Load KJV verses and TIPNR entities
 * 2. Build a name-to-entity-type lookup with divine name overrides
 * 3. For each verse, tokenize into words, then find and tag matching entities
 * 4. Use BIO scheme: B-TYPE for beginning of entity, I-TYPE for continuation, O for outside
 * 5. Split by book (not verse) into train/val/test (80/10/10) to prevent data leakage
 * 6. Output as JSONL files
 *
 * Entity types: PERSON, DIVINE, PEOPLE_GROUP, PLACE, EVENT, ARTIFACT
 */

import { readFile, writeFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;
const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

const KJV_FILE_CHIRHO = `${RAW_DIR_CHIRHO}kjv-chirho.json`;
const TIPNR_FILE_CHIRHO = `${RAW_DIR_CHIRHO}tipnr-chirho.json`;

// ============================================================
// Divine names and titles - these take priority over TIPNR data
// ============================================================

const DIVINE_NAMES_CHIRHO: string[] = [
  "God",
  "LORD",
  "Lord",
  "Jesus",
  "Christ",
  "Almighty",
  "Messiah",
  "Saviour",
  "Savior",
  "Redeemer",
  "Jehovah",
  "Immanuel",
  "Emmanuel",
];

const DIVINE_MULTI_WORD_CHIRHO: string[] = [
  "Holy Spirit",
  "Holy Ghost",
  "Jesus Christ",
  "Son of God",
  "Son of man",
  "Son of Man",
  "Lord God",
  "Lord Jesus",
  "Lord Jesus Christ",
  "God Almighty",
  "Lord of hosts",
  "LORD of hosts",
  "King of kings",
  "Lord of lords",
  "Lamb of God",
  "Ancient of days",
  "Ancient of Days",
  "Prince of Peace",
  "Mighty God",
  "I AM",
  "I am",
  "Most High",
  "the Almighty",
];

// People groups that appear frequently in scripture
const PEOPLE_GROUPS_CHIRHO: string[] = [
  "Israel",
  "Israelites",
  "Philistines",
  "Egyptians",
  "Canaanites",
  "Amorites",
  "Hittites",
  "Perizzites",
  "Hivites",
  "Jebusites",
  "Moabites",
  "Ammonites",
  "Edomites",
  "Midianites",
  "Amalekites",
  "Assyrians",
  "Babylonians",
  "Chaldeans",
  "Persians",
  "Greeks",
  "Romans",
  "Samaritans",
  "Sadducees",
  "Pharisees",
  "Gentiles",
  "Jews",
  "Hebrews",
  "Levites",
  "Benjamites",
  "Danites",
  "Gibeonites",
  "Zidonians",
  "Sidonians",
];

// Notable events
const EVENTS_CHIRHO: string[] = [
  "Passover",
  "Pentecost",
  "Sabbath",
  "Jubilee",
  "Purim",
];

// Notable artifacts/objects
const ARTIFACTS_CHIRHO: string[] = [
  "Urim",
  "Thummim",
];

// ============================================================
// Types
// ============================================================

type EntityTypeChirho = "PERSON" | "DIVINE" | "PEOPLE_GROUP" | "PLACE" | "EVENT" | "ARTIFACT";

interface EntityLookupChirho {
  nameChirho: string;
  typeChirho: EntityTypeChirho;
  tokensChirho: string[]; // pre-split into words for matching
}

interface VerseDataChirho {
  bookIdChirho: number;
  bookNameChirho: string;
  chapterChirho: number;
  verseChirho: number;
  textChirho: string;
  referenceChirho: string;
}

interface NerExampleChirho {
  tokens_chirho: string[];
  ner_tags_chirho: string[];
  reference_chirho: string;
  book_name_chirho: string;
  book_id_chirho: number;
}

// ============================================================
// Entity lookup building
// ============================================================

function buildEntityLookupChirho(
  tipnrEntitiesChirho: Array<{
    nameChirho: string;
    typeChirho: string;
    alternateNamesChirho?: string[];
  }>
): EntityLookupChirho[] {
  const lookupChirho: EntityLookupChirho[] = [];
  const seenNamesChirho = new Set<string>();

  // 1. Add divine names (highest priority - these override TIPNR)
  for (const multiWordChirho of DIVINE_MULTI_WORD_CHIRHO) {
    const keyChirho = multiWordChirho.toLowerCase();
    if (!seenNamesChirho.has(keyChirho)) {
      lookupChirho.push({
        nameChirho: multiWordChirho,
        typeChirho: "DIVINE",
        tokensChirho: multiWordChirho.split(/\s+/),
      });
      seenNamesChirho.add(keyChirho);
    }
  }

  for (const divineNameChirho of DIVINE_NAMES_CHIRHO) {
    const keyChirho = divineNameChirho.toLowerCase();
    if (!seenNamesChirho.has(keyChirho)) {
      lookupChirho.push({
        nameChirho: divineNameChirho,
        typeChirho: "DIVINE",
        tokensChirho: [divineNameChirho],
      });
      seenNamesChirho.add(keyChirho);
    }
  }

  // 2. Add people groups
  for (const groupChirho of PEOPLE_GROUPS_CHIRHO) {
    const keyChirho = groupChirho.toLowerCase();
    if (!seenNamesChirho.has(keyChirho)) {
      lookupChirho.push({
        nameChirho: groupChirho,
        typeChirho: "PEOPLE_GROUP",
        tokensChirho: groupChirho.split(/\s+/),
      });
      seenNamesChirho.add(keyChirho);
    }
  }

  // 3. Add events
  for (const eventChirho of EVENTS_CHIRHO) {
    const keyChirho = eventChirho.toLowerCase();
    if (!seenNamesChirho.has(keyChirho)) {
      lookupChirho.push({
        nameChirho: eventChirho,
        typeChirho: "EVENT",
        tokensChirho: eventChirho.split(/\s+/),
      });
      seenNamesChirho.add(keyChirho);
    }
  }

  // 4. Add artifacts
  for (const artifactChirho of ARTIFACTS_CHIRHO) {
    const keyChirho = artifactChirho.toLowerCase();
    if (!seenNamesChirho.has(keyChirho)) {
      lookupChirho.push({
        nameChirho: artifactChirho,
        typeChirho: "ARTIFACT",
        tokensChirho: artifactChirho.split(/\s+/),
      });
      seenNamesChirho.add(keyChirho);
    }
  }

  // 5. Add TIPNR entities (won't override if already seen)
  for (const entityChirho of tipnrEntitiesChirho) {
    const namesChirho = [entityChirho.nameChirho, ...(entityChirho.alternateNamesChirho || [])];

    for (const nameChirho of namesChirho) {
      const cleanNameChirho = nameChirho.trim();
      if (cleanNameChirho.length < 2) continue;

      const keyChirho = cleanNameChirho.toLowerCase();
      if (seenNamesChirho.has(keyChirho)) continue;

      // Map TIPNR type to our entity type
      let mappedTypeChirho: EntityTypeChirho;
      const tipnrTypeChirho = entityChirho.typeChirho?.toUpperCase() || "PERSON";

      if (tipnrTypeChirho === "PERSON") mappedTypeChirho = "PERSON";
      else if (tipnrTypeChirho === "PLACE") mappedTypeChirho = "PLACE";
      else if (tipnrTypeChirho === "PEOPLE_GROUP") mappedTypeChirho = "PEOPLE_GROUP";
      else if (tipnrTypeChirho === "ARTIFACT") mappedTypeChirho = "ARTIFACT";
      else if (tipnrTypeChirho === "EVENT") mappedTypeChirho = "EVENT";
      else if (tipnrTypeChirho === "DIVINE") mappedTypeChirho = "DIVINE";
      else mappedTypeChirho = "PERSON";

      lookupChirho.push({
        nameChirho: cleanNameChirho,
        typeChirho: mappedTypeChirho,
        tokensChirho: cleanNameChirho.split(/\s+/),
      });
      seenNamesChirho.add(keyChirho);
    }
  }

  // Sort by token length descending so longer matches take precedence
  lookupChirho.sort((aChirho, bChirho) => bChirho.tokensChirho.length - aChirho.tokensChirho.length);

  return lookupChirho;
}

// ============================================================
// Tokenization and tagging
// ============================================================

/**
 * Tokenize a verse text into words, handling KJV punctuation.
 * Splits on whitespace, keeps punctuation attached to preceding word.
 */
function tokenizeVerseChirho(textChirho: string): string[] {
  // Split on whitespace
  const rawTokensChirho = textChirho.split(/\s+/).filter((tChirho) => tChirho.length > 0);
  return rawTokensChirho;
}

/**
 * Strip punctuation from a token for matching purposes.
 */
function stripPunctuationChirho(tokenChirho: string): string {
  return tokenChirho.replace(/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g, "");
}

/**
 * Check if two tokens match (case-insensitive, ignoring surrounding punctuation).
 */
function tokensMatchChirho(verseTokenChirho: string, entityTokenChirho: string): boolean {
  const cleanVerseChirho = stripPunctuationChirho(verseTokenChirho).toLowerCase();
  const cleanEntityChirho = stripPunctuationChirho(entityTokenChirho).toLowerCase();
  return cleanVerseChirho === cleanEntityChirho && cleanVerseChirho.length > 0;
}

/**
 * Tag a tokenized verse with BIO NER labels.
 * Uses longest-match-first strategy to handle overlapping entities.
 */
function tagVerseChirho(
  tokensChirho: string[],
  entityLookupChirho: EntityLookupChirho[]
): string[] {
  const tagsChirho: string[] = new Array(tokensChirho.length).fill("O");
  const taggedPositionsChirho = new Set<number>();

  // For each entity in the lookup (sorted by length, longest first)
  for (const entityChirho of entityLookupChirho) {
    const entityTokensChirho = entityChirho.tokensChirho;
    const entityLenChirho = entityTokensChirho.length;

    // Slide over the verse tokens looking for matches
    for (let iChirho = 0; iChirho <= tokensChirho.length - entityLenChirho; iChirho++) {
      // Skip if any position in this range is already tagged
      let alreadyTaggedChirho = false;
      for (let jChirho = 0; jChirho < entityLenChirho; jChirho++) {
        if (taggedPositionsChirho.has(iChirho + jChirho)) {
          alreadyTaggedChirho = true;
          break;
        }
      }
      if (alreadyTaggedChirho) continue;

      // Check if all tokens match
      let allMatchChirho = true;
      for (let jChirho = 0; jChirho < entityLenChirho; jChirho++) {
        if (!tokensMatchChirho(tokensChirho[iChirho + jChirho], entityTokensChirho[jChirho])) {
          allMatchChirho = false;
          break;
        }
      }

      if (allMatchChirho) {
        // Tag the matched tokens
        tagsChirho[iChirho] = `B-${entityChirho.typeChirho}`;
        taggedPositionsChirho.add(iChirho);

        for (let jChirho = 1; jChirho < entityLenChirho; jChirho++) {
          tagsChirho[iChirho + jChirho] = `I-${entityChirho.typeChirho}`;
          taggedPositionsChirho.add(iChirho + jChirho);
        }
      }
    }
  }

  return tagsChirho;
}

// ============================================================
// Dataset splitting (by book, not verse)
// ============================================================

/**
 * Split examples by book into train/val/test (80/10/10).
 * This prevents data leakage since verses in the same book share context.
 */
function splitByBookChirho(
  examplesChirho: NerExampleChirho[]
): {
  trainChirho: NerExampleChirho[];
  valChirho: NerExampleChirho[];
  testChirho: NerExampleChirho[];
} {
  // Group by book
  const bookGroupsChirho = new Map<number, NerExampleChirho[]>();
  for (const exampleChirho of examplesChirho) {
    const bookIdChirho = exampleChirho.book_id_chirho;
    if (!bookGroupsChirho.has(bookIdChirho)) {
      bookGroupsChirho.set(bookIdChirho, []);
    }
    bookGroupsChirho.get(bookIdChirho)!.push(exampleChirho);
  }

  // Get all book IDs sorted
  const bookIdsChirho = Array.from(bookGroupsChirho.keys()).sort((aChirho, bChirho) => aChirho - bChirho);

  // Deterministic split: assign books to splits based on position
  // Use a fixed seed-like approach: spread books across splits
  // Books 1-66, we want ~80% train, ~10% val, ~10% test
  // Strategy: every 10th book to val, every 10th+5 to test, rest to train
  const trainBooksChirho: number[] = [];
  const valBooksChirho: number[] = [];
  const testBooksChirho: number[] = [];

  for (let iChirho = 0; iChirho < bookIdsChirho.length; iChirho++) {
    const bookIdChirho = bookIdsChirho[iChirho];
    const modChirho = iChirho % 10;
    if (modChirho === 3) {
      valBooksChirho.push(bookIdChirho);
    } else if (modChirho === 7) {
      testBooksChirho.push(bookIdChirho);
    } else {
      trainBooksChirho.push(bookIdChirho);
    }
  }

  const trainChirho: NerExampleChirho[] = [];
  const valChirho: NerExampleChirho[] = [];
  const testChirho: NerExampleChirho[] = [];

  for (const bookIdChirho of trainBooksChirho) {
    trainChirho.push(...(bookGroupsChirho.get(bookIdChirho) || []));
  }
  for (const bookIdChirho of valBooksChirho) {
    valChirho.push(...(bookGroupsChirho.get(bookIdChirho) || []));
  }
  for (const bookIdChirho of testBooksChirho) {
    testChirho.push(...(bookGroupsChirho.get(bookIdChirho) || []));
  }

  console.log(`  Train books (${trainBooksChirho.length}): ${trainBooksChirho.join(", ")}`);
  console.log(`  Val books (${valBooksChirho.length}): ${valBooksChirho.join(", ")}`);
  console.log(`  Test books (${testBooksChirho.length}): ${testBooksChirho.join(", ")}`);

  return { trainChirho, valChirho, testChirho };
}

// ============================================================
// JSONL writing
// ============================================================

async function writeJsonlChirho(
  pathChirho: string,
  examplesChirho: NerExampleChirho[]
): Promise<void> {
  const linesChirho = examplesChirho.map((exChirho) =>
    JSON.stringify({
      tokens_chirho: exChirho.tokens_chirho,
      ner_tags_chirho: exChirho.ner_tags_chirho,
      reference_chirho: exChirho.reference_chirho,
    })
  );
  await writeFile(pathChirho, linesChirho.join("\n") + "\n", "utf-8");
}

// ============================================================
// Main pipeline
// ============================================================

async function mainChirho(): Promise<void> {
  console.log("NER Dataset Builder");
  console.log("===================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  // Load KJV data
  console.log("Loading KJV verses...");
  let kjvDataChirho: { versesChirho: VerseDataChirho[] };
  try {
    const kjvContentChirho = await readFile(KJV_FILE_CHIRHO, "utf-8");
    kjvDataChirho = JSON.parse(kjvContentChirho);
  } catch (errorChirho) {
    console.error(`Failed to load KJV data from ${KJV_FILE_CHIRHO}`);
    console.error("Run 'bun run download-kjv-chirho' first.");
    process.exit(1);
  }
  console.log(`  Loaded ${kjvDataChirho.versesChirho.length} verses`);

  // Load TIPNR data
  console.log("Loading TIPNR entities...");
  let tipnrDataChirho: {
    entitiesChirho: Array<{
      nameChirho: string;
      typeChirho: string;
      alternateNamesChirho?: string[];
    }>;
  };
  try {
    const tipnrContentChirho = await readFile(TIPNR_FILE_CHIRHO, "utf-8");
    tipnrDataChirho = JSON.parse(tipnrContentChirho);
  } catch (errorChirho) {
    console.error(`Failed to load TIPNR data from ${TIPNR_FILE_CHIRHO}`);
    console.error("Run 'bun run download-tipnr-chirho' first.");
    process.exit(1);
  }
  console.log(`  Loaded ${tipnrDataChirho.entitiesChirho.length} entities`);

  // Build entity lookup
  console.log("\nBuilding entity lookup table...");
  const entityLookupChirho = buildEntityLookupChirho(tipnrDataChirho.entitiesChirho);
  console.log(`  Total entity patterns: ${entityLookupChirho.length}`);

  // Type distribution in lookup
  const lookupTypeCountsChirho: Record<string, number> = {};
  for (const entChirho of entityLookupChirho) {
    lookupTypeCountsChirho[entChirho.typeChirho] =
      (lookupTypeCountsChirho[entChirho.typeChirho] || 0) + 1;
  }
  console.log("  Lookup type distribution:");
  for (const [typeChirho, countChirho] of Object.entries(lookupTypeCountsChirho)) {
    console.log(`    ${typeChirho}: ${countChirho}`);
  }

  // Process all verses
  console.log("\nTagging verses with NER labels...");
  const allExamplesChirho: NerExampleChirho[] = [];
  let entitiesFoundChirho = 0;
  let versesWithEntitiesChirho = 0;
  const tagDistributionChirho: Record<string, number> = {};

  const totalVersesChirho = kjvDataChirho.versesChirho.length;
  const progressIntervalChirho = Math.floor(totalVersesChirho / 20);

  for (let iChirho = 0; iChirho < totalVersesChirho; iChirho++) {
    const verseChirho = kjvDataChirho.versesChirho[iChirho];

    // Progress reporting
    if (iChirho > 0 && iChirho % progressIntervalChirho === 0) {
      const pctChirho = ((iChirho / totalVersesChirho) * 100).toFixed(0);
      console.log(
        `  Progress: ${pctChirho}% (${iChirho}/${totalVersesChirho}) - entities found: ${entitiesFoundChirho}`
      );
    }

    // Tokenize the verse
    const tokensChirho = tokenizeVerseChirho(verseChirho.textChirho);
    if (tokensChirho.length === 0) continue;

    // Tag the tokens
    const tagsChirho = tagVerseChirho(tokensChirho, entityLookupChirho);

    // Count entities in this verse
    let hasEntityChirho = false;
    for (const tagChirho of tagsChirho) {
      tagDistributionChirho[tagChirho] = (tagDistributionChirho[tagChirho] || 0) + 1;
      if (tagChirho.startsWith("B-")) {
        entitiesFoundChirho++;
        hasEntityChirho = true;
      }
    }
    if (hasEntityChirho) {
      versesWithEntitiesChirho++;
    }

    allExamplesChirho.push({
      tokens_chirho: tokensChirho,
      ner_tags_chirho: tagsChirho,
      reference_chirho: `${verseChirho.bookNameChirho} ${verseChirho.chapterChirho}:${verseChirho.verseChirho}`,
      book_name_chirho: verseChirho.bookNameChirho,
      book_id_chirho: verseChirho.bookIdChirho,
    });
  }

  console.log(`\n  Total examples: ${allExamplesChirho.length}`);
  console.log(`  Verses with entities: ${versesWithEntitiesChirho} (${((versesWithEntitiesChirho / allExamplesChirho.length) * 100).toFixed(1)}%)`);
  console.log(`  Total entities tagged: ${entitiesFoundChirho}`);

  console.log("\n  Tag distribution:");
  for (const [tagChirho, countChirho] of Object.entries(tagDistributionChirho).sort(
    (aChirho, bChirho) => bChirho[1] - aChirho[1]
  )) {
    console.log(`    ${tagChirho}: ${countChirho}`);
  }

  // Split by book
  console.log("\nSplitting by book (80/10/10)...");
  const { trainChirho, valChirho, testChirho } = splitByBookChirho(allExamplesChirho);
  console.log(`  Train: ${trainChirho.length} examples`);
  console.log(`  Validation: ${valChirho.length} examples`);
  console.log(`  Test: ${testChirho.length} examples`);

  // Write JSONL files
  console.log("\nWriting JSONL output files...");

  await writeJsonlChirho(`${PROCESSED_DIR_CHIRHO}train-chirho.jsonl`, trainChirho);
  console.log(`  train-chirho.jsonl: ${trainChirho.length} examples`);

  await writeJsonlChirho(`${PROCESSED_DIR_CHIRHO}val-chirho.jsonl`, valChirho);
  console.log(`  val-chirho.jsonl: ${valChirho.length} examples`);

  await writeJsonlChirho(`${PROCESSED_DIR_CHIRHO}test-chirho.jsonl`, testChirho);
  console.log(`  test-chirho.jsonl: ${testChirho.length} examples`);

  // Show sample annotations
  console.log("\n  Sample annotations:");
  const sampleExamplesChirho = allExamplesChirho
    .filter((exChirho) => exChirho.ner_tags_chirho.some((tChirho) => tChirho !== "O"))
    .slice(0, 5);

  for (const sampleChirho of sampleExamplesChirho) {
    console.log(`\n  ${sampleChirho.reference_chirho}:`);
    const annotatedChirho: string[] = [];
    for (let iChirho = 0; iChirho < sampleChirho.tokens_chirho.length; iChirho++) {
      const tokenChirho = sampleChirho.tokens_chirho[iChirho];
      const tagChirho = sampleChirho.ner_tags_chirho[iChirho];
      if (tagChirho !== "O") {
        annotatedChirho.push(`[${tokenChirho}/${tagChirho}]`);
      } else {
        annotatedChirho.push(tokenChirho);
      }
    }
    console.log(`    ${annotatedChirho.join(" ")}`);
  }

  // Write metadata
  const metadataChirho = {
    generatedAtChirho: new Date().toISOString(),
    totalExamplesChirho: allExamplesChirho.length,
    trainCountChirho: trainChirho.length,
    valCountChirho: valChirho.length,
    testCountChirho: testChirho.length,
    totalEntitiesTaggedChirho: entitiesFoundChirho,
    versesWithEntitiesChirho,
    tagDistributionChirho,
    entityLookupSizeChirho: entityLookupChirho.length,
  };
  await writeFile(
    `${PROCESSED_DIR_CHIRHO}metadata-chirho.json`,
    JSON.stringify(metadataChirho, null, 2),
    "utf-8"
  );

  console.log("\nDone! Dataset built successfully.");
}

mainChirho();
