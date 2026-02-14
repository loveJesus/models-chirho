// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * build-simplifier-dataset-chirho.ts
 * Builds dual-task training data for Flan-T5-small:
 *
 * Task 1: Difficulty Scoring (~64K examples)
 *   Input:  "rate difficulty: [verse text]"
 *   Output: "reading_level: [1-12] | vocab_complexity: [low/medium/high] | archaic_forms: [count] | difficulty: [easy/medium/hard]"
 *
 * Task 2: Simplification (~96K examples)
 *   Input:  "simplify: [complex verse text]"
 *   Output: "[simplified verse text]"
 *
 * Pairs complex translations (KJV, ASV, YLT, Darby) with simpler ones (BBE, OEB).
 * Split 80/10/10 by book to prevent verse-level leakage.
 *
 * Output: data-chirho/processed-chirho/{train,val,test}-simplifier-chirho.jsonl
 */

import { readFile, writeFile, mkdir } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;
const PROCESSED_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/processed-chirho/`;

// ─── Common word list (top ~3000 English words) ───
// We use a condensed set: if a word is NOT in this set, it counts as complex vocabulary.
// This is a representative sample of the 3000 most frequent English words.
const COMMON_WORDS_CHIRHO = new Set<string>([
  // Articles, pronouns, prepositions, conjunctions
  "a", "an", "the", "i", "me", "my", "mine", "we", "us", "our", "ours",
  "you", "your", "yours", "he", "him", "his", "she", "her", "hers",
  "it", "its", "they", "them", "their", "theirs", "this", "that", "these",
  "those", "who", "whom", "whose", "which", "what", "where", "when",
  "why", "how", "all", "each", "every", "both", "few", "more", "most",
  "other", "some", "such", "no", "not", "only", "own", "same", "so",
  "than", "too", "very", "just", "because", "but", "and", "or", "if",
  "while", "although", "though", "after", "before", "since", "until",
  "unless", "about", "above", "across", "against", "along", "among",
  "around", "at", "behind", "below", "beneath", "beside", "between",
  "beyond", "by", "down", "during", "except", "for", "from", "in",
  "inside", "into", "near", "of", "off", "on", "out", "outside",
  "over", "past", "through", "to", "toward", "under", "up", "upon",
  "with", "within", "without",
  // Common verbs
  "be", "am", "is", "are", "was", "were", "been", "being", "have",
  "has", "had", "having", "do", "does", "did", "doing", "will", "would",
  "shall", "should", "may", "might", "can", "could", "must", "need",
  "dare", "ought", "used", "go", "goes", "went", "gone", "going",
  "come", "came", "coming", "take", "took", "taken", "taking", "make",
  "made", "making", "know", "knew", "known", "knowing", "think",
  "thought", "thinking", "see", "saw", "seen", "seeing", "want",
  "wanted", "wanting", "give", "gave", "given", "giving", "say",
  "said", "saying", "tell", "told", "telling", "get", "got", "getting",
  "find", "found", "finding", "put", "putting", "set", "setting",
  "keep", "kept", "keeping", "let", "letting", "begin", "began",
  "begun", "beginning", "show", "showed", "shown", "showing", "hear",
  "heard", "hearing", "play", "played", "playing", "run", "ran",
  "running", "move", "moved", "moving", "live", "lived", "living",
  "believe", "believed", "call", "called", "calling", "try", "tried",
  "trying", "ask", "asked", "asking", "turn", "turned", "turning",
  "leave", "left", "leaving", "help", "helped", "helping", "talk",
  "talked", "talking", "walk", "walked", "walking", "stand", "stood",
  "standing", "sit", "sat", "sitting", "bring", "brought", "bringing",
  "hold", "held", "holding", "write", "wrote", "written", "writing",
  "read", "reading", "learn", "learned", "learning", "grow", "grew",
  "grown", "growing", "draw", "drew", "drawn", "drawing", "lead",
  "led", "leading", "feel", "felt", "feeling", "pay", "paid",
  "paying", "meet", "met", "meeting", "send", "sent", "sending",
  "fall", "fell", "fallen", "falling", "speak", "spoke", "spoken",
  "speaking", "raise", "raised", "raising", "fill", "filled",
  "filling", "open", "opened", "opening", "close", "closed", "closing",
  "stop", "stopped", "stopping", "eat", "ate", "eaten", "eating",
  "drink", "drank", "drunk", "drinking", "die", "died", "dying",
  "kill", "killed", "killing", "break", "broke", "broken", "breaking",
  "build", "built", "building", "carry", "carried", "carrying",
  "cut", "cutting", "reach", "reached", "reaching", "watch", "watched",
  "watching", "follow", "followed", "following", "love", "loved",
  "loving", "use", "used", "using", "work", "worked", "working",
  "look", "looked", "looking", "need", "needed", "pass", "passed",
  "passing", "wait", "waited", "waiting", "serve", "served", "serving",
  "appear", "appeared", "change", "changed", "answer", "answered",
  "continue", "continued", "happen", "happened", "start", "started",
  "remember", "fight", "fought", "fighting", "become", "became",
  "lose", "lost", "add", "added", "expect", "save", "saved", "offer",
  "fear", "feared", "remain", "remained", "allow", "allowed",
  "receive", "received", "seem", "seemed", "return", "returned",
  "cover", "covered", "cry", "cried", "enter", "entered", "stay",
  "stayed", "rise", "rose", "risen", "rising", "create", "created",
  "destroy", "destroyed", "burn", "burned", "teach", "taught",
  "thank", "praised", "praise", "pray", "prayed",
  // Common nouns
  "time", "year", "people", "way", "day", "man", "woman", "child",
  "children", "world", "life", "hand", "part", "place", "case",
  "week", "company", "system", "program", "question", "work", "number",
  "night", "point", "home", "water", "room", "mother", "area", "money",
  "story", "fact", "month", "lot", "right", "study", "book", "eye",
  "job", "word", "business", "issue", "side", "kind", "head", "house",
  "service", "friend", "father", "power", "hour", "game", "line",
  "end", "member", "law", "car", "city", "community", "name",
  "president", "team", "minute", "idea", "body", "information", "back",
  "parent", "face", "others", "level", "office", "door", "health",
  "person", "art", "war", "history", "party", "result", "change",
  "morning", "reason", "research", "girl", "guy", "moment", "air",
  "teacher", "force", "education", "boy", "age", "food", "son",
  "daughter", "brother", "sister", "king", "lord", "god", "land",
  "earth", "sea", "mountain", "fire", "light", "dark", "darkness",
  "heaven", "heart", "soul", "spirit", "blood", "bread", "wine",
  "stone", "gold", "silver", "iron", "wood", "tree", "fruit", "seed",
  "field", "garden", "river", "rock", "road", "gate", "wall", "city",
  "house", "temple", "church", "sword", "shield", "beast", "angel",
  "devil", "sin", "death", "grace", "faith", "hope", "joy", "peace",
  "truth", "glory", "mercy", "justice", "prayer", "sacrifice",
  "covenant", "promise", "nation", "tribe", "servant", "master",
  "prophet", "priest", "sheep", "lamb", "fish", "bird", "horse",
  "cattle", "ox", "well", "camp", "tent", "altar", "offering",
  "commandment", "law", "voice", "sign", "wonder", "crowd", "army",
  "battle", "victory", "judgment", "throne", "kingdom", "treasure",
  "gift", "wedding", "feast", "name", "morning", "evening", "night",
  "rest", "work", "strength", "wisdom", "knowledge", "fear", "anger",
  "love", "hate", "good", "evil", "holy", "clean", "wilderness",
  // Common adjectives
  "good", "new", "first", "last", "long", "great", "little", "own",
  "old", "right", "big", "high", "different", "small", "large",
  "next", "early", "young", "important", "public", "bad", "same",
  "able", "best", "better", "true", "free", "strong", "full",
  "sure", "clear", "close", "common", "hard", "poor", "real",
  "open", "late", "simple", "dead", "whole", "white", "black",
  "red", "blue", "green", "dark", "deep", "wide", "beautiful",
  "rich", "happy", "holy", "righteous", "wicked", "mighty", "faithful",
  "blessed", "eternal", "divine", "sacred", "pure", "humble", "gentle",
  // Common adverbs
  "not", "also", "very", "often", "however", "again", "once", "never",
  "always", "sometimes", "together", "likely", "simply", "generally",
  "instead", "actually", "already", "enough", "well", "still", "yet",
  "now", "then", "here", "there", "where", "when", "today",
  "tomorrow", "yesterday", "ever", "always", "forever", "above",
  "below", "away", "far", "near", "quickly", "slowly", "therefore",
  // Numbers and ordinals
  "one", "two", "three", "four", "five", "six", "seven", "eight",
  "nine", "ten", "hundred", "thousand", "second", "third",
]);

// ─── Archaic words to detect ───
const ARCHAIC_WORDS_CHIRHO = new Set<string>([
  "thee", "thou", "thy", "thine", "ye", "hath", "doth", "dost",
  "shalt", "wilt", "shouldst", "wouldst", "couldst", "didst",
  "hast", "art", "wert", "saith", "verily", "behold", "unto",
  "thereof", "therein", "thereto", "therewith", "thereof", "whereby",
  "wherein", "wherefore", "wherewith", "whither", "thither", "hither",
  "yea", "nay", "lo", "oft", "ere", "lest", "betwixt", "begat",
  "begotten", "cometh", "goeth", "maketh", "taketh", "giveth",
  "speaketh", "knoweth", "liveth", "loveth", "seeketh", "keepeth",
  "bringeth", "calleth", "findeth", "heareth", "leadeth", "passeth",
  "sendeth", "teacheth", "turneth", "walketh", "worketh", "wrought",
  "spake", "smote", "smite", "smitten", "slew", "brethren", "kinsmen",
  "damsel", "raiment", "apparel", "vesture", "bulwark", "buckler",
  "chariot", "manna", "sepulchre", "burneth", "knowest", "seest",
  "hearest", "sayest", "doest", "goest", "comest", "wast",
  "straightway", "forasmuch", "inasmuch", "peradventure", "howbeit",
  "notwithstanding", "hitherto", "aforetime", "aforementioned",
]);

// ─── Bible book names to identify them in CSV ───
const BIBLE_BOOKS_CHIRHO: string[] = [
  "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
  "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
  "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
  "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Psalm",
  "Proverbs", "Ecclesiastes", "Song of Solomon",
  "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel",
  "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah",
  "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
  "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
  "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
  "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
  "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
  "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
  "Jude", "Revelation",
];

// Book groupings for 80/10/10 split by book (deterministic)
const TRAIN_BOOKS_CHIRHO = new Set<string>([
  "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
  "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
  "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
  "Ezra", "Nehemiah", "Esther", "Job",
  "Proverbs", "Ecclesiastes", "Song of Solomon",
  "Isaiah", "Jeremiah", "Lamentations", "Ezekiel",
  "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah",
  "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
  "Matthew", "Mark", "Luke", "Acts", "Romans",
  "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
  "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
  "1 Timothy", "2 Timothy", "Titus", "Philemon",
  "James", "1 Peter", "2 Peter",
]);

const VAL_BOOKS_CHIRHO = new Set<string>([
  "Psalms", "Psalm", "Daniel", "John", "Hebrews",
  "1 John", "2 John", "3 John",
]);

const TEST_BOOKS_CHIRHO = new Set<string>([
  "Jude", "Revelation",
]);

interface VerseChirho {
  bookChirho: string;
  chapterChirho: number;
  verseNumChirho: number;
  textChirho: string;
  refChirho: string;
}

interface TrainingExampleChirho {
  inputChirho: string;
  targetChirho: string;
  taskChirho: string;
  refChirho: string;
  bookChirho: string;
}

// ─── CSV parser ───
function parseCsvLineChirho(lineChirho: string): string[] {
  const fieldsChirho: string[] = [];
  let currentChirho = "";
  let inQuotesChirho = false;

  for (let iChirho = 0; iChirho < lineChirho.length; iChirho++) {
    const charChirho = lineChirho[iChirho];
    if (charChirho === '"') {
      inQuotesChirho = !inQuotesChirho;
    } else if (charChirho === "," && !inQuotesChirho) {
      fieldsChirho.push(currentChirho.trim());
      currentChirho = "";
    } else {
      currentChirho += charChirho;
    }
  }
  fieldsChirho.push(currentChirho.trim());
  return fieldsChirho;
}

// ─── Load a translation ───
async function loadTranslationChirho(
  codeChirho: string
): Promise<Map<string, VerseChirho>> {
  const filePathChirho = `${RAW_DIR_CHIRHO}${codeChirho}-chirho.csv`;
  const contentChirho = await readFile(filePathChirho, "utf-8");
  const linesChirho = contentChirho.split("\n").filter((lChirho) => lChirho.trim());

  const versesChirho = new Map<string, VerseChirho>();

  for (const lineChirho of linesChirho) {
    const fieldsChirho = parseCsvLineChirho(lineChirho);
    if (fieldsChirho.length < 4) continue;

    const bookChirho = fieldsChirho[0]?.replace(/^"|"$/g, "").trim();
    const chapterStrChirho = fieldsChirho[1]?.trim();
    const verseStrChirho = fieldsChirho[2]?.trim();
    const textChirho = fieldsChirho[3]?.replace(/^"|"$/g, "").trim();

    // Skip header row
    if (
      bookChirho === "Book" ||
      !textChirho ||
      !chapterStrChirho ||
      isNaN(parseInt(chapterStrChirho))
    )
      continue;

    const chapterChirho = parseInt(chapterStrChirho);
    const verseNumChirho = parseInt(verseStrChirho);
    const refChirho = `${bookChirho}.${chapterChirho}.${verseNumChirho}`;

    versesChirho.set(refChirho, {
      bookChirho,
      chapterChirho,
      verseNumChirho,
      textChirho,
      refChirho,
    });
  }

  return versesChirho;
}

// ─── Difficulty scoring functions ───
function tokenizeChirho(textChirho: string): string[] {
  return textChirho
    .toLowerCase()
    .replace(/[^a-z\s'-]/g, "")
    .split(/\s+/)
    .filter((wChirho) => wChirho.length > 0);
}

function countSentencesChirho(textChirho: string): number {
  const sentenceEndingsChirho = textChirho.match(/[.!?;:]+/g);
  return Math.max(1, sentenceEndingsChirho ? sentenceEndingsChirho.length : 1);
}

function countArchaicChirho(wordsChirho: string[]): number {
  let countChirho = 0;
  for (const wordChirho of wordsChirho) {
    if (ARCHAIC_WORDS_CHIRHO.has(wordChirho)) {
      countChirho++;
    }
    // Also catch -eth, -est verb endings as archaic
    if (
      wordChirho.endsWith("eth") &&
      wordChirho.length > 4 &&
      !ARCHAIC_WORDS_CHIRHO.has(wordChirho)
    ) {
      countChirho++;
    }
    if (
      wordChirho.endsWith("est") &&
      wordChirho.length > 4 &&
      !COMMON_WORDS_CHIRHO.has(wordChirho)
    ) {
      countChirho++;
    }
  }
  return countChirho;
}

function computeVocabComplexityChirho(
  wordsChirho: string[]
): { ratioChirho: number; levelChirho: string } {
  if (wordsChirho.length === 0) return { ratioChirho: 0, levelChirho: "low" };

  let uncommonCountChirho = 0;
  for (const wordChirho of wordsChirho) {
    if (wordChirho.length <= 2) continue; // skip tiny words
    if (!COMMON_WORDS_CHIRHO.has(wordChirho)) {
      uncommonCountChirho++;
    }
  }

  const ratioChirho = uncommonCountChirho / wordsChirho.length;

  let levelChirho: string;
  if (ratioChirho < 0.15) {
    levelChirho = "low";
  } else if (ratioChirho < 0.35) {
    levelChirho = "medium";
  } else {
    levelChirho = "high";
  }

  return { ratioChirho, levelChirho };
}

function computeReadingLevelChirho(
  wordsChirho: string[],
  sentenceCountChirho: number,
  vocabRatioChirho: number,
  archaicCountChirho: number
): number {
  // Approximate Flesch-Kincaid grade level analog
  const avgWordLengthChirho =
    wordsChirho.reduce((sChirho, wChirho) => sChirho + wChirho.length, 0) /
    Math.max(1, wordsChirho.length);
  const wordsPerSentenceChirho = wordsChirho.length / sentenceCountChirho;

  // Base grade from word length and sentence length
  let gradeChirho = 0.39 * wordsPerSentenceChirho + 11.8 * (avgWordLengthChirho / 5) - 15.59;

  // Adjust for archaic vocabulary
  gradeChirho += archaicCountChirho * 0.5;

  // Adjust for uncommon vocabulary
  gradeChirho += vocabRatioChirho * 4;

  // Clamp to 1-12
  return Math.max(1, Math.min(12, Math.round(gradeChirho)));
}

function computeDifficultyLabelChirho(
  readingLevelChirho: number,
  vocabLevelChirho: string,
  archaicCountChirho: number
): string {
  let scoreChirho = 0;

  // Reading level contribution
  if (readingLevelChirho <= 4) scoreChirho += 0;
  else if (readingLevelChirho <= 7) scoreChirho += 1;
  else scoreChirho += 2;

  // Vocab complexity contribution
  if (vocabLevelChirho === "low") scoreChirho += 0;
  else if (vocabLevelChirho === "medium") scoreChirho += 1;
  else scoreChirho += 2;

  // Archaic forms contribution
  if (archaicCountChirho === 0) scoreChirho += 0;
  else if (archaicCountChirho <= 2) scoreChirho += 1;
  else scoreChirho += 2;

  if (scoreChirho <= 1) return "easy";
  if (scoreChirho <= 3) return "medium";
  return "hard";
}

function buildDifficultyExampleChirho(
  verseChirho: VerseChirho
): TrainingExampleChirho {
  const wordsChirho = tokenizeChirho(verseChirho.textChirho);
  const sentenceCountChirho = countSentencesChirho(verseChirho.textChirho);
  const archaicCountChirho = countArchaicChirho(wordsChirho);
  const { ratioChirho: vocabRatioChirho, levelChirho: vocabLevelChirho } =
    computeVocabComplexityChirho(wordsChirho);
  const readingLevelChirho = computeReadingLevelChirho(
    wordsChirho,
    sentenceCountChirho,
    vocabRatioChirho,
    archaicCountChirho
  );
  const difficultyChirho = computeDifficultyLabelChirho(
    readingLevelChirho,
    vocabLevelChirho,
    archaicCountChirho
  );

  const inputChirho = `rate difficulty: ${verseChirho.textChirho}`;
  const targetChirho =
    `reading_level: ${readingLevelChirho} | vocab_complexity: ${vocabLevelChirho} | archaic_forms: ${archaicCountChirho} | difficulty: ${difficultyChirho}`;

  return {
    inputChirho,
    targetChirho,
    taskChirho: "difficulty_scoring",
    refChirho: verseChirho.refChirho,
    bookChirho: verseChirho.bookChirho,
  };
}

// ─── Shuffle utility ───
function shuffleChirho<T>(arrChirho: T[]): T[] {
  const shuffledChirho = [...arrChirho];
  for (let iChirho = shuffledChirho.length - 1; iChirho > 0; iChirho--) {
    const jChirho = Math.floor(Math.random() * (iChirho + 1));
    [shuffledChirho[iChirho], shuffledChirho[jChirho]] = [
      shuffledChirho[jChirho],
      shuffledChirho[iChirho],
    ];
  }
  return shuffledChirho;
}

// ─── Simplification pairs ───
const SIMPLIFICATION_PAIRS_CHIRHO: Array<{
  complexChirho: string;
  simpleChirho: string;
  labelChirho: string;
}> = [
  { complexChirho: "kjv", simpleChirho: "bbe", labelChirho: "KJV->BBE" },
  { complexChirho: "kjv", simpleChirho: "oeb", labelChirho: "KJV->OEB" },
  { complexChirho: "asv", simpleChirho: "bbe", labelChirho: "ASV->BBE" },
  { complexChirho: "ylt", simpleChirho: "oeb", labelChirho: "YLT->OEB" },
];

// ─── Main ───
async function mainChirho(): Promise<void> {
  console.log("Dual-Task Simplifier Dataset Builder");
  console.log("=====================================\n");

  await mkdir(PROCESSED_DIR_CHIRHO, { recursive: true });

  // Load all translations
  console.log("Loading translations...");
  const translationsChirho = new Map<string, Map<string, VerseChirho>>();

  const codesToLoadChirho = ["kjv", "bbe", "oeb", "asv", "ylt", "darby"];
  for (const codeChirho of codesToLoadChirho) {
    try {
      const versesChirho = await loadTranslationChirho(codeChirho);
      translationsChirho.set(codeChirho, versesChirho);
      console.log(`  ${codeChirho.toUpperCase()}: ${versesChirho.size} verses`);
    } catch (errorChirho) {
      console.error(`  Failed to load ${codeChirho}: ${errorChirho}`);
    }
  }

  // ─── Task 1: Difficulty Scoring ───
  console.log("\n--- Task 1: Difficulty Scoring ---");

  const difficultyExamplesChirho: TrainingExampleChirho[] = [];

  // Generate difficulty examples from all translations
  const difficultySourcesChirho = ["kjv", "bbe", "oeb", "asv", "ylt", "darby"];
  const seenRefsForDifficultyChirho = new Set<string>();

  for (const codeChirho of difficultySourcesChirho) {
    const transChirho = translationsChirho.get(codeChirho);
    if (!transChirho) continue;

    for (const [refChirho, verseChirho] of transChirho) {
      // Unique by translation+ref to get variety
      const uniqueKeyChirho = `${codeChirho}:${refChirho}`;
      if (seenRefsForDifficultyChirho.has(uniqueKeyChirho)) continue;
      seenRefsForDifficultyChirho.add(uniqueKeyChirho);

      // Skip very short verses
      if (verseChirho.textChirho.length < 15) continue;

      difficultyExamplesChirho.push(buildDifficultyExampleChirho(verseChirho));
    }
  }

  // Cap difficulty examples at ~64K, shuffled
  const TARGET_DIFFICULTY_CHIRHO = 64000;
  let finalDifficultyChirho = shuffleChirho(difficultyExamplesChirho);
  if (finalDifficultyChirho.length > TARGET_DIFFICULTY_CHIRHO) {
    finalDifficultyChirho = finalDifficultyChirho.slice(0, TARGET_DIFFICULTY_CHIRHO);
  }

  console.log(`  Generated: ${difficultyExamplesChirho.length} total difficulty examples`);
  console.log(`  Capped to: ${finalDifficultyChirho.length}`);

  // Show distribution
  const diffDistChirho: Record<string, number> = { easy: 0, medium: 0, hard: 0 };
  for (const exChirho of finalDifficultyChirho) {
    const matchChirho = exChirho.targetChirho.match(/difficulty: (\w+)/);
    if (matchChirho) {
      diffDistChirho[matchChirho[1]] = (diffDistChirho[matchChirho[1]] || 0) + 1;
    }
  }
  console.log(`  Distribution: easy=${diffDistChirho.easy}, medium=${diffDistChirho.medium}, hard=${diffDistChirho.hard}`);

  // ─── Task 2: Simplification ───
  console.log("\n--- Task 2: Simplification ---");

  const simplificationExamplesChirho: TrainingExampleChirho[] = [];

  for (const pairChirho of SIMPLIFICATION_PAIRS_CHIRHO) {
    const complexTransChirho = translationsChirho.get(pairChirho.complexChirho);
    const simpleTransChirho = translationsChirho.get(pairChirho.simpleChirho);

    if (!complexTransChirho || !simpleTransChirho) {
      console.log(`  Skipping ${pairChirho.labelChirho}: translation not loaded`);
      continue;
    }

    let pairCountChirho = 0;

    for (const [refChirho, complexVerseChirho] of complexTransChirho) {
      const simpleVerseChirho = simpleTransChirho.get(refChirho);
      if (!simpleVerseChirho) continue;

      // Skip very short verses
      if (complexVerseChirho.textChirho.length < 15 || simpleVerseChirho.textChirho.length < 10)
        continue;

      // Skip if texts are identical (no simplification needed)
      if (
        complexVerseChirho.textChirho.toLowerCase().trim() ===
        simpleVerseChirho.textChirho.toLowerCase().trim()
      )
        continue;

      simplificationExamplesChirho.push({
        inputChirho: `simplify: ${complexVerseChirho.textChirho}`,
        targetChirho: simpleVerseChirho.textChirho,
        taskChirho: "simplification",
        refChirho,
        bookChirho: complexVerseChirho.bookChirho,
      });

      pairCountChirho++;
    }

    console.log(`  ${pairChirho.labelChirho}: ${pairCountChirho} pairs`);
  }

  // Cap simplification examples at ~96K
  const TARGET_SIMPLIFICATION_CHIRHO = 96000;
  let finalSimplificationChirho = shuffleChirho(simplificationExamplesChirho);
  if (finalSimplificationChirho.length > TARGET_SIMPLIFICATION_CHIRHO) {
    finalSimplificationChirho = finalSimplificationChirho.slice(0, TARGET_SIMPLIFICATION_CHIRHO);
  }

  console.log(`  Total simplification examples: ${simplificationExamplesChirho.length}`);
  console.log(`  Capped to: ${finalSimplificationChirho.length}`);

  // ─── Combine and split by book ───
  console.log("\n--- Combining and splitting by book ---");

  const allExamplesChirho = [...finalDifficultyChirho, ...finalSimplificationChirho];
  console.log(`  Total combined examples: ${allExamplesChirho.length}`);

  const trainExamplesChirho: TrainingExampleChirho[] = [];
  const valExamplesChirho: TrainingExampleChirho[] = [];
  const testExamplesChirho: TrainingExampleChirho[] = [];

  for (const exChirho of allExamplesChirho) {
    const bookChirho = exChirho.bookChirho;
    if (VAL_BOOKS_CHIRHO.has(bookChirho)) {
      valExamplesChirho.push(exChirho);
    } else if (TEST_BOOKS_CHIRHO.has(bookChirho)) {
      testExamplesChirho.push(exChirho);
    } else {
      // Default to train (includes TRAIN_BOOKS_CHIRHO and any unrecognized books)
      trainExamplesChirho.push(exChirho);
    }
  }

  // Shuffle each split
  const trainShuffledChirho = shuffleChirho(trainExamplesChirho);
  const valShuffledChirho = shuffleChirho(valExamplesChirho);
  const testShuffledChirho = shuffleChirho(testExamplesChirho);

  // ─── Write JSONL ───
  const writeJsonlChirho = async (
    dataChirho: TrainingExampleChirho[],
    fileNameChirho: string
  ) => {
    const outputChirho = dataChirho
      .map((exChirho) =>
        JSON.stringify({
          input_chirho: exChirho.inputChirho,
          target_chirho: exChirho.targetChirho,
          task_chirho: exChirho.taskChirho,
          ref_chirho: exChirho.refChirho,
        })
      )
      .join("\n");
    const pathChirho = `${PROCESSED_DIR_CHIRHO}${fileNameChirho}`;
    await writeFile(pathChirho, outputChirho, "utf-8");
    console.log(`  Wrote ${fileNameChirho}: ${dataChirho.length} examples`);
  };

  console.log("\n--- Writing dataset splits ---");
  await writeJsonlChirho(trainShuffledChirho, "train-simplifier-chirho.jsonl");
  await writeJsonlChirho(valShuffledChirho, "val-simplifier-chirho.jsonl");
  await writeJsonlChirho(testShuffledChirho, "test-simplifier-chirho.jsonl");

  // ─── Summary ───
  const countTaskChirho = (dataChirho: TrainingExampleChirho[], taskChirho: string) =>
    dataChirho.filter((eChirho) => eChirho.taskChirho === taskChirho).length;

  console.log("\n=====================================");
  console.log("Dataset Summary:");
  console.log(`  Total examples: ${allExamplesChirho.length}`);
  console.log(
    `  Train: ${trainShuffledChirho.length} (difficulty: ${countTaskChirho(trainShuffledChirho, "difficulty_scoring")}, simplification: ${countTaskChirho(trainShuffledChirho, "simplification")})`
  );
  console.log(
    `  Val: ${valShuffledChirho.length} (difficulty: ${countTaskChirho(valShuffledChirho, "difficulty_scoring")}, simplification: ${countTaskChirho(valShuffledChirho, "simplification")})`
  );
  console.log(
    `  Test: ${testShuffledChirho.length} (difficulty: ${countTaskChirho(testShuffledChirho, "difficulty_scoring")}, simplification: ${countTaskChirho(testShuffledChirho, "simplification")})`
  );
  console.log(`  Split method: by book (train=${TRAIN_BOOKS_CHIRHO.size} books, val=${VAL_BOOKS_CHIRHO.size} books, test=${TEST_BOOKS_CHIRHO.size} books)`);
  console.log("\nDone!");
}

mainChirho();
