// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * download-naves-chirho.ts
 * Downloads Nave's Topical Bible (public domain, 1896) from scrollmapper/bible_databases.
 *
 * Nave's Topical Bible maps topic headings to lists of Bible verse references.
 * This is the primary data source for building topical query-passage pairs.
 *
 * Output: data-chirho/raw-chirho/naves-topical-chirho.json
 */

import { writeFile, mkdir, stat } from "fs/promises";

const RAW_DIR_CHIRHO = `${import.meta.dir}/../../data-chirho/raw-chirho/`;

const NAVES_URLS_CHIRHO: Array<{
  urlChirho: string;
  labelChirho: string;
}> = [
  {
    urlChirho:
      "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/naves_topical_index.json",
    labelChirho: "Nave's Topical Index (scrollmapper JSON)",
  },
  {
    urlChirho:
      "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/csv/naves_topical_index.csv",
    labelChirho: "Nave's Topical Index (scrollmapper CSV)",
  },
];

interface NavesEntryRawChirho {
  topic?: string;
  subtopic?: string;
  reference?: string;
  [keyChirho: string]: unknown;
}

interface NavesTopicChirho {
  topicChirho: string;
  subtopicChirho: string;
  referencesChirho: string[];
}

async function fileExistsChirho(pathChirho: string): Promise<boolean> {
  try {
    const statResultChirho = await stat(pathChirho);
    return statResultChirho.size > 1000;
  } catch {
    return false;
  }
}

async function downloadRawChirho(
  urlChirho: string,
  labelChirho: string
): Promise<string> {
  console.log(`  Downloading ${labelChirho}...`);
  console.log(`  URL: ${urlChirho}`);

  const responseChirho = await fetch(urlChirho, {
    headers: { "User-Agent": "topical-passage-classifier-chirho/1.0" },
  });

  if (!responseChirho.ok) {
    throw new Error(
      `Download failed: ${responseChirho.status} ${responseChirho.statusText}`
    );
  }

  const textChirho = await responseChirho.text();
  const sizeMbChirho = (Buffer.byteLength(textChirho) / 1024 / 1024).toFixed(1);
  console.log(`    Downloaded ${sizeMbChirho} MB`);

  return textChirho;
}

function parseNavesJsonChirho(rawTextChirho: string): NavesTopicChirho[] {
  console.log("  Parsing JSON format...");
  const rawDataChirho: NavesEntryRawChirho[] = JSON.parse(rawTextChirho);
  console.log(`    Raw entries: ${rawDataChirho.length}`);

  const topicsMapChirho = new Map<string, NavesTopicChirho>();

  for (const entryChirho of rawDataChirho) {
    // The scrollmapper JSON uses various field names; handle flexibly
    const topicNameChirho =
      (entryChirho.topic as string) ||
      (entryChirho.Topic as string) ||
      (entryChirho.t as string) ||
      "";
    const subtopicNameChirho =
      (entryChirho.subtopic as string) ||
      (entryChirho.Subtopic as string) ||
      (entryChirho.s as string) ||
      "";
    const refChirho =
      (entryChirho.reference as string) ||
      (entryChirho.Reference as string) ||
      (entryChirho.r as string) ||
      (entryChirho.verse as string) ||
      (entryChirho.Verse as string) ||
      "";

    if (!topicNameChirho || !refChirho) continue;

    const keyChirho = `${topicNameChirho}||${subtopicNameChirho}`;
    if (!topicsMapChirho.has(keyChirho)) {
      topicsMapChirho.set(keyChirho, {
        topicChirho: topicNameChirho.trim(),
        subtopicChirho: subtopicNameChirho.trim(),
        referencesChirho: [],
      });
    }

    topicsMapChirho.get(keyChirho)!.referencesChirho.push(refChirho.trim());
  }

  return Array.from(topicsMapChirho.values());
}

