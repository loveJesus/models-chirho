// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * validate-dataset-chirho.ts
 * Validates the variant classification dataset.
 */

import { readFile, stat } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

interface CheckResultChirho {
  nameChirho: string;
  passedChirho: boolean;
  detailsChirho: string;
}

async function mainChirho(): Promise<void> {
  console.log("Variant Dataset Validator");
  console.log("========================\n");

  const checksChirho: CheckResultChirho[] = [];

  // Check files exist
  const filesChirho = [
    "train-variant-chirho.jsonl",
    "val-variant-chirho.jsonl",
    "test-variant-chirho.jsonl",
  ];

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

  // Check content
  for (const fileChirho of filesChirho) {
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${fileChirho}`;
    try {
      const contentChirho = await readFile(pathChirho, "utf-8");
      const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());

      // Count and check for empty fields
      let emptyInputsChirho = 0;
      let emptyTargetsChirho = 0;
      const typesChirho = new Set<string>();

      for (const lineChirho of linesChirho) {
        const objChirho = JSON.parse(lineChirho);
        if (!objChirho.input_chirho?.trim()) emptyInputsChirho++;
        if (!objChirho.target_chirho?.trim()) emptyTargetsChirho++;
        // Extract type from target
        const typeMatchChirho = objChirho.target_chirho?.match(/type:(\w+)/);
        if (typeMatchChirho) typesChirho.add(typeMatchChirho[1]);
      }

      checksChirho.push({
        nameChirho: `${fileChirho}: count`,
        passedChirho: linesChirho.length > 0,
        detailsChirho: `${linesChirho.length} examples`,
      });

      checksChirho.push({
        nameChirho: `${fileChirho}: no empty fields`,
        passedChirho: emptyInputsChirho === 0 && emptyTargetsChirho === 0,
        detailsChirho: `empty inputs=${emptyInputsChirho}, empty targets=${emptyTargetsChirho}`,
      });

      checksChirho.push({
        nameChirho: `${fileChirho}: variant types`,
        passedChirho: typesChirho.size >= 2,
        detailsChirho: `${typesChirho.size} types: ${Array.from(typesChirho).join(", ")}`,
      });
    } catch {
      // File doesn't exist, already caught above
    }
  }

  // Report
  let passedChirho = 0;
  let failedChirho = 0;

  for (const checkChirho of checksChirho) {
    const statusChirho = checkChirho.passedChirho ? "PASS" : "FAIL";
    const markerChirho = checkChirho.passedChirho ? "+" : "x";
    console.log(`  [${markerChirho}] ${statusChirho}: ${checkChirho.nameChirho} — ${checkChirho.detailsChirho}`);
    if (checkChirho.passedChirho) passedChirho++;
    else failedChirho++;
  }

  console.log(`\n========================`);
  console.log(`Results: ${passedChirho} passed, ${failedChirho} failed out of ${checksChirho.length}`);

  if (failedChirho > 0) process.exit(1);
}

mainChirho();
