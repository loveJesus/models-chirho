// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * augment-dataset-chirho.ts
 * Expands 500 seed examples to ~22,500 via Grok/xAI-assisted paraphrasing.
 * RESUMABLE with PARALLEL API calls for speed.
 *
 * Usage:
 *   bun run src-chirho/data-chirho/augment-dataset-chirho.ts           # augment (resumable)
 *   bun run src-chirho/data-chirho/augment-dataset-chirho.ts finalize  # shuffle + split
 */

import { writeFile, readFile, mkdir, appendFile, access } from "fs/promises";

const SEEDS_DIR_CHIRHO = `${process.cwd()}/data-chirho/seeds-chirho/`;
const PROCESSED_DIR_CHIRHO = `${process.cwd()}/data-chirho/processed-chirho/`;

const GROK_API_KEY_CHIRHO = process.env.GROK_API_KEY_CHIRHO || process.env.GROK_API_KEY;
if (!GROK_API_KEY_CHIRHO) {
  throw new Error("GROK_API_KEY_CHIRHO not set. Source .env-chirho first.");
}

const GROK_API_URL_CHIRHO = "https://api.x.ai/v1/chat/completions";

const TARGET_COUNT_CHIRHO = 22500;
const BATCH_SIZE_CHIRHO = 5; // seeds per API call (smaller = faster response)
const PARAPHRASES_PER_CALL_CHIRHO = 10; // paraphrases per seed per call
const CONCURRENCY_CHIRHO = 5; // parallel API calls
const TOTAL_ROUNDS_CHIRHO = 9; // rounds per seed batch (9 * 10 ≈ 90 > 44 needed)

const PARTIAL_FILE_CHIRHO = `${PROCESSED_DIR_CHIRHO}augmented-partial-chirho.jsonl`;
const PROGRESS_FILE_CHIRHO = `${PROCESSED_DIR_CHIRHO}augment-progress-chirho.json`;

interface DatasetExampleChirho {
  text_chirho: string;
  label_chirho: string;
  heresy_types_chirho: string[];
  confidence_chirho: number;
  explanation_chirho: string;
  scripture_refs_chirho: string[];
  creed_refs_chirho: string[];
  domain_chirho: string;
  denominational_note_chirho: string | null;
  source_chirho: "seed" | "augmented";
  seed_index_chirho: number;
}

interface GrokResponseChirho {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

interface ProgressChirho {
  completedJobsChirho: number[];
  totalAugmentedChirho: number;
  timestampChirho: string;
}

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    await access(pathChirho);
    return true;
  } catch {
    return false;
  }
}

async function loadSeedsChirho(): Promise<DatasetExampleChirho[]> {
  const seedContentChirho = await readFile(`${SEEDS_DIR_CHIRHO}seeds-chirho.jsonl`, "utf-8");
  return seedContentChirho
    .trim()
    .split("\n")
    .map((lineChirho, indexChirho) => ({
      ...JSON.parse(lineChirho),
      source_chirho: "seed" as const,
      seed_index_chirho: indexChirho,
    }));
}

async function loadProgressChirho(): Promise<ProgressChirho> {
  if (await fileExistsChirho(PROGRESS_FILE_CHIRHO)) {
    const contentChirho = await readFile(PROGRESS_FILE_CHIRHO, "utf-8");
    return JSON.parse(contentChirho);
  }
  return { completedJobsChirho: [], totalAugmentedChirho: 0, timestampChirho: "" };
}

async function saveProgressChirho(progressChirho: ProgressChirho): Promise<void> {
  progressChirho.timestampChirho = new Date().toISOString();
  await writeFile(PROGRESS_FILE_CHIRHO, JSON.stringify(progressChirho, null, 2), "utf-8");
}

// Mutex for file appends
let writeLockChirho = Promise.resolve();

