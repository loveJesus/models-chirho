// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * build-variant-dataset-chirho.ts
 * Processes TAGNT files to build a variant classification dataset.
 *
 * The TAGNT format marks each word with which editions include it:
 *   Editions: NA27/28 (N), TR (T), SBLGNT (S), Byzantine (B), Westcott-Hort (W), THGNT (H)
 *
 * We classify variants by comparing edition agreements:
 *   - substitution: Different word forms across editions at same position
 *   - omission: Word present in some editions but not others
 *   - addition: Extra words in some editions
 *   - word_order: Same words in different sequences
 *   - harmonization: Reading from parallel passage (detected by cross-reference)
 *   - spelling: Minor orthographic variants
 *
 * Output: data-chirho/processed-chirho/{train,val,test}-variant-chirho.jsonl
 */

import { readFile, writeFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;
const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

interface VariantExampleChirho {
  inputChirho: string;
  targetChirho: string;
  refChirho: string;
  typeChirho: string;
}

interface TagntWordChirho {
  refChirho: string;       // e.g., "Mat.1.1#01=NKO"
  greekChirho: string;     // e.g., "Βίβλος" (Greek word form without transliteration)
  translitChirho: string;  // e.g., "Biblos"
  glossChirho: string;     // e.g., "[The] book"
  strongMorphChirho: string; // e.g., "G0976=N-NSF"
  lemmaChirho: string;     // e.g., "βίβλος" (Greek lemma only)
  lemmaMeaningChirho: string; // e.g., "book"
  editionsChirho: string;  // e.g., "NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz"
  variantChirho: string;   // e.g., "Tyn+WH: Δαυεὶδ ; +TR: Δαβὶδ ;"
}

function parseTagntLineChirho(lineChirho: string): TagntWordChirho | null {
  // TAGNT actual column layout (tab-separated):
  //   [0] Reference:    Mat.1.1#01=NKO
  //   [1] Greek+translit: Βίβλος (Biblos)
  //   [2] English gloss: [The] book
  //   [3] Strong's=Morph: G0976=N-NSF
  //   [4] Lemma=English: βίβλος=book
  //   [5] Editions:     NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz
  //   [6] (empty or spacer)
  //   [7] Variant info:  Tyn+WH: Δαυεὶδ ; +TR: Δαβὶδ ;
  //   [8] Spanish translation
  //   [9] English meaning
  //   [10+] Word position, Strong's ref, etc.

  if (!lineChirho.trim() || lineChirho.startsWith("#") || lineChirho.startsWith("$") || lineChirho.startsWith("=") || lineChirho.startsWith("TAGNT") || lineChirho.startsWith("(") || lineChirho.startsWith("All ") || lineChirho.startsWith("\t")) {
    return null;
  }

  const fieldsChirho = lineChirho.split("\t");
  if (fieldsChirho.length < 6) return null;

  const refChirho = fieldsChirho[0]?.trim() || "";
  if (!refChirho.match(/^\w+\.\d+\.\d+/)) return null;

  // Parse Greek text: "Βίβλος (Biblos)" → greek="Βίβλος", translit="Biblos"
  const greekFieldChirho = fieldsChirho[1]?.trim() || "";
  let greekChirho = greekFieldChirho;
  let translitChirho = "";
  const translitMatchChirho = greekFieldChirho.match(/^(.+?)\s*\(([^)]+)\)\s*$/);
  if (translitMatchChirho) {
    greekChirho = translitMatchChirho[1].trim();
    translitChirho = translitMatchChirho[2].trim();
  }

  // Parse lemma: "βίβλος=book" → lemma="βίβλος", meaning="book"
  const lemmaFieldChirho = fieldsChirho[4]?.trim() || "";
  let lemmaChirho = lemmaFieldChirho;
  let lemmaMeaningChirho = "";
  const lemmaMatchChirho = lemmaFieldChirho.match(/^(.+?)=(.+)$/);
  if (lemmaMatchChirho) {
    lemmaChirho = lemmaMatchChirho[1].trim();
    lemmaMeaningChirho = lemmaMatchChirho[2].trim();
  }

  return {
    refChirho,
    greekChirho,
    translitChirho,
    glossChirho: fieldsChirho[2]?.trim() || "",
    strongMorphChirho: fieldsChirho[3]?.trim() || "",
    lemmaChirho,
    lemmaMeaningChirho,
    editionsChirho: fieldsChirho[5]?.trim() || "",
    variantChirho: fieldsChirho[7]?.trim() || "",
  };
}

