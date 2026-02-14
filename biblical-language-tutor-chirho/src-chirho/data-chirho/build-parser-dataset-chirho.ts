// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * build-parser-dataset-chirho.ts
 * Builds the morphological parser training dataset from Macula Hebrew + Greek TSVs.
 *
 * For each word, builds:
 *   Input:  "parse [hebrew]: בָּרָא [GEN 1:1] context: בְּרֵאשִׁית בָּרָא אֱלֹהִים"
 *   Target: "class:verb | stem:qal | lemma:ברא | tense:perfect | person:3 | gender:m | number:s | gloss:he created"
 *
 * Subsamples to ~200K total (100K Hebrew + 100K Greek), stratified by book.
 * Splits 80/10/10 → {train,val,test}-parser-chirho.jsonl
 *
 * Macula TSV columns (Hebrew):
 *   xml:id, ref, class, text, transliteration, after, strongnumberx, stronglemma,
 *   sensenumber, greek, greekstrong, gloss, english, mandarin, stem, morph, lang,
 *   lemma, pos, person, gender, number, state, type, lexdomain, contextualdomain,
 *   coredomain, sdbh, extends, frame, subjref, participantref
 */

import { readFile, writeFile, mkdir } from "fs/promises";

const BASE_DIR_CHIRHO = `${import.meta.dir}/../..`;
const RAW_DIR_CHIRHO = `${BASE_DIR_CHIRHO}/data-chirho/raw-chirho`;
const OUTPUT_DIR_CHIRHO = `${BASE_DIR_CHIRHO}/data-chirho/processed-chirho`;

const HEBREW_TSV_PATH_CHIRHO = `${RAW_DIR_CHIRHO}/macula-hebrew-chirho.tsv`;
const GREEK_TSV_PATH_CHIRHO = `${RAW_DIR_CHIRHO}/macula-greek-chirho.tsv`;

const TARGET_HEBREW_CHIRHO = 400_000; // Use ALL Hebrew words (was 100K)
const TARGET_GREEK_CHIRHO = 130_000; // Use ALL Greek words (was 100K)
const CONTEXT_WINDOW_CHIRHO = 3; // ±3 words for richer context (was ±2)

interface MaculaWordChirho {
  xmlIdChirho: string;
  refChirho: string;
  classChirho: string;
  textChirho: string;
  transliterationChirho: string;
  glossChirho: string;
  englishChirho: string;
  stemChirho: string;
  morphChirho: string;
  langChirho: string;
  lemmaChirho: string;
  posChirho: string;
  personChirho: string;
  genderChirho: string;
  numberChirho: string;
  stateChirho: string;
  typeChirho: string;
  strongNumberChirho: string;
}

interface ParserExampleChirho {
  inputChirho: string;
  targetChirho: string;
  refChirho: string;
  langChirho: string;
  bookChirho: string;
}

