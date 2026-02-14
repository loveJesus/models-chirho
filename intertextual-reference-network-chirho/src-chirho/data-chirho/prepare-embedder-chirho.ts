// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * prepare-embedder-chirho.ts
 * Creates training triplets from resolved cross-reference pairs for the embedder.
 * Anchor = verse A, Positive = cross-referenced verse B, Negative = random unrelated verse
 * Hard negatives: prefer same-book verses for harder training signal.
 * Split 80/10/10 → {train,val,test}-embedder-chirho.jsonl
 */

import { writeFile, readFile, mkdir } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${process.cwd()}/data-chirho/processed-chirho/`;

interface ResolvedRefChirho {
  fromIdChirho: string;
  toIdChirho: string;
  fromTextChirho: string;
  toTextChirho: string;
  votesChirho: number;
}

interface TripletChirho {
  anchor_id_chirho: string;
  anchor_text_chirho: string;
  positive_id_chirho: string;
  positive_text_chirho: string;
  negative_id_chirho: string;
  negative_text_chirho: string;
  votes_chirho: number;
}

// Seeded random for reproducibility
function seededRandomChirho(seedChirho: number): () => number {
  let stateChirho = seedChirho;
  return () => {
    stateChirho = (stateChirho * 1664525 + 1013904223) & 0xffffffff;
    return (stateChirho >>> 0) / 0xffffffff;
  };
}

async function mainChirho(): Promise<void> {
  console.log("Embedder Triplet Preparation");
  console.log("============================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  // Load resolved cross-references
  console.log("Loading resolved cross-references...");
  const refsContentChirho = await readFile(`${PROCESSED_DIR_CHIRHO}crossrefs-resolved-chirho.json`, "utf-8");
  const refsChirho: ResolvedRefChirho[] = JSON.parse(refsContentChirho);
  console.log(`  Loaded ${refsChirho.length} resolved pairs`);

  // Load verse map for negative sampling
  console.log("Loading verse map...");
  const verseMapContentChirho = await readFile(`${PROCESSED_DIR_CHIRHO}verse-map-chirho.json`, "utf-8");
  const verseMapChirho: Record<string, string> = JSON.parse(verseMapContentChirho);
  const allVerseIdsChirho = Object.keys(verseMapChirho);
  console.log(`  Loaded ${allVerseIdsChirho.length} verses`);

  // Build book-to-verse index for hard negatives
  const bookIndexChirho: Record<string, string[]> = {};
  for (const idChirho of allVerseIdsChirho) {
    const bookChirho = idChirho.split(".")[0];
    if (!bookIndexChirho[bookChirho]) bookIndexChirho[bookChirho] = [];
    bookIndexChirho[bookChirho].push(idChirho);
  }

  // Build set of known cross-ref pairs for negative filtering
  const knownPairsChirho = new Set<string>();
  for (const refChirho of refsChirho) {
    knownPairsChirho.add(`${refChirho.fromIdChirho}|${refChirho.toIdChirho}`);
    knownPairsChirho.add(`${refChirho.toIdChirho}|${refChirho.fromIdChirho}`);
  }

  // Generate triplets
  console.log("\nGenerating triplets...");
  const randomChirho = seededRandomChirho(42);
  const tripletsChirho: TripletChirho[] = [];

  for (let iChirho = 0; iChirho < refsChirho.length; iChirho++) {
    const refChirho = refsChirho[iChirho];

    // Find a hard negative: same book as anchor, but NOT a known cross-reference
    const anchorBookChirho = refChirho.fromIdChirho.split(".")[0];
    const sameBookVersesChirho = bookIndexChirho[anchorBookChirho] || [];

    let negativeIdChirho: string | null = null;
    let negativeTextChirho: string | null = null;

    // Try hard negative (same book) first — 3 attempts
    for (let attemptChirho = 0; attemptChirho < 3; attemptChirho++) {
      const candidateIdxChirho = Math.floor(randomChirho() * sameBookVersesChirho.length);
      const candidateIdChirho = sameBookVersesChirho[candidateIdxChirho];

      if (
        candidateIdChirho !== refChirho.fromIdChirho &&
        candidateIdChirho !== refChirho.toIdChirho &&
        !knownPairsChirho.has(`${refChirho.fromIdChirho}|${candidateIdChirho}`)
      ) {
        negativeIdChirho = candidateIdChirho;
        negativeTextChirho = verseMapChirho[candidateIdChirho];
        break;
      }
    }

    // Fallback: random verse from any book
    if (!negativeIdChirho || !negativeTextChirho) {
      const candidateIdxChirho = Math.floor(randomChirho() * allVerseIdsChirho.length);
      negativeIdChirho = allVerseIdsChirho[candidateIdxChirho];
      negativeTextChirho = verseMapChirho[negativeIdChirho];
    }

    if (negativeTextChirho) {
      tripletsChirho.push({
        anchor_id_chirho: refChirho.fromIdChirho,
        anchor_text_chirho: refChirho.fromTextChirho,
        positive_id_chirho: refChirho.toIdChirho,
        positive_text_chirho: refChirho.toTextChirho,
        negative_id_chirho: negativeIdChirho!,
        negative_text_chirho: negativeTextChirho,
        votes_chirho: refChirho.votesChirho,
      });
    }

    if ((iChirho + 1) % 50000 === 0) {
      console.log(`  Generated ${iChirho + 1}/${refsChirho.length} triplets...`);
    }
  }

  console.log(`  Total triplets: ${tripletsChirho.length}`);

  // Shuffle (Fisher-Yates)
  for (let iChirho = tripletsChirho.length - 1; iChirho > 0; iChirho--) {
    const jChirho = Math.floor(randomChirho() * (iChirho + 1));
    [tripletsChirho[iChirho], tripletsChirho[jChirho]] = [tripletsChirho[jChirho], tripletsChirho[iChirho]];
  }

  // Split 80/10/10
  const trainEndChirho = Math.floor(tripletsChirho.length * 0.8);
  const valEndChirho = Math.floor(tripletsChirho.length * 0.9);

  const trainChirho = tripletsChirho.slice(0, trainEndChirho);
  const valChirho = tripletsChirho.slice(trainEndChirho, valEndChirho);
  const testChirho = tripletsChirho.slice(valEndChirho);

  // Write JSONL files
  const toJsonlChirho = (dataChirho: TripletChirho[]) =>
    dataChirho.map((tChirho) => JSON.stringify(tChirho)).join("\n");

  await writeFile(`${PROCESSED_DIR_CHIRHO}train-embedder-chirho.jsonl`, toJsonlChirho(trainChirho), "utf-8");
  await writeFile(`${PROCESSED_DIR_CHIRHO}val-embedder-chirho.jsonl`, toJsonlChirho(valChirho), "utf-8");
  await writeFile(`${PROCESSED_DIR_CHIRHO}test-embedder-chirho.jsonl`, toJsonlChirho(testChirho), "utf-8");

  console.log(`\nSplit results:`);
  console.log(`  Train: ${trainChirho.length}`);
  console.log(`  Validation: ${valChirho.length}`);
  console.log(`  Test: ${testChirho.length}`);

  // Stats on hard negatives
  let hardNegativeCountChirho = 0;
  for (const tripletChirho of tripletsChirho) {
    const anchorBookChirho = tripletChirho.anchor_id_chirho.split(".")[0];
    const negBookChirho = tripletChirho.negative_id_chirho.split(".")[0];
    if (anchorBookChirho === negBookChirho) hardNegativeCountChirho++;
  }

  console.log(`\n  Hard negatives (same book): ${hardNegativeCountChirho} (${(hardNegativeCountChirho / tripletsChirho.length * 100).toFixed(1)}%)`);
  console.log(`  Sample triplet:`);
  const sampleChirho = tripletsChirho[0];
  console.log(`    Anchor: ${sampleChirho.anchor_id_chirho} = "${sampleChirho.anchor_text_chirho.substring(0, 60)}..."`);
  console.log(`    Positive: ${sampleChirho.positive_id_chirho} = "${sampleChirho.positive_text_chirho.substring(0, 60)}..."`);
  console.log(`    Negative: ${sampleChirho.negative_id_chirho} = "${sampleChirho.negative_text_chirho.substring(0, 60)}..."`);
}

mainChirho();
