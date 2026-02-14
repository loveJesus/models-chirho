// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * augment-classifier-chirho.ts
 * Expands classifier seeds by labeling more cross-reference pairs from the 344K pool.
 * Target: 30K labeled pairs (2K seeds + 28K augmented).
 * RESUMABLE with PARALLEL API calls.
 *
 * Usage:
 *   bun run src-chirho/data-chirho/augment-classifier-chirho.ts           # augment (resumable)
 *   bun run src-chirho/data-chirho/augment-classifier-chirho.ts finalize  # shuffle + split
 */

import { writeFile, readFile, mkdir, appendFile, access } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${process.cwd()}/data-chirho/processed-chirho/`;
const SEEDS_DIR_CHIRHO = `${process.cwd()}/data-chirho/seeds-chirho/`;

const GROK_API_KEY_CHIRHO = process.env.GROK_API_KEY_CHIRHO || process.env.GROK_API_KEY;
if (!GROK_API_KEY_CHIRHO) {
  throw new Error("GROK_API_KEY_CHIRHO not set. Export it first.");
}

const GROK_API_URL_CHIRHO = "https://api.x.ai/v1/chat/completions";

const TARGET_COUNT_CHIRHO = 30000;
const BATCH_SIZE_CHIRHO = 20; // pairs per API call (larger since just labeling)
const CONCURRENCY_CHIRHO = 5;

const CONNECTION_TYPES_CHIRHO = [
  "direct_quote",
  "allusion",
  "thematic_parallel",
  "typological",
  "prophecy_fulfillment",
  "parallel_narrative",
  "contrast",
] as const;

type ConnectionTypeChirho = (typeof CONNECTION_TYPES_CHIRHO)[number];

interface ResolvedRefChirho {
  fromIdChirho: string;
  toIdChirho: string;
  fromTextChirho: string;
  toTextChirho: string;
  votesChirho: number;
}

interface GrokResponseChirho {
  choices: Array<{ message: { content: string } }>;
}

interface ProgressChirho {
  completedBatchesChirho: number[];
  totalAugmentedChirho: number;
  timestampChirho: string;
}

const AUGMENTED_FILE_CHIRHO = `${PROCESSED_DIR_CHIRHO}augmented-classifier-chirho.jsonl`;
const PROGRESS_FILE_CHIRHO = `${PROCESSED_DIR_CHIRHO}augment-classifier-progress-chirho.json`;

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    await access(pathChirho);
    return true;
  } catch {
    return false;
  }
}

async function loadProgressChirho(): Promise<ProgressChirho> {
  if (await fileExistsChirho(PROGRESS_FILE_CHIRHO)) {
    return JSON.parse(await readFile(PROGRESS_FILE_CHIRHO, "utf-8"));
  }
  return { completedBatchesChirho: [], totalAugmentedChirho: 0, timestampChirho: "" };
}

async function saveProgressChirho(progressChirho: ProgressChirho): Promise<void> {
  progressChirho.timestampChirho = new Date().toISOString();
  await writeFile(PROGRESS_FILE_CHIRHO, JSON.stringify(progressChirho, null, 2), "utf-8");
}

let writeLockChirho = Promise.resolve();
async function appendSafeChirho(dataChirho: string): Promise<void> {
  writeLockChirho = writeLockChirho.then(() => appendFile(AUGMENTED_FILE_CHIRHO, dataChirho, "utf-8"));
  await writeLockChirho;
}

async function labelBatchChirho(pairsChirho: ResolvedRefChirho[]): Promise<Record<string, unknown>[]> {
  const pairsDescChirho = pairsChirho.map((pChirho, iChirho) => ({
    iChirho,
    fChirho: pChirho.fromIdChirho,
    tChirho: pChirho.toIdChirho,
    ftChirho: pChirho.fromTextChirho.substring(0, 250),
    ttChirho: pChirho.toTextChirho.substring(0, 250),
  }));

  const promptChirho = `Classify these ${pairsChirho.length} Bible cross-reference pairs by connection type.

