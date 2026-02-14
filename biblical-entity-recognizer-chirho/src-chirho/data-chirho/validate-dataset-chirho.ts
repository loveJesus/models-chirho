// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * validate-dataset-chirho.ts
 * Validates the constructed NER dataset for consistency, coverage, and quality.
 *
 * Checks:
 * 1. File existence and format validation
 * 2. Token/tag count alignment (must be equal per example)
 * 3. BIO tag consistency (I-X must follow B-X or I-X of same type)
 * 4. Entity type distribution across splits
 * 5. Sample inspection for manual review
 * 6. Coverage statistics
 */

import { readFile, stat } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

const VALID_TAGS_CHIRHO = new Set([
  "O",
  "B-PERSON", "I-PERSON",
  "B-DIVINE", "I-DIVINE",
  "B-PEOPLE_GROUP", "I-PEOPLE_GROUP",
  "B-PLACE", "I-PLACE",
  "B-EVENT", "I-EVENT",
  "B-ARTIFACT", "I-ARTIFACT",
]);

interface NerExampleChirho {
  tokens_chirho: string[];
  ner_tags_chirho: string[];
  reference_chirho: string;
}

interface ValidationResultChirho {
  fileNameChirho: string;
  totalExamplesChirho: number;
  errorCountChirho: number;
  warningCountChirho: number;
  errorsChirho: string[];
  warningsChirho: string[];
  tagDistributionChirho: Record<string, number>;
  entityCountsChirho: Record<string, number>;
  avgTokenLengthChirho: number;
  examplesWithEntitiesChirho: number;
}

async function loadJsonlChirho(pathChirho: string): Promise<NerExampleChirho[]> {
  const contentChirho = await readFile(pathChirho, "utf-8");
  const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());
  return linesChirho.map((lineChirho) => JSON.parse(lineChirho));
}

function validateSplitChirho(
  fileNameChirho: string,
  examplesChirho: NerExampleChirho[]
): ValidationResultChirho {
  const errorsChirho: string[] = [];
  const warningsChirho: string[] = [];
  const tagDistributionChirho: Record<string, number> = {};
  const entityCountsChirho: Record<string, number> = {};
  let totalTokensChirho = 0;
  let examplesWithEntitiesChirho = 0;

  for (let iChirho = 0; iChirho < examplesChirho.length; iChirho++) {
    const exChirho = examplesChirho[iChirho];
    const refChirho = exChirho.reference_chirho || `example-${iChirho}`;

    // Check 1: tokens and tags must exist and be arrays
    if (!Array.isArray(exChirho.tokens_chirho)) {
      errorsChirho.push(`[${refChirho}] tokens_chirho is not an array`);
      continue;
    }
    if (!Array.isArray(exChirho.ner_tags_chirho)) {
      errorsChirho.push(`[${refChirho}] ner_tags_chirho is not an array`);
      continue;
    }

    // Check 2: token/tag count alignment
    if (exChirho.tokens_chirho.length !== exChirho.ner_tags_chirho.length) {
      errorsChirho.push(
        `[${refChirho}] Token/tag count mismatch: ${exChirho.tokens_chirho.length} tokens vs ${exChirho.ner_tags_chirho.length} tags`
      );
      continue;
    }

    // Check 3: empty examples
    if (exChirho.tokens_chirho.length === 0) {
      warningsChirho.push(`[${refChirho}] Empty example (0 tokens)`);
      continue;
    }

    totalTokensChirho += exChirho.tokens_chirho.length;
    let hasEntityChirho = false;

    // Check 4: BIO tag validity and consistency
    for (let jChirho = 0; jChirho < exChirho.ner_tags_chirho.length; jChirho++) {
      const tagChirho = exChirho.ner_tags_chirho[jChirho];

      // Valid tag check
      if (!VALID_TAGS_CHIRHO.has(tagChirho)) {
        errorsChirho.push(
          `[${refChirho}] Invalid tag "${tagChirho}" at position ${jChirho}`
        );
      }

      // Count tags
      tagDistributionChirho[tagChirho] = (tagDistributionChirho[tagChirho] || 0) + 1;

      // BIO consistency: I-X must follow B-X or I-X
      if (tagChirho.startsWith("I-")) {
        const entityTypeChirho = tagChirho.substring(2);
        const prevTagChirho = jChirho > 0 ? exChirho.ner_tags_chirho[jChirho - 1] : "O";

        if (
          prevTagChirho !== `B-${entityTypeChirho}` &&
          prevTagChirho !== `I-${entityTypeChirho}`
        ) {
          errorsChirho.push(
            `[${refChirho}] BIO violation: ${tagChirho} at pos ${jChirho} follows ${prevTagChirho}`
          );
        }
      }

      // Count entities (B- tags start new entities)
      if (tagChirho.startsWith("B-")) {
        const entityTypeChirho = tagChirho.substring(2);
        entityCountsChirho[entityTypeChirho] =
          (entityCountsChirho[entityTypeChirho] || 0) + 1;
        hasEntityChirho = true;
      }
    }

    if (hasEntityChirho) {
      examplesWithEntitiesChirho++;
    }
  }

  return {
    fileNameChirho,
    totalExamplesChirho: examplesChirho.length,
    errorCountChirho: errorsChirho.length,
    warningCountChirho: warningsChirho.length,
    errorsChirho,
    warningsChirho,
    tagDistributionChirho,
    entityCountsChirho,
    avgTokenLengthChirho:
      examplesChirho.length > 0 ? totalTokensChirho / examplesChirho.length : 0,
    examplesWithEntitiesChirho,
  };
}

