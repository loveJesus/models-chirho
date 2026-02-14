// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-tipnr-chirho.ts
 * Downloads the STEPBible TIPNR (Translators Individualised Proper Names with all References)
 * data and parses it into a structured JSON file for NER dataset construction.
 *
 * Source: STEPBible-Data (CC BY license)
 * Contains proper names from the Bible with their types (person/place/thing) and verse references.
 */

import { writeFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;
const OUTPUT_FILE_CHIRHO = `${RAW_DIR_CHIRHO}tipnr-chirho.json`;

const TIPNR_URL_CHIRHO =
  "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/TIPNR%20-%20Translators%20Individualised%20Proper%20Names%20with%20all%20References%20-%20STEPBible.org%20CC%20BY.txt";

interface TipnrEntityChirho {
  nameChirho: string;
  typeChirho: "PERSON" | "PLACE" | "ARTIFACT" | "PEOPLE_GROUP" | "EVENT" | "DIVINE";
  referencesChirho: string[];
  descriptionChirho: string;
  alternateNamesChirho: string[];
}

/**
 * Map TIPNR tag codes to our NER entity types.
 * TIPNR uses tags like: Person, Place, Thing, PeopleGroup, etc.
 */
function mapTipnrTypeChirho(rawTypeChirho: string): TipnrEntityChirho["typeChirho"] | null {
  const normalizedChirho = rawTypeChirho.trim().toLowerCase();

  if (normalizedChirho.includes("person") || normalizedChirho.includes("human")) {
    return "PERSON";
  }
  if (normalizedChirho.includes("place") || normalizedChirho.includes("location")) {
    return "PLACE";
  }
  if (normalizedChirho.includes("peoplegroup") || normalizedChirho.includes("people group") || normalizedChirho.includes("nation")) {
    return "PEOPLE_GROUP";
  }
  if (normalizedChirho.includes("thing") || normalizedChirho.includes("object")) {
    return "ARTIFACT";
  }
  if (normalizedChirho.includes("event")) {
    return "EVENT";
  }
  if (normalizedChirho.includes("divine") || normalizedChirho.includes("god")) {
    return "DIVINE";
  }

  return null;
}

/**
 * Parse a TIPNR verse reference string like "Gen.1.1" or "Gen.1.1-Gen.1.3"
 * into a simpler "Gen 1:1" format.
 */
function parseReferenceChirho(refChirho: string): string {
  const cleanRefChirho = refChirho.trim();
  // Handle format like "Gen.1.1"
  const matchChirho = cleanRefChirho.match(/^(\w+)\.(\d+)\.(\d+)/);
  if (matchChirho) {
    return `${matchChirho[1]} ${matchChirho[2]}:${matchChirho[3]}`;
  }
  return cleanRefChirho;
}

/**
 * Parse the TIPNR TSV file content into structured entities.
 * The TIPNR file is a tab-separated file with a complex header structure.
 * Lines starting with $ are headers/section markers.
 * Data lines contain: UniqueName\tType\tEnglishName\tReferences\t...
 */
function parseTipnrContentChirho(contentChirho: string): TipnrEntityChirho[] {
  const linesChirho = contentChirho.split("\n");
  const entitiesChirho: TipnrEntityChirho[] = [];

  let currentSectionChirho = "";
  let headersParsedChirho = false;

  for (const lineChirho of linesChirho) {
    const trimmedLineChirho = lineChirho.trim();

    // Skip empty lines and comments
    if (!trimmedLineChirho || trimmedLineChirho.startsWith("#")) {
      continue;
    }

    // Section headers start with $
    if (trimmedLineChirho.startsWith("$")) {
      currentSectionChirho = trimmedLineChirho;
      headersParsedChirho = true;
      continue;
    }

    // Skip until we've seen at least one header
    if (!headersParsedChirho) {
      continue;
    }

    // Parse tab-separated data lines
    const fieldsChirho = trimmedLineChirho.split("\t");

    // Need at least a name and some data
    if (fieldsChirho.length < 3) {
      continue;
    }

    // The TIPNR format varies but generally:
    // Field 0: Unique identifier / name reference
    // Field 1: Often contains the type or additional name info
    // Field 2+: English name, references, description
    const rawNameFieldChirho = fieldsChirho[0].trim();
    const secondFieldChirho = fieldsChirho[1]?.trim() || "";
    const thirdFieldChirho = fieldsChirho[2]?.trim() || "";

    // Extract the English name - typically after "=" sign or in a dedicated column
    let englishNameChirho = "";
    let rawTypeChirho = "";
    let refsStringChirho = "";
    let descriptionChirho = "";

    // TIPNR entries often have the pattern: @UniqueID[TAB]@Type=Value[TAB]...
    // or simpler: Name[TAB]Type[TAB]References
    // We'll handle both formats

    // Look for name in fields
    for (let iChirho = 0; iChirho < fieldsChirho.length; iChirho++) {
      const fieldChirho = fieldsChirho[iChirho].trim();

      // Check for type indicators
      if (fieldChirho.match(/^(Person|Place|Thing|PeopleGroup|Event|Divine|Animal|Object)/i)) {
        rawTypeChirho = fieldChirho;
      }

      // Look for verse references (pattern like Gen.1.1 or Mat.1.1)
      if (fieldChirho.match(/[A-Z][a-z]{1,3}\.\d+\.\d+/)) {
        refsStringChirho += (refsStringChirho ? ";" : "") + fieldChirho;
      }

      // English name is typically the readable name field
      if (
        !fieldChirho.startsWith("@") &&
        !fieldChirho.startsWith("$") &&
        !fieldChirho.match(/^[A-Z][a-z]{1,3}\.\d+/) &&
        !fieldChirho.match(/^(Person|Place|Thing|PeopleGroup|Event|Divine)/i) &&
        fieldChirho.length > 0 &&
        fieldChirho.length < 50 &&
        fieldChirho.match(/^[A-Z]/)
      ) {
        if (!englishNameChirho) {
          englishNameChirho = fieldChirho;
        }
      }
    }

    // If we found a name with @, extract it
    if (!englishNameChirho && rawNameFieldChirho.startsWith("@")) {
      // Try to extract the name after @ and before any = or special chars
      const nameMatchChirho = rawNameFieldChirho.match(/@([A-Za-z]+)/);
      if (nameMatchChirho) {
        englishNameChirho = nameMatchChirho[1];
      }
    }

    // Fallback: use the first readable field
    if (!englishNameChirho) {
      englishNameChirho = rawNameFieldChirho.replace(/^@/, "").replace(/[=.].*/g, "").trim();
    }

    // Skip entries without a meaningful name
    if (!englishNameChirho || englishNameChirho.length < 2) {
      continue;
    }

    // Determine entity type
    let entityTypeChirho = mapTipnrTypeChirho(rawTypeChirho);
    if (!entityTypeChirho) {
      // Try inferring from the section header
      if (currentSectionChirho.toLowerCase().includes("person")) {
        entityTypeChirho = "PERSON";
      } else if (currentSectionChirho.toLowerCase().includes("place")) {
        entityTypeChirho = "PLACE";
      } else if (currentSectionChirho.toLowerCase().includes("thing")) {
        entityTypeChirho = "ARTIFACT";
      } else {
        entityTypeChirho = "PERSON"; // Default to person
      }
    }

    // Parse references
    const parsedReferencesChirho: string[] = [];
    if (refsStringChirho) {
      const refsArrayChirho = refsStringChirho.split(/[;,]/);
      for (const refChirho of refsArrayChirho) {
        const parsedRefChirho = parseReferenceChirho(refChirho);
        if (parsedRefChirho) {
          parsedReferencesChirho.push(parsedRefChirho);
        }
      }
    }

    entitiesChirho.push({
      nameChirho: englishNameChirho,
      typeChirho: entityTypeChirho,
      referencesChirho: parsedReferencesChirho,
      descriptionChirho: descriptionChirho,
      alternateNamesChirho: [],
    });
  }

  return entitiesChirho;
}

/**
 * Deduplicate entities by name, merging references and preferring
 * the most specific type assignment.
 */
function deduplicateEntitiesChirho(entitiesChirho: TipnrEntityChirho[]): TipnrEntityChirho[] {
  const entityMapChirho = new Map<string, TipnrEntityChirho>();

  for (const entityChirho of entitiesChirho) {
    const keyChirho = entityChirho.nameChirho.toLowerCase();
    const existingChirho = entityMapChirho.get(keyChirho);

    if (existingChirho) {
      // Merge references
      const allRefsChirho = new Set([
        ...existingChirho.referencesChirho,
        ...entityChirho.referencesChirho,
      ]);
      existingChirho.referencesChirho = Array.from(allRefsChirho);

      // Keep alternate names
      if (
        entityChirho.nameChirho !== existingChirho.nameChirho &&
        !existingChirho.alternateNamesChirho.includes(entityChirho.nameChirho)
      ) {
        existingChirho.alternateNamesChirho.push(entityChirho.nameChirho);
      }
    } else {
      entityMapChirho.set(keyChirho, { ...entityChirho });
    }
  }

  return Array.from(entityMapChirho.values());
}

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    const statResultChirho = await stat(pathChirho);
    return statResultChirho.size > 1000;
  } catch {
    return false;
  }
}

