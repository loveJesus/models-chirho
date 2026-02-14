// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * validate-dataset-chirho.ts
 * Validates the dual-task simplifier dataset:
 *   - File existence and size
 *   - Example counts per split
 *   - Task distribution (difficulty_scoring vs simplification)
 *   - Field completeness (no empty inputs or targets)
 *   - Input prefix correctness ("rate difficulty:" or "simplify:")
 *   - Difficulty label format validation
 *   - Sample output display
 */

import { readFile, stat } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

interface CheckResultChirho {
  nameChirho: string;
  passedChirho: boolean;
  detailsChirho: string;
}

interface DatasetStatsChirho {
  totalChirho: number;
  difficultyCountChirho: number;
  simplificationCountChirho: number;
  emptyInputsChirho: number;
  emptyTargetsChirho: number;
  badPrefixChirho: number;
  difficultyLabelDistChirho: Record<string, number>;
  vocabDistChirho: Record<string, number>;
}

function parseAndValidateChirho(contentChirho: string): DatasetStatsChirho {
  const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());

  const statsChirho: DatasetStatsChirho = {
    totalChirho: linesChirho.length,
    difficultyCountChirho: 0,
    simplificationCountChirho: 0,
    emptyInputsChirho: 0,
    emptyTargetsChirho: 0,
    badPrefixChirho: 0,
    difficultyLabelDistChirho: { easy: 0, medium: 0, hard: 0 },
    vocabDistChirho: { low: 0, medium: 0, high: 0 },
  };

  for (const lineChirho of linesChirho) {
    const objChirho = JSON.parse(lineChirho);
    const inputChirho: string = objChirho.input_chirho || "";
    const targetChirho: string = objChirho.target_chirho || "";
    const taskChirho: string = objChirho.task_chirho || "";

    if (!inputChirho.trim()) statsChirho.emptyInputsChirho++;
    if (!targetChirho.trim()) statsChirho.emptyTargetsChirho++;

    if (taskChirho === "difficulty_scoring") {
      statsChirho.difficultyCountChirho++;

      if (!inputChirho.startsWith("rate difficulty:")) {
        statsChirho.badPrefixChirho++;
      }

      // Parse difficulty label
      const diffMatchChirho = targetChirho.match(/difficulty: (\w+)/);
      if (diffMatchChirho) {
        const labelChirho = diffMatchChirho[1];
        statsChirho.difficultyLabelDistChirho[labelChirho] =
          (statsChirho.difficultyLabelDistChirho[labelChirho] || 0) + 1;
      }

      // Parse vocab complexity
      const vocabMatchChirho = targetChirho.match(/vocab_complexity: (\w+)/);
      if (vocabMatchChirho) {
        const levelChirho = vocabMatchChirho[1];
        statsChirho.vocabDistChirho[levelChirho] =
          (statsChirho.vocabDistChirho[levelChirho] || 0) + 1;
      }
    } else if (taskChirho === "simplification") {
      statsChirho.simplificationCountChirho++;

      if (!inputChirho.startsWith("simplify:")) {
        statsChirho.badPrefixChirho++;
      }
    }
  }

  return statsChirho;
}