async function appendSafeChirho(dataChirho: string): Promise<void> {
  writeLockChirho = writeLockChirho.then(() => appendFile(PARTIAL_FILE_CHIRHO, dataChirho, "utf-8"));
  await writeLockChirho;
}

async function augmentBatchChirho(
  seedsChirho: DatasetExampleChirho[],
  augmentCountChirho: number,
): Promise<DatasetExampleChirho[]> {
  const seedTextsChirho = seedsChirho.map((sChirho, iChirho) => ({
    indexChirho: iChirho,
    textChirho: sChirho.text_chirho,
    labelChirho: sChirho.label_chirho,
    heresyTypesChirho: sChirho.heresy_types_chirho,
    domainChirho: sChirho.domain_chirho,
  }));

  const promptChirho = `Generate ${augmentCountChirho} paraphrased versions for EACH of the following ${seedsChirho.length} theological statements. Vary phrasing, formality, context, length, and vocabulary while maintaining the EXACT same theological position.

Statements:
${JSON.stringify(seedTextsChirho, null, 2)}

Return a JSON array. Each item: {"text_chirho":"...","seed_index_chirho":N,"label_chirho":"...","heresy_types_chirho":[...],"domain_chirho":"...","confidence_chirho":N}

IMPORTANT: Preserve the theological position exactly. Return ONLY valid JSON array.`;

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
          content: "You are a theological expert generating training data. Produce paraphrases preserving the exact theological position. Return only valid JSON.",
        },
        { role: "user", content: promptChirho },
      ],
      max_tokens: 12000,
      temperature: 0.8,
    }),
  });

  if (!responseChirho.ok) {
    const errorTextChirho = await responseChirho.text();
    throw new Error(`Grok API error ${responseChirho.status}: ${errorTextChirho}`);
  }

  const dataChirho = (await responseChirho.json()) as GrokResponseChirho;
  const contentChirho = dataChirho.choices[0]?.message?.content ?? "";

  let jsonTextChirho = contentChirho.trim();
  if (jsonTextChirho.startsWith("```")) {
    jsonTextChirho = jsonTextChirho.replace(/^```(?:json)?\n?/, "").replace(/\n?```$/, "");
  }

  const parsedChirho = JSON.parse(jsonTextChirho) as Array<Record<string, unknown>>;

  return parsedChirho.map((itemChirho) => {
    const seedIdxChirho = Number(itemChirho.seed_index_chirho ?? 0);
    const originalSeedChirho = seedsChirho[seedIdxChirho] ?? seedsChirho[0];

    return {
      text_chirho: String(itemChirho.text_chirho ?? ""),
      label_chirho: String(itemChirho.label_chirho ?? originalSeedChirho.label_chirho),
      heresy_types_chirho: (itemChirho.heresy_types_chirho ?? originalSeedChirho.heresy_types_chirho) as string[],
      confidence_chirho: Number(itemChirho.confidence_chirho ?? originalSeedChirho.confidence_chirho),
      explanation_chirho: originalSeedChirho.explanation_chirho,
      scripture_refs_chirho: originalSeedChirho.scripture_refs_chirho,
      creed_refs_chirho: originalSeedChirho.creed_refs_chirho,
      domain_chirho: String(itemChirho.domain_chirho ?? originalSeedChirho.domain_chirho),
      denominational_note_chirho: originalSeedChirho.denominational_note_chirho,
      source_chirho: "augmented" as const,
      seed_index_chirho: originalSeedChirho.seed_index_chirho,
    };
  });
}

interface JobChirho {
  jobIdChirho: number;
  batchIdxChirho: number;
  roundChirho: number;
  seedsChirho: DatasetExampleChirho[];
}

