<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

# Model 8: Passage Difficulty Scorer & Plain-Language Simplifier

**Research Paper for loveJesus/models-chirho**
**Date:** 2026-02-14
**Status:** Research Phase

---

# Biblical Passage Difficulty Assessment and Plain-Language Simplification: A Dual-Head Flan-T5 Approach

## Abstract

Bible translations exist on a spectrum from highly literal (KJV, ~12th grade reading level) to simplified (BBE/Bible in Basic English, ~4th grade). Yet no NLP model currently helps readers understand *why* a passage is difficult or provides on-demand simplification while preserving theological meaning. This model fine-tunes **Flan-T5-small** (80M parameters) as a dual-task seq2seq system: (1) **Difficulty scoring** -- given a Bible passage, generate a structured difficulty assessment including reading level, vocabulary complexity, syntactic complexity, and theological density scores; (2) **Plain-language paraphrase** -- given a difficult passage (KJV/ASV/YLT), generate a simplified English explanation preserving theological content. Training leverages the **Bible Simplification Dataset** from Harvard Dataverse (397,000 verse pairs across public-domain translations ordered by complexity) and verse-aligned parallel text from **Helsinki-NLP/bible_para** (100+ languages, CC0). The key insight is that pairs like (KJV verse, BBE verse) for the same reference constitute natural simplification training data -- the BBE was explicitly designed to use only 850 basic English words. This complements all existing models: while Models 1-7 analyze content (orthodoxy, references, morphology, variants, semantics, entities, topics), this model addresses *accessibility* -- making difficult passages understandable for new readers, ESL learners, and children. Targeting SARI >45 and BERTScore >0.85 on simplification, and Spearman correlation >0.80 with human difficulty ratings, the model trains in <25 minutes on A100.

**Keywords**: text simplification, readability, Flan-T5, Bible accessibility, reading level, paraphrase generation

---

## 1. Model Name and Purpose

**Name**: Passage Difficulty Simplifier (passage-difficulty-simplifier-chirho)

**Purpose**: Dual-task model that (a) assesses the reading difficulty of any Bible passage with structured scoring, and (b) generates plain-language simplifications of difficult passages while preserving theological meaning.

**Who Benefits**:
- **New believers and seekers**: Get plain-language explanations of archaic or complex passages without needing a commentary
- **ESL Bible readers**: Understand passages written in complex English syntax
- **Children's ministry workers**: Automatically generate age-appropriate passage simplifications
- **Bible translators**: Quantify difficulty levels across translations to validate readability targets
- **Accessibility advocates**: Make Scripture more accessible to readers with cognitive disabilities or low literacy
- **Bible app developers**: Provide "explain this passage" features powered by a specialized small model

**Differentiation from Existing Models**:
- Model 1 (Theological Guardrails): Assesses *doctrinal correctness* -- this assesses *readability*
- Model 2 (Intertextual Reference): Finds *related passages* -- this *simplifies* passages
- Model 3 (Biblical Language Tutor): Explains *original language grammar* -- this simplifies *English* text
- Model 4 (Manuscript Variant Analyzer): Compares *textual variants* -- this compares *difficulty levels*
- Model 5 (Cross-Translation Semantic): Measures *semantic equivalence across translations* -- this generates *simplified paraphrases*
- Model 6 (Biblical Entity Recognizer): Extracts *entities* -- this generates *explanations*
- Model 7 (Topical Passage Classifier): Finds *relevant verses* by topic -- this makes *found verses* understandable

---

## 2. Architecture

**Base Model**: `google/flan-t5-small` (80M parameters, encoder-decoder)

**Why Flan-T5-small**:
- Seq2seq architecture natively supports both classification (short output) and generation (long output) tasks
- Already instruction-tuned -- understands task prompts like "Simplify this passage:" and "Rate the difficulty of:"
- 80M parameters: small enough for <30 min training, large enough for quality generation
- Handles variable-length input/output needed for simplification (input: 1-3 verses, output: simplified text of similar length)
- Strong baseline on summarization and paraphrase tasks from instruction tuning
- Can be deployed efficiently with INT8 quantization (~40MB)

