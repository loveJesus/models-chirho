// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * validate-dataset-chirho.ts
 * Validates the built parser and glosser datasets:
 *   - Verify counts (parser ~200K, glosser ~31K)
 *   - Check no empty input/target fields
 *   - Verify both languages present
 *   - Sample inspection
 *   - Check for data leakage between splits
 */

import { readFile, stat } from "fs/promises";

const BASE_DIR_CHIRHO = `${import.meta.dir}/../..`;
const PROCESSED_DIR_CHIRHO = `${BASE_DIR_CHIRHO}/data-chirho/processed-chirho`;

interface ValidationResultChirho {
  nameChirho: string;
  passedChirho: boolean;
  messageChirho: string;
}

interface DatasetStatsChirho {
  countChirho: number;
  emptyInputsChirho: number;
  emptyTargetsChirho: number;
  langCountsChirho: Record<string, number>;
  avgInputLenChirho: number;
  avgTargetLenChirho: number;
  refsChirho: Set<string>;
}

async function loadJsonlChirho(
  pathChirho: string
): Promise<Array<Record<string, string | number>>> {
  try {
    const contentChirho = await readFile(pathChirho, "utf-8");
    return contentChirho
      .split("\n")
      .filter((lChirho) => lChirho.trim())
      .map((lChirho) => JSON.parse(lChirho));
  } catch {
    return [];
  }
}

function computeStatsChirho(
  recordsChirho: Array<Record<string, string | number>>
): DatasetStatsChirho {
  let emptyInputsChirho = 0;
  let emptyTargetsChirho = 0;
  let totalInputLenChirho = 0;
  let totalTargetLenChirho = 0;
  const langCountsChirho: Record<string, number> = {};
  const refsChirho = new Set<string>();

  for (const recChirho of recordsChirho) {
    const inputChirho = String(recChirho.input_chirho ?? "");
    const targetChirho = String(recChirho.target_chirho ?? "");
    const langChirho = String(recChirho.lang_chirho ?? "unknown");
    const refChirho = String(recChirho.ref_chirho ?? "");

    if (!inputChirho.trim()) emptyInputsChirho++;
    if (!targetChirho.trim()) emptyTargetsChirho++;

    totalInputLenChirho += inputChirho.length;
    totalTargetLenChirho += targetChirho.length;

    langCountsChirho[langChirho] = (langCountsChirho[langChirho] ?? 0) + 1;
    if (refChirho) refsChirho.add(refChirho);
  }

  return {
    countChirho: recordsChirho.length,
    emptyInputsChirho,
    emptyTargetsChirho,
    langCountsChirho,
    avgInputLenChirho: recordsChirho.length > 0 ? totalInputLenChirho / recordsChirho.length : 0,
    avgTargetLenChirho:
      recordsChirho.length > 0 ? totalTargetLenChirho / recordsChirho.length : 0,
    refsChirho,
  };
}

