// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * validate-dataset-chirho.ts
 * Quality checks on both embedder and classifier datasets.
 */

import { readFile, access } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${process.cwd()}/data-chirho/processed-chirho/`;

const CONNECTION_TYPES_CHIRHO = [
  "direct_quote", "allusion", "thematic_parallel", "typological",
  "prophecy_fulfillment", "parallel_narrative", "contrast",
];

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    await access(pathChirho);
    return true;
  } catch {
    return false;
  }
}

async function loadJsonlChirho(pathChirho: string): Promise<Record<string, unknown>[]> {
  if (!(await fileExistsChirho(pathChirho))) return [];
  const contentChirho = await readFile(pathChirho, "utf-8");
  return contentChirho.trim().split("\n").filter((lChirho) => lChirho.trim()).map((lChirho) => JSON.parse(lChirho));
}

async function validateEmbedderChirho(): Promise<boolean> {
  console.log("\n--- Embedder Dataset Validation ---");
  let passedChirho = true;

  for (const splitChirho of ["train", "val", "test"]) {
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${splitChirho}-embedder-chirho.jsonl`;
    const dataChirho = await loadJsonlChirho(pathChirho);

    if (dataChirho.length === 0) {
      console.log(`  WARN: ${splitChirho} empty or missing`);
      passedChirho = false;
      continue;
    }

    console.log(`\n  ${splitChirho}: ${dataChirho.length} triplets`);

    // Check required fields
    let emptyFieldsChirho = 0;
    let missingFieldsChirho = 0;

    for (const itemChirho of dataChirho) {
      const requiredChirho = ["anchor_id_chirho", "anchor_text_chirho", "positive_id_chirho", "positive_text_chirho", "negative_id_chirho", "negative_text_chirho"];
      for (const fieldChirho of requiredChirho) {
        if (!(fieldChirho in itemChirho)) {
          missingFieldsChirho++;
        } else if (!String(itemChirho[fieldChirho]).trim()) {
          emptyFieldsChirho++;
        }
      }
    }

    if (missingFieldsChirho > 0) {
      console.log(`    FAIL: ${missingFieldsChirho} missing fields`);
      passedChirho = false;
    }
    if (emptyFieldsChirho > 0) {
      console.log(`    WARN: ${emptyFieldsChirho} empty fields`);
    }

    // Check no anchor == positive or anchor == negative
    let selfRefsChirho = 0;
    for (const itemChirho of dataChirho) {
      if (itemChirho.anchor_id_chirho === itemChirho.positive_id_chirho) selfRefsChirho++;
      if (itemChirho.anchor_id_chirho === itemChirho.negative_id_chirho) selfRefsChirho++;
    }
    if (selfRefsChirho > 0) {
      console.log(`    WARN: ${selfRefsChirho} self-references in triplets`);
    }

    console.log(`    OK: ${dataChirho.length} triplets validated`);
  }

  return passedChirho;
}

async function validateClassifierChirho(): Promise<boolean> {
  console.log("\n--- Classifier Dataset Validation ---");
  let passedChirho = true;

  for (const splitChirho of ["train", "val", "test"]) {
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${splitChirho}-classifier-chirho.jsonl`;
    const dataChirho = await loadJsonlChirho(pathChirho);

    if (dataChirho.length === 0) {
      console.log(`  WARN: ${splitChirho} empty or missing`);
      passedChirho = false;
      continue;
    }

    console.log(`\n  ${splitChirho}: ${dataChirho.length} pairs`);

    // Check required fields
    let emptyTextsChirho = 0;
    let invalidTypesChirho = 0;

    const distributionChirho: Record<string, number> = {};

    for (const itemChirho of dataChirho) {
      const fromTextChirho = String(itemChirho.from_text_chirho || "").trim();
      const toTextChirho = String(itemChirho.to_text_chirho || "").trim();
      const typeChirho = String(itemChirho.connection_type_chirho || "");

      if (!fromTextChirho || !toTextChirho) emptyTextsChirho++;
      if (!CONNECTION_TYPES_CHIRHO.includes(typeChirho)) {
        invalidTypesChirho++;
      } else {
        distributionChirho[typeChirho] = (distributionChirho[typeChirho] || 0) + 1;
      }
    }

    if (emptyTextsChirho > 0) {
      console.log(`    WARN: ${emptyTextsChirho} empty texts`);
    }
    if (invalidTypesChirho > 0) {
      console.log(`    FAIL: ${invalidTypesChirho} invalid connection types`);
      passedChirho = false;
    }

    // Distribution
    console.log(`    Distribution:`);
    for (const [typeChirho, countChirho] of Object.entries(distributionChirho).sort((aChirho, bChirho) => bChirho[1] - aChirho[1])) {
      const pctChirho = (countChirho / dataChirho.length * 100).toFixed(1);
      console.log(`      ${typeChirho}: ${countChirho} (${pctChirho}%)`);
    }

    // Check for severe imbalance
    const countsChirho = Object.values(distributionChirho);
    if (countsChirho.length > 0) {
      const maxChirho = Math.max(...countsChirho);
      const minChirho = Math.min(...countsChirho);
      if (maxChirho > minChirho * 10) {
        console.log(`    WARN: Severe class imbalance (${maxChirho}x vs ${minChirho}x)`);
      }
    }

    // Check for exact duplicates
    const seenChirho = new Set<string>();
    let duplicatesChirho = 0;
    for (const itemChirho of dataChirho) {
      const keyChirho = `${itemChirho.from_id_chirho}|${itemChirho.to_id_chirho}`;
      if (seenChirho.has(keyChirho)) {
        duplicatesChirho++;
      }
      seenChirho.add(keyChirho);
    }
    if (duplicatesChirho > 0) {
      console.log(`    WARN: ${duplicatesChirho} duplicate pairs`);
    }

    console.log(`    OK: ${dataChirho.length} pairs validated`);
  }

  return passedChirho;
}

async function mainChirho(): Promise<void> {
  console.log("Dataset Validation");
  console.log("==================");

  const embedderPassedChirho = await validateEmbedderChirho();
  const classifierPassedChirho = await validateClassifierChirho();

  console.log("\n==================");
  console.log(`Embedder: ${embedderPassedChirho ? "PASSED" : "ISSUES FOUND"}`);
  console.log(`Classifier: ${classifierPassedChirho ? "PASSED" : "ISSUES FOUND"}`);

  if (!embedderPassedChirho || !classifierPassedChirho) {
    console.log("\nSome checks failed — review warnings above.");
    process.exit(1);
  } else {
    console.log("\nAll checks passed!");
  }
}

mainChirho();
