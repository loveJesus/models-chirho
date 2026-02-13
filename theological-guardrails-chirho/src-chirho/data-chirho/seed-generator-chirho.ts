// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * seed-generator-chirho.ts
 * Generates 500 curated seed examples using Grok/xAI API (OpenAI-compatible).
 * Each seed is an orthodox/heretical statement pair with full metadata.
 */

import { writeFile, readFile, mkdir } from "fs/promises";

const SEEDS_DIR_CHIRHO = `${process.cwd()}/data-chirho/seeds-chirho/`;
const RAW_DIR_CHIRHO = `${process.cwd()}/data-chirho/raw-chirho/`;

const GROK_API_KEY_CHIRHO = process.env.GROK_API_KEY_CHIRHO || process.env.GROK_API_KEY;
if (!GROK_API_KEY_CHIRHO) {
  throw new Error("GROK_API_KEY_CHIRHO not set. Source .env-chirho first.");
}

const GROK_API_URL_CHIRHO = "https://api.x.ai/v1/chat/completions";

const TARGET_SEED_COUNT_CHIRHO = 500;
const BATCH_SIZE_CHIRHO = 25; // examples per API call

interface SeedExampleChirho {
  textChirho: string;
  labelChirho: "orthodox" | "heterodox" | "denominational_distinctive";
  heresyTypesChirho: string[];
  confidenceChirho: number;
  explanationChirho: string;
  scriptureRefsChirho: string[];
  creedRefsChirho: string[];
  domainChirho: string;
  denominationalNoteChirho: string | null;
}

const HERESY_TYPES_CHIRHO = [
  "arianism",
  "pelagianism",
  "gnosticism",
  "modalism",
  "docetism",
  "nestorianism",
  "marcionism",
  "apollinarianism",
  "monothelitism",
  "semi_pelagianism",
  "adoptionism",
  "patripassianism",
];

const DOMAINS_CHIRHO = [
  "christology",
  "trinity",
  "soteriology",
  "theology_proper",
  "incarnation",
  "creation",
  "pneumatology",
  "eschatology",
];

async function loadRawDataChirho(): Promise<{ creedsChirho: string; heresiesChirho: string; scriptureChirho: string }> {
  try {
    const creedsChirho = await readFile(`${RAW_DIR_CHIRHO}creeds-chirho.json`, "utf-8");
    const heresiesChirho = await readFile(`${RAW_DIR_CHIRHO}heresies-chirho.json`, "utf-8");
    const scriptureChirho = await readFile(`${RAW_DIR_CHIRHO}scripture-chirho.json`, "utf-8");
    return { creedsChirho, heresiesChirho, scriptureChirho };
  } catch (errorChirho) {
    console.warn("Raw data not found. Run gather scripts first. Using built-in context.");
    return { creedsChirho: "{}", heresiesChirho: "{}", scriptureChirho: "{}" };
  }
}