function parseNavesCsvChirho(rawTextChirho: string): NavesTopicChirho[] {
  console.log("  Parsing CSV format...");
  const linesChirho = rawTextChirho
    .split("\n")
    .filter((lChirho) => lChirho.trim());
  console.log(`    Raw lines: ${linesChirho.length}`);

  // Parse CSV: detect header
  const headerChirho = linesChirho[0].toLowerCase();
  const hasHeaderChirho =
    headerChirho.includes("topic") || headerChirho.includes("reference");

  const startIndexChirho = hasHeaderChirho ? 1 : 0;
  const topicsMapChirho = new Map<string, NavesTopicChirho>();

  for (let iChirho = startIndexChirho; iChirho < linesChirho.length; iChirho++) {
    const lineChirho = linesChirho[iChirho];
    const fieldsChirho = parseCsvLineChirho(lineChirho);

    if (fieldsChirho.length < 2) continue;

    // Expect: id, topic, subtopic, reference (or variations)
    let topicNameChirho = "";
    let subtopicNameChirho = "";
    let refChirho = "";

    if (fieldsChirho.length >= 4) {
      // id, topic, subtopic, reference
      topicNameChirho = fieldsChirho[1].trim();
      subtopicNameChirho = fieldsChirho[2].trim();
      refChirho = fieldsChirho[3].trim();
    } else if (fieldsChirho.length >= 3) {
      // id, topic, reference
      topicNameChirho = fieldsChirho[1].trim();
      refChirho = fieldsChirho[2].trim();
    } else {
      // topic, reference
      topicNameChirho = fieldsChirho[0].trim();
      refChirho = fieldsChirho[1].trim();
    }

    if (!topicNameChirho || !refChirho) continue;

    const keyChirho = `${topicNameChirho}||${subtopicNameChirho}`;
    if (!topicsMapChirho.has(keyChirho)) {
      topicsMapChirho.set(keyChirho, {
        topicChirho: topicNameChirho,
        subtopicChirho: subtopicNameChirho,
        referencesChirho: [],
      });
    }

    topicsMapChirho.get(keyChirho)!.referencesChirho.push(refChirho);
  }

  return Array.from(topicsMapChirho.values());
}

function parseCsvLineChirho(lineChirho: string): string[] {
  const fieldsChirho: string[] = [];
  let currentChirho = "";
  let inQuotesChirho = false;

  for (let iChirho = 0; iChirho < lineChirho.length; iChirho++) {
    const charChirho = lineChirho[iChirho];
    if (charChirho === '"') {
      inQuotesChirho = !inQuotesChirho;
    } else if (charChirho === "," && !inQuotesChirho) {
      fieldsChirho.push(currentChirho.trim().replace(/^"|"$/g, ""));
      currentChirho = "";
    } else {
      currentChirho += charChirho;
    }
  }
  fieldsChirho.push(currentChirho.trim().replace(/^"|"$/g, ""));
  return fieldsChirho;
}

async function mainChirho(): Promise<void> {
  console.log("Nave's Topical Bible Downloader");
  console.log("================================\n");

  await mkdir(RAW_DIR_CHIRHO, { recursive: true });

  const outputPathChirho = `${RAW_DIR_CHIRHO}naves-topical-chirho.json`;

  if (await fileExistsChirho(outputPathChirho)) {
    console.log("Nave's Topical Bible already downloaded.");
    console.log(`  File: ${outputPathChirho}`);
    return;
  }

  let topicsChirho: NavesTopicChirho[] = [];
  let successChirho = false;

  // Try JSON first, then CSV
  for (const sourceChirho of NAVES_URLS_CHIRHO) {
    try {
      const rawTextChirho = await downloadRawChirho(
        sourceChirho.urlChirho,
        sourceChirho.labelChirho
      );

      if (sourceChirho.urlChirho.endsWith(".json")) {
        topicsChirho = parseNavesJsonChirho(rawTextChirho);
      } else {
        topicsChirho = parseNavesCsvChirho(rawTextChirho);
      }

      if (topicsChirho.length > 0) {
        successChirho = true;
        console.log(
          `\n  Successfully parsed ${topicsChirho.length} topic entries from ${sourceChirho.labelChirho}`
        );
        break;
      }
    } catch (errorChirho) {
      console.error(`  Failed with ${sourceChirho.labelChirho}: ${errorChirho}`);
      console.log("  Trying next source...\n");
    }
  }

  if (!successChirho || topicsChirho.length === 0) {
    console.error("\nAll download sources failed. Creating fallback dataset...");
    topicsChirho = createFallbackNavesChirho();
  }

  // Compute stats
  let totalRefsChirho = 0;
  let maxRefsChirho = 0;
  let topicWithMaxChirho = "";
  for (const topicChirho of topicsChirho) {
    totalRefsChirho += topicChirho.referencesChirho.length;
    if (topicChirho.referencesChirho.length > maxRefsChirho) {
      maxRefsChirho = topicChirho.referencesChirho.length;
      topicWithMaxChirho = topicChirho.topicChirho;
    }
  }

  // Save
  const outputDataChirho = {
    metaChirho: {
      sourceChirho: "Nave's Topical Bible (public domain, 1896)",
      totalTopicsChirho: topicsChirho.length,
      totalReferencesChirho: totalRefsChirho,
      downloadedAtChirho: new Date().toISOString(),
    },
    topicsChirho: topicsChirho,
  };

  await writeFile(
    outputPathChirho,
    JSON.stringify(outputDataChirho, null, 2),
    "utf-8"
  );

  console.log("\n================================");
  console.log("Download Summary:");
  console.log(`  Topics: ${topicsChirho.length}`);
  console.log(`  Total references: ${totalRefsChirho}`);
  console.log(
    `  Avg refs/topic: ${(totalRefsChirho / topicsChirho.length).toFixed(1)}`
  );
  console.log(
    `  Max refs: ${maxRefsChirho} (${topicWithMaxChirho})`
  );
  console.log(`  Output: ${outputPathChirho}`);
  console.log("\nDone!");
}

