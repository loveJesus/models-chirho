// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * seed-classifier-chirho.ts
 * LLM-labels the top 2,000 highest-voted cross-reference pairs by connection type
 * using the Grok/xAI API. Resumable with concurrent API calls.
 *
 * Connection types:
 *   direct_quote, allusion, thematic_parallel, typological,
 *   prophecy_fulfillment, parallel_narrative, contrast
 */

import { writeFile, readFile, mkdir, appendFile, access } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${process.cwd()}/data-chirho/processed-chirho/`;
const SEEDS_DIR_CHIRHO = `${process.cwd()}/data-chirho/seeds-chirho/`;

const GROK_API_KEY_CHIRHO = process.env.GROK_API_KEY_CHIRHO || process.env.GROK_API_KEY;
if (!GROK_API_KEY_CHIRHO) {
  throw new Error("GROK_API_KEY_CHIRHO not set. Export it first.");
}

const GROK_API_URL_CHIRHO = "https://api.x.ai/v1/chat/completions";

const TARGET_SEED_COUNT_CHIRHO = 2000;
const BATCH_SIZE_CHIRHO = 10; // pairs per API call
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

interface LabeledPairChirho {
  from_id_chirho: string;
  to_id_chirho: string;
  from_text_chirho: string;
  to_text_chirho: string;
  connection_type_chirho: ConnectionTypeChirho;
  confidence_chirho: number;
  reasoning_chirho: string;
  votes_chirho: number;
}

interface GrokResponseChirho {
  choices: Array<{ message: { content: string } }>;
}

interface ProgressChirho {
  completedBatchesChirho: number[];
  totalLabeledChirho: number;
  timestampChirho: string;
}

const SEEDS_OUTPUT_CHIRHO = `${SEEDS_DIR_CHIRHO}seeds-chirho.jsonl`;
const PROGRESS_PATH_CHIRHO = `${SEEDS_DIR_CHIRHO}seed-progress-chirho.json`;

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    await access(pathChirho);
    return true;
  } catch {
    return false;
  }
}

async function loadProgressChirho(): Promise<ProgressChirho> {
  if (await fileExistsChirho(PROGRESS_PATH_CHIRHO)) {
    return JSON.parse(await readFile(PROGRESS_PATH_CHIRHO, "utf-8"));
  }
  return { completedBatchesChirho: [], totalLabeledChirho: 0, timestampChirho: "" };
}

async function saveProgressChirho(progressChirho: ProgressChirho): Promise<void> {
  progressChirho.timestampChirho = new Date().toISOString();
  await writeFile(PROGRESS_PATH_CHIRHO, JSON.stringify(progressChirho, null, 2), "utf-8");
}

// File write mutex
let writeLockChirho = Promise.resolve();
async function appendSafeChirho(dataChirho: string): Promise<void> {
  writeLockChirho = writeLockChirho.then(() => appendFile(SEEDS_OUTPUT_CHIRHO, dataChirho, "utf-8"));
  await writeLockChirho;
}

async function labelBatchChirho(pairsChirho: ResolvedRefChirho[]): Promise<LabeledPairChirho[]> {
  const pairsDescChirho = pairsChirho.map((pChirho, iChirho) => ({
    indexChirho: iChirho,
    fromChirho: pChirho.fromIdChirho,
    toChirho: pChirho.toIdChirho,
    fromTextChirho: pChirho.fromTextChirho.substring(0, 300),
    toTextChirho: pChirho.toTextChirho.substring(0, 300),
  }));

  const promptChirho = `Classify each of the following ${pairsChirho.length} biblical cross-reference pairs by their connection type.

Connection types:
- "direct_quote": NT directly quotes OT text (e.g., "it is written", verbatim or near-verbatim)
- "allusion": Clear reference without direct quotation (imagery, phrasing echoes)
- "thematic_parallel": Shared theme or motif (shepherd imagery, covenant themes)
- "typological": OT type foreshadows NT antitype (sacrifice, exodus patterns)
- "prophecy_fulfillment": OT prophecy fulfilled in NT
- "parallel_narrative": Same event in parallel accounts (Synoptic gospels, Kings/Chronicles)
- "contrast": Deliberate theological contrast (law vs grace, Adam vs Christ)