interface GrokResponseChirho {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

async function generateBatchChirho(
  batchIndexChirho: number,
  heresyFocusChirho: string,
  rawContextChirho: string,
): Promise<SeedExampleChirho[]> {
  const promptChirho = `Generate exactly ${BATCH_SIZE_CHIRHO} theological training examples as a JSON array. Each example should be a statement that a person might actually say or write.

Focus this batch on: ${heresyFocusChirho}

For EACH example, provide:
- "text_chirho": A natural-sounding statement (1-3 sentences) that someone might actually write or say
- "label_chirho": One of "orthodox", "heterodox", or "denominational_distinctive"
- "heresy_types_chirho": Array of heresy labels from [${HERESY_TYPES_CHIRHO.join(", ")}] (empty for orthodox)
- "confidence_chirho": 0.7-1.0 (how clearly this fits the category)
- "explanation_chirho": Why this is orthodox/heterodox, citing specific creeds or scripture
- "scripture_refs_chirho": Relevant Bible references (e.g., "John 1:1")
- "creed_refs_chirho": Relevant creed references (e.g., "nicene_creed", "chalcedonian_definition")
- "domain_chirho": One of [${DOMAINS_CHIRHO.join(", ")}]
- "denominational_note_chirho": null or a note about denominational relevance

Guidelines:
- Mix orthodox (~40%), heterodox (~50%), and denominational_distinctive (~10%) examples
- Make heterodox statements SUBTLE - not cartoonish, but things people actually say
- Include modern phrasings, not just ancient formulations
- Vary the confidence based on how clear-cut the classification is
- For "denominational_distinctive", these are genuine theological disagreements between denominations (predestination, baptism mode, etc.) that are NOT heresies
- Core orthodoxy is defined by the first SIX ecumenical councils (Nicaea 325, Constantinople I 381, Ephesus 431, Chalcedon 451, Constantinople II 553, Constantinople III 681)

Context from historical sources:
${rawContextChirho.substring(0, 3000)}

Return ONLY the JSON array, no other text. Ensure valid JSON.`;

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
          content: "You are a theological expert generating training data for an ML model that classifies theological statements. Generate precise, well-labeled examples with accurate theological classification. Return only valid JSON.",
        },
        {
          role: "user",
          content: promptChirho,
        },
      ],
      max_tokens: 8000,
      temperature: 0.7,
    }),
  });

  if (!responseChirho.ok) {
    const errorTextChirho = await responseChirho.text();
    throw new Error(`Grok API error ${responseChirho.status}: ${errorTextChirho}`);
  }

  const dataChirho = (await responseChirho.json()) as GrokResponseChirho;
  const contentChirho = dataChirho.choices[0]?.message?.content ?? "";

  // Extract JSON from response
  let jsonTextChirho = contentChirho.trim();
  // Handle potential markdown code blocks
  if (jsonTextChirho.startsWith("```")) {
    jsonTextChirho = jsonTextChirho.replace(/^```(?:json)?\n?/, "").replace(/\n?```$/, "");
  }

  const parsedChirho = JSON.parse(jsonTextChirho) as Array<Record<string, unknown>>;

  return parsedChirho.map((itemChirho) => ({
    textChirho: String(itemChirho.text_chirho ?? itemChirho.textChirho ?? ""),
    labelChirho: String(itemChirho.label_chirho ?? itemChirho.labelChirho ?? "orthodox") as SeedExampleChirho["labelChirho"],
    heresyTypesChirho: (itemChirho.heresy_types_chirho ?? itemChirho.heresyTypesChirho ?? []) as string[],
    confidenceChirho: Number(itemChirho.confidence_chirho ?? itemChirho.confidenceChirho ?? 0.8),
    explanationChirho: String(itemChirho.explanation_chirho ?? itemChirho.explanationChirho ?? ""),
    scriptureRefsChirho: (itemChirho.scripture_refs_chirho ?? itemChirho.scriptureRefsChirho ?? []) as string[],
    creedRefsChirho: (itemChirho.creed_refs_chirho ?? itemChirho.creedRefsChirho ?? []) as string[],
    domainChirho: String(itemChirho.domain_chirho ?? itemChirho.domainChirho ?? "christology"),
    denominationalNoteChirho: (itemChirho.denominational_note_chirho ?? itemChirho.denominationalNoteChirho ?? null) as string | null,
  }));
}