async function mainChirho(): Promise<void> {
  console.log("TIPNR Entity Downloader");
  console.log("=======================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  // Check if already downloaded
  if (await fileExistsChirho(OUTPUT_FILE_CHIRHO)) {
    console.log(`  TIPNR data already exists at ${OUTPUT_FILE_CHIRHO}`);
    console.log("  Delete file to re-download.\n");
    return;
  }

  // Download
  console.log(`  Downloading TIPNR from STEPBible-Data...`);
  const responseChirho = await fetch(TIPNR_URL_CHIRHO, {
    headers: { "User-Agent": "biblical-entity-recognizer-chirho/1.0" },
  });

  if (!responseChirho.ok) {
    throw new Error(`Download failed: ${responseChirho.status} ${responseChirho.statusText}`);
  }

  const rawContentChirho = await responseChirho.text();
  const rawSizeMbChirho = (Buffer.byteLength(rawContentChirho) / 1024 / 1024).toFixed(1);
  console.log(`  Downloaded ${rawSizeMbChirho} MB of TIPNR data`);

  // Also save the raw file
  const rawOutputChirho = `${RAW_DIR_CHIRHO}tipnr-raw-chirho.txt`;
  await writeFile(rawOutputChirho, rawContentChirho, "utf-8");
  console.log(`  Raw file saved to ${rawOutputChirho}`);

  // Parse
  console.log("\n  Parsing TIPNR entries...");
  const rawEntitiesChirho = parseTipnrContentChirho(rawContentChirho);
  console.log(`  Parsed ${rawEntitiesChirho.length} raw entity entries`);

  // Deduplicate
  const entitiesChirho = deduplicateEntitiesChirho(rawEntitiesChirho);
  console.log(`  After deduplication: ${entitiesChirho.length} unique entities`);

  // Type distribution
  const typeCountsChirho: Record<string, number> = {};
  for (const entityChirho of entitiesChirho) {
    typeCountsChirho[entityChirho.typeChirho] =
      (typeCountsChirho[entityChirho.typeChirho] || 0) + 1;
  }
  console.log("\n  Entity type distribution:");
  for (const [typeChirho, countChirho] of Object.entries(typeCountsChirho).sort(
    (aChirho, bChirho) => bChirho[1] - aChirho[1]
  )) {
    console.log(`    ${typeChirho}: ${countChirho}`);
  }

  // Save parsed output
  const outputDataChirho = {
    metadataChirho: {
      generatedAtChirho: new Date().toISOString(),
      sourceChirho: "STEPBible TIPNR (CC BY)",
      urlChirho: TIPNR_URL_CHIRHO,
      totalEntitiesChirho: entitiesChirho.length,
      typeDistributionChirho: typeCountsChirho,
    },
    entitiesChirho,
  };

  await writeFile(OUTPUT_FILE_CHIRHO, JSON.stringify(outputDataChirho, null, 2), "utf-8");
  console.log(`\n  Parsed entities saved to ${OUTPUT_FILE_CHIRHO}`);

  // Show some samples
  console.log("\n  Sample entities:");
  const samplesChirho = entitiesChirho.slice(0, 10);
  for (const sampleChirho of samplesChirho) {
    const refsPreviewChirho = sampleChirho.referencesChirho.slice(0, 3).join(", ");
    const moreChirho =
      sampleChirho.referencesChirho.length > 3
        ? ` (+${sampleChirho.referencesChirho.length - 3} more)`
        : "";
    console.log(
      `    ${sampleChirho.nameChirho} [${sampleChirho.typeChirho}] refs: ${refsPreviewChirho}${moreChirho}`
    );
  }

  console.log("\nDone!");
}

mainChirho();