function parseTsvChirho(contentChirho: string): MaculaWordChirho[] {
  const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());
  if (linesChirho.length < 2) return [];

  const headerChirho = linesChirho[0].split("\t");
  const colIndexChirho: Record<string, number> = {};
  headerChirho.forEach((colChirho, iChirho) => {
    colIndexChirho[colChirho.trim()] = iChirho;
  });

  // Map column names — handle both possible naming conventions
  const getColChirho = (rowChirho: string[], nameChirho: string): string => {
    const idxChirho = colIndexChirho[nameChirho];
    if (idxChirho === undefined) return "";
    return (rowChirho[idxChirho] ?? "").trim();
  };

  const wordsChirho: MaculaWordChirho[] = [];

  for (let iChirho = 1; iChirho < linesChirho.length; iChirho++) {
    const fieldsChirho = linesChirho[iChirho].split("\t");
    if (fieldsChirho.length < 10) continue;

    const textChirho = getColChirho(fieldsChirho, "text");
    if (!textChirho) continue;

    wordsChirho.push({
      xmlIdChirho: getColChirho(fieldsChirho, "xml:id"),
      refChirho: getColChirho(fieldsChirho, "ref"),
      classChirho: getColChirho(fieldsChirho, "class"),
      textChirho,
      transliterationChirho: getColChirho(fieldsChirho, "transliteration"),
      glossChirho: getColChirho(fieldsChirho, "gloss"),
      englishChirho: getColChirho(fieldsChirho, "english"),
      stemChirho: getColChirho(fieldsChirho, "stem"),
      morphChirho: getColChirho(fieldsChirho, "morph"),
      langChirho: getColChirho(fieldsChirho, "lang"),
      lemmaChirho: getColChirho(fieldsChirho, "lemma"),
      posChirho: getColChirho(fieldsChirho, "pos"),
      personChirho: getColChirho(fieldsChirho, "person"),
      genderChirho: getColChirho(fieldsChirho, "gender"),
      numberChirho: getColChirho(fieldsChirho, "number"),
      stateChirho: getColChirho(fieldsChirho, "state"),
      typeChirho: getColChirho(fieldsChirho, "type"),
      strongNumberChirho: getColChirho(fieldsChirho, "strongnumberx"),
    });
  }

  return wordsChirho;
}

function extractBookChirho(refChirho: string): string {
  // Refs are like "GEN 1:1!1" or "MAT 1:1!1" — extract the book code
  const partsChirho = refChirho.split(" ");
  return partsChirho[0] ?? "UNKNOWN";
}

function formatRefChirho(refChirho: string): string {
  // Clean ref: "GEN 1:1!1" → "GEN 1:1"
  return refChirho.replace(/![0-9]+$/, "").trim();
}

function buildMorphTargetChirho(wordChirho: MaculaWordChirho): string {
  // Build pipe-separated morphological tag string
  const partsChirho: string[] = [];

  if (wordChirho.classChirho) partsChirho.push(`class:${wordChirho.classChirho}`);
  if (wordChirho.stemChirho) partsChirho.push(`stem:${wordChirho.stemChirho}`);
  if (wordChirho.lemmaChirho) partsChirho.push(`lemma:${wordChirho.lemmaChirho}`);
  if (wordChirho.posChirho) partsChirho.push(`pos:${wordChirho.posChirho}`);

  // Verbal features
  if (wordChirho.morphChirho) partsChirho.push(`morph:${wordChirho.morphChirho}`);
  if (wordChirho.personChirho) partsChirho.push(`person:${wordChirho.personChirho}`);
  if (wordChirho.genderChirho) partsChirho.push(`gender:${wordChirho.genderChirho}`);
  if (wordChirho.numberChirho) partsChirho.push(`number:${wordChirho.numberChirho}`);
  if (wordChirho.stateChirho) partsChirho.push(`state:${wordChirho.stateChirho}`);
  if (wordChirho.typeChirho) partsChirho.push(`type:${wordChirho.typeChirho}`);

  // Gloss — prefer gloss field, fall back to english
  const glossChirho = (wordChirho.glossChirho || wordChirho.englishChirho || "").trim();
  if (glossChirho) partsChirho.push(`gloss:${glossChirho}`);

  return partsChirho.join(" | ");
}