async function validateDatasetChirho(
  prefixChirho: string,
  labelChirho: string,
  expectedMinChirho: number
): Promise<ValidationResultChirho[]> {
  const resultsChirho: ValidationResultChirho[] = [];

  const trainPathChirho = `${PROCESSED_DIR_CHIRHO}/train-${prefixChirho}-chirho.jsonl`;
  const valPathChirho = `${PROCESSED_DIR_CHIRHO}/val-${prefixChirho}-chirho.jsonl`;
  const testPathChirho = `${PROCESSED_DIR_CHIRHO}/test-${prefixChirho}-chirho.jsonl`;

  // Load all splits
  const trainChirho = await loadJsonlChirho(trainPathChirho);
  const valChirho = await loadJsonlChirho(valPathChirho);
  const testChirho = await loadJsonlChirho(testPathChirho);

  const totalChirho = trainChirho.length + valChirho.length + testChirho.length;

  // Check 1: Files exist and are non-empty
  resultsChirho.push({
    nameChirho: `${labelChirho}: files exist`,
    passedChirho: totalChirho > 0,
    messageChirho:
      totalChirho > 0
        ? `train=${trainChirho.length}, val=${valChirho.length}, test=${testChirho.length}, total=${totalChirho}`
        : "No data files found!",
  });

  if (totalChirho === 0) return resultsChirho;

  // Check 2: Minimum count
  resultsChirho.push({
    nameChirho: `${labelChirho}: minimum count (${expectedMinChirho})`,
    passedChirho: totalChirho >= expectedMinChirho,
    messageChirho: `${totalChirho} examples (need ${expectedMinChirho})`,
  });

  // Check 3: Split ratios (~80/10/10)
  const trainRatioChirho = trainChirho.length / totalChirho;
  const valRatioChirho = valChirho.length / totalChirho;
  const testRatioChirho = testChirho.length / totalChirho;
  const ratioOkChirho =
    trainRatioChirho > 0.7 &&
    trainRatioChirho < 0.9 &&
    valRatioChirho > 0.05 &&
    testRatioChirho > 0.05;
  resultsChirho.push({
    nameChirho: `${labelChirho}: split ratios`,
    passedChirho: ratioOkChirho,
    messageChirho: `train=${(trainRatioChirho * 100).toFixed(1)}%, val=${(valRatioChirho * 100).toFixed(1)}%, test=${(testRatioChirho * 100).toFixed(1)}%`,
  });

  // Check 4: No empty fields
  const trainStatsChirho = computeStatsChirho(trainChirho);
  const allStatsChirho = computeStatsChirho([...trainChirho, ...valChirho, ...testChirho]);
  resultsChirho.push({
    nameChirho: `${labelChirho}: no empty inputs`,
    passedChirho: allStatsChirho.emptyInputsChirho === 0,
    messageChirho:
      allStatsChirho.emptyInputsChirho === 0
        ? "All inputs non-empty"
        : `${allStatsChirho.emptyInputsChirho} empty inputs found!`,
  });
  resultsChirho.push({
    nameChirho: `${labelChirho}: no empty targets`,
    passedChirho: allStatsChirho.emptyTargetsChirho === 0,
    messageChirho:
      allStatsChirho.emptyTargetsChirho === 0
        ? "All targets non-empty"
        : `${allStatsChirho.emptyTargetsChirho} empty targets found!`,
  });

  // Check 5: Both languages present
  const langsChirho = Object.keys(allStatsChirho.langCountsChirho);
  const bothLangsChirho = langsChirho.includes("hebrew") && langsChirho.includes("greek");
  const langDistChirho = Object.entries(allStatsChirho.langCountsChirho)
    .map(([lChirho, cChirho]) => `${lChirho}=${cChirho}`)
    .join(", ");
  resultsChirho.push({
    nameChirho: `${labelChirho}: both languages`,
    passedChirho: bothLangsChirho,
    messageChirho: bothLangsChirho ? `Languages: ${langDistChirho}` : `Only found: ${langDistChirho}`,
  });

  // Check 6: No data leakage (refs don't overlap between splits)
  const trainRefsChirho = computeStatsChirho(trainChirho).refsChirho;
  const valRefsChirho = computeStatsChirho(valChirho).refsChirho;
  const testRefsChirho = computeStatsChirho(testChirho).refsChirho;

  // For parser, refs can overlap (same verse, different words). For glosser, they shouldn't.
  if (prefixChirho === "glosser") {
    let leakCountChirho = 0;
    for (const refChirho of valRefsChirho) {
      if (trainRefsChirho.has(refChirho)) leakCountChirho++;
    }
    for (const refChirho of testRefsChirho) {
      if (trainRefsChirho.has(refChirho)) leakCountChirho++;
    }
    resultsChirho.push({
      nameChirho: `${labelChirho}: no verse leakage`,
      passedChirho: leakCountChirho === 0,
      messageChirho:
        leakCountChirho === 0
          ? "No verse overlap between splits"
          : `${leakCountChirho} verses leak between splits`,
    });
  }

  // Check 7: Average lengths reasonable
  resultsChirho.push({
    nameChirho: `${labelChirho}: input/target lengths`,
    passedChirho:
      allStatsChirho.avgInputLenChirho > 10 && allStatsChirho.avgTargetLenChirho > 5,
    messageChirho: `avg input=${allStatsChirho.avgInputLenChirho.toFixed(0)} chars, avg target=${allStatsChirho.avgTargetLenChirho.toFixed(0)} chars`,
  });

  return resultsChirho;
}

async function mainChirho(): Promise<void> {
  console.log("Dataset Validation");
  console.log("==================\n");

  const allResultsChirho: ValidationResultChirho[] = [];

  // Validate parser dataset
  console.log("Validating PARSER dataset...");
  const parserResultsChirho = await validateDatasetChirho("parser", "Parser", 50_000);
  allResultsChirho.push(...parserResultsChirho);

  // Validate glosser dataset
  console.log("Validating GLOSSER dataset...");
  const glosserResultsChirho = await validateDatasetChirho("glosser", "Glosser", 10_000);
  allResultsChirho.push(...glosserResultsChirho);

  // Print results
  console.log("\n==================");
  console.log("Validation Results:");
  console.log("==================\n");

  let passedCountChirho = 0;
  let failedCountChirho = 0;

  for (const resultChirho of allResultsChirho) {
    const statusChirho = resultChirho.passedChirho ? "PASS" : "FAIL";
    const symbolChirho = resultChirho.passedChirho ? "[+]" : "[X]";

    if (resultChirho.passedChirho) {
      passedCountChirho++;
    } else {
      failedCountChirho++;
    }

    console.log(`  ${symbolChirho} ${resultChirho.nameChirho}: ${resultChirho.messageChirho}`);
  }

  console.log(
    `\nTotal: ${passedCountChirho} passed, ${failedCountChirho} failed out of ${allResultsChirho.length} checks`
  );

  // Show sample entries from each dataset
  console.log("\n--- Parser Samples ---");
  const parserTrainChirho = await loadJsonlChirho(
    `${PROCESSED_DIR_CHIRHO}/train-parser-chirho.jsonl`
  );
  for (const sampleChirho of parserTrainChirho.slice(0, 2)) {
    console.log(`  Input:  ${String(sampleChirho.input_chirho).substring(0, 100)}`);
    console.log(`  Target: ${String(sampleChirho.target_chirho).substring(0, 100)}`);
    console.log();
  }

  console.log("--- Glosser Samples ---");
  const glosserTrainChirho = await loadJsonlChirho(
    `${PROCESSED_DIR_CHIRHO}/train-glosser-chirho.jsonl`
  );
  for (const sampleChirho of glosserTrainChirho.slice(0, 2)) {
    console.log(`  Input:  ${String(sampleChirho.input_chirho).substring(0, 100)}`);
    console.log(`  Target: ${String(sampleChirho.target_chirho).substring(0, 100)}`);
    console.log();
  }

  if (failedCountChirho > 0) {
    console.log("WARNING: Some validation checks failed!");
    process.exit(1);
  }

  console.log("All validations passed!");
}

mainChirho();