function classifyVariantChirho(
  wordChirho: TagntWordChirho,
  contextWordsChirho: TagntWordChirho[]
): string {
  const edChirho = wordChirho.editionsChirho;

  // Editions field contains edition names like "NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz"
  const hasNA28Chirho = edChirho.includes("NA28");
  const hasNA27Chirho = edChirho.includes("NA27");
  const hasTynChirho = edChirho.includes("Tyn");
  const hasSBLChirho = edChirho.includes("SBL");
  const hasWHChirho = edChirho.includes("WH");
  const hasTregChirho = edChirho.includes("Treg");
  const hasTRChirho = edChirho.includes("TR");
  const hasByzChirho = edChirho.includes("Byz");

  const edCountChirho = [
    hasNA28Chirho, hasNA27Chirho, hasTynChirho, hasSBLChirho,
    hasWHChirho, hasTregChirho, hasTRChirho, hasByzChirho,
  ].filter(Boolean).length;

  // All 8 editions agree — no variant
  if (edCountChirho >= 7) {
    // Still might have spelling variants noted in variant field
    if (wordChirho.variantChirho) return "spelling";
    return "agreement";
  }

  // Check for explicit variant readings (e.g., "Tyn: Δαυεὶδ ; +TR: Δαβὶδ")
  if (wordChirho.variantChirho) {
    // Multiple variant readings with different forms → substitution
    if (wordChirho.variantChirho.includes(":") && wordChirho.variantChirho.includes(";")) {
      return "substitution";
    }
  }

  // Word missing from many editions → omission
  if (edCountChirho <= 3) return "omission";

  // Byzantine vs Alexandrian split
  const hasCriticalChirho = hasNA28Chirho || hasNA27Chirho || hasSBLChirho || hasWHChirho;
  const hasByzantineChirho = hasTRChirho || hasByzChirho;

  if (hasByzantineChirho && !hasCriticalChirho) return "addition";
  if (hasCriticalChirho && !hasByzantineChirho) return "omission";

  return "substitution";
}

