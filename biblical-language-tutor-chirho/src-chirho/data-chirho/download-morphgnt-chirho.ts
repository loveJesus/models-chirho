// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-morphgnt-chirho.ts
 * Downloads MorphGNT (morphgnt/sblgnt) files as supplementary Greek NT morphology source.
 * 27 book files with word-level morphological analysis.
 *
 * Source: https://github.com/morphgnt/sblgnt
 * Format: space-separated columns per word
 *   bcv (book-chapter-verse) | part-of-speech | parsing-code | text | word | normalized | lemma
 *
 * Parsing code format: tense-voice-mood-person-case-number-gender-degree
 *
 * Output: data-chirho/raw-chirho/morphgnt-chirho/ (27 book files)
 */

import { writeFile, readFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;
const MORPHGNT_DIR_CHIRHO = `${RAW_DIR_CHIRHO}morphgnt-chirho/`;

// MorphGNT book files (SBLGNT)
// File naming: XX-bookname.txt where XX = 2-digit number
const MORPHGNT_BASE_URL_CHIRHO =
  "https://raw.githubusercontent.com/morphgnt/sblgnt/master/";

const BOOKS_CHIRHO: Array<{ codeChirho: string; nameChirho: string }> = [
  { codeChirho: "61", nameChirho: "Mt" },
  { codeChirho: "62", nameChirho: "Mk" },
  { codeChirho: "63", nameChirho: "Lk" },
  { codeChirho: "64", nameChirho: "Jn" },
  { codeChirho: "65", nameChirho: "Ac" },
  { codeChirho: "66", nameChirho: "Ro" },
  { codeChirho: "67", nameChirho: "1Co" },
  { codeChirho: "68", nameChirho: "2Co" },
  { codeChirho: "69", nameChirho: "Ga" },
  { codeChirho: "70", nameChirho: "Eph" },
  { codeChirho: "71", nameChirho: "Php" },
  { codeChirho: "72", nameChirho: "Col" },
  { codeChirho: "73", nameChirho: "1Th" },
  { codeChirho: "74", nameChirho: "2Th" },
  { codeChirho: "75", nameChirho: "1Ti" },
  { codeChirho: "76", nameChirho: "2Ti" },
  { codeChirho: "77", nameChirho: "Tit" },
  { codeChirho: "78", nameChirho: "Phm" },
  { codeChirho: "79", nameChirho: "Heb" },
  { codeChirho: "80", nameChirho: "Jas" },
  { codeChirho: "81", nameChirho: "1Pe" },
  { codeChirho: "82", nameChirho: "2Pe" },
  { codeChirho: "83", nameChirho: "1Jn" },
  { codeChirho: "84", nameChirho: "2Jn" },
  { codeChirho: "85", nameChirho: "3Jn" },
  { codeChirho: "86", nameChirho: "Jud" },
  { codeChirho: "87", nameChirho: "Re" },
];

async function downloadBookChirho(
  bookChirho: { codeChirho: string; nameChirho: string }
): Promise<{ nameChirho: string; wordsChirho: number }> {
  const fileNameChirho = `${bookChirho.codeChirho}-${bookChirho.nameChirho}-morphgnt.txt`;
  const urlChirho = `${MORPHGNT_BASE_URL_CHIRHO}${fileNameChirho}`;
  const outputPathChirho = `${MORPHGNT_DIR_CHIRHO}${fileNameChirho}`;

  // Check if already exists
  try {
    const existingChirho = await stat(outputPathChirho);
    if (existingChirho.size > 100) {
      const contentChirho = await readFile(outputPathChirho, "utf-8");
      const wordsChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim()).length;
      return { nameChirho: bookChirho.nameChirho, wordsChirho };
    }
  } catch {
    // Need to download
  }

  const responseChirho = await fetch(urlChirho);
  if (!responseChirho.ok) {
    throw new Error(`Failed to download ${fileNameChirho}: ${responseChirho.status}`);
  }

  const textChirho = await responseChirho.text();
  await writeFile(outputPathChirho, textChirho, "utf-8");

  const wordsChirho = textChirho.split("\n").filter((lChirho) => lChirho.trim()).length;
  return { nameChirho: bookChirho.nameChirho, wordsChirho };
}

async function mainChirho(): Promise<void> {
  console.log("MorphGNT (SBLGNT) Downloader");
  console.log("============================\n");

  await mkdir(MORPHGNT_DIR_CHIRHO, { recursive: true });

  // Download all 27 books in batches of 5 to avoid hammering GitHub
  const batchSizeChirho = 5;
  const allResultsChirho: Array<{ nameChirho: string; wordsChirho: number }> = [];
  let totalWordsChirho = 0;

  for (let iChirho = 0; iChirho < BOOKS_CHIRHO.length; iChirho += batchSizeChirho) {
    const batchChirho = BOOKS_CHIRHO.slice(iChirho, iChirho + batchSizeChirho);
    const batchNamesChirho = batchChirho.map((bChirho) => bChirho.nameChirho).join(", ");
    console.log(
      `Downloading batch ${Math.floor(iChirho / batchSizeChirho) + 1}: ${batchNamesChirho}`
    );

    const resultsChirho = await Promise.all(
      batchChirho.map((bookChirho) => downloadBookChirho(bookChirho))
    );

    for (const resultChirho of resultsChirho) {
      allResultsChirho.push(resultChirho);
      totalWordsChirho += resultChirho.wordsChirho;
      console.log(`  ${resultChirho.nameChirho}: ${resultChirho.wordsChirho} words`);
    }
  }

  // Summary
  console.log("\n============================");
  console.log("MorphGNT Download Summary:");
  console.log(`  Books: ${allResultsChirho.length}`);
  console.log(`  Total words: ${totalWordsChirho.toLocaleString()}`);
  console.log(`  Output: ${MORPHGNT_DIR_CHIRHO}`);

  // Preview format from first book
  try {
    const firstFileChirho = `${MORPHGNT_DIR_CHIRHO}${BOOKS_CHIRHO[0].codeChirho}-${BOOKS_CHIRHO[0].nameChirho}.txt`;
    const contentChirho = await readFile(firstFileChirho, "utf-8");
    const sampleLinesChirho = contentChirho.split("\n").slice(0, 3);
    console.log("\n  Format preview (Matthew):");
    console.log("  Columns: bcv | pos | parsing | text | word | normalized | lemma");
    for (const lineChirho of sampleLinesChirho) {
      if (lineChirho.trim()) {
        console.log(`    ${lineChirho}`);
      }
    }
  } catch {
    // OK if preview fails
  }

  console.log("\nDone!");
}

mainChirho();
