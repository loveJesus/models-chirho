// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-tagnt-chirho.ts
 * Downloads STEPBible TAGNT (Translators Amalgamated Greek NT) files.
 * These contain variant readings across 6+ critical editions:
 *   NA27/28, TR (Textus Receptus), SBLGNT, Byzantine, Westcott-Hort, THGNT
 *
 * Source: https://github.com/STEPBible/STEPBible-Data
 * License: CC BY 4.0
 *
 * Output: data-chirho/raw-chirho/tagnt-*.txt
 */

import { writeFile, mkdir, stat, readFile } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;

const TAGNT_URLS_CHIRHO: Array<{ urlChirho: string; fileChirho: string; labelChirho: string }> = [
  {
    urlChirho:
      "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Translators%20Amalgamated%20OT%2BNT/TAGNT%20Mat-Jhn%20-%20Translators%20Amalgamated%20Greek%20NT%20-%20STEPBible.org%20CC-BY.txt",
    fileChirho: "tagnt-mat-jhn-chirho.txt",
    labelChirho: "TAGNT Gospels (Matt-John)",
  },
  {
    urlChirho:
      "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Translators%20Amalgamated%20OT%2BNT/TAGNT%20Act-Rev%20-%20Translators%20Amalgamated%20Greek%20NT%20-%20STEPBible.org%20CC-BY.txt",
    fileChirho: "tagnt-act-rev-chirho.txt",
    labelChirho: "TAGNT Acts-Revelation",
  },
];

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    const statChirho = await stat(pathChirho);
    return statChirho.size > 1000;
  } catch {
    return false;
  }
}

async function downloadFileChirho(
  urlChirho: string,
  outputPathChirho: string,
  labelChirho: string
): Promise<{ pathChirho: string; sizeChirho: number; lineCountChirho: number }> {
  console.log(`\nDownloading ${labelChirho}...`);
  console.log(`  URL: ${urlChirho}`);

  const responseChirho = await fetch(urlChirho, {
    headers: { "User-Agent": "manuscript-variant-analyzer-chirho/1.0" },
  });

  if (!responseChirho.ok) {
    throw new Error(`Download failed: ${responseChirho.status} ${responseChirho.statusText}`);
  }

  const textChirho = await responseChirho.text();
  await writeFile(outputPathChirho, textChirho, "utf-8");

  const lineCountChirho = textChirho.split("\n").length;
  const sizeMbChirho = (Buffer.byteLength(textChirho) / 1024 / 1024).toFixed(1);
  console.log(`  Downloaded ${sizeMbChirho} MB (${lineCountChirho} lines)`);

  return {
    pathChirho: outputPathChirho,
    sizeChirho: Buffer.byteLength(textChirho),
    lineCountChirho,
  };
}

async function previewTagntChirho(pathChirho: string): Promise<void> {
  const contentChirho = await readFile(pathChirho, "utf-8");
  const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());

  // Find first data line (skip comments starting with #)
  let dataStartChirho = 0;
  for (let iChirho = 0; iChirho < linesChirho.length; iChirho++) {
    if (!linesChirho[iChirho].startsWith("#") && !linesChirho[iChirho].startsWith("$")) {
      dataStartChirho = iChirho;
      break;
    }
  }

  console.log(`\n  Preview (${pathChirho}):`);
  console.log(`  Total lines: ${linesChirho.length}`);
  console.log(`  Data starts at line: ${dataStartChirho}`);

  // Show header comments
  const headerLinesChirho = linesChirho.slice(0, Math.min(5, dataStartChirho));
  for (const lineChirho of headerLinesChirho) {
    console.log(`    ${lineChirho.substring(0, 120)}`);
  }

  // Show first 3 data lines
  console.log(`  First data lines:`);
  for (let iChirho = dataStartChirho; iChirho < Math.min(dataStartChirho + 3, linesChirho.length); iChirho++) {
    console.log(`    ${linesChirho[iChirho].substring(0, 150)}`);
  }
}

async function mainChirho(): Promise<void> {
  console.log("STEPBible TAGNT Downloader");
  console.log("=========================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  for (const sourceChirho of TAGNT_URLS_CHIRHO) {
    const outputPathChirho = `${RAW_DIR_CHIRHO}${sourceChirho.fileChirho}`;
    const existsChirho = await fileExistsChirho(outputPathChirho);

    if (existsChirho) {
      console.log(`Already downloaded: ${sourceChirho.labelChirho}`);
      await previewTagntChirho(outputPathChirho);
      continue;
    }

    const resultChirho = await downloadFileChirho(
      sourceChirho.urlChirho,
      outputPathChirho,
      sourceChirho.labelChirho
    );

    await previewTagntChirho(resultChirho.pathChirho);
  }

  console.log("\nDone! Files saved to data-chirho/raw-chirho/");
}

mainChirho();