Types: direct_quote, allusion, thematic_parallel, typological, prophecy_fulfillment, parallel_narrative, contrast

${JSON.stringify(pairsDescChirho)}

Return JSON array. Each: {"i":N,"t":"type","c":0.7,"r":"brief reason"}
JSON only, no other text.`;

  const responseChirho = await fetch(GROK_API_URL_CHIRHO, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${GROK_API_KEY_CHIRHO}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "grok-4-1-fast-non-reasoning",
      messages: [
        {
          role: "system",
          content: "Biblical scholar classifying intertextual connections. Return only valid JSON array.",
        },
        { role: "user", content: promptChirho },
      ],
      max_tokens: 6000,
      temperature: 0.3,
    }),
  });

  if (!responseChirho.ok) {
    throw new Error(`Grok API error ${responseChirho.status}`);
  }

  const dataChirho = (await responseChirho.json()) as GrokResponseChirho;
  let contentChirho = dataChirho.choices[0]?.message?.content ?? "";
  contentChirho = contentChirho.trim();
  if (contentChirho.startsWith("```")) {
    contentChirho = contentChirho.replace(/^```(?:json)?\n?/, "").replace(/\n?```$/, "");
  }

  const parsedChirho = JSON.parse(contentChirho) as Array<Record<string, unknown>>;

  return parsedChirho.map((itemChirho) => {
    const idxChirho = Number(itemChirho.i ?? itemChirho.iChirho ?? itemChirho.index_chirho ?? 0);
    const pairChirho = pairsChirho[idxChirho] ?? pairsChirho[0];

    const rawTypeChirho = String(itemChirho.t ?? itemChirho.connection_type_chirho ?? "thematic_parallel");
    const typeChirho = CONNECTION_TYPES_CHIRHO.includes(rawTypeChirho as ConnectionTypeChirho)
      ? rawTypeChirho
      : "thematic_parallel";

    return {
      from_id_chirho: pairChirho.fromIdChirho,
      to_id_chirho: pairChirho.toIdChirho,
      from_text_chirho: pairChirho.fromTextChirho,
      to_text_chirho: pairChirho.toTextChirho,
      connection_type_chirho: typeChirho,
      confidence_chirho: Math.min(1.0, Math.max(0.5, Number(itemChirho.c ?? itemChirho.confidence_chirho ?? 0.8))),
      reasoning_chirho: String(itemChirho.r ?? itemChirho.reasoning_chirho ?? ""),
      votes_chirho: pairChirho.votesChirho,
      source_chirho: "augmented",
    };
  });
}

