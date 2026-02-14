// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * build-embedding-dataset-chirho.ts
 * Builds contrastive learning pairs from parallel Bible translations.
 *
 * CSV format from scrollmapper: Book,Chapter,Verse,Text
 * (Book is a string name like "Genesis", "Matthew", etc.)
 *
 * For each verse, create positive pairs (same verse, different translations)
 * and negative pairs (different verses).
 *
 * Output: data-chirho/processed-chirho/{train,val,test}-embedding-chirho.jsonl
 */

import { readFile, writeFile, mkdir } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;
const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

interface PairExampleChirho {
  sentence1Chirho: string;
  sentence2Chirho: string;
  labelChirho: number;
}

const TRANSLATIONS_CHIRHO = ["kjv", "asv", "ylt", "darby", "akjv"];

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

async function loadTranslationChirho(
  codeChirho: string
): Promise<Map<string, string>> {
  const filePathChirho = `${RAW_DIR_CHIRHO}${codeChirho}-chirho.csv`;
  const contentChirho = await readFile(filePathChirho, "utf-8");
  const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());

  const versesChirho = new Map<string, string>();

  for (const lineChirho of linesChirho) {
    const fieldsChirho = parseCsvLineChirho(lineChirho);
    if (fieldsChirho.length < 4) continue;

    // Format: Book, Chapter, Verse, Text
    const bookChirho = fieldsChirho[0]?.replace(/^"|"$/g, "").trim();
    const chapterChirho = fieldsChirho[1]?.trim();
    const verseNumChirho = fieldsChirho[2]?.trim();
    const textChirho = fieldsChirho[3]?.replace(/^"|"$/g, "").trim();

    // Skip header row
    if (bookChirho === "Book" || !textChirho || !chapterChirho || isNaN(parseInt(chapterChirho))) continue;

    const refChirho = `${bookChirho}.${chapterChirho}.${verseNumChirho}`;
    versesChirho.set(refChirho, textChirho);
  }

  return versesChirho;
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
  console.log("Cross-Translation Embedding Dataset Builder");
  console.log("============================================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  // Load all translations
  console.log("Loading translations...");
  const translationsChirho = new Map<string, Map<string, string>>();

  for (const codeChirho of TRANSLATIONS_CHIRHO) {
    try {
      const versesChirho = await loadTranslationChirho(codeChirho);
      translationsChirho.set(codeChirho, versesChirho);
      console.log(`  ${codeChirho.toUpperCase()}: ${versesChirho.size} verses`);
    } catch (errorChirho) {
      console.error(`  Failed to load ${codeChirho}: ${errorChirho}`);
    }
  }

  if (translationsChirho.size < 2) {
    console.error("Need at least 2 translations loaded. Exiting.");
    process.exit(1);
  }

  // Find common verses (present in ALL loaded translations)
  const translationCodesChirho = Array.from(translationsChirho.keys());
  const firstTransChirho = translationsChirho.get(translationCodesChirho[0])!;
  const allRefsChirho = new Set<string>();

  for (const refChirho of firstTransChirho.keys()) {
    let inAllChirho = true;
    for (const [, versesChirho] of translationsChirho) {
      if (!versesChirho.has(refChirho)) {
        inAllChirho = false;
        break;
      }
    }
    if (inAllChirho) allRefsChirho.add(refChirho);
  }

  console.log(`\nCommon verses across all translations: ${allRefsChirho.size}`);

  // Build positive pairs: same verse, different translations
  const refsArrayChirho = Array.from(allRefsChirho);
  const allPairsChirho: PairExampleChirho[] = [];

  console.log("\nBuilding contrastive pairs...");

  for (const refChirho of refsArrayChirho) {
    // Generate translation pair combinations for this verse
    for (let iChirho = 0; iChirho < translationCodesChirho.length; iChirho++) {
      for (let jChirho = iChirho + 1; jChirho < translationCodesChirho.length; jChirho++) {
        const trans1Chirho = translationCodesChirho[iChirho];
        const trans2Chirho = translationCodesChirho[jChirho];
        const text1Chirho = translationsChirho.get(trans1Chirho)!.get(refChirho)!;
        const text2Chirho = translationsChirho.get(trans2Chirho)!.get(refChirho)!;

        // Skip very short verses
        if (text1Chirho.length < 10 || text2Chirho.length < 10) continue;

        allPairsChirho.push({
          sentence1Chirho: `[${trans1Chirho.toUpperCase()}] ${text1Chirho}`,
          sentence2Chirho: `[${trans2Chirho.toUpperCase()}] ${text2Chirho}`,
          labelChirho: 1.0,
        });
      }
    }
  }

  console.log(`  Positive pairs: ${allPairsChirho.length}`);

  // Generate hard negative pairs
  const negativePairsChirho: PairExampleChirho[] = [];
  const TARGET_NEGATIVES_CHIRHO = Math.min(allPairsChirho.length, 200000);
  const shuffledRefsChirho = shuffleChirho(refsArrayChirho);

  for (let iChirho = 0; iChirho < TARGET_NEGATIVES_CHIRHO && iChirho < shuffledRefsChirho.length; iChirho++) {
    const ref1Chirho = shuffledRefsChirho[iChirho];
    const ref2IndexChirho = (iChirho + Math.floor(Math.random() * (shuffledRefsChirho.length - 1)) + 1) % shuffledRefsChirho.length;
    const ref2Chirho = shuffledRefsChirho[ref2IndexChirho];

    if (ref1Chirho === ref2Chirho) continue;

    const transCodeChirho = translationCodesChirho[iChirho % translationCodesChirho.length];
    const text1Chirho = translationsChirho.get(transCodeChirho)!.get(ref1Chirho);
    const text2Chirho = translationsChirho.get(transCodeChirho)!.get(ref2Chirho);

    if (!text1Chirho || !text2Chirho || text1Chirho.length < 10 || text2Chirho.length < 10) continue;

    negativePairsChirho.push({
      sentence1Chirho: `[${transCodeChirho.toUpperCase()}] ${text1Chirho}`,
      sentence2Chirho: `[${transCodeChirho.toUpperCase()}] ${text2Chirho}`,
      labelChirho: 0.0,
    });
  }

  console.log(`  Negative pairs: ${negativePairsChirho.length}`);

  // Combine, cap, shuffle, split
  let combinedChirho = [...allPairsChirho, ...negativePairsChirho];

  const MAX_TOTAL_CHIRHO = 300000;
  if (combinedChirho.length > MAX_TOTAL_CHIRHO) {
    combinedChirho = shuffleChirho(combinedChirho).slice(0, MAX_TOTAL_CHIRHO);
  }

  const shuffledChirho = shuffleChirho(combinedChirho);
  const totalChirho = shuffledChirho.length;
  const trainEndChirho = Math.floor(totalChirho * 0.8);
  const valEndChirho = Math.floor(totalChirho * 0.9);

  const trainChirho = shuffledChirho.slice(0, trainEndChirho);
  const valChirho = shuffledChirho.slice(trainEndChirho, valEndChirho);
  const testChirho = shuffledChirho.slice(valEndChirho);

  // Write JSONL
  const writeJsonlChirho = async (
    dataChirho: PairExampleChirho[],
    fileNameChirho: string
  ) => {
    const outputChirho = dataChirho
      .map((exChirho) =>
        JSON.stringify({
          sentence1_chirho: exChirho.sentence1Chirho,
          sentence2_chirho: exChirho.sentence2Chirho,
          label_chirho: exChirho.labelChirho,
        })
      )
      .join("\n");
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${fileNameChirho}`;
    await writeFile(pathChirho, outputChirho, "utf-8");
    console.log(`  Wrote ${pathChirho}: ${dataChirho.length} examples`);
  };

  console.log("\n============================================");
  console.log("Writing dataset splits...");

  await writeJsonlChirho(trainChirho, "train-embedding-chirho.jsonl");
  await writeJsonlChirho(valChirho, "val-embedding-chirho.jsonl");
  await writeJsonlChirho(testChirho, "test-embedding-chirho.jsonl");

  const posCountChirho = combinedChirho.filter((pChirho) => pChirho.labelChirho === 1.0).length;
  const negCountChirho = combinedChirho.filter((pChirho) => pChirho.labelChirho === 0.0).length;

  console.log("\n============================================");
  console.log("Dataset Summary:");
  console.log(`  Total pairs: ${totalChirho}`);
  console.log(`  Positive (same verse): ${posCountChirho}`);
  console.log(`  Negative (different verse): ${negCountChirho}`);
  console.log(`  Train: ${trainChirho.length}`);
  console.log(`  Validation: ${valChirho.length}`);
  console.log(`  Test: ${testChirho.length}`);
  console.log(`  Translations: ${translationCodesChirho.join(", ").toUpperCase()}`);
  console.log("\nDone!");
}

mainChirho();
