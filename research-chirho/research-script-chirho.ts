// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * research-script-chirho.ts
 * Uses Perplexity API (sonar model) to generate academic research papers
 * for each of the 5 Bible ML model projects.
 */

import { writeFile, mkdir } from "fs/promises";

const PERPLEXITY_API_KEY_CHIRHO = process.env.PERPLEXITY_API_KEY_CHIRHO;
if (!PERPLEXITY_API_KEY_CHIRHO) {
  throw new Error("PERPLEXITY_API_KEY_CHIRHO is not set. Source .env-chirho first.");
}

const API_URL_CHIRHO = "https://api.perplexity.ai/chat/completions";

interface ResearchTopicChirho {
  titleChirho: string;
  fileNameChirho: string;
  queriesChirho: string[];
  systemPromptChirho: string;
}

const TOPICS_CHIRHO: ResearchTopicChirho[] = [
  {
    titleChirho: "Theological Guardrails: AI-Powered Orthodox Doctrine Classification",
    fileNameChirho: "01-theological-guardrails-chirho.md",
    queriesChirho: [
      "What existing AI/ML models exist for theological text classification, heresy detection, or doctrinal analysis? Include any HuggingFace models, academic papers, or open source projects. What are their limitations?",
      "What are the best approaches for multi-label text classification of theological statements? Compare DeBERTa, BERT, RoBERTa for nuanced semantic classification tasks. What training data strategies work for low-resource specialized domains?",
      "What public domain theological datasets exist? Include historical creeds (Nicene, Apostles, Chalcedonian, Athanasian), church father writings, catechisms. What APIs or archives provide structured access to these texts?",
      "How can contrastive learning and sentence transformers be used for theological embedding spaces? What are best practices for triplet loss training with domain-specific semantic similarity? How can zero-shot classification complement fine-tuned models?",
      "What evaluation metrics and benchmarks are appropriate for theological text classification? How should models handle denominational differences vs core orthodoxy? What are the ethical considerations of AI in theology?"
    ],
    systemPromptChirho: `You are an AI research assistant writing an academic paper on building ML models for theological guardrails - detecting heretical statements and classifying them against orthodox Christian doctrine as defined by the first six ecumenical councils (Nicaea 325, Constantinople I 381, Ephesus 431, Chalcedon 451, Constantinople II 553, Constantinople III 681). The model pipeline includes a DeBERTa-v3-large classifier, a MiniLM-L12 sentence transformer for embeddings, and a Flan-T5-base explainer. Focus on practical ML architecture, dataset construction, and evaluation methodology.`
  },
  {
    titleChirho: "Intertextual Reference Network: ML-Powered Biblical Cross-Reference Discovery",
    fileNameChirho: "02-intertextual-reference-network-chirho.md",
    queriesChirho: [
      "What existing tools or ML models handle biblical cross-references, typology detection, or intertextual analysis? Include Treasury of Scripture Knowledge, OpenBible cross-references, and any academic NLP work on biblical intertextuality.",
      "How can sentence transformers and graph neural networks model relationships between Bible passages? What architectures best capture typological connections (OT prophecy to NT fulfillment), direct quotations, and thematic parallels?",
      "What structured datasets of biblical cross-references exist? How large are they? What labeling schemas distinguish between direct quotes, allusions, typological fulfillment, thematic parallels, and conceptual links?",
      "What are state-of-the-art approaches for link prediction in knowledge graphs applied to religious or literary texts? How can GNN embeddings combine with transformer-based semantic similarity for cross-reference discovery?",
      "How should novel cross-reference suggestions be evaluated? What gold standard datasets exist for biblical cross-references? What precision/recall targets are reasonable for different reference types?"
    ],
    systemPromptChirho: `You are an AI research assistant writing an academic paper on building an ML-powered intertextual reference network for the Bible. The goal is a sentence transformer that encodes biblical passages into an embedding space where cross-references, typological connections, and thematic parallels are nearby. This would enable discovering new cross-references and understanding the Bible's internal structure. Focus on practical ML approaches, existing datasets, and evaluation methodology.`
  },
  {
    titleChirho: "Biblical Language Tutor: Seq2Seq Models for Hebrew, Greek, and Aramaic",
    fileNameChirho: "03-biblical-language-tutor-chirho.md",
    queriesChirho: [
      "What existing NLP tools and ML models handle biblical Hebrew, Koine Greek, and biblical Aramaic? Include morphological analyzers, parsers, lexicons, and any HuggingFace models for ancient languages.",
      "What are best approaches for seq2seq models that teach morphological analysis of ancient languages? How can models be trained to break down Hebrew verb forms (binyanim, stems, roots) and Greek verb forms (tense, voice, mood, parsing)?",
      "What open datasets exist for biblical language learning? Include parsed texts (OSHB, SBLGNT with morphological tags), interlinear Bibles, and lexical databases (BDAG, BDB equivalents that are open). What annotation standards exist?",
      "How can transformer models handle the unique challenges of biblical Hebrew (consonantal text, vowel pointing, construct chains) and Koine Greek (deponent verbs, middle voice, aspect vs tense)? What tokenization strategies work for morphologically rich languages?",
      "What evaluation approaches work for language tutoring models? How should translation quality be measured for biblical texts? What are best practices for interactive grammar exercise generation using ML?"
    ],
    systemPromptChirho: `You are an AI research assistant writing an academic paper on building seq2seq ML models for biblical language tutoring. The system would help students learn biblical Hebrew, Koine Greek, and biblical Aramaic through morphological analysis, parsing exercises, and translation assistance. Focus on practical ML approaches for ancient morphologically-rich languages, available training data, and pedagogical evaluation.`
  },
  {
    titleChirho: "Manuscript Variant Analyzer: ML for Textual Criticism",
    fileNameChirho: "04-manuscript-variant-analyzer-chirho.md",
    queriesChirho: [
      "What existing computational tools exist for New Testament textual criticism? Include the Munster INTF tools, CBGM (Coherence-Based Genealogical Method), Open Greek New Testament project, and any ML approaches to variant analysis.",
      "How can ML classification models be applied to textual criticism - specifically classifying manuscript variants by type (harmonization, homoeoteleuton, theological modification, scribal error)? What architectures work for this specialized classification?",
      "What digitized manuscript datasets are available for training? Include the INTF transcriptions, Center for the Study of New Testament Manuscripts (CSNTM), and any structured variant apparatus data. What data formats are used?",
      "How can ML models learn scribal behavior patterns and manuscript family relationships? What graph-based or phylogenetic approaches have been applied to stemmatology? Can transformers improve on traditional stemmatic methods?",
      "What evaluation methods are appropriate for textual criticism models? How should variant classification accuracy be measured? What expert consensus datasets exist for benchmarking against established critical editions (NA28/UBS5)?"
    ],
    systemPromptChirho: `You are an AI research assistant writing an academic paper on building ML models for biblical manuscript variant analysis (textual criticism). The goal is a classifier that can analyze textual variants across manuscripts, classify the type of variant, and assist scholars in determining likely original readings. Focus on practical ML approaches, available manuscript data, and evaluation against established critical editions.`
  },
  {
    titleChirho: "Cross-Translation Semantic Model: Multilingual Bible Embeddings",
    fileNameChirho: "05-cross-translation-semantic-chirho.md",
    queriesChirho: [
      "What existing multilingual embedding models or tools compare Bible translations? Include any academic work on translation comparison, semantic equivalence detection across Bible versions, and tools like STEPBible or Paratext.",
      "How can multilingual sentence transformers create a shared embedding space for Bible translations? What architectures handle the challenge of formal equivalence vs dynamic equivalence translations? How do models like LaBSE or multilingual E5 perform on religious texts?",
      "What parallel Bible corpora exist for training? How many translations are available in structured format? Include resources like bible.com API, eBible.org, Digital Bible Library, and open-license translations. What alignment data exists at verse/phrase level?",
      "How can semantic similarity models distinguish between legitimate translation differences and actual meaning shifts? What loss functions and training strategies work for learning translation-invariant representations of biblical passages?",
      "How should cross-translation semantic models be evaluated? What gold standard datasets exist for translation quality assessment of Bible texts? How can we measure whether embeddings correctly capture meaning across formal and dynamic equivalence translations?"
    ],
    systemPromptChirho: `You are an AI research assistant writing an academic paper on building multilingual embedding models for cross-translation semantic analysis of the Bible. The goal is to create a shared embedding space where the same verse across different translations (KJV, ESV, NIV, NLT, original languages) maps to similar vectors, enabling translation comparison and semantic analysis. Focus on practical ML approaches, available parallel corpora, and evaluation methodology.`
  }
];

