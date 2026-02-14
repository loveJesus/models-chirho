// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-kjv-chirho.ts
 * Downloads KJV Bible text from ScrollMapper bible_databases (CSV format).
 * Parses into a structured JSON with book/chapter/verse/text for NER annotation.
 *
 * Source: https://github.com/scrollmapper/bible_databases (Public Domain)
 * Format: "Book","Chapter","Verse","Text" (with numeric book IDs that need mapping)
 */

import { writeFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;
const OUTPUT_FILE_CHIRHO = `${RAW_DIR_CHIRHO}kjv-chirho.json`;

const KJV_URL_CHIRHO =
  "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/csv/KJV.csv";

interface VerseChirho {
  bookIdChirho: number;
  bookNameChirho: string;
  chapterChirho: number;
  verseChirho: number;
  textChirho: string;
  referenceChirho: string;
}

/**
 * Maps numeric book IDs (1-66) to canonical book names.
 */
const BOOK_NAMES_CHIRHO: Record<number, string> = {
  1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers", 5: "Deuteronomy",
  6: "Joshua", 7: "Judges", 8: "Ruth", 9: "1 Samuel", 10: "2 Samuel",
  11: "1 Kings", 12: "2 Kings", 13: "1 Chronicles", 14: "2 Chronicles",
  15: "Ezra", 16: "Nehemiah", 17: "Esther", 18: "Job", 19: "Psalms",
  20: "Proverbs", 21: "Ecclesiastes", 22: "Song of Solomon", 23: "Isaiah",
  24: "Jeremiah", 25: "Lamentations", 26: "Ezekiel", 27: "Daniel",
  28: "Hosea", 29: "Joel", 30: "Amos", 31: "Obadiah", 32: "Jonah",
  33: "Micah", 34: "Nahum", 35: "Habakkuk", 36: "Zephaniah", 37: "Haggai",
  38: "Zechariah", 39: "Malachi",
  40: "Matthew", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts",
  45: "Romans", 46: "1 Corinthians", 47: "2 Corinthians", 48: "Galatians",
  49: "Ephesians", 50: "Philippians", 51: "Colossians", 52: "1 Thessalonians",
  53: "2 Thessalonians", 54: "1 Timothy", 55: "2 Timothy", 56: "Titus",
  57: "Philemon", 58: "Hebrews", 59: "James", 60: "1 Peter", 61: "2 Peter",
  62: "1 John", 63: "2 John", 64: "3 John", 65: "Jude", 66: "Revelation",
};

/**
 * Short book name abbreviations used in cross-referencing with TIPNR data.
 */
const BOOK_ABBREVIATIONS_CHIRHO: Record<number, string> = {
  1: "Gen", 2: "Exo", 3: "Lev", 4: "Num", 5: "Deu",
  6: "Jos", 7: "Jdg", 8: "Rut", 9: "1Sa", 10: "2Sa",
  11: "1Ki", 12: "2Ki", 13: "1Ch", 14: "2Ch",
  15: "Ezr", 16: "Neh", 17: "Est", 18: "Job", 19: "Psa",
  20: "Pro", 21: "Ecc", 22: "Sng", 23: "Isa",
  24: "Jer", 25: "Lam", 26: "Eze", 27: "Dan",
  28: "Hos", 29: "Joe", 30: "Amo", 31: "Oba", 32: "Jon",
  33: "Mic", 34: "Nah", 35: "Hab", 36: "Zep", 37: "Hag",
  38: "Zec", 39: "Mal",
  40: "Mat", 41: "Mar", 42: "Luk", 43: "Joh", 44: "Act",
  45: "Rom", 46: "1Co", 47: "2Co", 48: "Gal",
  49: "Eph", 50: "Phi", 51: "Col", 52: "1Th",
  53: "2Th", 54: "1Ti", 55: "2Ti", 56: "Tit",
  57: "Phm", 58: "Heb", 59: "Jam", 60: "1Pe", 61: "2Pe",
  62: "1Jn", 63: "2Jn", 64: "3Jn", 65: "Jud", 66: "Rev",
};

/**
 * Parse a CSV line handling quoted fields.
 * ScrollMapper CSV uses: "Book","Chapter","Verse","Text"
 * where Text may contain commas and double-quotes (escaped as "").
 */
function parseCsvLineChirho(lineChirho: string): string[] {
  const fieldsChirho: string[] = [];
  let currentFieldChirho = "";
  let insideQuotesChirho = false;
  let iChirho = 0;

  while (iChirho < lineChirho.length) {
    const charChirho = lineChirho[iChirho];

    if (insideQuotesChirho) {
      if (charChirho === '"') {
        // Check for escaped quote ("")
        if (iChirho + 1 < lineChirho.length && lineChirho[iChirho + 1] === '"') {
          currentFieldChirho += '"';
          iChirho += 2;
          continue;
        } else {
          // End of quoted field
          insideQuotesChirho = false;
          iChirho++;
          continue;
        }
      } else {
        currentFieldChirho += charChirho;
      }
    } else {
      if (charChirho === '"') {
        insideQuotesChirho = true;
      } else if (charChirho === ",") {
        fieldsChirho.push(currentFieldChirho);
        currentFieldChirho = "";
      } else {
        currentFieldChirho += charChirho;
      }
    }

    iChirho++;
  }

  // Push last field
  fieldsChirho.push(currentFieldChirho);

  return fieldsChirho;
}

/**
 * Build a reverse lookup from book name -> numeric book ID.
 */
const BOOK_NAME_TO_ID_CHIRHO: Record<string, number> = {};
for (const [idStrChirho, nameChirho] of Object.entries(BOOK_NAMES_CHIRHO)) {
  BOOK_NAME_TO_ID_CHIRHO[nameChirho.toLowerCase()] = parseInt(idStrChirho, 10);
}
// Also add common alternate spellings and CSV variants
BOOK_NAME_TO_ID_CHIRHO["psalm"] = 19;
BOOK_NAME_TO_ID_CHIRHO["song of songs"] = 22;
BOOK_NAME_TO_ID_CHIRHO["revelation of john"] = 66;
// Roman numeral variants used in ScrollMapper CSV
BOOK_NAME_TO_ID_CHIRHO["i samuel"] = 9;
BOOK_NAME_TO_ID_CHIRHO["ii samuel"] = 10;
BOOK_NAME_TO_ID_CHIRHO["i kings"] = 11;
BOOK_NAME_TO_ID_CHIRHO["ii kings"] = 12;
BOOK_NAME_TO_ID_CHIRHO["i chronicles"] = 13;
BOOK_NAME_TO_ID_CHIRHO["ii chronicles"] = 14;
BOOK_NAME_TO_ID_CHIRHO["i corinthians"] = 46;
BOOK_NAME_TO_ID_CHIRHO["ii corinthians"] = 47;
BOOK_NAME_TO_ID_CHIRHO["i thessalonians"] = 52;
BOOK_NAME_TO_ID_CHIRHO["ii thessalonians"] = 53;
BOOK_NAME_TO_ID_CHIRHO["i timothy"] = 54;
BOOK_NAME_TO_ID_CHIRHO["ii timothy"] = 55;
BOOK_NAME_TO_ID_CHIRHO["i peter"] = 60;
BOOK_NAME_TO_ID_CHIRHO["ii peter"] = 61;
BOOK_NAME_TO_ID_CHIRHO["i john"] = 62;
BOOK_NAME_TO_ID_CHIRHO["ii john"] = 63;
BOOK_NAME_TO_ID_CHIRHO["iii john"] = 64;

/**
 * Parse the full KJV CSV content into structured verse objects.
 * Handles both numeric book IDs and book name strings in the first column.
 */
function parseKjvContentChirho(contentChirho: string): VerseChirho[] {
  const linesChirho = contentChirho.split("\n");
  const versesChirho: VerseChirho[] = [];

  for (let iChirho = 0; iChirho < linesChirho.length; iChirho++) {
    const lineChirho = linesChirho[iChirho].trim();
    if (!lineChirho) continue;

    const fieldsChirho = parseCsvLineChirho(lineChirho);
    if (fieldsChirho.length < 4) continue;

    const chapterChirho = parseInt(fieldsChirho[1], 10);
    const verseNumChirho = parseInt(fieldsChirho[2], 10);
    const textChirho = fieldsChirho.slice(3).join(",").trim();

    // Skip header row or invalid entries
    if (isNaN(chapterChirho) || isNaN(verseNumChirho)) {
      continue;
    }

    // Determine book ID: first try numeric, then try name lookup
    let bookIdChirho = parseInt(fieldsChirho[0], 10);
    let bookNameChirho: string;

    if (!isNaN(bookIdChirho)) {
      // Numeric book ID format
      bookNameChirho = BOOK_NAMES_CHIRHO[bookIdChirho] || `Book${bookIdChirho}`;
    } else {
      // Book name string format (e.g., "Genesis")
      const rawNameChirho = fieldsChirho[0].trim();
      const lookupKeyChirho = rawNameChirho.toLowerCase();
      bookIdChirho = BOOK_NAME_TO_ID_CHIRHO[lookupKeyChirho] ?? -1;
      bookNameChirho = bookIdChirho > 0
        ? (BOOK_NAMES_CHIRHO[bookIdChirho] || rawNameChirho)
        : rawNameChirho;

      if (bookIdChirho < 0) {
        // Unknown book name, skip
        continue;
      }
    }

    const abbreviationChirho = BOOK_ABBREVIATIONS_CHIRHO[bookIdChirho] || `B${bookIdChirho}`;
    const referenceChirho = `${abbreviationChirho} ${chapterChirho}:${verseNumChirho}`;

    versesChirho.push({
      bookIdChirho,
      bookNameChirho,
      chapterChirho,
      verseChirho: verseNumChirho,
      textChirho,
      referenceChirho,
    });
  }

  return versesChirho;
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
  console.log("KJV Bible Downloader");
  console.log("====================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  // Check if already downloaded
  if (await fileExistsChirho(OUTPUT_FILE_CHIRHO)) {
    console.log(`  KJV data already exists at ${OUTPUT_FILE_CHIRHO}`);
    console.log("  Delete file to re-download.\n");
    return;
  }

  // Download
  console.log(`  Downloading KJV from ScrollMapper...`);
  const responseChirho = await fetch(KJV_URL_CHIRHO, {
    headers: { "User-Agent": "biblical-entity-recognizer-chirho/1.0" },
  });

  if (!responseChirho.ok) {
    throw new Error(`Download failed: ${responseChirho.status} ${responseChirho.statusText}`);
  }

  const rawContentChirho = await responseChirho.text();
  const rawSizeMbChirho = (Buffer.byteLength(rawContentChirho) / 1024 / 1024).toFixed(1);
  console.log(`  Downloaded ${rawSizeMbChirho} MB of KJV data`);

  // Also save the raw CSV
  const rawCsvPathChirho = `${RAW_DIR_CHIRHO}kjv-raw-chirho.csv`;
  await writeFile(rawCsvPathChirho, rawContentChirho, "utf-8");
  console.log(`  Raw CSV saved to ${rawCsvPathChirho}`);

  // Parse
  console.log("\n  Parsing KJV verses...");
  const versesChirho = parseKjvContentChirho(rawContentChirho);
  console.log(`  Parsed ${versesChirho.length} verses`);

  // Book distribution
  const bookCountsChirho: Record<string, number> = {};
  for (const verseChirho of versesChirho) {
    bookCountsChirho[verseChirho.bookNameChirho] =
      (bookCountsChirho[verseChirho.bookNameChirho] || 0) + 1;
  }
  const totalBooksChirho = Object.keys(bookCountsChirho).length;
  console.log(`  Total books: ${totalBooksChirho}`);

  // Testament split
  const otVersesChirho = versesChirho.filter((vChirho) => vChirho.bookIdChirho <= 39).length;
  const ntVersesChirho = versesChirho.filter((vChirho) => vChirho.bookIdChirho >= 40).length;
  console.log(`  OT verses: ${otVersesChirho}`);
  console.log(`  NT verses: ${ntVersesChirho}`);

  // Save parsed output
  const outputDataChirho = {
    metadataChirho: {
      generatedAtChirho: new Date().toISOString(),
      sourceChirho: "ScrollMapper bible_databases (Public Domain)",
      translationChirho: "King James Version (KJV)",
      totalVersesChirho: versesChirho.length,
      totalBooksChirho,
      otVersesChirho,
      ntVersesChirho,
    },
    versesChirho,
    bookNamesChirho: BOOK_NAMES_CHIRHO,
    bookAbbreviationsChirho: BOOK_ABBREVIATIONS_CHIRHO,
  };

  await writeFile(OUTPUT_FILE_CHIRHO, JSON.stringify(outputDataChirho, null, 2), "utf-8");
  console.log(`\n  Parsed verses saved to ${OUTPUT_FILE_CHIRHO}`);

  // Show samples
  console.log("\n  Sample verses:");
  const sampleIndicesChirho = [0, 100, 500, 15000, 25000, versesChirho.length - 1];
  for (const idxChirho of sampleIndicesChirho) {
    if (idxChirho < versesChirho.length) {
      const vChirho = versesChirho[idxChirho];
      console.log(
        `    [${idxChirho}] ${vChirho.bookNameChirho} ${vChirho.chapterChirho}:${vChirho.verseChirho}: ${vChirho.textChirho.slice(0, 80)}...`
      );
    }
  }

  console.log("\nDone!");
}

mainChirho();
