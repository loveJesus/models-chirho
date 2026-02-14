<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

# Model 7: Topical Passage Classifier & Thematic Search

**Research Paper for loveJesus/models-chirho**
**Date:** 2026-02-14
**Status:** Research Phase

---

# Topical Bible Passage Classification: Fine-Tuning Sentence Transformers for Thematic Verse Retrieval

## Abstract

One of the most common Bible study tasks is finding verses "about" a topic -- prayer, forgiveness, suffering, the second coming. Traditional topical indexes like **Nave's Topical Bible** (public domain, 20,000+ topics, 100,000+ verse references) provide hand-curated mappings but are static, incomplete for nuanced queries, and cannot handle natural language queries like "verses about trusting God when afraid." This model fine-tunes **all-MiniLM-L6-v2** (22M parameters) via contrastive learning to create a Bible-specialized semantic search embedding that maps natural-language topic queries to relevant Bible verses in a shared vector space. Training data is constructed by pairing Nave's Topical Bible topic headings with their referenced verses from the KJV (both public domain), augmented with **Treasury of Scripture Knowledge** cross-references (~340,000 connections, public domain via OpenBible.info) and the **BibleSTS dataset** (6 million verse pairs from Harvard Dataverse). The model learns that "forgiveness" is semantically close to "If we confess our sins, he is faithful and just to forgive us" (1 John 1:9) while distant from "In the beginning God created the heaven and the earth" (Genesis 1:1). This complements existing models: Model 2 finds verse-to-verse cross-references, Model 5 compares the same verse across translations -- this model maps *topics/questions to verses*, enabling natural language Bible search. Targeting >0.85 NDCG@10 on topical retrieval, the model trains in <20 minutes on A100.

**Keywords**: topical Bible, semantic search, sentence transformers, contrastive learning, information retrieval, Nave's Topical Bible

---

## 1. Model Name and Purpose

**Name**: Topical Passage Classifier (topical-passage-classifier-chirho)

**Purpose**: Semantic search model that maps natural language topic queries and theological concepts to relevant Bible verses, enabling "Google-like" search over Scripture that understands meaning rather than just keywords.

**Who Benefits**:
- **Bible students**: Ask "What does the Bible say about anxiety?" and get ranked, relevant verses -- not just keyword matches for "anxiety" but also semantically related passages about worry, fear, trust, peace
- **Pastors/teachers**: Quickly find topically relevant passages for sermon preparation, counseling, and teaching
- **Devotional app users**: "Give me a verse about hope" returns contextually appropriate results
- **Scholars**: Computational analysis of thematic distribution across biblical books, genre-based topical patterns
- **Developers**: Build semantic Bible search APIs, chatbot-style Bible Q&A, and topical recommendation engines

**Differentiation from Existing Models**:
- Model 1 (Theological Guardrails): Classifies *orthodoxy* of statements -- this finds *topically relevant verses*
- Model 2 (Intertextual Reference): Finds *verse-to-verse* connections based on literary dependence -- this finds *query-to-verse* connections based on topical relevance
- Model 3 (Biblical Language Tutor): Parses *grammar/morphology* -- this understands *thematic content*
- Model 4 (Manuscript Variant Analyzer): Compares *textual variants* -- this classifies *topical content*
- Model 5 (Cross-Translation Semantic): Maps *same verse across translations* -- this maps *different topic descriptions to matching verses*
- Model 6 (Biblical Entity Recognizer): Extracts *named entities* (who/where) -- this classifies *themes/topics* (what about)

---

## 2. Architecture

**Base Model**: `sentence-transformers/all-MiniLM-L6-v2` (22M parameters, 384-dimensional embeddings)

**Why all-MiniLM-L6-v2**:
- Extremely efficient: 22M params, 5x faster than BERT-base with comparable quality
- Already pre-trained on 1B+ sentence pairs for semantic similarity
- 384-dimensional output is compact for vector storage (vs. 768 for larger models)
- Excellent balance of quality and speed for retrieval tasks
- Well-supported in the sentence-transformers ecosystem with established fine-tuning pipelines
- Small enough for edge deployment and Cloudflare Workers