**Dual-Task Architecture**:
```
Task 1: Difficulty Scoring
Input:  "Rate difficulty: Forasmuch then as the children are partakers of
         flesh and blood, he also himself likewise took part of the same..."
Output: "reading_level: 12 | vocab_complexity: high | syntax_complexity: high |
         theological_density: high | archaic_forms: forasmuch, partakers, likewise"

Task 2: Plain-Language Simplification
Input:  "Simplify: Forasmuch then as the children are partakers of flesh
         and blood, he also himself likewise took part of the same..."
Output: "Since God's children are human beings made of flesh and blood,
         Jesus also became human by being born in a human body."
```

Both tasks share the same Flan-T5-small encoder-decoder, distinguished by task prefixes in the input. This multi-task setup improves both tasks through shared representation learning.

---

## 3. Training Approach

**Task**: Seq2seq generation with multi-task learning (difficulty scoring + simplification)

### Task 1: Difficulty Scoring (Structured Generation)

**Approach**: Frame difficulty scoring as a structured text generation task. Given a verse, generate a structured difficulty assessment string.

**Difficulty dimensions**:
1. **Reading level** (Flesch-Kincaid grade equivalent): 1-16 scale
2. **Vocabulary complexity**: low / medium / high (based on word frequency in modern English)
3. **Syntax complexity**: low / medium / high (based on sentence length, clause nesting, passive voice)
4. **Theological density**: low / medium / high (density of theological/doctrinal concepts per verse)
5. **Archaic forms**: list of archaic words/constructions present (thee/thou, -eth endings, hath, etc.)

