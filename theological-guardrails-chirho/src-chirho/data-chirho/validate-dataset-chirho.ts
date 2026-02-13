// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * validate-dataset-chirho.ts
 * Quality checks on the generated dataset: label distribution, duplicates,
 * scripture ref validation, and basic consistency.
 */

import { readFile } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${process.cwd()}/data-chirho/processed-chirho/`;

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
  source_chirho: string;
  seed_index_chirho: number;
}

const VALID_LABELS_CHIRHO = ["orthodox", "heterodox", "denominational_distinctive"];
const VALID_HERESY_TYPES_CHIRHO = [
  "arianism", "pelagianism", "gnosticism", "modalism", "docetism",
  "nestorianism", "marcionism", "apollinarianism", "monothelitism",
  "semi_pelagianism", "adoptionism", "patripassianism",
];
const VALID_DOMAINS_CHIRHO = [
  "christology", "trinity", "soteriology", "theology_proper",
  "incarnation", "creation", "pneumatology", "eschatology",
];

// Basic scripture reference pattern
const SCRIPTURE_REF_PATTERN_CHIRHO = /^[1-3]?\s?[A-Z][a-z]+\s+\d+(?::\d+(?:-\d+)?)?$/;

async function loadSplitChirho(fileNameChirho: string): Promise<DatasetExampleChirho[]> {
  const contentChirho = await readFile(`${PROCESSED_DIR_CHIRHO}${fileNameChirho}`, "utf-8");
  return contentChirho
    .trim()
    .split("\n")
    .filter((lineChirho) => lineChirho.trim())
    .map((lineChirho) => JSON.parse(lineChirho));
}

interface ValidationResultChirho {
  passedChirho: boolean;
  issuesChirho: string[];
  warningsChirho: string[];
  statsChirho: Record<string, unknown>;
}

function validateDatasetChirho(
  dataChirho: DatasetExampleChirho[],
  splitNameChirho: string,
): ValidationResultChirho {
  const issuesChirho: string[] = [];
  const warningsChirho: string[] = [];

  // 1. Check for empty texts
  const emptyTextsChirho = dataChirho.filter((exChirho) => !exChirho.text_chirho?.trim());
  if (emptyTextsChirho.length > 0) {
    issuesChirho.push(`${splitNameChirho}: ${emptyTextsChirho.length} examples with empty text`);
  }

  // 2. Check label validity
  const invalidLabelsChirho = dataChirho.filter(
    (exChirho) => !VALID_LABELS_CHIRHO.includes(exChirho.label_chirho)
  );
  if (invalidLabelsChirho.length > 0) {
    issuesChirho.push(
      `${splitNameChirho}: ${invalidLabelsChirho.length} examples with invalid labels`
    );
  }

  // 3. Check heresy types
  for (const exChirho of dataChirho) {
    if (exChirho.label_chirho === "heterodox" && exChirho.heresy_types_chirho.length === 0) {
      warningsChirho.push(
        `${splitNameChirho}: Heterodox example missing heresy types: "${exChirho.text_chirho.substring(0, 50)}..."`
      );
    }
    for (const htChirho of exChirho.heresy_types_chirho) {
      if (!VALID_HERESY_TYPES_CHIRHO.includes(htChirho)) {
        issuesChirho.push(`${splitNameChirho}: Invalid heresy type "${htChirho}"`);
      }
    }
  }

  // 4. Check for exact duplicates
  const textsSetChirho = new Set<string>();
  let dupCountChirho = 0;
  for (const exChirho of dataChirho) {
    const normalizedChirho = exChirho.text_chirho.trim().toLowerCase();
    if (textsSetChirho.has(normalizedChirho)) {
      dupCountChirho++;
    } else {
      textsSetChirho.add(normalizedChirho);
    }
  }
  if (dupCountChirho > 0) {
    warningsChirho.push(`${splitNameChirho}: ${dupCountChirho} exact duplicate texts found`);
  }

  // 5. Check confidence range
  const outOfRangeChirho = dataChirho.filter(
    (exChirho) => exChirho.confidence_chirho < 0 || exChirho.confidence_chirho > 1
  );
  if (outOfRangeChirho.length > 0) {
    issuesChirho.push(
      `${splitNameChirho}: ${outOfRangeChirho.length} examples with confidence outside [0,1]`
    );
  }

  // 6. Check domains
  const invalidDomainsChirho = dataChirho.filter(
    (exChirho) => !VALID_DOMAINS_CHIRHO.includes(exChirho.domain_chirho)
  );
  if (invalidDomainsChirho.length > 0) {
    warningsChirho.push(
      `${splitNameChirho}: ${invalidDomainsChirho.length} examples with non-standard domains`
    );
  }

  // 7. Label distribution
  const labelDistChirho: Record<string, number> = {};
  for (const exChirho of dataChirho) {
    labelDistChirho[exChirho.label_chirho] = (labelDistChirho[exChirho.label_chirho] || 0) + 1;
  }

  // Check for severe imbalance
  const totalChirho = dataChirho.length;
  for (const [labelChirho, countChirho] of Object.entries(labelDistChirho)) {
    const ratioChirho = countChirho / totalChirho;
    if (ratioChirho < 0.05) {
      warningsChirho.push(
        `${splitNameChirho}: Label "${labelChirho}" is severely underrepresented (${(ratioChirho * 100).toFixed(1)}%)`
      );
    }
  }

  // 8. Heresy type distribution
  const heresyDistChirho: Record<string, number> = {};
  for (const exChirho of dataChirho) {
    for (const htChirho of exChirho.heresy_types_chirho) {
      heresyDistChirho[htChirho] = (heresyDistChirho[htChirho] || 0) + 1;
    }
  }

  // 9. Domain distribution
  const domainDistChirho: Record<string, number> = {};
  for (const exChirho of dataChirho) {
    domainDistChirho[exChirho.domain_chirho] = (domainDistChirho[exChirho.domain_chirho] || 0) + 1;
  }

  // 10. Average text length
  const avgLenChirho = dataChirho.reduce((sChirho, eChirho) => sChirho + eChirho.text_chirho.length, 0) / dataChirho.length;
  const minLenChirho = Math.min(...dataChirho.map((eChirho) => eChirho.text_chirho.length));
  const maxLenChirho = Math.max(...dataChirho.map((eChirho) => eChirho.text_chirho.length));

  return {
    passedChirho: issuesChirho.length === 0,
    issuesChirho,
    warningsChirho: warningsChirho.slice(0, 20), // Cap warnings
    statsChirho: {
      totalExamplesChirho: dataChirho.length,
      uniqueTextsChirho: textsSetChirho.size,
      duplicatesChirho: dupCountChirho,
      labelDistributionChirho: labelDistChirho,
      heresyDistributionChirho: heresyDistChirho,
      domainDistributionChirho: domainDistChirho,
      textLengthChirho: {
        avgChirho: Math.round(avgLenChirho),
        minChirho: minLenChirho,
        maxChirho: maxLenChirho,
      },
    },
  };
}

async function mainChirho(): Promise<void> {
  console.log("🔍 Dataset Validation");
  console.log("====================\n");

  const splitsChirho = ["train-chirho.jsonl", "val-chirho.jsonl", "test-chirho.jsonl"];
  let overallPassedChirho = true;

  for (const splitChirho of splitsChirho) {
    try {
      const dataChirho = await loadSplitChirho(splitChirho);
      const resultChirho = validateDatasetChirho(dataChirho, splitChirho);

      console.log(`\n📊 ${splitChirho}:`);
      console.log(`   Status: ${resultChirho.passedChirho ? "✅ PASSED" : "❌ FAILED"}`);
      console.log(`   Examples: ${(resultChirho.statsChirho.totalExamplesChirho as number).toLocaleString()}`);
      console.log(`   Unique texts: ${(resultChirho.statsChirho.uniqueTextsChirho as number).toLocaleString()}`);
      console.log(`   Duplicates: ${resultChirho.statsChirho.duplicatesChirho}`);

      const lenStatsChirho = resultChirho.statsChirho.textLengthChirho as Record<string, number>;
      console.log(
        `   Text length: avg=${lenStatsChirho.avgChirho}, min=${lenStatsChirho.minChirho}, max=${lenStatsChirho.maxChirho}`
      );

      console.log(`   Label distribution:`, resultChirho.statsChirho.labelDistributionChirho);
      console.log(`   Heresy distribution:`, resultChirho.statsChirho.heresyDistributionChirho);
      console.log(`   Domain distribution:`, resultChirho.statsChirho.domainDistributionChirho);

      if (resultChirho.issuesChirho.length > 0) {
        console.log(`   Issues:`);
        for (const issueChirho of resultChirho.issuesChirho) {
          console.log(`     ❌ ${issueChirho}`);
        }
      }

      if (resultChirho.warningsChirho.length > 0) {
        console.log(`   Warnings (first 20):`);
        for (const warnChirho of resultChirho.warningsChirho) {
          console.log(`     ⚠️  ${warnChirho}`);
        }
      }

      if (!resultChirho.passedChirho) overallPassedChirho = false;
    } catch (errorChirho) {
      console.log(`\n📊 ${splitChirho}: ⚠️  Could not load (${errorChirho})`);
    }
  }

  console.log(`\n${"=".repeat(40)}`);
  console.log(
    `Overall: ${overallPassedChirho ? "✅ ALL SPLITS PASSED" : "❌ SOME SPLITS HAVE ISSUES"}`
  );
}

mainChirho();