async function mainChirho(): Promise<void> {
  console.log("Dual-Task Simplifier Dataset Validator");
  console.log("=======================================\n");

  const checksChirho: CheckResultChirho[] = [];

  const filesChirho = [
    "train-simplifier-chirho.jsonl",
    "val-simplifier-chirho.jsonl",
    "test-simplifier-chirho.jsonl",
  ];

  // Check file existence and sizes
  for (const fileChirho of filesChirho) {
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${fileChirho}`;
    try {
      const statChirho = await stat(pathChirho);
      checksChirho.push({
        nameChirho: `File exists: ${fileChirho}`,
        passedChirho: statChirho.size > 100,
        detailsChirho: `${(statChirho.size / 1024 / 1024).toFixed(1)} MB`,
      });
    } catch {
      checksChirho.push({
        nameChirho: `File exists: ${fileChirho}`,
        passedChirho: false,
        detailsChirho: "Not found",
      });
    }
  }

  // Detailed validation per split
  let totalOverallChirho = 0;
  let totalDifficultyChirho = 0;
  let totalSimplificationChirho = 0;

  for (const fileChirho of filesChirho) {
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${fileChirho}`;
    try {
      const contentChirho = await readFile(pathChirho, "utf-8");
      const statsChirho = parseAndValidateChirho(contentChirho);

      totalOverallChirho += statsChirho.totalChirho;
      totalDifficultyChirho += statsChirho.difficultyCountChirho;
      totalSimplificationChirho += statsChirho.simplificationCountChirho;

      // Count check
      checksChirho.push({
        nameChirho: `${fileChirho}: example count`,
        passedChirho: statsChirho.totalChirho > 0,
        detailsChirho: `${statsChirho.totalChirho} examples`,
      });

      // Task distribution
      checksChirho.push({
        nameChirho: `${fileChirho}: has both tasks`,
        passedChirho:
          statsChirho.difficultyCountChirho > 0 && statsChirho.simplificationCountChirho > 0,
        detailsChirho: `difficulty=${statsChirho.difficultyCountChirho}, simplification=${statsChirho.simplificationCountChirho}`,
      });

      // No empty fields
      checksChirho.push({
        nameChirho: `${fileChirho}: no empty inputs`,
        passedChirho: statsChirho.emptyInputsChirho === 0,
        detailsChirho: `${statsChirho.emptyInputsChirho} empty`,
      });

      checksChirho.push({
        nameChirho: `${fileChirho}: no empty targets`,
        passedChirho: statsChirho.emptyTargetsChirho === 0,
        detailsChirho: `${statsChirho.emptyTargetsChirho} empty`,
      });

      // Correct prefixes
      checksChirho.push({
        nameChirho: `${fileChirho}: correct input prefixes`,
        passedChirho: statsChirho.badPrefixChirho === 0,
        detailsChirho: `${statsChirho.badPrefixChirho} bad prefixes`,
      });

      // Difficulty label distribution
      if (statsChirho.difficultyCountChirho > 0) {
        const distStrChirho = Object.entries(statsChirho.difficultyLabelDistChirho)
          .map(([kChirho, vChirho]) => `${kChirho}=${vChirho}`)
          .join(", ");
        checksChirho.push({
          nameChirho: `${fileChirho}: difficulty labels`,
          passedChirho:
            (statsChirho.difficultyLabelDistChirho["easy"] || 0) > 0 &&
            (statsChirho.difficultyLabelDistChirho["medium"] || 0) > 0 &&
            (statsChirho.difficultyLabelDistChirho["hard"] || 0) > 0,
          detailsChirho: distStrChirho,
        });
      }
    } catch (errorChirho) {
      checksChirho.push({
        nameChirho: `${fileChirho}: parse error`,
        passedChirho: false,
        detailsChirho: `${errorChirho}`,
      });
    }
  }

  // Overall checks
  checksChirho.push({
    nameChirho: "Overall: total examples >= 50K",
    passedChirho: totalOverallChirho >= 50000,
    detailsChirho: `${totalOverallChirho} total`,
  });

  checksChirho.push({
    nameChirho: "Overall: task ratio reasonable",
    passedChirho:
      totalDifficultyChirho > 0 &&
      totalSimplificationChirho > 0 &&
      totalSimplificationChirho / totalDifficultyChirho > 0.5 &&
      totalSimplificationChirho / totalDifficultyChirho < 5.0,
    detailsChirho: `difficulty=${totalDifficultyChirho}, simplification=${totalSimplificationChirho}, ratio=${(totalSimplificationChirho / Math.max(1, totalDifficultyChirho)).toFixed(2)}`,
  });

  // Show sample examples
  console.log("--- Sample Examples ---\n");

  try {
    const trainContentChirho = await readFile(
      `${PROCESSED_DIR_CHIRHO}train-simplifier-chirho.jsonl`,
      "utf-8"
    );
    const trainLinesChirho = trainContentChirho.split("\n").filter((lChirho) => lChirho.trim());

    // Show one difficulty example
    for (const lineChirho of trainLinesChirho) {
      const objChirho = JSON.parse(lineChirho);
      if (objChirho.task_chirho === "difficulty_scoring") {
        console.log("  [Difficulty Scoring Example]");
        console.log(`    Input:  ${objChirho.input_chirho.substring(0, 120)}...`);
        console.log(`    Target: ${objChirho.target_chirho}`);
        console.log();
        break;
      }
    }

    // Show one simplification example
    for (const lineChirho of trainLinesChirho) {
      const objChirho = JSON.parse(lineChirho);
      if (objChirho.task_chirho === "simplification") {
        console.log("  [Simplification Example]");
        console.log(`    Input:  ${objChirho.input_chirho.substring(0, 120)}...`);
        console.log(`    Target: ${objChirho.target_chirho.substring(0, 120)}...`);
        console.log();
        break;
      }
    }
  } catch {
    console.log("  (Could not load samples)");
  }

  // Print results
  console.log("--- Validation Results ---\n");
  let passedChirho = 0;
  let failedChirho = 0;

  for (const checkChirho of checksChirho) {
    const markerChirho = checkChirho.passedChirho ? "+" : "x";
    console.log(
      `  [${markerChirho}] ${checkChirho.passedChirho ? "PASS" : "FAIL"}: ${checkChirho.nameChirho} -- ${checkChirho.detailsChirho}`
    );
    if (checkChirho.passedChirho) passedChirho++;
    else failedChirho++;
  }

  console.log(`\n=======================================`);
  console.log(`Results: ${passedChirho} passed, ${failedChirho} failed out of ${checksChirho.length}`);

  if (failedChirho > 0) process.exit(1);
}

mainChirho();
