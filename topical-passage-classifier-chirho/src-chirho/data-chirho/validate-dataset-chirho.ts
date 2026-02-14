// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * validate-dataset-chirho.ts
 * Validates the topical passage search dataset.
 *
 * Checks:
 *   - Files exist and have content
 *   - JSONL structure is valid
 *   - No empty fields
 *   - Source distribution (naves vs crossref)
 *   - Total pair counts meet targets
 *   - Query and positive lengths are reasonable
 */

import { readFile, stat } from "fs/promises";

const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

interface CheckResultChirho {
  nameChirho: string;
  passedChirho: boolean;
  detailsChirho: string;
}

async function mainChirho(): Promise<void> {
  console.log("Topical Dataset Validator");
  console.log("========================\n");

  const checksChirho: CheckResultChirho[] = [];

  const filesChirho = [
    "train-topical-chirho.jsonl",
    "val-topical-chirho.jsonl",
    "test-topical-chirho.jsonl",
  ];

  let totalPairsChirho = 0;

  // Check file existence and size
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

  // Detailed validation per file
  for (const fileChirho of filesChirho) {
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${fileChirho}`;
    try {
      const contentChirho = await readFile(pathChirho, "utf-8");
      const linesChirho = contentChirho
        .split("\n")
        .filter((lChirho) => lChirho.trim());

      let navesCountChirho = 0;
      let crossrefCountChirho = 0;
      let emptyFieldsChirho = 0;
      let shortQueriesChirho = 0;
      let shortPositivesChirho = 0;
      let parseErrorsChirho = 0;
      let totalQueryLenChirho = 0;
      let totalPositiveLenChirho = 0;

      for (const lineChirho of linesChirho) {
        try {
          const objChirho = JSON.parse(lineChirho);

          if (!objChirho.query_chirho?.trim() || !objChirho.positive_chirho?.trim()) {
            emptyFieldsChirho++;
          }

          if (objChirho.query_chirho && objChirho.query_chirho.length < 5) {
            shortQueriesChirho++;
          }

          if (objChirho.positive_chirho && objChirho.positive_chirho.length < 10) {
            shortPositivesChirho++;
          }

          totalQueryLenChirho += (objChirho.query_chirho || "").length;
          totalPositiveLenChirho += (objChirho.positive_chirho || "").length;

          if (objChirho.source_chirho === "naves") navesCountChirho++;
          else if (objChirho.source_chirho === "crossref") crossrefCountChirho++;
        } catch {
          parseErrorsChirho++;
        }
      }

      totalPairsChirho += linesChirho.length;

      checksChirho.push({
        nameChirho: `${fileChirho}: pair count`,
        passedChirho: linesChirho.length > 0,
        detailsChirho: `${linesChirho.length} pairs`,
      });

      checksChirho.push({
        nameChirho: `${fileChirho}: no parse errors`,
        passedChirho: parseErrorsChirho === 0,
        detailsChirho: `${parseErrorsChirho} parse errors`,
      });

      checksChirho.push({
        nameChirho: `${fileChirho}: no empty fields`,
        passedChirho: emptyFieldsChirho === 0,
        detailsChirho: `${emptyFieldsChirho} empty`,
      });

      checksChirho.push({
        nameChirho: `${fileChirho}: source distribution`,
        passedChirho: navesCountChirho > 0 || crossrefCountChirho > 0,
        detailsChirho: `naves=${navesCountChirho}, crossref=${crossrefCountChirho}`,
      });

      const avgQueryChirho =
        linesChirho.length > 0
          ? (totalQueryLenChirho / linesChirho.length).toFixed(0)
          : "0";
      const avgPositiveChirho =
        linesChirho.length > 0
          ? (totalPositiveLenChirho / linesChirho.length).toFixed(0)
          : "0";

      checksChirho.push({
        nameChirho: `${fileChirho}: avg lengths`,
        passedChirho: parseInt(avgQueryChirho) > 5 && parseInt(avgPositiveChirho) > 10,
        detailsChirho: `avg query=${avgQueryChirho} chars, avg positive=${avgPositiveChirho} chars`,
      });

      if (shortQueriesChirho > 0 || shortPositivesChirho > 0) {
        checksChirho.push({
          nameChirho: `${fileChirho}: short entries`,
          passedChirho: shortQueriesChirho < linesChirho.length * 0.05,
          detailsChirho: `${shortQueriesChirho} short queries, ${shortPositivesChirho} short positives`,
        });
      }
    } catch {
      // File not found - already caught above
    }
  }

  // Global checks
  checksChirho.push({
    nameChirho: "Total pairs target (>= 10000)",
    passedChirho: totalPairsChirho >= 10000,
    detailsChirho: `${totalPairsChirho} total pairs`,
  });

  // Print results
  let passedChirho = 0;
  let failedChirho = 0;

  for (const checkChirho of checksChirho) {
    const markerChirho = checkChirho.passedChirho ? "+" : "x";
    const statusChirho = checkChirho.passedChirho ? "PASS" : "FAIL";
    console.log(
      `  [${markerChirho}] ${statusChirho}: ${checkChirho.nameChirho} — ${checkChirho.detailsChirho}`
    );
    if (checkChirho.passedChirho) passedChirho++;
    else failedChirho++;
  }

  console.log(`\n========================`);
  console.log(
    `Results: ${passedChirho} passed, ${failedChirho} failed out of ${checksChirho.length}`
  );

  if (failedChirho > 0) process.exit(1);
}

mainChirho();
