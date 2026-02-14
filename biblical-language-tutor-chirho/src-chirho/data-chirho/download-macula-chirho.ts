// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-macula-chirho.ts
 * Downloads Macula Hebrew and Greek TSV files from Clear-Bible GitHub repositories.
 * These contain word-level morphology + glosses for the entire OT (Hebrew) and NT (Greek).
 *
 * Sources:
 *   - Hebrew: https://github.com/Clear-Bible/macula-hebrew (LFS, ~425K words)
 *   - Greek:  https://github.com/Clear-Bible/macula-greek  (~138K words)
 *
 * Output: data-chirho/raw-chirho/macula-hebrew-chirho.tsv, macula-greek-chirho.tsv
 */

import { writeFile, readFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;

// Macula Hebrew — TSV in repo's WLC/tsv directory (Git LFS, ~83MB)
// Hebrew columns: xml:id, ref, class, text, transliteration, after, strongnumberx, stronglemma,
//   sensenumber, greek, greekstrong, gloss, english, mandarin, stem, morph, lang, lemma, pos,
//   person, gender, number, state, type, lexdomain, contextualdomain, coredomain, sdbh,
//   extends, frame, subjref, participantref
const MACULA_HEBREW_URL_CHIRHO =
  "https://raw.githubusercontent.com/Clear-Bible/macula-hebrew/main/WLC/tsv/macula-hebrew.tsv";

// Macula Greek SBLGNT — TSV in repo's SBLGNT/tsv directory (~20MB)
// Greek columns: same schema as Hebrew (xml:id, ref, class, text, ... gloss, english, ...)
const MACULA_GREEK_URL_CHIRHO =
  "https://raw.githubusercontent.com/Clear-Bible/macula-greek/main/SBLGNT/tsv/macula-greek-SBLGNT.tsv";

// Fallback: GitHub LFS may return pointer; try GitHub media CDN URLs
const LFS_HEBREW_URL_CHIRHO =
  "https://media.githubusercontent.com/media/Clear-Bible/macula-hebrew/main/WLC/tsv/macula-hebrew.tsv";
const LFS_GREEK_URL_CHIRHO =
  "https://media.githubusercontent.com/media/Clear-Bible/macula-greek/main/SBLGNT/tsv/macula-greek-SBLGNT.tsv";

interface DownloadResultChirho {
  pathChirho: string;
  sizeChirho: number;
  lineCountChirho: number;
}

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    const statChirho = await stat(pathChirho);
    return statChirho.size > 1000; // Must be more than just an LFS pointer
  } catch {
    return false;
  }
}

async function downloadFileChirho(
  urlChirho: string,
  outputPathChirho: string,
  labelChirho: string,
  fallbackUrlChirho?: string
): Promise<DownloadResultChirho> {
  console.log(`\nDownloading ${labelChirho}...`);
  console.log(`  URL: ${urlChirho}`);

  let responseChirho = await fetch(urlChirho, {
    headers: {
      "User-Agent": "biblical-language-tutor-chirho/1.0",
    },
  });

  if (!responseChirho.ok) {
    if (fallbackUrlChirho) {
      console.log(`  Primary URL failed (${responseChirho.status}), trying fallback...`);
      console.log(`  Fallback: ${fallbackUrlChirho}`);
      responseChirho = await fetch(fallbackUrlChirho, {
        headers: { "User-Agent": "biblical-language-tutor-chirho/1.0" },
      });
    }
    if (!responseChirho.ok) {
      throw new Error(
        `Download failed for ${labelChirho}: ${responseChirho.status} ${responseChirho.statusText}`
      );
    }
  }

  const textChirho = await responseChirho.text();

  // Check if we got an LFS pointer instead of actual data
  if (textChirho.startsWith("version https://git-lfs.github.com")) {
    console.log(`  Got LFS pointer, trying fallback URL...`);
    if (fallbackUrlChirho) {
      const fallbackResponseChirho = await fetch(fallbackUrlChirho, {
        headers: { "User-Agent": "biblical-language-tutor-chirho/1.0" },
      });
      if (!fallbackResponseChirho.ok) {
        throw new Error(`Fallback download failed: ${fallbackResponseChirho.status}`);
      }
      const fallbackTextChirho = await fallbackResponseChirho.text();
      await writeFile(outputPathChirho, fallbackTextChirho, "utf-8");
      const lineCountChirho = fallbackTextChirho.split("\n").length;
      console.log(
        `  Downloaded ${(Buffer.byteLength(fallbackTextChirho) / 1024 / 1024).toFixed(1)} MB (${lineCountChirho} lines)`
      );
      return {
        pathChirho: outputPathChirho,
        sizeChirho: Buffer.byteLength(fallbackTextChirho),
        lineCountChirho,
      };
    }
    throw new Error(`Got LFS pointer for ${labelChirho} and no fallback available`);
  }

  await writeFile(outputPathChirho, textChirho, "utf-8");
  const lineCountChirho = textChirho.split("\n").length;
  console.log(
    `  Downloaded ${(Buffer.byteLength(textChirho) / 1024 / 1024).toFixed(1)} MB (${lineCountChirho} lines)`
  );

  return {
    pathChirho: outputPathChirho,
    sizeChirho: Buffer.byteLength(textChirho),
    lineCountChirho,
  };
}