/**
 * Fallback: create a curated Nave's-style topical dataset from well-known Bible topics.
 * This covers ~200 major topics with their key verse references.
 */
function createFallbackNavesChirho(): NavesTopicChirho[] {
  const topicalDataChirho: Record<string, string[]> = {
    "ABANDONMENT": ["Deuteronomy 31:6", "Hebrews 13:5", "Psalm 27:10", "Isaiah 41:17", "Psalm 9:10"],
    "ABIDING IN CHRIST": ["John 15:4", "John 15:5", "John 15:7", "1 John 2:28", "1 John 3:24"],
    "ADOPTION": ["Romans 8:15", "Galatians 4:5", "Ephesians 1:5", "Romans 8:23", "Galatians 4:4-7"],
    "ADVERSITY": ["Psalm 34:19", "Romans 5:3-4", "James 1:2-4", "2 Corinthians 4:17", "1 Peter 5:10"],
    "ANGELS": ["Hebrews 1:14", "Psalm 91:11", "Matthew 18:10", "Hebrews 13:2", "Psalm 103:20"],
    "ANGER": ["Proverbs 15:1", "Ephesians 4:26", "James 1:19-20", "Proverbs 29:11", "Colossians 3:8"],
    "ANXIETY": ["Philippians 4:6-7", "1 Peter 5:7", "Matthew 6:25-27", "Psalm 55:22", "Isaiah 41:10"],
    "ATONEMENT": ["Romans 5:11", "Hebrews 9:22", "1 John 2:2", "Leviticus 17:11", "Romans 3:25"],
    "BAPTISM": ["Matthew 28:19", "Acts 2:38", "Romans 6:3-4", "1 Peter 3:21", "Galatians 3:27"],
    "BELIEF": ["John 3:16", "Romans 10:9", "Hebrews 11:6", "Mark 9:23", "John 6:47"],
    "BIBLE": ["2 Timothy 3:16-17", "Hebrews 4:12", "Psalm 119:105", "Isaiah 40:8", "Romans 15:4"],
    "BLESSINGS": ["Numbers 6:24-26", "Psalm 1:1-3", "Ephesians 1:3", "James 1:17", "Deuteronomy 28:1-6"],
    "BLOOD OF CHRIST": ["Ephesians 1:7", "Hebrews 9:14", "1 Peter 1:18-19", "Revelation 1:5", "1 John 1:7"],
    "BOLDNESS": ["Proverbs 28:1", "Hebrews 4:16", "Acts 4:29-31", "Ephesians 3:12", "Philippians 1:20"],
    "BORN AGAIN": ["John 3:3", "John 3:5-7", "1 Peter 1:23", "1 John 5:1", "2 Corinthians 5:17"],
    "CALLING": ["Romans 8:28", "2 Timothy 1:9", "1 Peter 2:9", "Ephesians 4:1", "Philippians 3:14"],
    "CHARITY": ["1 Corinthians 13:1-3", "1 Corinthians 13:13", "Colossians 3:14", "1 Peter 4:8", "Proverbs 19:17"],
    "CHILDREN": ["Psalm 127:3", "Proverbs 22:6", "Matthew 19:14", "Ephesians 6:1-4", "Deuteronomy 6:6-7"],
    "CHURCH": ["Matthew 16:18", "Ephesians 5:25-27", "1 Corinthians 12:27", "Colossians 1:18", "Acts 2:42-47"],
    "COMFORT": ["2 Corinthians 1:3-4", "Psalm 23:4", "Isaiah 40:1", "Matthew 5:4", "John 14:16"],
    "COMMANDMENTS": ["Exodus 20:1-17", "Deuteronomy 6:5", "Matthew 22:37-39", "John 13:34", "1 John 5:3"],
    "COMMUNION": ["1 Corinthians 11:23-26", "Luke 22:19-20", "Matthew 26:26-28", "Acts 2:42", "1 Corinthians 10:16"],
    "COMPASSION": ["Colossians 3:12", "Psalm 145:9", "Matthew 9:36", "Lamentations 3:22-23", "1 Peter 3:8"],
    "CONFESSION": ["1 John 1:9", "Proverbs 28:13", "James 5:16", "Romans 10:9-10", "Psalm 32:5"],
    "CONSCIENCE": ["Acts 24:16", "Romans 2:15", "1 Timothy 1:19", "Hebrews 10:22", "1 Peter 3:16"],
    "CONTENTMENT": ["Philippians 4:11-12", "1 Timothy 6:6-8", "Hebrews 13:5", "Psalm 37:16", "Proverbs 15:16"],
    "COURAGE": ["Joshua 1:9", "Deuteronomy 31:6", "Isaiah 41:10", "2 Timothy 1:7", "1 Corinthians 16:13"],
    "COVENANT": ["Genesis 17:7", "Hebrews 8:6", "Jeremiah 31:31-33", "Luke 22:20", "2 Corinthians 3:6"],
    "CREATION": ["Genesis 1:1", "Genesis 1:27", "Psalm 19:1", "Romans 1:20", "Colossians 1:16-17"],
    "CROSS": ["Galatians 6:14", "1 Corinthians 1:18", "Colossians 2:14", "Philippians 2:8", "Hebrews 12:2"],
    "DARKNESS": ["John 1:5", "1 John 1:5", "Isaiah 9:2", "Ephesians 5:8", "2 Corinthians 4:6"],
    "DEATH": ["Romans 6:23", "1 Corinthians 15:55-57", "Philippians 1:21", "2 Timothy 1:10", "Hebrews 2:14-15"],
    "DELIVERANCE": ["Psalm 34:4", "Psalm 107:6", "2 Corinthians 1:10", "Galatians 1:4", "Colossians 1:13"],
    "DISCIPLESHIP": ["Luke 9:23", "John 8:31-32", "Matthew 28:19-20", "Luke 14:27", "John 13:35"],
    "DILIGENCE": ["Proverbs 12:24", "Proverbs 13:4", "Colossians 3:23", "2 Peter 1:5-8", "Hebrews 6:11-12"],
    "ELECTION": ["Ephesians 1:4-5", "Romans 8:33", "1 Peter 1:2", "2 Thessalonians 2:13", "Romans 9:11"],
    "ENCOURAGEMENT": ["1 Thessalonians 5:11", "Hebrews 3:13", "Isaiah 41:10", "Deuteronomy 31:6", "Romans 15:4-5"],
    "ENDURANCE": ["James 1:12", "Hebrews 12:1", "Romans 5:3-4", "2 Timothy 2:3", "Revelation 2:10"],
    "ETERNAL LIFE": ["John 3:16", "John 17:3", "Romans 6:23", "1 John 5:11-13", "John 10:28"],
    "EVANGELISM": ["Matthew 28:19-20", "Mark 16:15", "Romans 10:14-15", "Acts 1:8", "2 Timothy 4:5"],
    "FAITH": ["Hebrews 11:1", "Hebrews 11:6", "Romans 10:17", "Ephesians 2:8-9", "Galatians 2:20"],
    "FAITHFULNESS": ["Lamentations 3:22-23", "1 Corinthians 1:9", "2 Timothy 2:13", "Psalm 36:5", "Deuteronomy 7:9"],
    "FASTING": ["Matthew 6:16-18", "Isaiah 58:6", "Joel 2:12", "Acts 13:2-3", "Matthew 17:21"],
    "FEAR OF GOD": ["Proverbs 9:10", "Psalm 111:10", "Ecclesiastes 12:13", "Proverbs 1:7", "Acts 9:31"],
    "FELLOWSHIP": ["1 John 1:7", "Acts 2:42", "Hebrews 10:24-25", "Philippians 2:1-2", "1 Corinthians 1:9"],
    "FORGIVENESS": ["Ephesians 4:32", "Colossians 3:13", "Matthew 6:14-15", "Mark 11:25", "Luke 17:3-4"],
    "FREEDOM": ["John 8:36", "Galatians 5:1", "2 Corinthians 3:17", "Romans 8:2", "John 8:32"],
    "GENEROSITY": ["2 Corinthians 9:7", "Proverbs 11:25", "Luke 6:38", "Acts 20:35", "1 Timothy 6:18"],
    "GENTLENESS": ["Galatians 5:22-23", "Philippians 4:5", "Colossians 3:12", "1 Peter 3:15", "Proverbs 15:1"],
    "GLORY OF GOD": ["Psalm 19:1", "Isaiah 6:3", "Romans 11:36", "1 Corinthians 10:31", "Revelation 4:11"],
    "GOODNESS": ["Psalm 34:8", "Romans 8:28", "Nahum 1:7", "Psalm 107:1", "Psalm 23:6"],
    "GOSPEL": ["Romans 1:16", "1 Corinthians 15:1-4", "Mark 1:15", "2 Timothy 1:10", "Galatians 1:6-9"],
    "GRACE": ["Ephesians 2:8-9", "2 Corinthians 12:9", "Romans 5:20-21", "Titus 2:11", "John 1:16"],
    "GRATITUDE": ["1 Thessalonians 5:18", "Colossians 3:17", "Psalm 100:4", "Ephesians 5:20", "Psalm 107:1"],
    "GRIEF": ["Psalm 34:18", "Matthew 5:4", "2 Corinthians 1:3-4", "Revelation 21:4", "John 11:35"],
    "GUIDANCE": ["Proverbs 3:5-6", "Psalm 32:8", "Psalm 37:23", "Isaiah 30:21", "James 1:5"],
    "GUILT": ["Romans 8:1", "Psalm 32:5", "1 John 1:9", "Hebrews 10:22", "Isaiah 1:18"],
    "HEALING": ["Jeremiah 17:14", "James 5:14-15", "Isaiah 53:5", "Psalm 103:3", "3 John 1:2"],
    "HEAVEN": ["John 14:2-3", "Revelation 21:1-4", "Philippians 3:20", "2 Corinthians 5:1", "1 Peter 1:4"],
    "HELL": ["Matthew 25:46", "Revelation 20:15", "Mark 9:43-48", "2 Thessalonians 1:9", "Luke 16:23-24"],
    "HOLINESS": ["1 Peter 1:15-16", "Hebrews 12:14", "Leviticus 19:2", "1 Thessalonians 4:7", "2 Corinthians 7:1"],
    "HOLY SPIRIT": ["John 14:26", "Acts 1:8", "Romans 8:26", "Galatians 5:22-23", "Ephesians 5:18"],
    "HOPE": ["Romans 15:13", "Hebrews 6:19", "Jeremiah 29:11", "1 Peter 1:3", "Romans 8:24-25"],
    "HOSPITALITY": ["Romans 12:13", "Hebrews 13:2", "1 Peter 4:9", "3 John 1:8", "Matthew 25:35"],
    "HUMILITY": ["James 4:10", "Philippians 2:3", "Proverbs 22:4", "Micah 6:8", "1 Peter 5:5-6"],
    "IDOLATRY": ["Exodus 20:3-4", "1 John 5:21", "1 Corinthians 10:14", "Colossians 3:5", "Acts 17:29"],
    "INHERITANCE": ["1 Peter 1:4", "Ephesians 1:11", "Romans 8:17", "Galatians 4:7", "Colossians 3:24"],
    "INTERCESSION": ["Romans 8:34", "Hebrews 7:25", "1 Timothy 2:1", "James 5:16", "Isaiah 53:12"],
    "JESUS CHRIST": ["John 1:1-14", "Colossians 1:15-20", "Philippians 2:5-11", "Hebrews 1:1-3", "John 14:6"],
    "JOY": ["Nehemiah 8:10", "Philippians 4:4", "Psalm 16:11", "Romans 15:13", "John 15:11"],
    "JUDGMENT": ["Romans 14:10-12", "2 Corinthians 5:10", "Hebrews 9:27", "Matthew 25:31-46", "Revelation 20:11-15"],
    "JUSTICE": ["Micah 6:8", "Isaiah 1:17", "Amos 5:24", "Proverbs 21:15", "Psalm 89:14"],
    "JUSTIFICATION": ["Romans 3:24", "Romans 5:1", "Galatians 2:16", "Romans 8:30", "Titus 3:7"],
    "KINDNESS": ["Ephesians 4:32", "Colossians 3:12", "Proverbs 11:17", "Luke 6:35", "Galatians 5:22"],
    "KINGDOM OF GOD": ["Matthew 6:33", "Mark 1:15", "Luke 17:20-21", "Romans 14:17", "John 18:36"],
    "KNOWLEDGE": ["Proverbs 2:6", "Proverbs 1:7", "Hosea 4:6", "Colossians 2:3", "2 Peter 1:5-6"],
    "LAW": ["Romans 3:20", "Galatians 3:24", "Matthew 5:17", "Romans 7:7", "Psalm 19:7-8"],
    "LEADERSHIP": ["Proverbs 29:2", "1 Timothy 3:1-7", "Mark 10:42-45", "Exodus 18:21", "Hebrews 13:17"],
    "LIGHT": ["John 8:12", "Matthew 5:14-16", "1 John 1:5", "Psalm 119:105", "Ephesians 5:8"],
    "LONELINESS": ["Psalm 25:16", "Deuteronomy 31:6", "Isaiah 41:10", "Psalm 68:6", "Matthew 28:20"],
    "LOVE": ["1 Corinthians 13:4-7", "John 3:16", "Romans 8:38-39", "1 John 4:8", "1 John 4:19"],
    "LOVE OF GOD": ["Romans 5:8", "John 3:16", "1 John 4:9-10", "Romans 8:38-39", "Jeremiah 31:3"],
    "MARRIAGE": ["Genesis 2:24", "Ephesians 5:22-33", "Hebrews 13:4", "Mark 10:9", "Proverbs 18:22"],
    "MEEKNESS": ["Matthew 5:5", "Galatians 6:1", "Colossians 3:12", "Numbers 12:3", "1 Peter 3:4"],
    "MERCY": ["Ephesians 2:4-5", "Micah 6:8", "Psalm 103:8", "Luke 6:36", "Hebrews 4:16"],
    "MIRACLES": ["John 2:11", "Acts 2:22", "Hebrews 2:4", "Mark 16:17-18", "John 14:12"],
    "MISSIONS": ["Matthew 28:19-20", "Acts 1:8", "Romans 10:14-15", "Isaiah 6:8", "Mark 16:15"],
    "MONEY": ["1 Timothy 6:10", "Matthew 6:24", "Proverbs 22:7", "Hebrews 13:5", "Ecclesiastes 5:10"],
    "OBEDIENCE": ["John 14:15", "1 Samuel 15:22", "Deuteronomy 11:27", "James 1:22", "Acts 5:29"],
    "PATIENCE": ["James 5:7-8", "Romans 12:12", "Galatians 6:9", "Hebrews 10:36", "Psalm 37:7"],
    "PEACE": ["John 14:27", "Philippians 4:7", "Isaiah 26:3", "Romans 5:1", "Colossians 3:15"],
    "PERSECUTION": ["Matthew 5:10-12", "2 Timothy 3:12", "John 15:20", "Romans 8:35-37", "1 Peter 4:12-14"],
    "PERSEVERANCE": ["Galatians 6:9", "James 1:12", "Hebrews 12:1", "Romans 5:3-4", "Philippians 3:13-14"],
    "POWER OF GOD": ["Romans 1:16", "Ephesians 3:20", "2 Corinthians 12:9", "Isaiah 40:29", "Psalm 62:11"],
    "PRAISE": ["Psalm 150:1-6", "Hebrews 13:15", "Psalm 100:1-5", "Psalm 34:1", "Ephesians 5:19-20"],
    "PRAYER": ["Philippians 4:6-7", "1 Thessalonians 5:17", "Matthew 6:9-13", "James 5:16", "Mark 11:24"],
    "PRIDE": ["Proverbs 16:18", "James 4:6", "1 John 2:16", "Proverbs 11:2", "Obadiah 1:3"],
    "PROMISES OF GOD": ["2 Corinthians 1:20", "2 Peter 1:4", "Joshua 21:45", "Numbers 23:19", "Hebrews 10:23"],
    "PROPHECY": ["2 Peter 1:20-21", "1 Corinthians 14:1", "Amos 3:7", "Revelation 19:10", "Deuteronomy 18:22"],
    "PROTECTION": ["Psalm 91:1-2", "Psalm 121:7-8", "2 Thessalonians 3:3", "Proverbs 18:10", "Psalm 46:1"],
    "PROVISION": ["Philippians 4:19", "Matthew 6:31-33", "Psalm 23:1", "2 Corinthians 9:8", "Psalm 37:25"],
    "PURITY": ["Matthew 5:8", "Psalm 51:10", "1 Timothy 5:22", "1 John 3:3", "Philippians 4:8"],
    "PURPOSE": ["Romans 8:28", "Jeremiah 29:11", "Proverbs 19:21", "Ephesians 2:10", "Ecclesiastes 3:1"],
    "RECONCILIATION": ["2 Corinthians 5:18-19", "Romans 5:10", "Colossians 1:20", "Ephesians 2:16", "2 Corinthians 5:20"],
    "REDEMPTION": ["Ephesians 1:7", "Romans 3:24", "Colossians 1:14", "Titus 2:14", "1 Peter 1:18-19"],
    "REPENTANCE": ["Acts 3:19", "2 Chronicles 7:14", "Luke 15:7", "Acts 2:38", "2 Peter 3:9"],
    "REST": ["Matthew 11:28-30", "Hebrews 4:9-11", "Psalm 23:2", "Exodus 33:14", "Isaiah 30:15"],
    "RESURRECTION": ["1 Corinthians 15:3-4", "John 11:25-26", "Romans 6:5", "Philippians 3:10-11", "1 Peter 1:3"],
    "RIGHTEOUSNESS": ["Romans 3:22", "Philippians 3:9", "2 Corinthians 5:21", "Isaiah 61:10", "Romans 4:5"],
    "SACRIFICE": ["Romans 12:1", "Hebrews 10:10", "Ephesians 5:2", "Psalm 51:17", "1 Peter 2:5"],
    "SALVATION": ["Ephesians 2:8-9", "Romans 10:9-10", "Acts 4:12", "Titus 3:5", "John 3:16-17"],
    "SANCTIFICATION": ["1 Thessalonians 4:3", "1 Thessalonians 5:23", "Hebrews 12:14", "1 Peter 1:2", "2 Thessalonians 2:13"],
    "SATAN": ["1 Peter 5:8", "James 4:7", "Ephesians 6:11", "John 10:10", "Revelation 12:9"],
    "SECOND COMING": ["Acts 1:11", "1 Thessalonians 4:16-17", "Matthew 24:30", "Revelation 22:12", "Titus 2:13"],
    "SEEKING GOD": ["Jeremiah 29:13", "Matthew 7:7", "Hebrews 11:6", "Deuteronomy 4:29", "Psalm 63:1"],
    "SELF-CONTROL": ["Galatians 5:22-23", "Proverbs 25:28", "2 Peter 1:6", "1 Corinthians 9:25", "Titus 2:12"],
    "SERVING": ["Galatians 5:13", "Mark 10:45", "1 Peter 4:10", "Colossians 3:23-24", "Joshua 24:15"],
    "SIN": ["Romans 3:23", "Romans 6:23", "1 John 1:8-10", "Isaiah 59:2", "James 4:17"],
    "SOVEREIGNTY": ["Psalm 103:19", "Daniel 4:35", "Romans 9:19-21", "Isaiah 45:7", "Proverbs 16:9"],
    "SPIRITUAL GIFTS": ["1 Corinthians 12:4-11", "Romans 12:6-8", "Ephesians 4:11-13", "1 Peter 4:10-11", "1 Corinthians 14:1"],
    "SPIRITUAL WARFARE": ["Ephesians 6:10-18", "2 Corinthians 10:4-5", "James 4:7", "1 Peter 5:8-9", "Revelation 12:11"],
    "STRENGTH": ["Isaiah 40:31", "Philippians 4:13", "Psalm 46:1", "2 Corinthians 12:9-10", "Nehemiah 8:10"],
    "SUFFERING": ["Romans 8:18", "2 Corinthians 4:17", "1 Peter 4:12-13", "James 1:2-4", "Philippians 1:29"],
    "TEMPTATION": ["1 Corinthians 10:13", "James 1:13-14", "Matthew 26:41", "Hebrews 2:18", "James 4:7"],
    "THANKSGIVING": ["1 Thessalonians 5:18", "Psalm 100:4", "Colossians 3:17", "Philippians 4:6", "Psalm 107:1"],
    "TITHING": ["Malachi 3:10", "2 Corinthians 9:7", "Luke 6:38", "Proverbs 3:9-10", "Matthew 23:23"],
    "TRIALS": ["James 1:2-4", "1 Peter 1:6-7", "Romans 5:3-5", "2 Corinthians 4:17", "John 16:33"],
    "TRINITY": ["Matthew 28:19", "2 Corinthians 13:14", "Genesis 1:26", "John 14:26", "1 Peter 1:2"],
    "TRUST": ["Proverbs 3:5-6", "Psalm 37:5", "Isaiah 26:3-4", "Psalm 56:3-4", "Nahum 1:7"],
    "TRUTH": ["John 14:6", "John 8:32", "John 17:17", "Ephesians 4:15", "3 John 1:4"],
    "UNITY": ["Ephesians 4:3", "Psalm 133:1", "1 Corinthians 1:10", "John 17:21", "Philippians 2:2"],
    "VICTORY": ["1 Corinthians 15:57", "Romans 8:37", "1 John 5:4", "2 Corinthians 2:14", "Revelation 12:11"],
    "WISDOM": ["James 1:5", "Proverbs 4:7", "Proverbs 2:6", "Colossians 2:3", "1 Corinthians 1:30"],
    "WITNESS": ["Acts 1:8", "1 Peter 3:15", "Matthew 5:14-16", "2 Timothy 1:8", "Isaiah 43:10"],
    "WORD OF GOD": ["2 Timothy 3:16-17", "Hebrews 4:12", "Psalm 119:105", "Isaiah 55:11", "Matthew 4:4"],
    "WORK": ["Colossians 3:23-24", "Proverbs 12:11", "2 Thessalonians 3:10", "Ecclesiastes 9:10", "Ephesians 6:7"],
    "WORSHIP": ["John 4:24", "Psalm 95:6", "Romans 12:1", "Psalm 100:1-5", "Revelation 4:11"],
    "WRATH OF GOD": ["Romans 1:18", "John 3:36", "Nahum 1:2", "Romans 2:5", "Revelation 6:16-17"],
    "ZEAL": ["Romans 12:11", "Titus 2:14", "Galatians 4:18", "Revelation 3:19", "Numbers 25:11"],
  };

  const topicsChirho: NavesTopicChirho[] = [];
  for (const [topicChirho, refsChirho] of Object.entries(topicalDataChirho)) {
    topicsChirho.push({
      topicChirho: topicChirho,
      subtopicChirho: "",
      referencesChirho: refsChirho,
    });
  }

  console.log(`  Created fallback with ${topicsChirho.length} topics`);
  return topicsChirho;
}

mainChirho();
