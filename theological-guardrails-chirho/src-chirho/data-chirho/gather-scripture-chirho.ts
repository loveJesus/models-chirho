// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * gather-scripture-chirho.ts
 * Pulls scripture texts from bible-api.com (no auth needed, World English Bible - public domain).
 * Gathers key doctrinal passages relevant to theological classification.
 */

import { writeFile, mkdir } from "fs/promises";

const OUTPUT_DIR_CHIRHO = `${process.cwd()}/data-chirho/raw-chirho/`;
const BIBLE_API_URL_CHIRHO = "https://bible-api.com";

interface ScripturePassageChirho {
  referenceChirho: string;
  textChirho: string;
  doctrinalCategoryChirho: string;
  relevantHeresiesChirho: string[];
}

// Key passages organized by doctrinal category
const PASSAGES_TO_FETCH_CHIRHO: Array<{
  referenceChirho: string;
  doctrinalCategoryChirho: string;
  relevantHeresiesChirho: string[];
}> = [
  // Trinity / Deity of Christ
  { referenceChirho: "John 1:1-18", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["arianism", "gnosticism", "docetism"] },
  { referenceChirho: "John 10:30", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["arianism"] },
  { referenceChirho: "John 8:58", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["arianism", "adoptionism"] },
  { referenceChirho: "Colossians 1:15-20", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["arianism", "gnosticism"] },
  { referenceChirho: "Hebrews 1:1-14", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["arianism", "adoptionism"] },
  { referenceChirho: "Philippians 2:5-11", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["arianism", "docetism", "adoptionism"] },
  { referenceChirho: "Colossians 2:9", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["arianism", "docetism", "nestorianism"] },
  { referenceChirho: "Titus 2:13", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["arianism"] },

  // Trinity
  { referenceChirho: "Matthew 3:16-17", doctrinalCategoryChirho: "trinity", relevantHeresiesChirho: ["modalism", "patripassianism"] },
  { referenceChirho: "Matthew 28:19", doctrinalCategoryChirho: "trinity", relevantHeresiesChirho: ["modalism"] },
  { referenceChirho: "2 Corinthians 13:14", doctrinalCategoryChirho: "trinity", relevantHeresiesChirho: ["modalism"] },
  { referenceChirho: "John 14:16-17", doctrinalCategoryChirho: "trinity", relevantHeresiesChirho: ["modalism"] },
  { referenceChirho: "John 17:1-5", doctrinalCategoryChirho: "trinity", relevantHeresiesChirho: ["modalism", "patripassianism"] },

  // Incarnation / Two Natures
  { referenceChirho: "John 1:14", doctrinalCategoryChirho: "incarnation", relevantHeresiesChirho: ["docetism", "gnosticism"] },
  { referenceChirho: "1 John 4:1-6", doctrinalCategoryChirho: "incarnation", relevantHeresiesChirho: ["docetism", "gnosticism"] },
  { referenceChirho: "Hebrews 2:14-18", doctrinalCategoryChirho: "incarnation", relevantHeresiesChirho: ["docetism", "apollinarianism"] },
  { referenceChirho: "Luke 2:52", doctrinalCategoryChirho: "incarnation", relevantHeresiesChirho: ["apollinarianism"] },
  { referenceChirho: "Luke 24:39", doctrinalCategoryChirho: "incarnation", relevantHeresiesChirho: ["docetism"] },
  { referenceChirho: "Hebrews 4:15", doctrinalCategoryChirho: "incarnation", relevantHeresiesChirho: ["docetism", "apollinarianism"] },

  // Two wills of Christ
  { referenceChirho: "Luke 22:42", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["monothelitism"] },
  { referenceChirho: "Matthew 26:39", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["monothelitism"] },
  { referenceChirho: "John 6:38", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["monothelitism"] },
  { referenceChirho: "John 5:30", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["monothelitism"] },

  // Theotokos / Unity of Christ's person
  { referenceChirho: "Luke 1:35", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["nestorianism"] },
  { referenceChirho: "Luke 1:43", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["nestorianism"] },
  { referenceChirho: "Galatians 4:4", doctrinalCategoryChirho: "christology", relevantHeresiesChirho: ["nestorianism", "docetism"] },

  // Soteriology / Grace
  { referenceChirho: "Romans 3:23-28", doctrinalCategoryChirho: "soteriology", relevantHeresiesChirho: ["pelagianism", "semi_pelagianism"] },
  { referenceChirho: "Romans 5:12-19", doctrinalCategoryChirho: "soteriology", relevantHeresiesChirho: ["pelagianism"] },
  { referenceChirho: "Ephesians 2:1-10", doctrinalCategoryChirho: "soteriology", relevantHeresiesChirho: ["pelagianism", "semi_pelagianism"] },
  { referenceChirho: "John 6:44", doctrinalCategoryChirho: "soteriology", relevantHeresiesChirho: ["semi_pelagianism"] },
  { referenceChirho: "John 6:65", doctrinalCategoryChirho: "soteriology", relevantHeresiesChirho: ["semi_pelagianism"] },
  { referenceChirho: "Philippians 1:29", doctrinalCategoryChirho: "soteriology", relevantHeresiesChirho: ["semi_pelagianism"] },
  { referenceChirho: "Psalm 51:5", doctrinalCategoryChirho: "soteriology", relevantHeresiesChirho: ["pelagianism"] },

  // OT/NT unity (contra Marcionism)
  { referenceChirho: "Matthew 5:17-20", doctrinalCategoryChirho: "theology_proper", relevantHeresiesChirho: ["marcionism"] },
  { referenceChirho: "Luke 24:27", doctrinalCategoryChirho: "theology_proper", relevantHeresiesChirho: ["marcionism"] },
  { referenceChirho: "Luke 24:44", doctrinalCategoryChirho: "theology_proper", relevantHeresiesChirho: ["marcionism"] },
  { referenceChirho: "2 Timothy 3:16-17", doctrinalCategoryChirho: "theology_proper", relevantHeresiesChirho: ["marcionism"] },
  { referenceChirho: "Hebrews 1:1-2", doctrinalCategoryChirho: "theology_proper", relevantHeresiesChirho: ["marcionism"] },
  { referenceChirho: "Acts 17:24-28", doctrinalCategoryChirho: "theology_proper", relevantHeresiesChirho: ["marcionism", "gnosticism"] },

  // Creation / Goodness of material world (contra Gnosticism)
  { referenceChirho: "Genesis 1:31", doctrinalCategoryChirho: "creation", relevantHeresiesChirho: ["gnosticism", "marcionism"] },
  { referenceChirho: "1 Timothy 4:1-5", doctrinalCategoryChirho: "creation", relevantHeresiesChirho: ["gnosticism"] },
  { referenceChirho: "Romans 8:19-23", doctrinalCategoryChirho: "creation", relevantHeresiesChirho: ["gnosticism"] },
];

