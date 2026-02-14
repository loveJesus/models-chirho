// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-crossrefs-chirho.ts
 * Downloads Treasury of Scripture Knowledge (TSK) cross-references.
 *
 * Primary source: OpenBible.info (tab-separated, two columns: source_verse \t target_verse)
 * Fallback source: shandran/openbible GitHub repo (CSV with From Verse, To Verse columns)
 *
 * References are in OSIS format (e.g., "Gen.1.1" or "John.3.16").
 *
 * These cross-references connect topically and thematically related verses,
 * providing a second major data source for training the topical search model.
 *
 * Output: data-chirho/raw-chirho/cross-references-chirho.txt
 */

import { writeFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;

const CROSSREF_URLS_CHIRHO = [
  {
    urlChirho: "https://www.openbible.info/labs/cross-references/cross_references.txt",
    nameChirho: "OpenBible.info (TSV)",
    formatChirho: "tsv" as const,
  },
  {
    urlChirho: "https://raw.githubusercontent.com/shandran/openbible/main/cross_references_expanded.csv",
    nameChirho: "shandran/openbible GitHub (CSV)",
    formatChirho: "csv" as const,
  },
];

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    const statResultChirho = await stat(pathChirho);
    return statResultChirho.size > 1000;
  } catch {
    return false;
  }
}

/**
 * Convert CSV cross-references to tab-separated format expected by the build script.
 * Input CSV columns: From Verse, To Verse, Votes, ... (we only need first two)
 */
function convertCsvToTsvChirho(csvTextChirho: string): string {
  const linesChirho = csvTextChirho.split("\n").filter((lChirho) => lChirho.trim());
  const outputLinesChirho: string[] = [];

  for (const lineChirho of linesChirho) {
    // Skip the header line
    if (lineChirho.startsWith("From Verse")) continue;

    // Parse CSV: first two fields are "From Verse" and "To Verse"
    const fieldsChirho = lineChirho.split(",");
    if (fieldsChirho.length >= 2) {
      const fromVerseChirho = fieldsChirho[0].trim();
      const toVerseChirho = fieldsChirho[1].trim();
      if (fromVerseChirho && toVerseChirho) {
        outputLinesChirho.push(`${fromVerseChirho}\t${toVerseChirho}`);
      }
    }
  }

  return outputLinesChirho.join("\n");
}

async function mainChirho(): Promise<void> {
  console.log("TSK Cross-References Downloader");
  console.log("================================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  const outputPathChirho = `${RAW_DIR_CHIRHO}cross-references-chirho.txt`;

  if (await fileExistsChirho(outputPathChirho)) {
    console.log("Cross-references already downloaded.");
    console.log(`  File: ${outputPathChirho}`);
    return;
  }

  let textChirho: string | null = null;

  for (const sourceChirho of CROSSREF_URLS_CHIRHO) {
    console.log(`Downloading TSK cross-references from ${sourceChirho.nameChirho}...`);
    console.log(`  URL: ${sourceChirho.urlChirho}`);

    try {
      const responseChirho = await fetch(sourceChirho.urlChirho, {
        headers: { "User-Agent": "topical-passage-classifier-chirho/1.0" },
      });

      if (!responseChirho.ok) {
        console.log(`  Failed: ${responseChirho.status} ${responseChirho.statusText}`);
        console.log("  Trying next source...\n");
        continue;
      }

      const rawTextChirho = await responseChirho.text();

      if (sourceChirho.formatChirho === "csv") {
        console.log("  Converting CSV to TSV format...");
        textChirho = convertCsvToTsvChirho(rawTextChirho);
      } else {
        textChirho = rawTextChirho;
      }

      console.log(`  Success from ${sourceChirho.nameChirho}!`);
      break;
    } catch (errorChirho) {
      console.log(`  Error: ${errorChirho}`);
      console.log("  Trying next source...\n");
    }
  }

  if (!textChirho) {
    throw new Error("All cross-reference download sources failed.");
  }

  await writeFile(outputPathChirho, textChirho, "utf-8");

  // Parse and count
  const linesChirho = textChirho
    .split("\n")
    .filter((lChirho) => lChirho.trim());

  // Count unique source verses and total cross-reference pairs
  let pairCountChirho = 0;
  const sourceVersesChirho = new Set<string>();
  const targetVersesChirho = new Set<string>();
  let skippedChirho = 0;

  for (const lineChirho of linesChirho) {
    // Skip comments / header lines
    if (lineChirho.startsWith("#") || lineChirho.startsWith("From")) {
      skippedChirho++;
      continue;
    }

    const partsChirho = lineChirho.split("\t");
    if (partsChirho.length >= 2) {
      const sourceRefChirho = partsChirho[0].trim();
      const targetRefChirho = partsChirho[1].trim();
      if (sourceRefChirho && targetRefChirho) {
        sourceVersesChirho.add(sourceRefChirho);
        targetVersesChirho.add(targetRefChirho);
        pairCountChirho++;
      }
    }
  }

  const sizeMbChirho = (Buffer.byteLength(textChirho) / 1024 / 1024).toFixed(1);

  console.log(`\n  Downloaded ${sizeMbChirho} MB`);
  console.log(`  Total lines: ${linesChirho.length}`);
  console.log(`  Skipped (headers/comments): ${skippedChirho}`);
  console.log(`  Cross-reference pairs: ${pairCountChirho}`);
  console.log(`  Unique source verses: ${sourceVersesChirho.size}`);
  console.log(`  Unique target verses: ${targetVersesChirho.size}`);

  // Show sample
  const sampleLinesChirho = linesChirho
    .filter(
      (lChirho) => !lChirho.startsWith("#") && !lChirho.startsWith("From")
    )
    .slice(0, 5);
  console.log("\n  Sample entries:");
  for (const sampleChirho of sampleLinesChirho) {
    const partsChirho = sampleChirho.split("\t");
    console.log(`    ${partsChirho[0]} -> ${partsChirho[1]}`);
  }

  console.log("\n================================");
  console.log(`Output: ${outputPathChirho}`);
  console.log("\nDone!");
}

mainChirho();
