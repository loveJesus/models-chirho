// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-kjv-chirho.ts
 * Downloads all 66 KJV Bible book JSON files from aruljohn/Bible-kjv (MIT licensed).
 * Outputs a single kjv-chirho.json with all 31,102 verses.
 */

import { writeFile, readFile, mkdir } from "fs/promises";

const RAW_DIR_CHIRHO = `${process.cwd()}/data-chirho/raw-chirho/`;
const OUTPUT_PATH_CHIRHO = `${RAW_DIR_CHIRHO}kjv-chirho.json`;

// GitHub raw content base for aruljohn/Bible-kjv
const GITHUB_BASE_CHIRHO = "https://raw.githubusercontent.com/aruljohn/Bible-kjv/master";

// All 66 books with their file names
const BOOKS_CHIRHO = [
  "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
  "Joshua", "Judges", "Ruth", "1Samuel", "2Samuel",
  "1Kings", "2Kings", "1Chronicles", "2Chronicles",
  "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
  "Ecclesiastes", "SongofSolomon", "Isaiah", "Jeremiah", "Lamentations",
  "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah",
  "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
  "Haggai", "Zechariah", "Malachi",
  "Matthew", "Mark", "Luke", "John", "Acts",
  "Romans", "1Corinthians", "2Corinthians", "Galatians", "Ephesians",
  "Philippians", "Colossians", "1Thessalonians", "2Thessalonians",
  "1Timothy", "2Timothy", "Titus", "Philemon",
  "Hebrews", "James", "1Peter", "2Peter", "1John", "2John", "3John",
  "Jude", "Revelation",
];

// Map from GitHub filenames to OSIS-style book abbreviations for verse IDs
const OSIS_MAP_CHIRHO: Record<string, string> = {
  "Genesis": "Gen", "Exodus": "Exod", "Leviticus": "Lev", "Numbers": "Num",
  "Deuteronomy": "Deut", "Joshua": "Josh", "Judges": "Judg", "Ruth": "Ruth",
  "1Samuel": "1Sam", "2Samuel": "2Sam", "1Kings": "1Kgs", "2Kings": "2Kgs",
  "1Chronicles": "1Chr", "2Chronicles": "2Chr", "Ezra": "Ezra", "Nehemiah": "Neh",
  "Esther": "Esth", "Job": "Job", "Psalms": "Ps", "Proverbs": "Prov",
  "Ecclesiastes": "Eccl", "SongofSolomon": "Song", "Isaiah": "Isa",
  "Jeremiah": "Jer", "Lamentations": "Lam", "Ezekiel": "Ezek", "Daniel": "Dan",
  "Hosea": "Hos", "Joel": "Joel", "Amos": "Amos", "Obadiah": "Obad",
  "Jonah": "Jonah", "Micah": "Mic", "Nahum": "Nah", "Habakkuk": "Hab",
  "Zephaniah": "Zeph", "Haggai": "Hag", "Zechariah": "Zech", "Malachi": "Mal",
  "Matthew": "Matt", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts",
  "Romans": "Rom", "1Corinthians": "1Cor", "2Corinthians": "2Cor",
  "Galatians": "Gal", "Ephesians": "Eph", "Philippians": "Phil",
  "Colossians": "Col", "1Thessalonians": "1Thess", "2Thessalonians": "2Thess",
  "1Timothy": "1Tim", "2Timothy": "2Tim", "Titus": "Titus", "Philemon": "Phlm",
  "Hebrews": "Heb", "James": "Jas", "1Peter": "1Pet", "2Peter": "2Pet",
  "1John": "1John", "2John": "2John", "3John": "3John",
  "Jude": "Jude", "Revelation": "Rev",
};

interface VerseChirho {
  verseIdChirho: string;  // OSIS format: Gen.1.1
  bookChirho: string;
  chapterChirho: number;
  verseNumChirho: number;
  textChirho: string;
}