interface PerplexityResponseChirho {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
  citations?: string[];
}

async function queryPerplexityChirho(
  systemPromptChirho: string,
  userQueryChirho: string
): Promise<{ contentChirho: string; citationsChirho: string[] }> {
  const responseChirho = await fetch(API_URL_CHIRHO, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${PERPLEXITY_API_KEY_CHIRHO}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "sonar",
      messages: [
        { role: "system", content: systemPromptChirho },
        { role: "user", content: userQueryChirho },
      ],
      max_tokens: 4096,
      temperature: 0.2,
      return_citations: true,
    }),
  });

  if (!responseChirho.ok) {
    const errorTextChirho = await responseChirho.text();
    throw new Error(`Perplexity API error ${responseChirho.status}: ${errorTextChirho}`);
  }

  const dataChirho = (await responseChirho.json()) as PerplexityResponseChirho;
  return {
    contentChirho: dataChirho.choices[0]?.message?.content ?? "",
    citationsChirho: dataChirho.citations ?? [],
  };
}

async function generatePaperChirho(topicChirho: ResearchTopicChirho): Promise<string> {
  console.log(`\n📖 Researching: ${topicChirho.titleChirho}`);

  const sectionsChirho: string[] = [];
  const allCitationsChirho: Set<string> = new Set();

  // Query each research question sequentially to avoid rate limits
  for (let iChirho = 0; iChirho < topicChirho.queriesChirho.length; iChirho++) {
    const queryChirho = topicChirho.queriesChirho[iChirho];
    console.log(`  Query ${iChirho + 1}/${topicChirho.queriesChirho.length}: ${queryChirho.substring(0, 80)}...`);

    try {
      const resultChirho = await queryPerplexityChirho(
        topicChirho.systemPromptChirho,
        queryChirho
      );
      sectionsChirho.push(resultChirho.contentChirho);
      resultChirho.citationsChirho.forEach((cChirho) => allCitationsChirho.add(cChirho));

      // Rate limit delay
      await new Promise((resolveChirho) => setTimeout(resolveChirho, 1500));
    } catch (errorChirho) {
      console.error(`  Error on query ${iChirho + 1}:`, errorChirho);
      sectionsChirho.push(`*[Research query failed - manual research needed]*`);
    }
  }

  // Now synthesize into a paper using Perplexity
  const synthesisPromptChirho = `Based on the following research findings, write a comprehensive academic research paper with these sections:

1. **Abstract** - What the model does and why it matters (200 words)
2. **Literature Review** - What exists, what's missing (detailed)
3. **Proposed Approach** - Architecture, data, training strategy (detailed with specific model choices)
4. **Dataset Requirements** - Sources, size, labeling schema (specific and actionable)
5. **Evaluation Methodology** - Metrics, benchmarks, baselines
6. **Impact & Applications** - Who benefits, integration possibilities
7. **References** - Cite all sources found

Research findings:
${sectionsChirho.map((sChirho, iChirho) => `\n### Finding ${iChirho + 1}\n${sChirho}`).join("\n")}

Write in academic style but keep it practical and actionable. Include specific model names, dataset sizes, and training parameters where possible.`;

  console.log(`  Synthesizing paper...`);
  const paperResultChirho = await queryPerplexityChirho(
    topicChirho.systemPromptChirho,
    synthesisPromptChirho
  );

  // Format the final paper
  const paperChirho = `<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

# ${topicChirho.titleChirho}

**Research Paper for loveJesus/models-chirho**
**Date:** ${new Date().toISOString().split("T")[0]}
**Status:** Research Phase

---

${paperResultChirho.contentChirho}

---

## Sources Discovered During Research

${Array.from(allCitationsChirho)
  .map((cChirho, iChirho) => `${iChirho + 1}. ${cChirho}`)
  .join("\n")}

---

## Raw Research Notes

${sectionsChirho.map((sChirho, iChirho) => `### Research Query ${iChirho + 1}\n\n${sChirho}\n`).join("\n---\n\n")}
`;

  return paperChirho;
}

async function mainChirho(): Promise<void> {
  console.log("🔬 Bible ML Models Research Generator");
  console.log("=====================================\n");

  const outputDirChirho = new URL(".", import.meta.url).pathname;

  // Process specific paper if argument provided, otherwise all
  const targetIndexChirho = process.argv[2] ? parseInt(process.argv[2]) - 1 : -1;
  const topicsToProcessChirho = targetIndexChirho >= 0
    ? [TOPICS_CHIRHO[targetIndexChirho]]
    : TOPICS_CHIRHO;

  for (const topicChirho of topicsToProcessChirho) {
    if (!topicChirho) continue;

    try {
      const paperContentChirho = await generatePaperChirho(topicChirho);
      const outputPathChirho = `${outputDirChirho}${topicChirho.fileNameChirho}`;
      await writeFile(outputPathChirho, paperContentChirho, "utf-8");
      console.log(`  ✅ Written: ${topicChirho.fileNameChirho}`);
    } catch (errorChirho) {
      console.error(`  ❌ Failed: ${topicChirho.fileNameChirho}`, errorChirho);
    }
  }

  console.log("\n🎉 Research generation complete!");
}

mainChirho();