function previewTsvChirho(pathChirho: string, contentChirho: string, labelChirho: string): void {
  const linesChirho = contentChirho.split("\n").filter((lineChirho) => lineChirho.trim());
  const headerChirho = linesChirho[0];
  const columnsChirho = headerChirho.split("\t");

  console.log(`\n  ${labelChirho} TSV Preview:`);
  console.log(`  Columns (${columnsChirho.length}): ${columnsChirho.join(", ")}`);
  console.log(`  Data rows: ${linesChirho.length - 1}`);

  // Show first 3 data rows
  console.log(`  Sample rows:`);
  for (let iChirho = 1; iChirho <= Math.min(3, linesChirho.length - 1); iChirho++) {
    const fieldsChirho = linesChirho[iChirho].split("\t");
    const previewChirho = columnsChirho
      .slice(0, 8)
      .map(
        (colChirho, jChirho) =>
          `${colChirho}=${fieldsChirho[jChirho]?.substring(0, 30) ?? "N/A"}`
      )
      .join(" | ");
    console.log(`    Row ${iChirho}: ${previewChirho}`);
  }
}

async function mainChirho(): Promise<void> {
  console.log("Macula Biblical Text Downloader");
  console.log("================================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  const hebrewPathChirho = `${RAW_DIR_CHIRHO}macula-hebrew-chirho.tsv`;
  const greekPathChirho = `${RAW_DIR_CHIRHO}macula-greek-chirho.tsv`;

  // Check if already downloaded
  const hebrewExistsChirho = await fileExistsChirho(hebrewPathChirho);
  const greekExistsChirho = await fileExistsChirho(greekPathChirho);

  if (hebrewExistsChirho && greekExistsChirho) {
    console.log("Both Macula files already downloaded. Skipping.");
    console.log(`  Hebrew: ${hebrewPathChirho}`);
    console.log(`  Greek:  ${greekPathChirho}`);

    // Still preview them
    const hebrewContentChirho = await readFile(hebrewPathChirho, "utf-8");
    const greekContentChirho = await readFile(greekPathChirho, "utf-8");
    previewTsvChirho(hebrewPathChirho, hebrewContentChirho, "Hebrew");
    previewTsvChirho(greekPathChirho, greekContentChirho, "Greek");
    return;
  }

  // Download both in parallel
  const resultsChirho = await Promise.allSettled([
    hebrewExistsChirho
      ? Promise.resolve({ pathChirho: hebrewPathChirho, sizeChirho: 0, lineCountChirho: 0 })
      : downloadFileChirho(
          MACULA_HEBREW_URL_CHIRHO,
          hebrewPathChirho,
          "Macula Hebrew (OT)",
          LFS_HEBREW_URL_CHIRHO
        ),
    greekExistsChirho
      ? Promise.resolve({ pathChirho: greekPathChirho, sizeChirho: 0, lineCountChirho: 0 })
      : downloadFileChirho(
          MACULA_GREEK_URL_CHIRHO,
          greekPathChirho,
          "Macula Greek (NT)",
          LFS_GREEK_URL_CHIRHO
        ),
  ]);

  // Report results
  console.log("\n================================");
  console.log("Download Summary:");
  for (const resultChirho of resultsChirho) {
    if (resultChirho.status === "fulfilled") {
      console.log(`  OK: ${resultChirho.value.pathChirho}`);
    } else {
      console.error(`  FAILED: ${resultChirho.reason}`);
    }
  }

  // Preview downloaded files
  try {
    const hebrewContentChirho = await readFile(hebrewPathChirho, "utf-8");
    previewTsvChirho(hebrewPathChirho, hebrewContentChirho, "Hebrew");
  } catch {
    console.log("  Could not preview Hebrew file");
  }

  try {
    const greekContentChirho = await readFile(greekPathChirho, "utf-8");
    previewTsvChirho(greekPathChirho, greekContentChirho, "Greek");
  } catch {
    console.log("  Could not preview Greek file");
  }

  console.log("\nDone! Files saved to data-chirho/raw-chirho/");
}

mainChirho();