Pairs:
${JSON.stringify(pairsDescChirho, null, 2)}

For EACH pair, return a JSON object with:
- "index_chirho": the pair index
- "connection_type_chirho": one of the 7 types above
- "confidence_chirho": 0.6-1.0
- "reasoning_chirho": brief explanation (1-2 sentences)

Return ONLY a JSON array. No other text.`;

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
          content: "You are a biblical scholar classifying the type of intertextual connection between Bible verse pairs. Be precise about distinguishing direct quotes from allusions, and typology from prophecy. Return only valid JSON.",
        },
        { role: "user", content: promptChirho },
      ],
      max_tokens: 6000,
      temperature: 0.3,
    }),
  });

  if (!responseChirho.ok) {
    const errorTextChirho = await responseChirho.text();
    throw new Error(`Grok API error ${responseChirho.status}: ${errorTextChirho}`);
  }

  const dataChirho = (await responseChirho.json()) as GrokResponseChirho;
  let contentChirho = dataChirho.choices[0]?.message?.content ?? "";

  // Clean markdown
  contentChirho = contentChirho.trim();
  if (contentChirho.startsWith("```")) {
    contentChirho = contentChirho.replace(/^```(?:json)?\n?/, "").replace(/\n?```$/, "");
  }

  const parsedChirho = JSON.parse(contentChirho) as Array<Record<string, unknown>>;

  return parsedChirho.map((itemChirho) => {
    const idxChirho = Number(itemChirho.index_chirho ?? 0);
    const pairChirho = pairsChirho[idxChirho] ?? pairsChirho[0];

    const rawTypeChirho = String(itemChirho.connection_type_chirho ?? "thematic_parallel");
    const connectionTypeChirho = CONNECTION_TYPES_CHIRHO.includes(rawTypeChirho as ConnectionTypeChirho)
      ? (rawTypeChirho as ConnectionTypeChirho)
      : "thematic_parallel";

    return {
      from_id_chirho: pairChirho.fromIdChirho,
      to_id_chirho: pairChirho.toIdChirho,
      from_text_chirho: pairChirho.fromTextChirho,
      to_text_chirho: pairChirho.toTextChirho,
      connection_type_chirho: connectionTypeChirho,
      confidence_chirho: Math.min(1.0, Math.max(0.6, Number(itemChirho.confidence_chirho ?? 0.8))),
      reasoning_chirho: String(itemChirho.reasoning_chirho ?? ""),
      votes_chirho: pairChirho.votesChirho,
    };
  });
}

