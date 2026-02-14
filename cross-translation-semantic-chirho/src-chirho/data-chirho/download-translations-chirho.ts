// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-translations-chirho.ts
 * Downloads multiple public-domain Bible translations from scrollmapper/bible_databases.
 * CSV format: Book,Chapter,Verse,Text (with book names as strings).
 *
 * Translations (all public domain):
 *   - KJV: King James Version (formal equivalence, 1611/1769)
 *   - ASV: American Standard Version (formal, 1901)
 *   - YLT: Young's Literal Translation (ultra-literal, 1862)
 *   - Darby: Darby Bible (literal, 1890)
 *   - AKJV: American King James Version
 *
 * Output: data-chirho/raw-chirho/{translation}-chirho.csv
 */

import { writeFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;

const BASE_URL_CHIRHO =
  "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/csv/";

const TRANSLATIONS_CHIRHO: Array<{
  codeChirho: string;
  nameChirho: string;
  fileNameChirho: string;
  philosophyChirho: string;
}> = [
  {
    codeChirho: "KJV",
    nameChirho: "King James Version",
    fileNameChirho: "KJV.csv",
    philosophyChirho: "formal",
  },
  {
    codeChirho: "ASV",
    nameChirho: "American Standard Version",
    fileNameChirho: "ASV.csv",
    philosophyChirho: "formal",
  },
  {
    codeChirho: "YLT",
    nameChirho: "Young's Literal Translation",
    fileNameChirho: "YLT.csv",
    philosophyChirho: "literal",
  },
  {
    codeChirho: "Darby",
    nameChirho: "Darby Bible",
    fileNameChirho: "Darby.csv",
    philosophyChirho: "literal",
  },
  {
    codeChirho: "AKJV",
    nameChirho: "American King James Version",
    fileNameChirho: "AKJV.csv",
    philosophyChirho: "formal",
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
): Promise<number> {
  console.log(`  Downloading ${labelChirho}...`);

  const responseChirho = await fetch(urlChirho, {
    headers: { "User-Agent": "cross-translation-semantic-chirho/1.0" },
  });

  if (!responseChirho.ok) {
    throw new Error(`Download failed for ${labelChirho}: ${responseChirho.status} ${responseChirho.statusText}`);
  }

  const textChirho = await responseChirho.text();
  await writeFile(outputPathChirho, textChirho, "utf-8");

  const lineCountChirho = textChirho.split("\n").filter((lChirho) => lChirho.trim()).length;
  const sizeMbChirho = (Buffer.byteLength(textChirho) / 1024 / 1024).toFixed(1);
  console.log(`    ${sizeMbChirho} MB, ${lineCountChirho} lines`);

  return lineCountChirho;
}

async function mainChirho(): Promise<void> {
  console.log("Bible Translation Downloader");
  console.log("============================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  // Download all translations in parallel
  console.log("Downloading translations...");

  const resultsChirho = await Promise.allSettled(
    TRANSLATIONS_CHIRHO.map(async (translationChirho) => {
      const outputPathChirho = `${RAW_DIR_CHIRHO}${translationChirho.codeChirho.toLowerCase()}-chirho.csv`;

      if (await fileExistsChirho(outputPathChirho)) {
        console.log(`  ${translationChirho.codeChirho}: already downloaded`);
        return { codeChirho: translationChirho.codeChirho, linesChirho: 0 };
      }

      const urlChirho = `${BASE_URL_CHIRHO}${translationChirho.fileNameChirho}`;
      const linesChirho = await downloadFileChirho(
        urlChirho,
        outputPathChirho,
        `${translationChirho.codeChirho} (${translationChirho.nameChirho})`
      );

      return { codeChirho: translationChirho.codeChirho, linesChirho };
    })
  );

  // Summary
  console.log("\n============================");
  console.log("Download Summary:");
  for (const resultChirho of resultsChirho) {
    if (resultChirho.status === "fulfilled") {
      console.log(`  OK: ${resultChirho.value.codeChirho}`);
    } else {
      console.error(`  FAILED: ${resultChirho.reason}`);
    }
  }

  console.log(`\nTranslations: ${TRANSLATIONS_CHIRHO.map((tChirho) => tChirho.codeChirho).join(", ")}`);
  console.log("Done! Files saved to data-chirho/raw-chirho/");
}

mainChirho();