function cleanRefChirho(refChirho: string): string {
  // "Mat.1.1#01=NKO" → "Mat.1.1"
  return refChirho.replace(/#.*$/, "").trim();
}

function buildInputChirho(
  wordChirho: TagntWordChirho,
  contextChirho: TagntWordChirho[]
): string {
  // Build context from actual Greek words
  const contextTextChirho = contextChirho
    .map((wChirho) => wChirho.greekChirho)
    .join(" ");

  const refCleanChirho = cleanRefChirho(wordChirho.refChirho);

  // Include transliteration to help mT5 with Greek
  const translitPartChirho = wordChirho.translitChirho
    ? ` (${wordChirho.translitChirho})`
    : "";

  return `classify variant [greek]: ${wordChirho.greekChirho}${translitPartChirho} [${refCleanChirho}] editions: ${wordChirho.editionsChirho} context: ${contextTextChirho}`;
}

function buildTargetChirho(
  typeChirho: string,
  wordChirho: TagntWordChirho
): string {
  // Clean, structured target format
  const partsChirho: string[] = [`type:${typeChirho}`];

  // Lemma (Greek only, no mixing)
  if (wordChirho.lemmaChirho) partsChirho.push(`lemma:${wordChirho.lemmaChirho}`);

  // Strong's+Morphology code (e.g., "G0976=N-NSF")
  if (wordChirho.strongMorphChirho) partsChirho.push(`morph:${wordChirho.strongMorphChirho}`);

  // English gloss
  if (wordChirho.glossChirho) partsChirho.push(`gloss:${wordChirho.glossChirho}`);

  // Which editions include this reading
  partsChirho.push(`editions:${wordChirho.editionsChirho}`);

  // Variant readings from other editions (clean, no Spanish)
  if (wordChirho.variantChirho) {
    partsChirho.push(`variant:${wordChirho.variantChirho.substring(0, 100)}`);
  }

  return partsChirho.join(" | ");
}

async function processTagntFileChirho(
  filePathChirho: string,
  labelChirho: string
): Promise<VariantExampleChirho[]> {
  console.log(`\nProcessing ${labelChirho}...`);

  const contentChirho = await readFile(filePathChirho, "utf-8");
  const linesChirho = contentChirho.split("\n");

  const wordsChirho: TagntWordChirho[] = [];
  for (const lineChirho of linesChirho) {
    const parsedChirho = parseTagntLineChirho(lineChirho);
    if (parsedChirho) wordsChirho.push(parsedChirho);
  }

  console.log(`  Parsed ${wordsChirho.length} words`);

  const examplesChirho: VariantExampleChirho[] = [];
  const typeCountsChirho: Record<string, number> = {};

  for (let iChirho = 0; iChirho < wordsChirho.length; iChirho++) {
    const wordChirho = wordsChirho[iChirho];

    // Get context window (±3 words)
    const contextStartChirho = Math.max(0, iChirho - 3);
    const contextEndChirho = Math.min(wordsChirho.length, iChirho + 4);
    const contextChirho = wordsChirho.slice(contextStartChirho, contextEndChirho);

    const typeChirho = classifyVariantChirho(wordChirho, contextChirho);

    // Skip "agreement" — we only want actual variants
    if (typeChirho === "agreement") continue;

    const inputChirho = buildInputChirho(wordChirho, contextChirho);
    const targetChirho = buildTargetChirho(typeChirho, wordChirho);

    examplesChirho.push({
      inputChirho,
      targetChirho,
      refChirho: wordChirho.refChirho,
      typeChirho,
    });

    typeCountsChirho[typeChirho] = (typeCountsChirho[typeChirho] || 0) + 1;
  }

  console.log(`  Variant examples: ${examplesChirho.length}`);
  console.log(`  Type distribution:`);
  for (const [typeChirho, countChirho] of Object.entries(typeCountsChirho).sort(
    (aChirho, bChirho) => bChirho[1] - aChirho[1]
  )) {
    const pctChirho = ((countChirho / examplesChirho.length) * 100).toFixed(1);
    console.log(`    ${typeChirho}: ${countChirho} (${pctChirho}%)`);
  }

  return examplesChirho;
}

function shuffleChirho<T>(arrChirho: T[]): T[] {
  const shuffledChirho = [...arrChirho];
  for (let iChirho = shuffledChirho.length - 1; iChirho > 0; iChirho--) {
    const jChirho = Math.floor(Math.random() * (iChirho + 1));
    [shuffledChirho[iChirho], shuffledChirho[jChirho]] = [shuffledChirho[jChirho], shuffledChirho[iChirho]];
  }
  return shuffledChirho;
}

async function mainChirho(): Promise<void> {
  console.log("Manuscript Variant Dataset Builder");
  console.log("==================================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  // Process both TAGNT files
  const filePathsChirho = [
    { pathChirho: `${RAW_DIR_CHIRHO}tagnt-mat-jhn-chirho.txt`, labelChirho: "Gospels (Matt-John)" },
    { pathChirho: `${RAW_DIR_CHIRHO}tagnt-act-rev-chirho.txt`, labelChirho: "Acts-Revelation" },
  ];

  let allExamplesChirho: VariantExampleChirho[] = [];

  for (const fileChirho of filePathsChirho) {
    try {
      await stat(fileChirho.pathChirho);
      const examplesChirho = await processTagntFileChirho(fileChirho.pathChirho, fileChirho.labelChirho);
      allExamplesChirho = allExamplesChirho.concat(examplesChirho);
    } catch {
      console.error(`  File not found: ${fileChirho.pathChirho}`);
      console.error(`  Run 'bun run download-tagnt-chirho' first.`);
    }
  }

  if (allExamplesChirho.length === 0) {
    console.error("\nNo examples generated. Check raw data files.");
    process.exit(1);
  }

  // Balance classes by undersampling dominant class
  const typeCountsChirho: Record<string, VariantExampleChirho[]> = {};
  for (const exChirho of allExamplesChirho) {
    if (!typeCountsChirho[exChirho.typeChirho]) typeCountsChirho[exChirho.typeChirho] = [];
    typeCountsChirho[exChirho.typeChirho].push(exChirho);
  }

  // Cap each type at max 30K examples to prevent extreme imbalance
  const MAX_PER_TYPE_CHIRHO = 30000;
  let balancedChirho: VariantExampleChirho[] = [];
  for (const [typeChirho, examplesChirho] of Object.entries(typeCountsChirho)) {
    const shuffledChirho = shuffleChirho(examplesChirho);
    const cappedChirho = shuffledChirho.slice(0, MAX_PER_TYPE_CHIRHO);
    balancedChirho = balancedChirho.concat(cappedChirho);
    console.log(`\n  ${typeChirho}: ${examplesChirho.length} → ${cappedChirho.length} (capped)`);
  }

  // Shuffle and split 80/10/10
  const shuffledAllChirho = shuffleChirho(balancedChirho);
  const totalChirho = shuffledAllChirho.length;
  const trainEndChirho = Math.floor(totalChirho * 0.8);
  const valEndChirho = Math.floor(totalChirho * 0.9);

  const trainChirho = shuffledAllChirho.slice(0, trainEndChirho);
  const valChirho = shuffledAllChirho.slice(trainEndChirho, valEndChirho);
  const testChirho = shuffledAllChirho.slice(valEndChirho);

  // Write JSONL files
  const writeJsonlChirho = async (
    dataChirho: VariantExampleChirho[],
    fileNameChirho: string
  ) => {
    const outputChirho = dataChirho
      .map((exChirho) =>
        JSON.stringify({
          input_chirho: exChirho.inputChirho,
          target_chirho: exChirho.targetChirho,
        })
      )
      .join("\n");
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${fileNameChirho}`;
    await writeFile(pathChirho, outputChirho, "utf-8");
    console.log(`  Wrote ${pathChirho}: ${dataChirho.length} examples`);
  };

  console.log("\n==================================");
  console.log("Writing dataset splits...");

  await writeJsonlChirho(trainChirho, "train-variant-chirho.jsonl");
  await writeJsonlChirho(valChirho, "val-variant-chirho.jsonl");
  await writeJsonlChirho(testChirho, "test-variant-chirho.jsonl");

  // Summary
  console.log("\n==================================");
  console.log("Dataset Summary:");
  console.log(`  Total examples: ${totalChirho}`);
  console.log(`  Train: ${trainChirho.length}`);
  console.log(`  Validation: ${valChirho.length}`);
  console.log(`  Test: ${testChirho.length}`);
  console.log("\nDone!");
}

mainChirho();