async function augmentChirho(): Promise<void> {
  console.log("Classifier Augmentation Pipeline (Grok/xAI)");
  console.log("=============================================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  // Load resolved cross-references
  console.log("Loading resolved cross-references...");
  const refsContentChirho = await readFile(`${PROCESSED_DIR_CHIRHO}crossrefs-resolved-chirho.json`, "utf-8");
  const allRefsChirho: ResolvedRefChirho[] = JSON.parse(refsContentChirho);

  // Load seeds count
  let seedCountChirho = 0;
  const seedsPathChirho = `${SEEDS_DIR_CHIRHO}seeds-chirho.jsonl`;
  if (await fileExistsChirho(seedsPathChirho)) {
    const seedsContentChirho = await readFile(seedsPathChirho, "utf-8");
    seedCountChirho = seedsContentChirho.trim().split("\n").filter((lChirho) => lChirho.trim()).length;
  }
  console.log(`  Seed count: ${seedCountChirho}`);

  // Skip the first seedCount pairs (already labeled in seeds)
  const augmentPoolChirho = allRefsChirho.slice(seedCountChirho);
  const neededChirho = TARGET_COUNT_CHIRHO - seedCountChirho;
  console.log(`  Augment pool: ${augmentPoolChirho.length} pairs`);
  console.log(`  Need: ${neededChirho} more labels`);

  // Take enough pairs from the pool
  const pairsToLabelChirho = augmentPoolChirho.slice(0, neededChirho);

  // Load progress
  const progressChirho = await loadProgressChirho();
  console.log(`  Previously: ${progressChirho.completedBatchesChirho.length} batches, ${progressChirho.totalAugmentedChirho} augmented`);

  const totalNeededChirho = neededChirho - progressChirho.totalAugmentedChirho;
  if (totalNeededChirho <= 0) {
    console.log("Target already reached! Run with 'finalize' to split.");
    return;
  }

  // Build batches
  const batchCountChirho = Math.ceil(pairsToLabelChirho.length / BATCH_SIZE_CHIRHO);
  const completedSetChirho = new Set(progressChirho.completedBatchesChirho);

  const pendingChirho: Array<{ batchIdChirho: number; pairsChirho: ResolvedRefChirho[] }> = [];
  for (let bChirho = 0; bChirho < batchCountChirho; bChirho++) {
    if (!completedSetChirho.has(bChirho)) {
      pendingChirho.push({
        batchIdChirho: bChirho,
        pairsChirho: pairsToLabelChirho.slice(bChirho * BATCH_SIZE_CHIRHO, (bChirho + 1) * BATCH_SIZE_CHIRHO),
      });
    }
  }

  console.log(`  Total batches: ${batchCountChirho}, Pending: ${pendingChirho.length}`);
  console.log(`  Concurrency: ${CONCURRENCY_CHIRHO}\n`);

  let totalAugmentedChirho = progressChirho.totalAugmentedChirho;
  let completedIdsChirho = [...progressChirho.completedBatchesChirho];
  let doneChirho = false;
  let batchIdxChirho = 0;

  while (batchIdxChirho < pendingChirho.length && !doneChirho) {
    const waveChirho: Promise<void>[] = [];
    const waveSizeChirho = Math.min(CONCURRENCY_CHIRHO, pendingChirho.length - batchIdxChirho);

    for (let wChirho = 0; wChirho < waveSizeChirho; wChirho++) {
      const batchChirho = pendingChirho[batchIdxChirho++];
      waveChirho.push(
        (async () => {
          try {
            const labeledChirho = await labelBatchChirho(batchChirho.pairsChirho);
            const linesChirho = labeledChirho.map((lChirho) => JSON.stringify(lChirho)).join("\n");
            await appendSafeChirho(linesChirho + "\n");

            totalAugmentedChirho += labeledChirho.length;
            completedIdsChirho.push(batchChirho.batchIdChirho);

            console.log(`  B${batchChirho.batchIdChirho + 1}/${batchCountChirho}: +${labeledChirho.length} (total: ${seedCountChirho + totalAugmentedChirho}/${TARGET_COUNT_CHIRHO})`);

            if (seedCountChirho + totalAugmentedChirho >= TARGET_COUNT_CHIRHO) {
              doneChirho = true;
            }
          } catch (errorChirho) {
            console.error(`  B${batchChirho.batchIdChirho + 1} FAILED: ${String(errorChirho).substring(0, 100)}`);
            completedIdsChirho.push(batchChirho.batchIdChirho);
          }
        })()
      );
    }

    await Promise.all(waveChirho);
    await saveProgressChirho({ completedBatchesChirho: completedIdsChirho, totalAugmentedChirho, timestampChirho: "" });
    await new Promise((rChirho) => setTimeout(rChirho, 300));
  }

  console.log(`\nAugmentation session complete. Total augmented: ${totalAugmentedChirho}`);
  if (seedCountChirho + totalAugmentedChirho >= TARGET_COUNT_CHIRHO) {
    console.log("Target reached! Run with 'finalize' to shuffle and split.");
  } else {
    console.log("Run again to continue (resumable).");
  }
}

async function finalizeChirho(): Promise<void> {
  console.log("Classifier Dataset Finalization - Shuffle & Split");
  console.log("=================================================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  // Load seeds
  const seedsPathChirho = `${SEEDS_DIR_CHIRHO}seeds-chirho.jsonl`;
  let seedsChirho: Record<string, unknown>[] = [];
  if (await fileExistsChirho(seedsPathChirho)) {
    const contentChirho = await readFile(seedsPathChirho, "utf-8");
    seedsChirho = contentChirho.trim().split("\n").filter((lChirho) => lChirho.trim()).map((lChirho) => JSON.parse(lChirho));
  }
  console.log(`  Seeds: ${seedsChirho.length}`);

  // Load augmented
  let augmentedChirho: Record<string, unknown>[] = [];
  if (await fileExistsChirho(AUGMENTED_FILE_CHIRHO)) {
    const contentChirho = await readFile(AUGMENTED_FILE_CHIRHO, "utf-8");
    augmentedChirho = contentChirho.trim().split("\n").filter((lChirho) => lChirho.trim()).map((lChirho) => JSON.parse(lChirho));
  }
  console.log(`  Augmented: ${augmentedChirho.length}`);

  // Combine and trim
  const allExamplesChirho = [...seedsChirho, ...augmentedChirho].slice(0, TARGET_COUNT_CHIRHO);
  console.log(`  Combined: ${allExamplesChirho.length}`);

  // Fisher-Yates shuffle
  for (let iChirho = allExamplesChirho.length - 1; iChirho > 0; iChirho--) {
    const jChirho = Math.floor(Math.random() * (iChirho + 1));
    [allExamplesChirho[iChirho], allExamplesChirho[jChirho]] = [allExamplesChirho[jChirho], allExamplesChirho[iChirho]];
  }

  // Split 80/10/10
  const trainEndChirho = Math.floor(allExamplesChirho.length * 0.8);
  const valEndChirho = Math.floor(allExamplesChirho.length * 0.9);

  const trainChirho = allExamplesChirho.slice(0, trainEndChirho);
  const valChirho = allExamplesChirho.slice(trainEndChirho, valEndChirho);
  const testChirho = allExamplesChirho.slice(valEndChirho);

  const toJsonlChirho = (dataChirho: Record<string, unknown>[]) =>
    dataChirho.map((exChirho) => JSON.stringify(exChirho)).join("\n");

  await writeFile(`${PROCESSED_DIR_CHIRHO}train-classifier-chirho.jsonl`, toJsonlChirho(trainChirho), "utf-8");
  await writeFile(`${PROCESSED_DIR_CHIRHO}val-classifier-chirho.jsonl`, toJsonlChirho(valChirho), "utf-8");
  await writeFile(`${PROCESSED_DIR_CHIRHO}test-classifier-chirho.jsonl`, toJsonlChirho(testChirho), "utf-8");

  console.log(`\nDataset splits:`);
  console.log(`  Train: ${trainChirho.length}`);
  console.log(`  Validation: ${valChirho.length}`);
  console.log(`  Test: ${testChirho.length}`);

  // Distribution
  const distChirho: Record<string, number> = {};
  for (const exChirho of allExamplesChirho) {
    const typeChirho = String((exChirho as Record<string, unknown>).connection_type_chirho || "unknown");
    distChirho[typeChirho] = (distChirho[typeChirho] || 0) + 1;
  }

  console.log(`\nConnection type distribution:`);
  for (const [typeChirho, countChirho] of Object.entries(distChirho).sort((aChirho, bChirho) => bChirho[1] - aChirho[1])) {
    console.log(`  ${typeChirho}: ${countChirho} (${(countChirho / allExamplesChirho.length * 100).toFixed(1)}%)`);
  }
}

// Main dispatch
const modeChirho = process.argv[2];
if (modeChirho === "finalize") {
  finalizeChirho();
} else {
  augmentChirho();
}