function buildExamplesChirho(
  wordsChirho: MaculaWordChirho[],
  langLabelChirho: string
): ParserExampleChirho[] {
  const examplesChirho: ParserExampleChirho[] = [];

  for (let iChirho = 0; iChirho < wordsChirho.length; iChirho++) {
    const wordChirho = wordsChirho[iChirho];

    // Skip words with no useful morphological info
    if (!wordChirho.classChirho && !wordChirho.lemmaChirho) continue;

    // Build context (±3 words with transliteration for Hebrew)
    const contextWordsChirho: string[] = [];
    for (
      let jChirho = Math.max(0, iChirho - CONTEXT_WINDOW_CHIRHO);
      jChirho <= Math.min(wordsChirho.length - 1, iChirho + CONTEXT_WINDOW_CHIRHO);
      jChirho++
    ) {
      if (jChirho !== iChirho) {
        contextWordsChirho.push(wordsChirho[jChirho].textChirho);
      }
    }

    const refCleanChirho = formatRefChirho(wordChirho.refChirho);
    const contextStrChirho = contextWordsChirho.join(" ");

    // Include transliteration for Hebrew to help mT5 tokenizer with nikud
    // Format: "parse [hebrew]: בָּרָא (bārāʾ) [GEN 1:1] context: בְּרֵאשִׁית אֱלֹהִים"
    const translitPartChirho = wordChirho.transliterationChirho
      ? ` (${wordChirho.transliterationChirho})`
      : "";
    const inputChirho = `parse [${langLabelChirho}]: ${wordChirho.textChirho}${translitPartChirho} [${refCleanChirho}] context: ${contextStrChirho}`;

    // Target format: "class:verb | stem:qal | lemma:ברא | ..."
    const targetChirho = buildMorphTargetChirho(wordChirho);

    if (!targetChirho) continue;

    examplesChirho.push({
      inputChirho,
      targetChirho,
      refChirho: refCleanChirho,
      langChirho: langLabelChirho,
      bookChirho: extractBookChirho(wordChirho.refChirho),
    });
  }

  return examplesChirho;
}

function stratifiedSampleChirho(
  examplesChirho: ParserExampleChirho[],
  targetCountChirho: number
): ParserExampleChirho[] {
  if (examplesChirho.length <= targetCountChirho) return examplesChirho;

  // Group by book
  const byBookChirho = new Map<string, ParserExampleChirho[]>();
  for (const exChirho of examplesChirho) {
    const listChirho = byBookChirho.get(exChirho.bookChirho) ?? [];
    listChirho.push(exChirho);
    byBookChirho.set(exChirho.bookChirho, listChirho);
  }

  // Proportional sampling from each book
  const ratioChirho = targetCountChirho / examplesChirho.length;
  const sampledChirho: ParserExampleChirho[] = [];

  for (const [_bookChirho, bookExamplesChirho] of byBookChirho) {
    const countChirho = Math.max(1, Math.round(bookExamplesChirho.length * ratioChirho));

    // Shuffle and take
    const shuffledChirho = [...bookExamplesChirho].sort(() => Math.random() - 0.5);
    sampledChirho.push(...shuffledChirho.slice(0, countChirho));
  }

  // If we're slightly over/under, trim or add
  if (sampledChirho.length > targetCountChirho) {
    return sampledChirho.slice(0, targetCountChirho);
  }

  return sampledChirho;
}

function splitDatasetChirho(
  examplesChirho: ParserExampleChirho[]
): {
  trainChirho: ParserExampleChirho[];
  valChirho: ParserExampleChirho[];
  testChirho: ParserExampleChirho[];
} {
  // Shuffle
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
  examplesChirho: ParserExampleChirho[]
): Promise<void> {
  const linesChirho = examplesChirho.map((exChirho) =>
    JSON.stringify({
      input_chirho: exChirho.inputChirho,
      target_chirho: exChirho.targetChirho,
      ref_chirho: exChirho.refChirho,
      lang_chirho: exChirho.langChirho,
    })
  );
  await writeFile(pathChirho, linesChirho.join("\n") + "\n", "utf-8");
}