async function downloadBookChirho(bookNameChirho: string): Promise<VerseChirho[]> {
  const urlChirho = `${GITHUB_BASE_CHIRHO}/${bookNameChirho}.json`;
  const responseChirho = await fetch(urlChirho);

  if (!responseChirho.ok) {
    throw new Error(`Failed to download ${bookNameChirho}: ${responseChirho.status}`);
  }

  const dataChirho = await responseChirho.json() as Record<string, unknown>;
  const versesChirho: VerseChirho[] = [];
  const osisBookChirho = OSIS_MAP_CHIRHO[bookNameChirho] || bookNameChirho;

  // The JSON structure is: { "book": "name", "chapters": [ { "chapter": 1, "verses": [ { "verse": 1, "text": "..." } ] } ] }
  // Or sometimes: { "chapters": [ [ { "verse": 1, "text": "..." } ] ] }
  const chaptersChirho = dataChirho.chapters as Array<Record<string, unknown>>;

  if (!chaptersChirho || !Array.isArray(chaptersChirho)) {
    console.warn(`  Warning: Unexpected format for ${bookNameChirho}`);
    return versesChirho;
  }

  for (let cIdxChirho = 0; cIdxChirho < chaptersChirho.length; cIdxChirho++) {
    const chapterDataChirho = chaptersChirho[cIdxChirho];
    const chapterNumChirho = cIdxChirho + 1;

    // Handle both array-of-objects and object-with-verses formats
    let versesArrayChirho: Array<Record<string, unknown>>;
    if (Array.isArray(chapterDataChirho)) {
      versesArrayChirho = chapterDataChirho as Array<Record<string, unknown>>;
    } else if (chapterDataChirho && typeof chapterDataChirho === "object" && "verses" in chapterDataChirho) {
      versesArrayChirho = (chapterDataChirho as { verses: Array<Record<string, unknown>> }).verses;
    } else {
      continue;
    }

    for (const verseDataChirho of versesArrayChirho) {
      const verseNumChirho = Number(verseDataChirho.verse ?? verseDataChirho.number ?? 0);
      const textChirho = String(verseDataChirho.text ?? "").trim();

      if (verseNumChirho && textChirho) {
        versesChirho.push({
          verseIdChirho: `${osisBookChirho}.${chapterNumChirho}.${verseNumChirho}`,
          bookChirho: osisBookChirho,
          chapterChirho: chapterNumChirho,
          verseNumChirho,
          textChirho,
        });
      }
    }
  }

  return versesChirho;
}

async function mainChirho(): Promise<void> {
  console.log("KJV Bible Downloader (aruljohn/Bible-kjv)");
  console.log("==========================================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  // Check if already downloaded
  try {
    const existingChirho = await readFile(OUTPUT_PATH_CHIRHO, "utf-8");
    const parsedChirho = JSON.parse(existingChirho);
    if (Array.isArray(parsedChirho) && parsedChirho.length > 30000) {
      console.log(`KJV already downloaded (${parsedChirho.length} verses). Skipping.`);
      return;
    }
  } catch {
    // Not downloaded yet
  }

  const allVersesChirho: VerseChirho[] = [];
  const CONCURRENCY_CHIRHO = 5;

  // Download in batches for parallelism
  for (let iChirho = 0; iChirho < BOOKS_CHIRHO.length; iChirho += CONCURRENCY_CHIRHO) {
    const batchChirho = BOOKS_CHIRHO.slice(iChirho, iChirho + CONCURRENCY_CHIRHO);
    const resultsChirho = await Promise.all(
      batchChirho.map(async (bookChirho) => {
        try {
          const versesChirho = await downloadBookChirho(bookChirho);
          console.log(`  ${bookChirho}: ${versesChirho.length} verses`);
          return versesChirho;
        } catch (errorChirho) {
          console.error(`  ${bookChirho}: FAILED - ${errorChirho}`);
          return [];
        }
      })
    );
    allVersesChirho.push(...resultsChirho.flat());
  }

  // Write output
  await writeFile(OUTPUT_PATH_CHIRHO, JSON.stringify(allVersesChirho, null, 0), "utf-8");

  console.log(`\nDownloaded ${allVersesChirho.length} verses from ${BOOKS_CHIRHO.length} books`);
  console.log(`Saved to: ${OUTPUT_PATH_CHIRHO}`);

  // Stats
  const booksCountChirho = new Set(allVersesChirho.map((vChirho) => vChirho.bookChirho)).size;
  console.log(`\nStats:`);
  console.log(`  Total verses: ${allVersesChirho.length}`);
  console.log(`  Unique books: ${booksCountChirho}`);
  console.log(`  Sample: ${allVersesChirho[0]?.verseIdChirho} = "${allVersesChirho[0]?.textChirho.substring(0, 60)}..."`);
}

mainChirho();