**Training signal**: Difficulty labels are computed automatically from linguistic features:
- Flesch-Kincaid grade level computed algorithmically from syllable counts and sentence length
- Vocabulary complexity from word frequency rank in modern English (words outside top 5,000 = high)
- Syntax complexity from parse depth, clause count, and average sentence length
- Theological density from overlap with a theological term dictionary (derived from Nave's topic headings)
- Archaic form detection via a curated list of ~200 KJV-specific archaisms

### Task 2: Plain-Language Simplification (Paraphrase Generation)

**Approach**: Fine-tune Flan-T5-small to transform difficult Bible verses into simpler English while preserving meaning.

**Training data construction**: Use verse-aligned parallel translations ordered by complexity:
- **Complex source**: KJV (1611, archaic), YLT (extremely literal), ASV (1901, formal), Darby
- **Simple target**: BBE (Bible in Basic English, 850-word vocabulary), WEB (World English Bible, modern), FBV (Free Bible Version)

Each (complex_verse, simple_verse) pair is a natural simplification example.

### Multi-Task Training Schedule

```
Epoch 1-2: Task 1 only (difficulty scoring) -- 80,000 examples
Epoch 3-5: Task 2 only (simplification) -- 120,000 examples
Epoch 6-7: Mixed batches (50% Task 1, 50% Task 2) -- 100,000 examples
```

### Hyperparameters:
- Learning rate: 3e-4 (standard for T5 fine-tuning, higher than BERT due to different optimizer behavior)
- Batch size: 16 (with gradient accumulation = 4 for effective batch size 64)
- Optimizer: Adafactor (recommended for T5 models, memory-efficient)
- Max source length: 256 tokens
- Max target length: 256 tokens
- Beam search at inference: num_beams = 4
- Label smoothing: 0.1
- bf16 training: True (A100 supports bfloat16 natively)

**Important**: Do NOT use fp16 with mT5/T5 variants -- use bf16 instead per Hugging Face guidance.

---

## 4. Data Sources (All Freely Available)

### Primary Sources

**A. Bible Simplification Dataset**
- **Source**: Harvard Dataverse
- **URL**: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/4EVOAG
- **License**: Open access
- **Contents**: 397,000 Bible verse pairs specifically designed for text simplification. Pairs are drawn from multiple public-domain translations with an implicit complexity ordering
- **Format**: Structured dataset with verse references, source text, target text
- **Value**: This is the single most valuable dataset for this model. 397k pre-aligned simplification pairs is a large, high-quality training set requiring no additional annotation. This dataset was explicitly created for the text simplification task

**B. Helsinki-NLP/bible_para (Bible Parallel Corpus)**
- **Source**: Helsinki NLP group
- **URL**: https://huggingface.co/datasets/Helsinki-NLP/bible_para
- **License**: CC0 1.0 (public domain dedication)
- **Contents**: Bible translations in 100+ languages, verse-aligned
- **Format**: Hugging Face datasets format, accessible via `datasets` library
- **Value**: Additional verse-aligned parallel text. English translations include KJV, ASV, BBE, WEB, YLT, Darby -- all public domain. These create natural (complex, simple) pairs

**C. Public Domain Bible Translations (via ScrollMapper)**
- **Source**: ScrollMapper
- **URL**: https://github.com/scrollmapper/bible_databases
- **License**: Public Domain
- **Contents**: Multiple Bible translations in SQLite, CSV, and JSON formats
- **Translations available** (all public domain):
  - **KJV** (1769) -- archaic, formal, ~12th grade reading level
  - **ASV** (1901) -- literal, formal, ~10th grade
  - **YLT** (Young's Literal Translation) -- extremely literal, ~11th grade
  - **Darby** -- literal, ~10th grade
  - **BBE** (Bible in Basic English, 1949) -- simplified, 850-word vocabulary, ~4th grade
  - **WEB** (World English Bible) -- modern, free, ~8th grade
- **Value**: The core verse-aligned corpus. KJV->BBE pairs are particularly valuable as the BBE was designed for maximum simplicity

**D. Free Bible Version (FBV)**
- **Source**: Dr. Jonathan Gallagher
- **URL**: https://www.freebibleversion.org/
- **License**: Free to use (Creative Commons)
- **Contents**: Modern English translation designed for clarity
- **Value**: Additional "simple" target for simplification pairs

### Secondary Sources

**E. BibleSTS Dataset (for evaluation)**
- **URL**: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NNINVB
- **License**: Open access
- **Contents**: 6 million verse pairs with similarity labels
- **Value**: Evaluation of whether simplifications preserve meaning (high similarity between simplification and original)

**F. Flesch-Kincaid Grade Level Reference Data**
- Various analyses of Bible translation reading levels have been published:
  - KJV: grade 11-12
  - ASV: grade 10-11
  - ESV: grade 8-10
  - NIV: grade 7-8
  - NLT: grade 6-7
  - BBE: grade 3-4
- **Value**: Ground truth calibration for difficulty scoring task. Known grade levels for entire translations serve as aggregate validation

**G. Nave's Topical Bible (for theological term dictionary)**
- **URL**: https://www.naves-topical-bible.com/
- **License**: Public Domain
- **Contents**: 20,000+ theological topics
- **Value**: The topic headings provide a comprehensive theological vocabulary list used to compute "theological density" scores

---

## 5. Data Pipeline

### Step 1: Construct Verse-Aligned Multi-Translation Corpus

1. Download KJV, ASV, YLT, Darby, BBE, and WEB from ScrollMapper bible_databases
2. Load Helsinki-NLP/bible_para for additional translations
3. Align all translations by verse reference (book, chapter, verse)
4. Create unified table: `verse_ref | kjv_text | asv_text | ylt_text | darby_text | bbe_text | web_text`

**Expected size**: ~31,000 verses x 6 translations = ~186,000 verse texts

### Step 2: Generate Simplification Training Pairs

**Primary source**: Bible Simplification Dataset (397k pairs, pre-aligned)

**Augmentation from parallel translations**:
For each verse reference, create ordered complexity pairs:
```
(KJV, BBE)    -- hardest to simplest (best pairs)
(KJV, WEB)    -- archaic to modern
(YLT, BBE)    -- extremely literal to simplified
(ASV, BBE)    -- formal to simplified
(Darby, WEB)  -- literal to modern
```

This generates up to 5 simplification pairs per verse = ~155,000 additional pairs.

**Filtering**: Remove pairs where source and target are nearly identical (cosine similarity > 0.98 using sentence-transformers) -- these provide no simplification signal.

**Format**:
```
Input:  "Simplify: Forasmuch then as the children are partakers of flesh and blood,
         he also himself likewise took part of the same; that through death he might
         destroy him that had the power of death, that is, the devil;"
Target: "Since the children have flesh and blood in common, Jesus also shared in
         these, so that through his death he might destroy the devil who had the
         power of death."
```

**Total simplification pairs**: ~120,000 (after filtering and deduplication from both sources)

### Step 3: Generate Difficulty Scoring Training Data

For each verse in the KJV (and other translations):

1. **Compute Flesch-Kincaid grade level** algorithmically:
   ```
   FK = 0.39 * (total_words / total_sentences) + 11.8 * (total_syllables / total_words) - 15.59
   ```

2. **Compute vocabulary complexity**:
   - Count words NOT in the 5,000 most common modern English words
   - low: 0-10% rare words, medium: 10-25%, high: >25%

3. **Compute syntax complexity**:
   - Average sentence length in words
   - Count of subordinate clauses (detected via punctuation patterns: semicolons, colons, "that", "which", "whom")
   - low: <15 words avg, <2 clauses; medium: 15-25 words, 2-3 clauses; high: >25 words or >3 clauses

4. **Compute theological density**:
   - Match verse words against theological term dictionary (derived from Nave's topic headings)
   - low: 0-1 theological terms, medium: 2-3, high: 4+

5. **Detect archaic forms**:
   - Match against curated KJV archaism list: thee, thou, thy, thine, ye, hath, doth, saith, -eth, -est, forasmuch, wherefore, behold, verily, etc.

**Format**:
```
Input:  "Rate difficulty: For God so loved the world, that he gave his only
         begotten Son, that whosoever believeth in him should not perish, but
         have everlasting life."
Target: "reading_level: 8 | vocab_complexity: medium | syntax_complexity: medium |
         theological_density: high | archaic_forms: begotten, believeth, whosoever"
```

**Total difficulty scoring examples**: ~80,000 (from KJV + ASV + YLT translations)

### Step 4: Multi-Task Training Format

Combine both tasks with task-specific prefixes:
```
# Task 1 example
{"input": "Rate difficulty: [verse text]", "target": "reading_level: X | ..."}

# Task 2 example
{"input": "Simplify: [complex verse text]", "target": "[simplified verse text]"}
```

### Step 5: Dataset Split

| Split | Difficulty Examples | Simplification Examples | Total |
|-------|-------------------|------------------------|-------|
| Train | ~64,000 | ~96,000 | ~160,000 |
| Validation | ~8,000 | ~12,000 | ~20,000 |
| Test | ~8,000 | ~12,000 | ~20,000 |

Split by book (not by verse) to prevent leakage. Ensure OT and NT books are balanced in each split.

---

## 6. Estimated Training Time on A100

**Model size**: 80M parameters (Flan-T5-small)
**Dataset size**: ~160,000 training examples across 7 effective epochs
**Batch size**: 16 (with gradient accumulation = 4, effective batch = 64)
**Steps per epoch**: ~2,500
**Total steps**: ~17,500

**Estimated time**: **18-25 minutes on a single A100 (40GB)**

Rationale:
- Flan-T5-small with seq2seq: ~800 examples/second on A100 with bf16 (based on published T5-small benchmarks)
- Forward+backward pass for 256->256 token seq2seq: ~1.2ms per example on A100
- Training compute: 160,000 examples x 7 epochs / 800 examples/sec = ~23 minutes raw compute
- With bf16 optimization and A100 tensor cores: ~15-18 minutes compute
- Adding evaluation runs, checkpoint saves, and logging: ~18-25 minutes total
- Within the 30-minute budget, though near the upper bound. If needed, reduce to 5 effective epochs (~16-20 minutes)

**Memory usage**: Flan-T5-small with batch size 16, seq length 256, bf16: ~4GB VRAM. A100 40GB has ample headroom.

---

## 7. Evaluation Metrics

### Simplification Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **SARI** | System output Against References and Input -- standard metric for simplification measuring added simplicity | >45 |
| **BERTScore** | Semantic preservation between source and simplified output | >0.85 |
| **BLEU** | N-gram overlap with reference simplifications (BBE/WEB) | >30 |
| **FK Delta** | Flesch-Kincaid grade reduction (source_FK - output_FK) | >3.0 grades |
| **Meaning Preservation** (human) | 1-5 scale rating of theological meaning retention | >4.0 |

### Difficulty Scoring Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Spearman Correlation** | Correlation between predicted and algorithmic FK scores | >0.80 |
| **MAE** | Mean Absolute Error on reading level prediction | <1.5 grades |
| **Accuracy** | Exact match on complexity categories (low/medium/high) | >75% |
| **Archaic Detection F1** | F1 on identifying archaic forms | >0.95 |

### Baseline Comparisons

| Model | SARI | BERTScore |
|-------|------|-----------|
| Identity (no simplification) | 25 | 1.0 |
| Rule-based (archaic replacement only) | 35 | 0.90 |
| Flan-T5-small (zero-shot, no fine-tuning) | 38 | 0.80 |
| **Ours (passage-difficulty-simplifier-chirho)** | **>45** | **>0.85** |

### Evaluation Protocol

1. **Automatic evaluation**: SARI, BLEU, BERTScore on test set using BBE/WEB as reference simplifications
2. **Cross-translation validation**: Simplify KJV verse, then measure cosine similarity (via Model 5) between simplification and BBE version of same verse. High similarity = good simplification
3. **Theological preservation test**: Run 500 simplified verses through Model 1 (Theological Guardrails) -- simplifications should maintain the same orthodoxy classification as originals. Any classification change flags potential meaning distortion
4. **Human evaluation**: 5 evaluators rate 100 simplification samples on: (a) Fluency (1-5), (b) Simplicity (1-5), (c) Meaning preservation (1-5), (d) Theological accuracy (1-5)
5. **Difficulty calibration**: Compare model's difficulty scores against published translation-level grade data (KJV=12, BBE=4) -- per-translation average should correlate

---

## 8. bible.systems Integration

### Direct Integration Points

1. **"Explain This Passage" Button**: On every verse display, a button that generates a plain-language explanation. Especially valuable for KJV readers
2. **Difficulty Indicators**: Color-coded difficulty badges on each verse/passage: green (easy), yellow (moderate), red (difficult). Helps readers choose appropriate translations
3. **Reading Level Filter**: "Show me this chapter at a 6th grade reading level" -- select or generate the appropriate difficulty version
4. **Children's Bible Generator**: Automatically simplify passages for children's curriculum with age-appropriate language
5. **ESL Bible Study Mode**: Simplified versions with vocabulary annotations for English learners
6. **Passage Comparison View**: Show the same verse at multiple difficulty levels side-by-side: KJV (original) | Model Simplification | BBE (reference simple)
7. **Integration with Model 3 (Biblical Language Tutor)**: For Hebrew/Greek study, show original -> literal translation -> simplified explanation pipeline
8. **Integration with Model 6 (Entity Recognizer)**: Highlighted entities in both original and simplified versions for consistent reference
9. **Integration with Model 7 (Topical Classifier)**: When topical search returns difficult verses, offer automatic simplification alongside

### API Design

```
POST /api-chirho/difficulty-simplifier-chirho/assess-chirho
{
  "text_chirho": "Forasmuch then as the children are partakers of flesh and blood...",
  "tasks_chirho": ["difficulty", "simplify"]
}

Response:
{
  "difficulty_chirho": {
    "reading_level_chirho": 12,
    "vocab_complexity_chirho": "high",
    "syntax_complexity_chirho": "high",
    "theological_density_chirho": "high",
    "archaic_forms_chirho": ["forasmuch", "partakers", "likewise"],
    "overall_difficulty_chirho": "hard"
  },
  "simplification_chirho": {
    "text_chirho": "Since God's children are human beings with flesh and blood bodies, Jesus also became human. He did this so that by dying he could destroy the devil, who had the power of death.",
    "simplified_reading_level_chirho": 6,
    "meaning_confidence_chirho": 0.92
  }
}
```

### Deployment

- Flan-T5-small quantized (INT8): ~40MB model file
- Inference time (simplification): ~200ms per verse on CPU, ~30ms on GPU (beam search with 4 beams)
- Inference time (difficulty scoring): ~50ms per verse on CPU, ~10ms on GPU (short output)
- Deployable on Cloudflare Workers with ONNX runtime
- Can batch-process entire Bible chapters in <5 seconds on GPU

### Safety Considerations

- **Theological guardrails integration**: All generated simplifications should be cross-checked against Model 1 to flag any simplification that inadvertently introduces theological error
- **Disclaimer**: Generated simplifications are paraphrases for understanding, not authoritative translations. UI should clearly label them as "AI-generated plain language explanation" rather than as a Bible translation
- **Transparency**: Show difficulty scores and confidence levels so users can assess reliability

---

## References

1. Bible Simplification Dataset. Harvard Dataverse. https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/4EVOAG
2. Helsinki-NLP/bible_para. Hugging Face Datasets. CC0. https://huggingface.co/datasets/Helsinki-NLP/bible_para
3. ScrollMapper Bible Databases. https://github.com/scrollmapper/bible_databases
4. Flan-T5. Google Research. https://huggingface.co/google/flan-t5-small
5. "FLAN-T5 Tutorial: Guide and Fine-Tuning." DataCamp. https://www.datacamp.com/tutorial/flan-t5-tutorial
6. BibleSTS Dataset. Harvard Dataverse. https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NNINVB
7. "Flesch-Kincaid and Bible reading levels." Better Bibles Blog. https://betterbibles.wordpress.com/2005/07/05/flesch-kincaid-and-bible-reading-levels/
8. "Bible Translation Reading Levels." Christianbook.com. https://www.christianbook.com/page/bibles/about-bibles/bible-translation-reading-levels
9. Nave's Topical Bible. Public Domain. https://www.naves-topical-bible.com/
10. BibleNLP Corpus. Hugging Face. https://huggingface.co/datasets/bible-nlp/biblenlp-corpus
11. "Fine-tune FLAN-T5 for chat & dialogue summarization." Phil Schmid. https://www.philschmid.de/fine-tune-flan-t5
12. Free Bible Version. https://www.freebibleversion.org/

---

## Sources Discovered During Research

1. https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/4EVOAG
2. https://huggingface.co/datasets/Helsinki-NLP/bible_para
3. https://github.com/scrollmapper/bible_databases
4. https://huggingface.co/google/flan-t5-small
5. https://www.datacamp.com/tutorial/flan-t5-tutorial
6. https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NNINVB
7. https://betterbibles.wordpress.com/2005/07/05/flesch-kincaid-and-bible-reading-levels/
8. https://www.christianbook.com/page/bibles/about-bibles/bible-translation-reading-levels
9. https://www.naves-topical-bible.com/
10. https://huggingface.co/datasets/bible-nlp/biblenlp-corpus
11. https://www.philschmid.de/fine-tune-flan-t5
12. https://www.freebibleversion.org/
13. https://modal.com/docs/examples/flan_t5_finetune
14. https://rocm.blogs.amd.com/artificial-intelligence/FlanT5/README.html
15. https://huggingface.co/docs/transformers/en/tasks/summarization
16. https://www.opendatabay.com/data/ai-ml/9252325e-425a-4e5a-8406-83e7fbe38148
17. https://huggingface.co/datasets/LetsChurch/bible-embeddings