async function mainChirho(): Promise<void> {
  console.log("Seed Dataset Generator (Grok/xAI)");
  console.log("===================================\n");

  await mkdir(SEEDS_DIR_CHIRHO, { recursive: true });

  const rawDataChirho = await loadRawDataChirho();
  const rawContextChirho = JSON.stringify({
    creedsSnippetChirho: rawDataChirho.creedsChirho.substring(0, 1500),
    heresiesSnippetChirho: rawDataChirho.heresiesChirho.substring(0, 1500),
  });

  const allSeedsChirho: SeedExampleChirho[] = [];
  const batchCountChirho = Math.ceil(TARGET_SEED_COUNT_CHIRHO / BATCH_SIZE_CHIRHO);

  // Cycle through heresy focuses to ensure coverage
  const heresyFocusCycleChirho = [
    "Arianism and Christological heresies (deity of Christ)",
    "Pelagianism and Semi-Pelagianism (grace and salvation)",
    "Gnosticism and Marcionism (creation and OT/NT unity)",
    "Modalism and Patripassianism (Trinity and divine persons)",
    "Docetism and Apollinarianism (incarnation and humanity of Christ)",
    "Nestorianism (unity of Christ's person, Theotokos)",
    "Monothelitism (two wills of Christ)",
    "Adoptionism (eternal sonship of Christ)",
    "Mixed heresies and subtle edge cases",
    "Orthodox statements and denominational distinctives",
  ];

  for (let iChirho = 0; iChirho < batchCountChirho; iChirho++) {
    const focusChirho = heresyFocusCycleChirho[iChirho % heresyFocusCycleChirho.length];
    console.log(
      `  Batch ${iChirho + 1}/${batchCountChirho}: Focus on ${focusChirho}...`
    );

    try {
      const batchChirho = await generateBatchChirho(
        iChirho,
        focusChirho,
        rawContextChirho,
      );
      allSeedsChirho.push(...batchChirho);
      console.log(`    Generated ${batchChirho.length} examples (total: ${allSeedsChirho.length})`);

      // Rate limit delay
      await new Promise((rChirho) => setTimeout(rChirho, 1500));
    } catch (errorChirho) {
      console.error(`    Batch ${iChirho + 1} failed:`, errorChirho);
    }
  }

  // Trim to target count
  const finalSeedsChirho = allSeedsChirho.slice(0, TARGET_SEED_COUNT_CHIRHO);

  // Output as JSONL (one JSON object per line)
  const jsonlContentChirho = finalSeedsChirho
    .map((seedChirho) =>
      JSON.stringify({
        text_chirho: seedChirho.textChirho,
        label_chirho: seedChirho.labelChirho,
        heresy_types_chirho: seedChirho.heresyTypesChirho,
        confidence_chirho: seedChirho.confidenceChirho,
        explanation_chirho: seedChirho.explanationChirho,
        scripture_refs_chirho: seedChirho.scriptureRefsChirho,
        creed_refs_chirho: seedChirho.creedRefsChirho,
        domain_chirho: seedChirho.domainChirho,
        denominational_note_chirho: seedChirho.denominationalNoteChirho,
      })
    )
    .join("\n");

  const outputPathChirho = `${SEEDS_DIR_CHIRHO}seeds-chirho.jsonl`;
  await writeFile(outputPathChirho, jsonlContentChirho, "utf-8");

  // Also write a summary
  const labelDistributionChirho: Record<string, number> = {};
  const heresyDistributionChirho: Record<string, number> = {};
  const domainDistributionChirho: Record<string, number> = {};

  for (const seedChirho of finalSeedsChirho) {
    labelDistributionChirho[seedChirho.labelChirho] = (labelDistributionChirho[seedChirho.labelChirho] || 0) + 1;
    for (const hChirho of seedChirho.heresyTypesChirho) {
      heresyDistributionChirho[hChirho] = (heresyDistributionChirho[hChirho] || 0) + 1;
    }
    domainDistributionChirho[seedChirho.domainChirho] = (domainDistributionChirho[seedChirho.domainChirho] || 0) + 1;
  }

  const summaryChirho = {
    totalSeedsChirho: finalSeedsChirho.length,
    generatedAtChirho: new Date().toISOString(),
    labelDistributionChirho,
    heresyDistributionChirho,
    domainDistributionChirho,
  };

  await writeFile(
    `${SEEDS_DIR_CHIRHO}seeds-summary-chirho.json`,
    JSON.stringify(summaryChirho, null, 2),
    "utf-8"
  );

  console.log(`\nGenerated ${finalSeedsChirho.length} seed examples`);
  console.log(`   Written to: ${outputPathChirho}`);
  console.log("\nLabel distribution:");
  for (const [labelChirho, countChirho] of Object.entries(labelDistributionChirho)) {
    console.log(`  ${labelChirho}: ${countChirho}`);
  }
  console.log("\nHeresy type distribution:");
  for (const [heresyChirho, countChirho] of Object.entries(heresyDistributionChirho).sort(
    (aChirho, bChirho) => (bChirho[1] as number) - (aChirho[1] as number)
  )) {
    console.log(`  ${heresyChirho}: ${countChirho}`);
  }
}

mainChirho();
