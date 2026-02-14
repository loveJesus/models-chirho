// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * build-verse-map-chirho.ts
 * Builds a verse ID → text map from the KJV data.
 * Also normalizes cross-reference verse IDs to match the KJV verse IDs.
 * Output: verse-map-chirho.json (~31K entries)
 */

import { writeFile, readFile, mkdir } from "fs/promises";

const RAW_DIR_CHIRHO = `${process.cwd()}/data-chirho/raw-chirho/`;
const PROCESSED_DIR_CHIRHO = `${process.cwd()}/data-chirho/processed-chirho/`;

interface VerseChirho {
  verseIdChirho: string;
  bookChirho: string;
  chapterChirho: number;
  verseNumChirho: number;
  textChirho: string;
}

interface CrossRefChirho {
  fromVerseChirho: string;
  toVerseChirho: string;
  votesChirho: number;
}

// OpenBible uses format like "Gen.1.1" or "Gen 1:1" — normalize both
// Our KJV data uses OSIS format: "Gen.1.1"
function normalizeVerseIdChirho(rawIdChirho: string): string {
  // Handle ranges like "Gen.1.1-Gen.1.3" — take the start
  let idChirho = rawIdChirho.split("-")[0].trim();

  // Handle "Gen 1:1" format → "Gen.1.1"
  idChirho = idChirho.replace(/\s+/g, ".").replace(/:/g, ".");

  return idChirho;
}

async function mainChirho(): Promise<void> {
  console.log("Verse Map Builder");
  console.log("=================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  // Load KJV verses
  console.log("Loading KJV verses...");
  const kjvContentChirho = await readFile(`${RAW_DIR_CHIRHO}kjv-chirho.json`, "utf-8");
  const kjvVersesChirho: VerseChirho[] = JSON.parse(kjvContentChirho);
  console.log(`  Loaded ${kjvVersesChirho.length} verses`);

  // Build verse map: ID → text
  const verseMapChirho: Record<string, string> = {};
  for (const verseChirho of kjvVersesChirho) {
    verseMapChirho[verseChirho.verseIdChirho] = verseChirho.textChirho;
  }

  console.log(`  Built map with ${Object.keys(verseMapChirho).length} entries`);

  // Save verse map
  const verseMapPathChirho = `${PROCESSED_DIR_CHIRHO}verse-map-chirho.json`;
  await writeFile(verseMapPathChirho, JSON.stringify(verseMapChirho), "utf-8");
  console.log(`  Saved: ${verseMapPathChirho}`);

  // Load cross-references and resolve verse texts
  console.log("\nLoading cross-references...");
  const crossrefsContentChirho = await readFile(`${RAW_DIR_CHIRHO}crossrefs-chirho.json`, "utf-8");
  const crossrefsChirho: CrossRefChirho[] = JSON.parse(crossrefsContentChirho);
  console.log(`  Loaded ${crossrefsChirho.length} cross-references`);

  // Resolve cross-references against verse map
  let resolvedCountChirho = 0;
  let unresolvedCountChirho = 0;
  const unresolvedIdsChirho = new Set<string>();

  const resolvedRefsChirho: Array<{
    fromIdChirho: string;
    toIdChirho: string;
    fromTextChirho: string;
    toTextChirho: string;
    votesChirho: number;
  }> = [];

  for (const refChirho of crossrefsChirho) {
    const fromIdChirho = normalizeVerseIdChirho(refChirho.fromVerseChirho);
    const toIdChirho = normalizeVerseIdChirho(refChirho.toVerseChirho);

    const fromTextChirho = verseMapChirho[fromIdChirho];
    const toTextChirho = verseMapChirho[toIdChirho];

    if (fromTextChirho && toTextChirho) {
      resolvedRefsChirho.push({
        fromIdChirho,
        toIdChirho,
        fromTextChirho,
        toTextChirho,
        votesChirho: refChirho.votesChirho,
      });
      resolvedCountChirho++;
    } else {
      unresolvedCountChirho++;
      if (!fromTextChirho) unresolvedIdsChirho.add(fromIdChirho);
      if (!toTextChirho) unresolvedIdsChirho.add(toIdChirho);
    }
  }

  // Save resolved cross-references (with text)
  const resolvedPathChirho = `${PROCESSED_DIR_CHIRHO}crossrefs-resolved-chirho.json`;
  await writeFile(resolvedPathChirho, JSON.stringify(resolvedRefsChirho, null, 0), "utf-8");

  console.log(`\nResolution results:`);
  console.log(`  Resolved: ${resolvedCountChirho} (${(resolvedCountChirho / crossrefsChirho.length * 100).toFixed(1)}%)`);
  console.log(`  Unresolved: ${unresolvedCountChirho}`);
  console.log(`  Unique unresolved IDs: ${unresolvedIdsChirho.size}`);

  if (unresolvedIdsChirho.size > 0 && unresolvedIdsChirho.size <= 20) {
    console.log(`  Sample unresolved: ${[...unresolvedIdsChirho].slice(0, 10).join(", ")}`);
  }

  // Save book-level stats
  const bookStatsChirho: Record<string, { versesChirho: number; refsFromChirho: number; refsToChirho: number }> = {};
  for (const verseChirho of kjvVersesChirho) {
    if (!bookStatsChirho[verseChirho.bookChirho]) {
      bookStatsChirho[verseChirho.bookChirho] = { versesChirho: 0, refsFromChirho: 0, refsToChirho: 0 };
    }
    bookStatsChirho[verseChirho.bookChirho].versesChirho++;
  }
  for (const refChirho of resolvedRefsChirho) {
    const fromBookChirho = refChirho.fromIdChirho.split(".")[0];
    const toBookChirho = refChirho.toIdChirho.split(".")[0];
    if (bookStatsChirho[fromBookChirho]) bookStatsChirho[fromBookChirho].refsFromChirho++;
    if (bookStatsChirho[toBookChirho]) bookStatsChirho[toBookChirho].refsToChirho++;
  }

  console.log(`\nTop 10 most-referenced books:`);
  const sortedBooksChirho = Object.entries(bookStatsChirho)
    .sort((aChirho, bChirho) => (bChirho[1].refsFromChirho + bChirho[1].refsToChirho) - (aChirho[1].refsFromChirho + aChirho[1].refsToChirho))
    .slice(0, 10);

  for (const [bookChirho, statsChirho] of sortedBooksChirho) {
    console.log(`  ${bookChirho}: ${statsChirho.versesChirho} verses, ${statsChirho.refsFromChirho} from, ${statsChirho.refsToChirho} to`);
  }

  console.log(`\nSaved resolved cross-references to: ${resolvedPathChirho}`);
}

mainChirho();
