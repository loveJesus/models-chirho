// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-kjv-chirho.ts
 * Downloads the King James Version Bible text from scrollmapper/bible_databases.
 * CSV format: Book,Chapter,Verse,Text
 *
 * This is needed to resolve Nave's topic references and TSK cross-references
 * into actual verse text for training the topical embedding model.
 *
 * Output: data-chirho/raw-chirho/kjv-chirho.csv
 */

import { writeFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;

const KJV_URL_CHIRHO =
  "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/csv/KJV.csv";

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    const statResultChirho = await stat(pathChirho);
    return statResultChirho.size > 1000;
  } catch {
    return false;
  }
}

async function downloadFileChirho(
  urlChirho: string,
  outputPathChirho: string,
  labelChirho: string
): Promise<number> {
  console.log(`  Downloading ${labelChirho}...`);
  console.log(`  URL: ${urlChirho}`);

  const responseChirho = await fetch(urlChirho, {
    headers: { "User-Agent": "topical-passage-classifier-chirho/1.0" },
  });

  if (!responseChirho.ok) {
    throw new Error(
      `Download failed for ${labelChirho}: ${responseChirho.status} ${responseChirho.statusText}`
    );
  }

  const textChirho = await responseChirho.text();
  await writeFile(outputPathChirho, textChirho, "utf-8");

  const lineCountChirho = textChirho
    .split("\n")
    .filter((lChirho) => lChirho.trim()).length;
  const sizeMbChirho = (Buffer.byteLength(textChirho) / 1024 / 1024).toFixed(1);
  console.log(`    ${sizeMbChirho} MB, ${lineCountChirho} lines`);

  return lineCountChirho;
}

async function mainChirho(): Promise<void> {
  console.log("KJV Bible Downloader");
  console.log("====================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  const outputPathChirho = `${RAW_DIR_CHIRHO}kjv-chirho.csv`;

  if (await fileExistsChirho(outputPathChirho)) {
    console.log("KJV Bible already downloaded.");
    console.log(`  File: ${outputPathChirho}`);
    return;
  }

  console.log("Downloading KJV Bible...");
  const lineCountChirho = await downloadFileChirho(
    KJV_URL_CHIRHO,
    outputPathChirho,
    "King James Version"
  );

  console.log("\n====================");
  console.log("Download Summary:");
  console.log(`  Verses: ${lineCountChirho - 1} (excluding header)`);
  console.log(`  Output: ${outputPathChirho}`);
  console.log("\nDone!");
}

mainChirho();
