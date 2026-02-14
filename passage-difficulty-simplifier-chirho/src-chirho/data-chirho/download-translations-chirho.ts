// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-translations-chirho.ts
 * Downloads multiple public-domain Bible translations from scrollmapper/bible_databases.
 * CSV format: Book,Chapter,Verse,Text (with book names as strings).
 *
 * Translations:
 *   - KJV: King James Version (formal archaic, 1611/1769)
 *   - BBE: Bible in Basic English (850-word vocabulary, grade 4 reading level)
 *   - OEB: Open English Bible (modern, public domain)
 *   - ASV: American Standard Version (formal, 1901)
 *   - YLT: Young's Literal Translation (ultra-literal, 1862)
 *   - Darby: Darby Bible (literal, 1890)
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
  roleChirho: string;
}> = [
  {
    codeChirho: "KJV",
    nameChirho: "King James Version",
    fileNameChirho: "KJV.csv",
    roleChirho: "complex_source",
  },
  {
    codeChirho: "BBE",
    nameChirho: "Bible in Basic English",
    fileNameChirho: "BBE.csv",
    roleChirho: "simple_target",
  },
  {
    codeChirho: "OEB",
    nameChirho: "Open English Bible",
    fileNameChirho: "OEB.csv",
    roleChirho: "simple_target",
  },
  {
    codeChirho: "ASV",
    nameChirho: "American Standard Version",
    fileNameChirho: "ASV.csv",
    roleChirho: "complex_source",
  },
  {
    codeChirho: "YLT",
    nameChirho: "Young's Literal Translation",
    fileNameChirho: "YLT.csv",
    roleChirho: "complex_source",
  },
  {
    codeChirho: "Darby",
    nameChirho: "Darby Bible",
    fileNameChirho: "Darby.csv",
    roleChirho: "complex_source",
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
    headers: { "User-Agent": "passage-difficulty-simplifier-chirho/1.0" },
  });

  if (!responseChirho.ok) {
    throw new Error(
      `Download failed for ${labelChirho}: ${responseChirho.status} ${responseChirho.statusText}`
    );
  }

  const textChirho = await responseChirho.text();
  await writeFile(outputPathChirho, textChirho, "utf-8");

  const lineCountChirho = textChirho.split("\n").filter((lChirho) => lChirho.trim()).length;
  const sizeMbChirho = (Buffer.byteLength(textChirho) / 1024 / 1024).toFixed(1);
  console.log(`    ${sizeMbChirho} MB, ${lineCountChirho} lines`);

  return lineCountChirho;
}

async function mainChirho(): Promise<void> {
  console.log("Bible Translation Downloader - Difficulty & Simplification");
  console.log("==========================================================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

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
  console.log("\n==========================================================");
  console.log("Download Summary:");
  for (const resultChirho of resultsChirho) {
    if (resultChirho.status === "fulfilled") {
      console.log(`  OK: ${resultChirho.value.codeChirho}`);
    } else {
      console.error(`  FAILED: ${resultChirho.reason}`);
    }
  }

  console.log(
    `\nTranslations: ${TRANSLATIONS_CHIRHO.map((tChirho) => tChirho.codeChirho).join(", ")}`
  );
  console.log("Roles:");
  console.log("  Complex sources (for difficulty + simplification input): KJV, ASV, YLT, Darby");
  console.log("  Simple targets (for simplification output): BBE, OEB");
  console.log("\nDone! Files saved to data-chirho/raw-chirho/");
}

mainChirho();