function printSampleAnnotationsChirho(
  examplesChirho: NerExampleChirho[],
  countChirho: number
): void {
  const withEntitiesChirho = examplesChirho.filter((exChirho) =>
    exChirho.ner_tags_chirho.some((tChirho) => tChirho !== "O")
  );

  // Pick samples spread across the data
  const stepChirho = Math.max(1, Math.floor(withEntitiesChirho.length / countChirho));
  const samplesChirho: NerExampleChirho[] = [];
  for (let iChirho = 0; iChirho < withEntitiesChirho.length && samplesChirho.length < countChirho; iChirho += stepChirho) {
    samplesChirho.push(withEntitiesChirho[iChirho]);
  }

  console.log(`\n  Sample annotations (${samplesChirho.length} of ${withEntitiesChirho.length} entity-bearing examples):`);

  for (const sampleChirho of samplesChirho) {
    console.log(`\n    ${sampleChirho.reference_chirho}:`);

    const partsChirho: string[] = [];
    let iChirho = 0;
    while (iChirho < sampleChirho.tokens_chirho.length) {
      const tagChirho = sampleChirho.ner_tags_chirho[iChirho];

      if (tagChirho.startsWith("B-")) {
        const entityTypeChirho = tagChirho.substring(2);
        const entityTokensChirho = [sampleChirho.tokens_chirho[iChirho]];
        let jChirho = iChirho + 1;
        while (
          jChirho < sampleChirho.tokens_chirho.length &&
          sampleChirho.ner_tags_chirho[jChirho] === `I-${entityTypeChirho}`
        ) {
          entityTokensChirho.push(sampleChirho.tokens_chirho[jChirho]);
          jChirho++;
        }
        partsChirho.push(`[${entityTokensChirho.join(" ")}|${entityTypeChirho}]`);
        iChirho = jChirho;
      } else {
        partsChirho.push(sampleChirho.tokens_chirho[iChirho]);
        iChirho++;
      }
    }

    console.log(`      ${partsChirho.join(" ")}`);
  }
}