**Architecture Details**:
```
Query: "verses about forgiveness"
    |
    v
all-MiniLM-L6-v2 Encoder (shared weights)
    |
    v
384-dim embedding -> cosine similarity -> ranked verses

Verse: "If we confess our sins, he is faithful..."
    |
    v
all-MiniLM-L6-v2 Encoder (shared weights)
    |
    v
384-dim embedding (pre-computed, stored in vector DB)
```

**Inference Flow**:
1. Pre-compute embeddings for all ~31,000 Bible verses (one-time, stored in vector index)
2. At query time, encode the user's topic query into 384-dim vector
3. Retrieve top-K verses by cosine similarity
4. Return ranked results with similarity scores

---

## 3. Training Approach

**Task**: Bi-encoder contrastive learning for asymmetric semantic search (short query -> longer passage)

**Training Strategy**:

### Loss Function: Multiple Negatives Ranking Loss (MNRL)

This is the standard loss for training retrieval models with sentence-transformers. Given a batch of (query, positive_passage) pairs, every other passage in the batch serves as a negative. This is highly efficient -- a batch of 64 pairs yields 64 positives and 63*64 negatives per step.

### Training Stages:

**Stage 1: Topical Anchor Training (~50,000 pairs)**
- Pairs: (Nave's topic heading, referenced KJV verse)
- Example: ("FORGIVENESS", "If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness.")
- This teaches the model to map topic labels to their canonical verses

**Stage 2: Cross-Reference Augmentation (~100,000 pairs)**
- From TSK cross-references: treat (verse_A, verse_B) pairs as topically related
- Example: (Psalm 32:1 "Blessed is he whose transgression is forgiven", Romans 4:7 "Blessed are they whose iniquities are forgiven")
- This teaches the model that cross-referenced passages share topical content

**Stage 3: Hard Negative Mining (~20,000 triplets)**
- Mine hard negatives: verses that share keywords but differ in topic
- Example: Query "God's love", Positive: John 3:16, Hard Negative: "If a man say, I love God, and hateth his brother, he is a liar" (topically about *hypocrisy*, not God's love per se)
- Uses TripletLoss with margin 0.2

### Hyperparameters:
- Learning rate: 2e-5 with cosine annealing
- Batch size: 64 (large batch critical for MNRL effectiveness)
- Epochs: 3 per stage, 9 total
- Warmup: 10% of total steps
- Max sequence length: 128 tokens (query), 256 tokens (passage)
- Optimizer: AdamW
- Temperature: 0.05 for MNRL scaling

---

## 4. Data Sources (All Freely Available)

### Primary Sources

**A. Nave's Topical Bible**
- **Source**: Orville J. Nave, originally published 1896
- **URL**: https://www.naves-topical-bible.com/ (full text), https://archive.org/details/navestopicalbibl00nave (Internet Archive)
- **License**: Public Domain (published 1896, author died 1917)
- **Contents**: 20,000+ topics and subtopics with 100,000+ scripture references. Organized alphabetically by topic (e.g., "ABANDONMENT", "FAITH", "PRAYER", "REDEMPTION")
- **Format**: Structured text with topic headings, sub-topics, and verse references
- **Value**: This is the core training signal -- curated topic-to-verse mappings built over decades of scholarship. Each topic heading becomes a "query" and each referenced verse becomes a "positive passage"

**B. Treasury of Scripture Knowledge (TSK) Cross-References**
- **Source**: R.A. Torrey, originally compiled in the 1800s
- **URL**: https://www.openbible.info/labs/cross-references/ (download ~340,000 cross-refs, 2MB zip)
- **License**: Public Domain (via OpenBible.info, CC BY)
- **Format**: CSV with verse-to-verse pairs and vote counts
- **Contents**: ~340,000 cross-reference connections identifying thematic, verbal, and conceptual links between verses
- **Value**: Massive source of topically-related verse pairs for contrastive training

**C. BibleSTS -- Bible Verse Semantic Textual Similarity Dataset**
- **Source**: Harvard Dataverse
- **URL**: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NNINVB
- **License**: Open access
- **Contents**: 6 million Bible verse pairs across 18 public-domain translations (KJV, ASV, YLT, Darby, BBE, WEB, Geneva, etc.). Each pair categorized as exact match, cross-reference, or neither
- **Format**: Structured dataset with verse IDs, text, and similarity labels
- **Value**: Pre-labeled positive/negative pairs. "Cross-reference" pairs = topically related positives; "neither" pairs = negatives

**D. KJV Bible Text**
- **Source**: Public domain (1769 Cambridge Edition)
- **URL**: https://github.com/scrollmapper/bible_databases
- **License**: Public Domain
- **Contents**: Complete Old and New Testament, ~31,102 verses
- **Value**: Base verse corpus for embedding and retrieval

### Secondary Sources

**E. Torrey's New Topical Textbook**
- **Source**: R.A. Torrey, public domain
- **URL**: Available via https://biblehub.com/topical/
- **License**: Public Domain
- **Contents**: Complementary topical index with different organizational structure than Nave's
- **Value**: Additional topic-to-verse mappings for training augmentation

**F. OpenBible.info Topical Bible**
- **URL**: https://www.openbible.info/topics/
- **License**: CC BY
- **Contents**: Crowdsourced topical verse rankings with user vote scores
- **Value**: Modern, user-rated relevance scores for topic-verse pairs -- can weight training examples by community agreement

**G. Theographic Bible Metadata**
- **URL**: https://github.com/robertrouse/theographic-bible-metadata
- **License**: Open source
- **Contents**: Topic tags and thematic categories for passages
- **Value**: Additional topical labels from knowledge graph perspective

---

## 5. Data Pipeline

### Step 1: Parse Nave's Topical Bible into Structured Pairs

```python
# Pseudocode for data pipeline
# Input: Nave's raw text
# Output: (topic_query, verse_text, verse_ref) tuples

# Example raw entry:
# FORGIVENESS
#   Of Enemies: Matt 5:44; Luke 6:27,35; Rom 12:14,19-21
#   Of Injuries: Matt 5:39-41; Luke 6:29-30
#   Enjoined: Mark 11:25; Luke 6:37; Luke 17:3-4

# Produces:
# ("Forgiveness of enemies", "But I say unto you, Love your enemies...", "Matt 5:44")
# ("Forgiveness of injuries", "But I say unto you, That ye resist not evil...", "Matt 5:39")
```

1. Parse topic headings and sub-headings from Nave's text
2. Resolve verse references to full KJV text using scrollmapper bible_databases
3. Create pairs: (topic_heading + sub_heading, full_verse_text)
4. Deduplicate where same verse appears under multiple topics (keep all pairs -- a verse CAN be relevant to multiple topics)

**Expected output**: ~50,000 (query, passage) pairs from Nave's alone

### Step 2: Add Cross-Reference Pairs from TSK

1. Download OpenBible.info cross-reference data
2. Parse CSV to extract (verse_A_ref, verse_B_ref) pairs
3. Resolve both references to KJV text
4. Filter to pairs with vote_count >= 2 for quality
5. Create training pairs: (verse_A_text, verse_B_text) as semantically related

**Expected output**: ~200,000 high-confidence cross-reference pairs

### Step 3: Integrate BibleSTS Labels

1. Download BibleSTS from Harvard Dataverse
2. Filter to KJV translation pairs (or use any public domain translation)
3. Use "cross-reference" label pairs as positives
4. Use "neither" label pairs with high text overlap but semantic difference as hard negatives

**Expected output**: ~100,000 labeled pairs from BibleSTS

### Step 4: Construct Training Dataset

```
Final training data composition:
- Stage 1: ~50,000 (topic_heading, verse) pairs from Nave's
- Stage 2: ~100,000 (verse, related_verse) pairs from TSK (sampled)
- Stage 3: ~20,000 hard-negative triplets from BibleSTS + mining
- Total: ~170,000 training examples
```

### Step 5: Query Augmentation

To handle diverse query phrasings at inference time, augment Nave's topic headings:
- "FORGIVENESS" -> also generate: "forgiveness", "forgiving others", "verses about forgiveness", "what does the Bible say about forgiving", "how to forgive someone"
- Use simple template-based augmentation (no LLM needed):
  - "{topic}"
  - "verses about {topic}"
  - "what does the Bible say about {topic}"
  - "Bible passages on {topic}"
  - "{topic} in the Bible"

This 5x multiplies Nave's pairs to ~250,000 augmented query-passage pairs

### Step 6: Evaluation Split

- **Train**: 85% of Nave's topics (with all their verses)
- **Validation**: 7.5% of Nave's topics (held-out topics)
- **Test**: 7.5% of Nave's topics (held-out topics)
- Split by topic (not by verse) to test generalization to unseen topics
- TSK cross-references split proportionally

---

## 6. Estimated Training Time on A100

**Model size**: 22M parameters (all-MiniLM-L6-v2)
**Dataset size**: ~170,000 training pairs across 3 stages
**Batch size**: 64
**Steps per epoch**: ~2,656 (Stage 1) + ~1,562 (Stage 2) + ~312 (Stage 3)
**Epochs**: 3 per stage
**Total steps**: ~13,590

**Estimated time**: **12-18 minutes on a single A100 (40GB)**

Rationale:
- all-MiniLM-L6-v2 is ~5x faster than BERT-base for inference/training
- Sentence-transformers training with MNRL is very efficient -- most computation is forward pass through shared encoder
- At batch size 64 on A100: ~4,000 pairs/second for MiniLM
- Stage 1: 250,000 augmented pairs x 3 epochs / 4,000 = ~3 minutes
- Stage 2: 100,000 pairs x 3 epochs / 4,000 = ~1.25 minutes
- Stage 3: 20,000 triplets x 3 epochs / 2,000 (triplet slower) = ~30 seconds
- Total compute: ~5 minutes; with overhead (eval, logging, checkpointing): ~12-18 minutes
- Comfortably within the 30-minute budget

---

## 7. Evaluation Metrics

### Primary Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **NDCG@10** | Normalized Discounted Cumulative Gain at 10 results | >0.85 |
| **MRR** | Mean Reciprocal Rank of first relevant result | >0.80 |
| **Recall@10** | Fraction of relevant verses in top 10 results | >0.75 |
| **Recall@50** | Fraction of relevant verses in top 50 results | >0.90 |
| **MAP** | Mean Average Precision across all queries | >0.70 |

### Baseline Comparisons

| Model | Expected NDCG@10 |
|-------|-----------------|
| BM25 (keyword search on KJV) | ~0.45 |
| all-MiniLM-L6-v2 (zero-shot, no fine-tuning) | ~0.55 |
| OpenAI text-embedding-3-small (zero-shot) | ~0.65 |
| **Ours (topical-passage-classifier-chirho)** | **>0.85** |

### Evaluation Protocol

1. **Held-out topic evaluation**: For each held-out Nave's topic, use the topic heading as query and its referenced verses as ground truth. Measure NDCG@10 and MRR
2. **Natural language query evaluation**: Create 200 natural-language queries (manually written, covering diverse topics: salvation, prayer, suffering, prophecy, creation, end times, etc.) with manually verified relevant verses. Measure retrieval quality
3. **Genre diversity evaluation**: Evaluate separately on queries targeting different genres (narrative, poetry/psalms, prophecy, epistles, wisdom literature) to ensure balanced performance
4. **Cross-topic consistency**: For topics that appear in both Nave's and Torrey's indexes, compare retrieved verse sets -- high overlap validates topical accuracy
5. **User study** (optional): Have 10 Bible study leaders rate top-5 results for 50 queries on a 1-5 relevance scale

---

## 8. bible.systems Integration

### Direct Integration Points

1. **Semantic Bible Search**: Primary search interface for bible.systems -- users type natural language queries and get ranked relevant verses
2. **"Verses About" Feature**: Dedicated UI for topical exploration: click a topic card (Faith, Hope, Love, Prayer, etc.) and see ranked verses with relevance scores
3. **Study Plan Generator**: Given a topic, automatically assemble a week-long Bible reading plan from the most relevant passages
4. **Sermon/Teaching Assistant**: Pastor enters a sermon topic, gets a ranked list of supporting verses with topical relevance scores
5. **Related Topics**: For any displayed verse, show other topics it's relevant to (multi-topic membership from Nave's)
6. **Integration with Model 6 (Entity Recognizer)**: Combine topical search with entity filtering -- "verses about prayer that mention David" = topical query + entity filter
7. **Integration with Model 5 (Cross-Translation)**: Show topically retrieved verses across multiple translations side-by-side

### API Design

```
POST /api-chirho/topical-classifier-chirho/search-chirho
{
  "query_chirho": "What does the Bible say about forgiving enemies?",
  "top_k_chirho": 10,
  "filter_testament_chirho": "both",
  "filter_genre_chirho": null
}

Response:
{
  "results_chirho": [
    {
      "reference_chirho": "Matthew 5:44",
      "text_chirho": "But I say unto you, Love your enemies, bless them that curse you...",
      "score_chirho": 0.94,
      "topics_chirho": ["FORGIVENESS", "ENEMIES", "LOVE"]
    },
    {
      "reference_chirho": "Romans 12:20",
      "text_chirho": "Therefore if thine enemy hunger, feed him; if he thirst, give him drink...",
      "score_chirho": 0.91,
      "topics_chirho": ["FORGIVENESS", "ENEMIES", "CHARITY"]
    }
  ]
}
```

### Deployment

- Pre-computed verse embeddings: 31,000 verses x 384 dims x 4 bytes = ~47MB (fits easily in memory)
- Query embedding computation: <5ms on CPU, <1ms on GPU
- Vector similarity search with HNSW index: <1ms for top-100 results
- Total latency: <10ms end-to-end
- Deployable on Cloudflare Workers with vector store (Vectorize) or any FAISS/Qdrant/Pinecone backend
- Model file (quantized): ~22MB

---

## References

1. Nave, Orville J. "Nave's Topical Bible." 1896. Public Domain. https://www.naves-topical-bible.com/
2. Torrey, R.A. "Treasury of Scripture Knowledge." Public Domain. Via OpenBible.info: https://www.openbible.info/labs/cross-references/
3. BibleSTS: Bible Verse Dataset Pairs for Semantic Textual Similarity. Harvard Dataverse. https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NNINVB
4. Sentence-Transformers: all-MiniLM-L6-v2. Hugging Face. https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
5. "Train and Fine-Tune Sentence Transformers Models." Hugging Face Blog. https://huggingface.co/blog/how-to-train-sentence-transformers
6. ScrollMapper Bible Databases. https://github.com/scrollmapper/bible_databases
7. Theographic Bible Metadata. https://github.com/robertrouse/theographic-bible-metadata
8. BibleNLP Awesome Bible NLP. https://github.com/BibleNLP/awesome-bible-nlp
9. OpenBible.info Topical Bible. https://www.openbible.info/topics/
10. BibleHub Topical Index. https://biblehub.com/topical/
11. "STF: Sentence Transformer Fine-tuning for Topic Categorization." arXiv:2407.03253. https://arxiv.org/html/2407.03253v1

---

## Sources Discovered During Research

1. https://www.naves-topical-bible.com/
2. https://archive.org/details/navestopicalbibl00nave
3. https://www.openbible.info/labs/cross-references/
4. https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NNINVB
5. https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
6. https://huggingface.co/blog/how-to-train-sentence-transformers
7. https://github.com/scrollmapper/bible_databases
8. https://github.com/robertrouse/theographic-bible-metadata
9. https://www.openbible.info/topics/
10. https://biblehub.com/topical/
11. https://arxiv.org/html/2407.03253v1
12. https://sbert.net/docs/sentence_transformer/training_overview.html
13. https://github.com/BibleNLP/awesome-bible-nlp
14. https://huggingface.co/datasets/bible-nlp/biblenlp-corpus
15. https://www.kaggle.com/datasets/oswinrh/bible
16. https://search.dataone.org/view/sha256:93c87b77e61d29d5f10aaf0b273592d5b7052d242769d7afe2cfe8d82cb745e5
17. https://www.kaggle.com/datasets/nileedixon/paired-bible-verses-for-semantic-similarity