async function augmentChirho(): Promise<void> {
  console.log("Dataset Augmentation Pipeline (Grok/xAI) - PARALLEL RESUMABLE");
  console.log("================================================================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  const seedsChirho = await loadSeedsChirho();
  console.log(`Loaded ${seedsChirho.length} seed examples`);

  const progressChirho = await loadProgressChirho();
  console.log(`Previously completed ${progressChirho.completedJobsChirho.length} jobs, ${progressChirho.totalAugmentedChirho} augmented`);

  // Build all jobs: each job = one API call for one batch of seeds for one round
  const allJobsChirho: JobChirho[] = [];
  const totalBatchesChirho = Math.ceil(seedsChirho.length / BATCH_SIZE_CHIRHO);
  let jobIdCounterChirho = 0;

  for (let batchIdxChirho = 0; batchIdxChirho < totalBatchesChirho; batchIdxChirho++) {
    const startChirho = batchIdxChirho * BATCH_SIZE_CHIRHO;
    const batchSeedsChirho = seedsChirho.slice(startChirho, startChirho + BATCH_SIZE_CHIRHO);

    for (let roundChirho = 0; roundChirho < TOTAL_ROUNDS_CHIRHO; roundChirho++) {
      allJobsChirho.push({
        jobIdChirho: jobIdCounterChirho++,
        batchIdxChirho,
        roundChirho,
        seedsChirho: batchSeedsChirho,
      });
    }
  }

  // Filter out completed jobs
  const completedSetChirho = new Set(progressChirho.completedJobsChirho);
  const pendingJobsChirho = allJobsChirho.filter(
    (jChirho) => !completedSetChirho.has(jChirho.jobIdChirho)
  );

  const neededChirho = TARGET_COUNT_CHIRHO - seedsChirho.length - progressChirho.totalAugmentedChirho;
  console.log(`Total jobs: ${allJobsChirho.length}, Pending: ${pendingJobsChirho.length}`);
  console.log(`Still need ~${neededChirho} augmented examples`);
  console.log(`Running ${CONCURRENCY_CHIRHO} parallel workers\n`);

  if (neededChirho <= 0) {
    console.log("Target already reached! Run with 'finalize' to split.");
    return;
  }

  let totalAugmentedChirho = progressChirho.totalAugmentedChirho;
  let completedIdsChirho = [...progressChirho.completedJobsChirho];
  let jobIndexChirho = 0;
  let activeChirho = 0;
  let doneChirho = false;

  const processJobChirho = async (jobChirho: JobChirho): Promise<void> => {
    const labelChirho = `B${jobChirho.batchIdxChirho + 1}R${jobChirho.roundChirho + 1}`;
    try {
      const augmentedChirho = await augmentBatchChirho(
        jobChirho.seedsChirho,
        PARAPHRASES_PER_CALL_CHIRHO,
      );

      const linesChirho = augmentedChirho.map((exChirho) => JSON.stringify(exChirho)).join("\n");
      await appendSafeChirho(linesChirho + "\n");

      totalAugmentedChirho += augmentedChirho.length;
      completedIdsChirho.push(jobChirho.jobIdChirho);

      console.log(`  [${labelChirho}] +${augmentedChirho.length} (total: ${seedsChirho.length + totalAugmentedChirho}/${TARGET_COUNT_CHIRHO})`);

      if (seedsChirho.length + totalAugmentedChirho >= TARGET_COUNT_CHIRHO) {
        doneChirho = true;
      }
    } catch (errorChirho) {
      console.error(`  [${labelChirho}] FAILED: ${String(errorChirho).substring(0, 100)}`);
      completedIdsChirho.push(jobChirho.jobIdChirho); // Skip failed jobs
    }
  };

  // Process in waves of CONCURRENCY_CHIRHO
  while (jobIndexChirho < pendingJobsChirho.length && !doneChirho) {
    const waveChirho: Promise<void>[] = [];
    const waveSizeChirho = Math.min(CONCURRENCY_CHIRHO, pendingJobsChirho.length - jobIndexChirho);

    for (let wChirho = 0; wChirho < waveSizeChirho; wChirho++) {
      waveChirho.push(processJobChirho(pendingJobsChirho[jobIndexChirho++]));
    }

    await Promise.all(waveChirho);

    // Save progress after each wave
    await saveProgressChirho({
      completedJobsChirho: completedIdsChirho,
      totalAugmentedChirho,
      timestampChirho: "",
    });

    // Brief pause between waves
    await new Promise((rChirho) => setTimeout(rChirho, 500));
  }

  console.log(`\nSession complete. Total augmented: ${totalAugmentedChirho}`);
  console.log(`Total with seeds: ${seedsChirho.length + totalAugmentedChirho}`);

  if (seedsChirho.length + totalAugmentedChirho >= TARGET_COUNT_CHIRHO) {
    console.log("Target reached! Run with 'finalize' to shuffle and split.");
  } else {
    console.log("Run again to continue augmentation (resumable).");
  }
}

async function finalizeChirho(): Promise<void> {
  console.log("Dataset Finalization - Shuffle & Split");
  console.log("======================================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  const seedsChirho = await loadSeedsChirho();
  console.log(`Loaded ${seedsChirho.length} seed examples`);

  let augmentedChirho: DatasetExampleChirho[] = [];
  if (await fileExistsChirho(PARTIAL_FILE_CHIRHO)) {
    const contentChirho = await readFile(PARTIAL_FILE_CHIRHO, "utf-8");
    augmentedChirho = contentChirho
      .trim()
      .split("\n")
      .filter((lineChirho) => lineChirho.trim())
      .map((lineChirho) => JSON.parse(lineChirho));
    console.log(`Loaded ${augmentedChirho.length} augmented examples`);
  }

  const allExamplesChirho = [...seedsChirho, ...augmentedChirho];
  const finalExamplesChirho = allExamplesChirho.slice(0, TARGET_COUNT_CHIRHO);

  // Shuffle (Fisher-Yates)
  for (let iChirho = finalExamplesChirho.length - 1; iChirho > 0; iChirho--) {
    const jChirho = Math.floor(Math.random() * (iChirho + 1));
    [finalExamplesChirho[iChirho], finalExamplesChirho[jChirho]] = [
      finalExamplesChirho[jChirho],
      finalExamplesChirho[iChirho],
    ];
  }

  // Split: 80% train, 10% val, 10% test
  const trainEndChirho = Math.floor(finalExamplesChirho.length * 0.8);
  const valEndChirho = Math.floor(finalExamplesChirho.length * 0.9);

  const trainChirho = finalExamplesChirho.slice(0, trainEndChirho);
  const valChirho = finalExamplesChirho.slice(trainEndChirho, valEndChirho);
  const testChirho = finalExamplesChirho.slice(valEndChirho);

  const writeJsonlChirho = (dataChirho: DatasetExampleChirho[]) =>
    dataChirho.map((exChirho) => JSON.stringify(exChirho)).join("\n");

  await writeFile(`${PROCESSED_DIR_CHIRHO}train-chirho.jsonl`, writeJsonlChirho(trainChirho), "utf-8");
  await writeFile(`${PROCESSED_DIR_CHIRHO}val-chirho.jsonl`, writeJsonlChirho(valChirho), "utf-8");
  await writeFile(`${PROCESSED_DIR_CHIRHO}test-chirho.jsonl`, writeJsonlChirho(testChirho), "utf-8");
  await writeFile(`${PROCESSED_DIR_CHIRHO}all-chirho.jsonl`, writeJsonlChirho(finalExamplesChirho), "utf-8");

  console.log(`\nDataset finalization complete!`);
  console.log(`   Total examples: ${finalExamplesChirho.length}`);
  console.log(`   Train: ${trainChirho.length}`);
  console.log(`   Validation: ${valChirho.length}`);
  console.log(`   Test: ${testChirho.length}`);
}

// Main dispatch
const modeChirho = process.argv[2];
if (modeChirho === "finalize") {
  finalizeChirho();
} else {
  augmentChirho();
}