async function mainChirho(): Promise<void> {
  console.log("NER Dataset Validator");
  console.log("=====================\n");

  const splitsChirho = [
    { nameChirho: "train", fileChirho: "train-chirho.jsonl" },
    { nameChirho: "val", fileChirho: "val-chirho.jsonl" },
    { nameChirho: "test", fileChirho: "test-chirho.jsonl" },
  ];

  let totalErrorsChirho = 0;
  let totalWarningsChirho = 0;
  const allResultsChirho: ValidationResultChirho[] = [];

  for (const splitChirho of splitsChirho) {
    const filePathChirho = `${PROCESSED_DIR_CHIRHO}${splitChirho.fileChirho}`;

    // Check file exists
    try {
      await stat(filePathChirho);
    } catch {
      console.error(`  MISSING: ${splitChirho.fileChirho} - run build-ner-dataset-chirho first`);
      totalErrorsChirho++;
      continue;
    }

    console.log(`Validating ${splitChirho.nameChirho} split (${splitChirho.fileChirho})...`);
    const examplesChirho = await loadJsonlChirho(filePathChirho);
    const resultChirho = validateSplitChirho(splitChirho.fileChirho, examplesChirho);
    allResultsChirho.push(resultChirho);

    console.log(`  Examples: ${resultChirho.totalExamplesChirho}`);
    console.log(`  Avg tokens/example: ${resultChirho.avgTokenLengthChirho.toFixed(1)}`);
    console.log(`  Examples with entities: ${resultChirho.examplesWithEntitiesChirho} (${((resultChirho.examplesWithEntitiesChirho / resultChirho.totalExamplesChirho) * 100).toFixed(1)}%)`);
    console.log(`  Errors: ${resultChirho.errorCountChirho}`);
    console.log(`  Warnings: ${resultChirho.warningCountChirho}`);

    // Print entity counts
    console.log("  Entity counts:");
    for (const [typeChirho, countChirho] of Object.entries(resultChirho.entityCountsChirho).sort(
      (aChirho, bChirho) => bChirho[1] - aChirho[1]
    )) {
      console.log(`    ${typeChirho}: ${countChirho}`);
    }

    // Print first few errors if any
    if (resultChirho.errorCountChirho > 0) {
      console.log("  First errors:");
      for (const errChirho of resultChirho.errorsChirho.slice(0, 5)) {
        console.log(`    ${errChirho}`);
      }
      if (resultChirho.errorCountChirho > 5) {
        console.log(`    ... and ${resultChirho.errorCountChirho - 5} more`);
      }
    }

    totalErrorsChirho += resultChirho.errorCountChirho;
    totalWarningsChirho += resultChirho.warningCountChirho;

    // Show sample annotations for test split
    if (splitChirho.nameChirho === "test") {
      printSampleAnnotationsChirho(examplesChirho, 8);
    }

    console.log("");
  }

  // Overall summary
  console.log("=" .repeat(60));
  console.log("VALIDATION SUMMARY");
  console.log("=" .repeat(60));

  let totalExamplesChirho = 0;
  let totalEntitiesChirho = 0;

  for (const resultChirho of allResultsChirho) {
    totalExamplesChirho += resultChirho.totalExamplesChirho;
    for (const countChirho of Object.values(resultChirho.entityCountsChirho)) {
      totalEntitiesChirho += countChirho;
    }
  }

  console.log(`  Total examples: ${totalExamplesChirho}`);
  console.log(`  Total entities: ${totalEntitiesChirho}`);
  console.log(`  Total errors: ${totalErrorsChirho}`);
  console.log(`  Total warnings: ${totalWarningsChirho}`);

  // Aggregate entity type distribution
  const aggregateEntityChirho: Record<string, number> = {};
  for (const resultChirho of allResultsChirho) {
    for (const [typeChirho, countChirho] of Object.entries(resultChirho.entityCountsChirho)) {
      aggregateEntityChirho[typeChirho] = (aggregateEntityChirho[typeChirho] || 0) + countChirho;
    }
  }

  console.log("\n  Aggregate entity distribution:");
  for (const [typeChirho, countChirho] of Object.entries(aggregateEntityChirho).sort(
    (aChirho, bChirho) => bChirho[1] - aChirho[1]
  )) {
    const pctChirho = ((countChirho / totalEntitiesChirho) * 100).toFixed(1);
    console.log(`    ${typeChirho}: ${countChirho} (${pctChirho}%)`);
  }

  // Split proportions
  console.log("\n  Split proportions:");
  for (const resultChirho of allResultsChirho) {
    const pctChirho = ((resultChirho.totalExamplesChirho / totalExamplesChirho) * 100).toFixed(1);
    console.log(`    ${resultChirho.fileNameChirho}: ${resultChirho.totalExamplesChirho} (${pctChirho}%)`);
  }

  // Final verdict
  console.log("");
  if (totalErrorsChirho === 0) {
    console.log("  PASS: All validation checks passed!");
  } else {
    console.log(`  FAIL: ${totalErrorsChirho} errors found. Review and fix before training.`);
    process.exit(1);
  }
}

mainChirho();
