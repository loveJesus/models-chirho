// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * validate-dataset-chirho.ts
 * Validates the cross-translation embedding dataset.
 */

import { readFile, stat } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

interface CheckResultChirho {
  nameChirho: string;
  passedChirho: boolean;
  detailsChirho: string;
}

async function mainChirho(): Promise<void> {
  console.log("Embedding Dataset Validator");
  console.log("===========================\n");

  const checksChirho: CheckResultChirho[] = [];

  const filesChirho = [
    "train-embedding-chirho.jsonl",
    "val-embedding-chirho.jsonl",
    "test-embedding-chirho.jsonl",
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

  for (const fileChirho of filesChirho) {
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${fileChirho}`;
    try {
      const contentChirho = await readFile(pathChirho, "utf-8");
      const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());

      let positiveCountChirho = 0;
      let negativeCountChirho = 0;
      let emptyFieldsChirho = 0;

      for (const lineChirho of linesChirho) {
        const objChirho = JSON.parse(lineChirho);
        if (!objChirho.sentence1_chirho?.trim() || !objChirho.sentence2_chirho?.trim()) emptyFieldsChirho++;
        if (objChirho.label_chirho === 1.0) positiveCountChirho++;
        else negativeCountChirho++;
      }

      checksChirho.push({
        nameChirho: `${fileChirho}: count`,
        passedChirho: linesChirho.length > 0,
        detailsChirho: `${linesChirho.length} pairs`,
      });

      checksChirho.push({
        nameChirho: `${fileChirho}: no empty fields`,
        passedChirho: emptyFieldsChirho === 0,
        detailsChirho: `${emptyFieldsChirho} empty`,
      });

      checksChirho.push({
        nameChirho: `${fileChirho}: label balance`,
        passedChirho: positiveCountChirho > 0 && negativeCountChirho > 0,
        detailsChirho: `pos=${positiveCountChirho}, neg=${negativeCountChirho}`,
      });
    } catch {
      // Already caught
    }
  }

  let passedChirho = 0;
  let failedChirho = 0;

  for (const checkChirho of checksChirho) {
    const markerChirho = checkChirho.passedChirho ? "+" : "x";
    console.log(`  [${markerChirho}] ${checkChirho.passedChirho ? "PASS" : "FAIL"}: ${checkChirho.nameChirho} — ${checkChirho.detailsChirho}`);
    if (checkChirho.passedChirho) passedChirho++;
    else failedChirho++;
  }

  console.log(`\n===========================`);
  console.log(`Results: ${passedChirho} passed, ${failedChirho} failed out of ${checksChirho.length}`);

  if (failedChirho > 0) process.exit(1);
}

mainChirho();