async function mainChirho(): Promise<void> {
  console.log("Parser Dataset Builder");
  console.log("======================\n");

  await mkdir(OUTPUT_DIR_CHIRHO, { recursive: true });

  // Load Hebrew TSV
  console.log("Loading Macula Hebrew TSV...");
  let hebrewWordsChirho: MaculaWordChirho[] = [];
  try {
    const hebrewContentChirho = await readFile(HEBREW_TSV_PATH_CHIRHO, "utf-8");
    hebrewWordsChirho = parseTsvChirho(hebrewContentChirho);
    console.log(`  Parsed ${hebrewWordsChirho.length} Hebrew words`);
  } catch (errorChirho) {
    console.error(`  Failed to load Hebrew TSV: ${errorChirho}`);
    console.error("  Run 'bun run download-macula-chirho' first.");
  }

  // Load Greek TSV
  console.log("Loading Macula Greek TSV...");
  let greekWordsChirho: MaculaWordChirho[] = [];
  try {
    const greekContentChirho = await readFile(GREEK_TSV_PATH_CHIRHO, "utf-8");
    greekWordsChirho = parseTsvChirho(greekContentChirho);
    console.log(`  Parsed ${greekWordsChirho.length} Greek words`);
  } catch (errorChirho) {
    console.error(`  Failed to load Greek TSV: ${errorChirho}`);
    console.error("  Run 'bun run download-macula-chirho' first.");
  }

  if (hebrewWordsChirho.length === 0 && greekWordsChirho.length === 0) {
    console.error("\nNo data loaded. Aborting.");
    process.exit(1);
  }

  // Build examples
  console.log("\nBuilding parser examples...");
  const hebrewExamplesChirho = buildExamplesChirho(hebrewWordsChirho, "hebrew");
  console.log(`  Hebrew examples: ${hebrewExamplesChirho.length}`);

  const greekExamplesChirho = buildExamplesChirho(greekWordsChirho, "greek");
  console.log(`  Greek examples: ${greekExamplesChirho.length}`);

  // Stratified subsample — use MORE Hebrew data to improve quality
  console.log(`\nSubsampling: Hebrew target=${TARGET_HEBREW_CHIRHO}, Greek target=${TARGET_GREEK_CHIRHO}...`);
  const sampledHebrewChirho = stratifiedSampleChirho(
    hebrewExamplesChirho,
    TARGET_HEBREW_CHIRHO
  );
  const sampledGreekChirho = stratifiedSampleChirho(
    greekExamplesChirho,
    TARGET_GREEK_CHIRHO
  );
  console.log(`  Hebrew sampled: ${sampledHebrewChirho.length}`);
  console.log(`  Greek sampled: ${sampledGreekChirho.length}`);

  // Combine and split
  const allExamplesChirho = [...sampledHebrewChirho, ...sampledGreekChirho];
  console.log(`  Combined: ${allExamplesChirho.length}`);

  const { trainChirho, valChirho, testChirho } = splitDatasetChirho(allExamplesChirho);
  console.log(`\nSplit sizes:`);
  console.log(`  Train: ${trainChirho.length}`);
  console.log(`  Val:   ${valChirho.length}`);
  console.log(`  Test:  ${testChirho.length}`);

  // Write JSONL files
  await writeJsonlChirho(`${OUTPUT_DIR_CHIRHO}/train-parser-chirho.jsonl`, trainChirho);
  await writeJsonlChirho(`${OUTPUT_DIR_CHIRHO}/val-parser-chirho.jsonl`, valChirho);
  await writeJsonlChirho(`${OUTPUT_DIR_CHIRHO}/test-parser-chirho.jsonl`, testChirho);

  console.log(`\nFiles written to ${OUTPUT_DIR_CHIRHO}/`);

  // Show samples
  console.log("\n--- Sample Entries ---");
  for (const exChirho of trainChirho.slice(0, 3)) {
    console.log(`\n  Input:  ${exChirho.inputChirho}`);
    console.log(`  Target: ${exChirho.targetChirho}`);
  }

  // Stats
  const langCountsChirho = { hebrew: 0, greek: 0 };
  for (const exChirho of allExamplesChirho) {
    langCountsChirho[exChirho.langChirho as keyof typeof langCountsChirho]++;
  }
  console.log(`\nLanguage distribution: Hebrew=${langCountsChirho.hebrew}, Greek=${langCountsChirho.greek}`);

  const bookSetChirho = new Set(allExamplesChirho.map((exChirho) => exChirho.bookChirho));
  console.log(`Books represented: ${bookSetChirho.size}`);

  console.log("\nDone!");
}

mainChirho();
