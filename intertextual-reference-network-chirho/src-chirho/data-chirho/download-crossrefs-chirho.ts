// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-crossrefs-chirho.ts
 * Downloads OpenBible.info cross-references (344,799 pairs with relevance votes).
 * Source: https://a.openbible.info/data/cross-references.zip (CC Attribution)
 * Parses TSV → JSON for downstream use.
 */

import { writeFile, readFile, mkdir } from "fs/promises";

const RAW_DIR_CHIRHO = `${process.cwd()}/data-chirho/raw-chirho/`;
const CROSSREFS_URL_CHIRHO = "https://a.openbible.info/data/cross-references.zip";
const OUTPUT_PATH_CHIRHO = `${RAW_DIR_CHIRHO}crossrefs-chirho.json`;

interface CrossRefChirho {
  fromVerseChirho: string;
  toVerseChirho: string;
  votesChirho: number;
}

async function downloadAndExtractChirho(): Promise<string> {
  console.log("Downloading OpenBible cross-references...");
  console.log(`  URL: ${CROSSREFS_URL_CHIRHO}`);

  const responseChirho = await fetch(CROSSREFS_URL_CHIRHO);
  if (!responseChirho.ok) {
    throw new Error(`Download failed: ${responseChirho.status} ${responseChirho.statusText}`);
  }

  const zipBufferChirho = await responseChirho.arrayBuffer();
  const zipPathChirho = `${RAW_DIR_CHIRHO}cross-references.zip`;
  await writeFile(zipPathChirho, Buffer.from(zipBufferChirho));
  console.log(`  Downloaded ${(zipBufferChirho.byteLength / 1024 / 1024).toFixed(1)} MB`);

  // Extract using unzip command (available on macOS)
  const procChirho = Bun.spawn(["unzip", "-o", zipPathChirho, "-d", RAW_DIR_CHIRHO], {
    stdout: "pipe",
    stderr: "pipe",
  });
  await procChirho.exited;

  // The zip contains cross_references.txt (TSV format)
  const extractedPathChirho = `${RAW_DIR_CHIRHO}cross_references.txt`;

  // Try to find the extracted file
  const possiblePathsChirho = [
    extractedPathChirho,
    `${RAW_DIR_CHIRHO}cross-references.txt`,
  ];

  for (const pathChirho of possiblePathsChirho) {
    try {
      const contentChirho = await readFile(pathChirho, "utf-8");
      console.log(`  Extracted: ${pathChirho}`);
      return contentChirho;
    } catch {
      // Try next
    }
  }

  // If no specific file found, list the directory and read whatever was extracted
  const lsChirho = Bun.spawn(["ls", "-la", RAW_DIR_CHIRHO], { stdout: "pipe" });
  const lsOutputChirho = await new Response(lsChirho.stdout).text();
  console.log("  Files in raw dir:", lsOutputChirho);

  throw new Error("Could not find extracted cross-references file");
}

function parseCrossRefsChirho(contentChirho: string): CrossRefChirho[] {
  console.log("Parsing cross-references...");

  const linesChirho = contentChirho.trim().split("\n");
  const refsChirho: CrossRefChirho[] = [];
  let skippedChirho = 0;

  for (const lineChirho of linesChirho) {
    // Skip header/comment lines
    if (lineChirho.startsWith("#") || lineChirho.startsWith("From") || !lineChirho.trim()) {
      continue;
    }

    // TSV format: FromVerse\tToVerse\tVotes
    const partsChirho = lineChirho.split("\t");
    if (partsChirho.length < 2) {
      skippedChirho++;
      continue;
    }

    const fromVerseChirho = partsChirho[0].trim();
    const toVerseChirho = partsChirho[1].trim();
    const votesChirho = partsChirho.length >= 3 ? parseInt(partsChirho[2], 10) : 0;

    if (!fromVerseChirho || !toVerseChirho) {
      skippedChirho++;
      continue;
    }

    refsChirho.push({
      fromVerseChirho,
      toVerseChirho,
      votesChirho: isNaN(votesChirho) ? 0 : votesChirho,
    });
  }

  console.log(`  Parsed ${refsChirho.length} cross-references (skipped ${skippedChirho} lines)`);
  return refsChirho;
}

async function mainChirho(): Promise<void> {
  console.log("OpenBible Cross-References Downloader");
  console.log("=====================================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  // Check if already downloaded
  try {
    const existingChirho = await readFile(OUTPUT_PATH_CHIRHO, "utf-8");
    const parsedChirho = JSON.parse(existingChirho);
    if (Array.isArray(parsedChirho) && parsedChirho.length > 100000) {
      console.log(`Cross-references already downloaded (${parsedChirho.length} pairs). Skipping.`);
      return;
    }
  } catch {
    // Not downloaded yet
  }

  const contentChirho = await downloadAndExtractChirho();
  const refsChirho = parseCrossRefsChirho(contentChirho);

  // Sort by votes (highest first) for priority labeling later
  refsChirho.sort((aChirho, bChirho) => bChirho.votesChirho - aChirho.votesChirho);

  // Write JSON
  await writeFile(OUTPUT_PATH_CHIRHO, JSON.stringify(refsChirho, null, 0), "utf-8");
  console.log(`\nSaved ${refsChirho.length} cross-references to ${OUTPUT_PATH_CHIRHO}`);

  // Stats
  const withVotesChirho = refsChirho.filter((rChirho) => rChirho.votesChirho > 0);
  const maxVotesChirho = refsChirho[0]?.votesChirho ?? 0;
  console.log(`\nStats:`);
  console.log(`  Total pairs: ${refsChirho.length}`);
  console.log(`  With votes > 0: ${withVotesChirho.length}`);
  console.log(`  Max votes: ${maxVotesChirho}`);

  // Sample top references
  console.log(`\nTop 5 cross-references:`);
  for (const refChirho of refsChirho.slice(0, 5)) {
    console.log(`  ${refChirho.fromVerseChirho} -> ${refChirho.toVerseChirho} (votes: ${refChirho.votesChirho})`);
  }
}

mainChirho();