interface BibleApiResponseChirho {
  reference: string;
  verses: Array<{
    book_id: string;
    book_name: string;
    chapter: number;
    verse: number;
    text: string;
  }>;
  text: string;
  translation_id: string;
  translation_name: string;
  translation_note: string;
}

async function fetchPassageChirho(
  referenceChirho: string
): Promise<string> {
  const encodedRefChirho = encodeURIComponent(referenceChirho);
  const urlChirho = `${BIBLE_API_URL_CHIRHO}/${encodedRefChirho}?translation=web`;

  const responseChirho = await fetch(urlChirho);
  if (!responseChirho.ok) {
    throw new Error(
      `Failed to fetch ${referenceChirho}: ${responseChirho.status}`
    );
  }

  const dataChirho = (await responseChirho.json()) as BibleApiResponseChirho;
  return dataChirho.text.trim();
}

async function mainChirho(): Promise<void> {
  console.log("📖 Gathering scripture passages from bible-api.com (WEB translation)...\n");

  await mkdir(OUTPUT_DIR_CHIRHO, { recursive: true });

  const passagesChirho: ScripturePassageChirho[] = [];
  let successCountChirho = 0;
  let failCountChirho = 0;

  for (const passageInfoChirho of PASSAGES_TO_FETCH_CHIRHO) {
    try {
      console.log(`  Fetching: ${passageInfoChirho.referenceChirho}...`);
      const textChirho = await fetchPassageChirho(passageInfoChirho.referenceChirho);

      passagesChirho.push({
        referenceChirho: passageInfoChirho.referenceChirho,
        textChirho,
        doctrinalCategoryChirho: passageInfoChirho.doctrinalCategoryChirho,
        relevantHeresiesChirho: passageInfoChirho.relevantHeresiesChirho,
      });
      successCountChirho++;

      // Delay to avoid rate limiting (bible-api.com has strict limits)
      await new Promise((rChirho) => setTimeout(rChirho, 1500));
    } catch (errorChirho) {
      console.error(`  ❌ Failed: ${passageInfoChirho.referenceChirho} - ${errorChirho}`);
      failCountChirho++;
    }
  }

  const outputChirho = {
    metadataChirho: {
      generatedAtChirho: new Date().toISOString(),
      translationChirho: "World English Bible (WEB) - Public Domain",
      totalPassagesChirho: passagesChirho.length,
      failedChirho: failCountChirho,
      categoriesChirho: [
        ...new Set(passagesChirho.map((pChirho) => pChirho.doctrinalCategoryChirho)),
      ],
    },
    passagesChirho,
  };

  const outputPathChirho = `${OUTPUT_DIR_CHIRHO}scripture-chirho.json`;
  await writeFile(outputPathChirho, JSON.stringify(outputChirho, null, 2), "utf-8");

  console.log(`\n✅ Written ${successCountChirho} passages to ${outputPathChirho}`);
  if (failCountChirho > 0) {
    console.log(`⚠️  ${failCountChirho} passages failed to fetch`);
  }

  // Category summary
  const categorySummaryChirho: Record<string, number> = {};
  for (const pChirho of passagesChirho) {
    categorySummaryChirho[pChirho.doctrinalCategoryChirho] =
      (categorySummaryChirho[pChirho.doctrinalCategoryChirho] || 0) + 1;
  }
  console.log("\nPassages by category:");
  for (const [catChirho, countChirho] of Object.entries(categorySummaryChirho)) {
    console.log(`  ${catChirho}: ${countChirho}`);
  }
}

mainChirho();