async function mainChirho(): Promise<void> {
  console.log("Seed Classifier Labeling (Grok/xAI)");
  console.log("====================================\n");

  await mkdir(SEEDS_DIR_CHIRHO, { recursive: true });

  // Load resolved cross-references (sorted by votes, highest first)
  console.log("Loading resolved cross-references...");
  const refsContentChirho = await readFile(`${PROCESSED_DIR_CHIRHO}crossrefs-resolved-chirho.json`, "utf-8");
  const allRefsChirho: ResolvedRefChirho[] = JSON.parse(refsContentChirho);

  // Take top N by votes
  const topRefsChirho = allRefsChirho.slice(0, TARGET_SEED_COUNT_CHIRHO);
  console.log(`  Using top ${topRefsChirho.length} pairs (votes range: ${topRefsChirho[0]?.votesChirho} - ${topRefsChirho[topRefsChirho.length - 1]?.votesChirho})`);

  // Load progress
  const progressChirho = await loadProgressChirho();
  console.log(`  Previously completed: ${progressChirho.completedBatchesChirho.length} batches, ${progressChirho.totalLabeledChirho} labeled`);

  // Build batches
  const batchCountChirho = Math.ceil(topRefsChirho.length / BATCH_SIZE_CHIRHO);
  const completedSetChirho = new Set(progressChirho.completedBatchesChirho);

  const pendingBatchesChirho: Array<{ batchIdChirho: number; pairsChirho: ResolvedRefChirho[] }> = [];
  for (let bChirho = 0; bChirho < batchCountChirho; bChirho++) {
    if (!completedSetChirho.has(bChirho)) {
      pendingBatchesChirho.push({
        batchIdChirho: bChirho,
        pairsChirho: topRefsChirho.slice(bChirho * BATCH_SIZE_CHIRHO, (bChirho + 1) * BATCH_SIZE_CHIRHO),
      });
    }
  }

  console.log(`  Total batches: ${batchCountChirho}, Pending: ${pendingBatchesChirho.length}`);
  console.log(`  Running ${CONCURRENCY_CHIRHO} concurrent workers\n`);

  if (pendingBatchesChirho.length === 0) {
    console.log("All batches completed! Seeds ready.");
    return;
  }

  let totalLabeledChirho = progressChirho.totalLabeledChirho;
  let completedIdsChirho = [...progressChirho.completedBatchesChirho];
  let batchIndexChirho = 0;

  while (batchIndexChirho < pendingBatchesChirho.length) {
    const waveChirho: Promise<void>[] = [];
    const waveSizeChirho = Math.min(CONCURRENCY_CHIRHO, pendingBatchesChirho.length - batchIndexChirho);

    for (let wChirho = 0; wChirho < waveSizeChirho; wChirho++) {
      const batchChirho = pendingBatchesChirho[batchIndexChirho++];
      waveChirho.push(
        (async () => {
          try {
            const labeledChirho = await labelBatchChirho(batchChirho.pairsChirho);
            const linesChirho = labeledChirho.map((lChirho) => JSON.stringify(lChirho)).join("\n");
            await appendSafeChirho(linesChirho + "\n");

            totalLabeledChirho += labeledChirho.length;
            completedIdsChirho.push(batchChirho.batchIdChirho);

            console.log(`  Batch ${batchChirho.batchIdChirho + 1}/${batchCountChirho}: +${labeledChirho.length} (total: ${totalLabeledChirho})`);
          } catch (errorChirho) {
            console.error(`  Batch ${batchChirho.batchIdChirho + 1} FAILED: ${String(errorChirho).substring(0, 100)}`);
            completedIdsChirho.push(batchChirho.batchIdChirho); // Skip on fail
          }
        })()
      );
    }

    await Promise.all(waveChirho);

    // Save progress after each wave
    await saveProgressChirho({
      completedBatchesChirho: completedIdsChirho,
      totalLabeledChirho,
      timestampChirho: "",
    });

    await new Promise((rChirho) => setTimeout(rChirho, 500));
  }

  // Print distribution
  console.log(`\nLabeling complete! Total: ${totalLabeledChirho} labeled pairs`);

  if (await fileExistsChirho(SEEDS_OUTPUT_CHIRHO)) {
    const contentChirho = await readFile(SEEDS_OUTPUT_CHIRHO, "utf-8");
    const linesChirho = contentChirho.trim().split("\n").filter((lChirho) => lChirho.trim());
    const distributionChirho: Record<string, number> = {};

    for (const lineChirho of linesChirho) {
      try {
        const itemChirho = JSON.parse(lineChirho);
        const typeChirho = itemChirho.connection_type_chirho || "unknown";
        distributionChirho[typeChirho] = (distributionChirho[typeChirho] || 0) + 1;
      } catch {
        // Skip malformed lines
      }
    }

    console.log("\nConnection type distribution:");
    for (const [typeChirho, countChirho] of Object.entries(distributionChirho).sort((aChirho, bChirho) => bChirho[1] - aChirho[1])) {
      console.log(`  ${typeChirho}: ${countChirho} (${(countChirho / linesChirho.length * 100).toFixed(1)}%)`);
    }
  }
}

mainChirho();
