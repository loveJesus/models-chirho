<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

# Model 6: Biblical Named Entity Recognizer

**Research Paper for loveJesus/models-chirho**
**Date:** 2026-02-14
**Status:** Research Phase

---

# Biblical Named Entity Recognition: Fine-Tuning DistilBERT for People, Places, and Divine References in Scripture

## Abstract

Standard NER models trained on general corpora (OntoNotes 5, CoNLL-2003) systematically fail on biblical text. Research has shown that many samples in OntoNotes do not contain PERSON labels even when they contain biblical names, causing models to learn to ignore names like "Melchizedek," "Jehoshaphat," or "Nebuchadnezzar." This model addresses that gap by fine-tuning **DistilBERT-base** (66M parameters) for token-level classification on a custom biblical NER dataset derived from multiple freely licensed sources: the **TIPNR dataset** (STEPBible, CC BY 4.0), **Theographic Bible Metadata** (knowledge graph of ~3,000 people and ~1,200 places), and **MetaV** (word-level "Who, Where, When" annotations for every KJV passage). The model recognizes six entity types specifically designed for biblical text: PERSON (individual people), DIVINE (God, Christ, Holy Spirit, divine titles), PEOPLE_GROUP (nations, tribes, ethnic groups), PLACE (cities, regions, bodies of water), EVENT (battles, covenants, miracles), and ARTIFACT (Ark of the Covenant, Temple, altars). Trained on ~35,000 annotated sentences from the KJV (public domain), the model targets >90% F1 on biblical entities where general-purpose NER achieves <60%. This is complementary to existing models 1-5: while Model 2 (Intertextual Reference Network) finds cross-references between passages and Model 5 (Cross-Translation Semantic) compares translations, this model extracts the structured entities *within* passages, enabling knowledge graph construction, entity-linked search, and relationship extraction across the entire Bible.

**Keywords**: named entity recognition, biblical NLP, DistilBERT, token classification, knowledge graph, STEPBible

---

## 1. Model Name and Purpose

**Name**: Biblical Entity Recognizer (biblical-entity-recognizer-chirho)

**Purpose**: Token-level named entity recognition specifically for biblical text, identifying and classifying mentions of people, divine references, people groups, places, events, and artifacts throughout Scripture.

**Who Benefits**:
- **Bible students**: Search for "all places Paul visited" or "every mention of the Ark" with structured results
- **Scholars**: Automated entity extraction for digital humanities research, social network analysis of biblical characters, geographic information systems for biblical geography
- **Developers**: Entity-linked Bible search APIs, knowledge graph population, relationship extraction pipelines
- **Translators**: Identify entity mentions that need consistent translation across passages

**Differentiation from Existing Models**:
- Model 1 (Theological Guardrails): Classifies *statements* as orthodox/heretical -- this model extracts *entities* from text
- Model 2 (Intertextual Reference): Finds *passage-level* connections -- this model finds *word-level* entity spans
- Model 3 (Biblical Language Tutor): Parses *morphology* of Hebrew/Greek -- this model classifies *semantic entity types* in English
- Model 4 (Manuscript Variant Analyzer): Compares *textual variants* -- this model recognizes *named entities* in established text
- Model 5 (Cross-Translation Semantic): Compares *meaning across translations* -- this model extracts *structured data* from single translations

---

## 2. Architecture

**Base Model**: `distilbert-base-uncased` (66M parameters)

**Why DistilBERT**:
- 40% smaller than BERT-base with 97% of its language understanding capability
- Fast inference (~5ms per sentence on GPU) suitable for real-time Bible search
- Well-established for NER tasks: `dslim/distilbert-NER` demonstrates strong performance on CoNLL-2003
- Small enough to train on a single A100 in <30 minutes with 35k examples
- Can be quantized to INT8 for edge deployment (mobile Bible apps)

**Architecture Details**:
```
DistilBERT-base (6 layers, 768 hidden, 12 attention heads)
    |
    v
Token Classification Head (768 -> 13 labels)
    |
    v
BIO-tagged output: B-PERSON, I-PERSON, B-DIVINE, I-DIVINE,
                    B-PEOPLE_GROUP, I-PEOPLE_GROUP, B-PLACE, I-PLACE,
                    B-EVENT, I-EVENT, B-ARTIFACT, I-ARTIFACT, O
```

**Entity Schema** (6 types, BIO encoding = 13 labels):

| Entity Type | Description | Examples |
|------------|-------------|----------|
| PERSON | Individual biblical figures | Abraham, Moses, Paul, Mary Magdalene |
| DIVINE | God, Christ, Holy Spirit, divine titles | the LORD, Jesus Christ, the Almighty, Spirit of God |
| PEOPLE_GROUP | Nations, tribes, ethnic groups | Israelites, Philistines, tribe of Judah, Samaritans |
| PLACE | Geographic locations | Jerusalem, Sea of Galilee, Mount Sinai, Babylon |
| EVENT | Named events, battles, covenants | the Exodus, Passover, the Flood, Day of Pentecost |
| ARTIFACT | Sacred objects, structures | Ark of the Covenant, the Temple, brazen serpent |

---

## 3. Training Approach

**Task**: Token classification (sequence labeling) with BIO tagging

**Training Strategy**:

1. **Pre-processing**: Tokenize KJV text with DistilBERT tokenizer; align BIO tags with WordPiece sub-tokens (propagate B-/I- tags to sub-tokens, or use first-sub-token-only strategy)
2. **Fine-tuning**: Standard supervised token classification with cross-entropy loss
3. **Class Imbalance Handling**: Weighted loss function -- O tokens vastly outnumber entity tokens. Use inverse frequency weighting or focal loss
4. **Hyperparameters**:
   - Learning rate: 5e-5 with linear warmup (10% of steps)
   - Batch size: 32
   - Epochs: 5
   - Max sequence length: 256 tokens (sufficient for individual verses + context)
   - Optimizer: AdamW with weight decay 0.01
   - Label smoothing: 0.1

**Why Token Classification (not Seq2Seq)**:
- NER is inherently a token-level task -- each word gets a label
- DistilBERT's bidirectional attention captures left+right context needed for disambiguation (e.g., "Jordan" as person vs. river)
- Far more efficient than generating entity strings via seq2seq
- Direct BIO output integrates cleanly with standard NER pipelines (spaCy, Hugging Face)

---

## 4. Data Sources (All Freely Available)

### Primary Sources

**A. TIPNR -- Translators Individualised Proper Names with all References**
- **Source**: STEPBible (Tyndale House, Cambridge)
- **URL**: https://github.com/STEPBible/STEPBible-Data
- **License**: CC BY 4.0
- **Contents**: Every proper noun in the Bible, linked to Hebrew/Greek forms, separated into individual people, places, and things. Each entry includes exhaustive verse references, parent/partner/sibling/offspring relationships, geolocation data, and descriptions
- **Format**: Tab-separated text file
- **Value**: Gold-standard entity-to-verse mappings. Provides the complete list of which entities appear in which verses, enabling automatic BIO tag generation

**B. Theographic Bible Metadata**
- **Source**: Robert Rouse / viz.bible
- **URL**: https://github.com/robertrouse/theographic-bible-metadata
- **License**: Open source
- **Contents**: Knowledge graph of ~3,000 people, ~1,200 places, time periods, and passages. Available as JSON and CSV
- **Format**: CSV (People.csv, Places.csv, Events.csv, Books.csv) and nested JSON
- **Value**: Structured entity type information (person roles, place types, event categories) used to assign entity type labels

**C. MetaV Bible Metadata**
- **Source**: Nilpo / viz.bible
- **URL**: https://github.com/Nilpo/bible-metadata
- **License**: Public Domain / Creative Commons
- **Contents**: "Who, Where, and When" of every passage at word-level detail. Includes Words Index table linking entities to individual word positions in the KJV text
- **Format**: SQLite database / CSV
- **Value**: Word-level entity annotations -- the closest thing to pre-existing NER annotations for biblical text. Maps entities directly to word positions, drastically reducing manual annotation effort

**D. BibleNLP Biblical Names Data**
- **Source**: BibleNLP (Partnership of Applied Biblical NLP)
- **URL**: https://github.com/BibleNLP/biblical-names-data
- **License**: Open
- **Contents**: Biblical name lists with annotations designed to address NER gaps in standard models
- **Value**: Supplementary entity gazetteer for name normalization and disambiguation

**E. KJV Bible Text**
- **Source**: Public domain (1769 Cambridge Edition)
- **URL**: Available via multiple sources including https://github.com/scrollmapper/bible_databases
- **License**: Public Domain
- **Contents**: Complete Old and New Testament text
- **Value**: Base text for annotation and training

### Secondary Sources

**F. OpenBible.info Geocoding Data**
- **URL**: https://github.com/openbibleinfo/Bible-Geocoding-Data
- **License**: CC BY
- **Contents**: Latitude/longitude coordinates for every identifiable place in the Bible
- **Value**: Place entity validation and disambiguation

**G. Macula Hebrew/Greek Linguistic Datasets**
- **URLs**: https://github.com/Clear-Bible/macula-hebrew, https://github.com/Clear-Bible/macula-greek
- **License**: CC BY 4.0
- **Contents**: Syntax trees, morphology, and linguistic annotations including referent tracking
- **Value**: Cross-validation of entity mentions against original language annotations

---

## 5. Data Pipeline

### Step 1: Entity Gazetteer Construction

```
TIPNR (all proper names + verse refs)
    + Theographic (entity type classification)
    + BibleNLP names (supplementary names)
    = Master Entity Gazetteer
      {entity_name, entity_type, aliases, verse_references[]}
```

Parse TIPNR TSV to extract: entity name, disambiguated individual ID, entity type (person/place/thing), and all verse references. Cross-reference with Theographic CSV to assign fine-grained types (PERSON vs. DIVINE vs. PEOPLE_GROUP; PLACE sub-typed by geographic feature; etc.).

**Expected size**: ~8,000 unique entities with ~380,000 total mentions across ~31,000 verses.

### Step 2: Automatic BIO Tag Generation

For each verse in the KJV:
1. Retrieve all entities known to appear in that verse (from TIPNR verse references)
2. Use MetaV word-level index to locate exact token positions of entity mentions
3. Apply BIO tags: B-{TYPE} for first token of entity span, I-{TYPE} for continuation tokens, O for non-entity tokens
4. Handle multi-word entities: "Sea of Galilee" -> B-PLACE I-PLACE I-PLACE
5. Handle ambiguity: When same surface form maps to multiple entities (e.g., "James" = James son of Zebedee vs. James brother of Jesus), use verse-level TIPNR disambiguation

### Step 3: Quality Assurance

- **Fuzzy matching**: KJV text uses archaic forms ("Jehovah" vs. "LORD", "shewed" vs. "showed"). Build a mapping table of KJV-specific orthographic variants
- **Context window**: Present each verse with +/- 1 verse context (256 token window) for better disambiguation
- **Random audit**: Manually review 500 randomly sampled annotated sentences to estimate automatic annotation accuracy; target >95% precision

### Step 4: Dataset Split

| Split | Sentences | Entity Mentions |
|-------|-----------|-----------------|
| Train | ~28,000 | ~300,000 |
| Validation | ~3,500 | ~40,000 |
| Test | ~3,500 | ~40,000 |

Split by book to avoid data leakage (e.g., train on Genesis-Malachi + Matthew-Romans, validate on 1 Corinthians-Philippians, test on Colossians-Revelation). Ensure all 6 entity types are represented in each split.

### Step 5: Training Data Format

Convert to Hugging Face `datasets` format compatible with `TokenClassification`:
```json
{
  "tokens": ["And", "God", "said", "unto", "Abraham", ",", "Get", "thee", "out", "of", "thy", "country"],
  "ner_tags": [0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0]
}
```
Where tag IDs map to: 0=O, 1=B-DIVINE, 2=I-DIVINE, 3=B-PERSON, 4=I-PERSON, ...

---

## 6. Estimated Training Time on A100

**Model size**: 66M parameters (DistilBERT-base)
**Dataset size**: ~28,000 training sentences, average ~25 tokens each = ~700,000 tokens
**Batch size**: 32
**Steps per epoch**: ~875
**Epochs**: 5
**Total steps**: ~4,375

**Estimated time**: **8-15 minutes on a single A100 (40GB)**

Rationale:
- DistilBERT processes ~3,000 sentences/second on A100 for token classification (based on published benchmarks showing DistilBERT is ~2x faster than BERT-base, and BERT-base processes ~1,500 sentences/second on A100)
- 28,000 sentences x 5 epochs = 140,000 forward+backward passes
- At 3,000 sentences/second: ~47 seconds per epoch, ~4 minutes total compute
- Adding optimizer steps, gradient accumulation, and evaluation: ~8-15 minutes total
- Well within the 30-minute budget even with conservative estimates

---

## 7. Evaluation Metrics

### Primary Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Entity-level F1** (strict) | Exact span + type match | >0.90 |
| **Entity-level F1** (partial) | Partial span overlap + correct type | >0.93 |
| **Token-level F1** | Per-token BIO tag accuracy | >0.95 |
| **Per-type F1** | F1 for each of 6 entity types | >0.85 each |

### Baseline Comparisons

| Model | Expected Biblical Entity F1 |
|-------|---------------------------|
| `dslim/distilbert-NER` (off-the-shelf) | ~0.55 (known poor on biblical names) |
| `dslim/bert-base-NER` (off-the-shelf) | ~0.58 |
| SpaCy `en_core_web_lg` | ~0.50 |
| **Ours (biblical-entity-recognizer-chirho)** | **>0.90** |

### Evaluation Protocol

1. **Standard NER evaluation**: Using `seqeval` library for entity-level P/R/F1
2. **Per-book evaluation**: F1 broken down by biblical book to identify genre-specific weaknesses (e.g., genealogies in Chronicles vs. narrative in Acts)
3. **Ambiguity test set**: Curated set of 200 ambiguous mentions (e.g., "Israel" as person vs. nation, "Jordan" as river vs. region) with gold disambiguation
4. **Error analysis**: Categorize errors as: boundary errors (wrong span), type errors (wrong entity class), missed entities, hallucinated entities

---

## 8. bible.systems Integration

### Direct Integration Points

1. **Entity-Linked Bible Search**: Users search "Paul" and get structured results distinguishing Paul the apostle from other Pauls, with all verse references and entity metadata
2. **Knowledge Graph Population**: Automatically extract (subject, predicate, object) triples from biblical text using NER + dependency parsing: "Abraham begat Isaac" -> (Abraham, PARENT_OF, Isaac)
3. **Interactive Bible Maps**: Combine PLACE entities with OpenBible.info geocoding for interactive geographic visualization of biblical narratives
4. **Character Relationship Graphs**: Extract and visualize social networks between biblical characters per book/chapter
5. **Cross-Reference Enhancement**: Feed entity annotations into Model 2 (Intertextual Reference Network) to improve cross-reference detection -- passages sharing the same entities are more likely to be related
6. **Theological Guardrails Enhancement**: Feed DIVINE entity annotations into Model 1 to better identify statements about God/Christ for orthodoxy checking

### API Design

```
POST /api-chirho/entity-recognizer-chirho/extract-chirho
{
  "text_chirho": "And the LORD said unto Moses, I AM THAT I AM",
  "include_metadata_chirho": true
}

Response:
{
  "entities_chirho": [
    {
      "text_chirho": "the LORD",
      "type_chirho": "DIVINE",
      "start_chirho": 4,
      "end_chirho": 12,
      "confidence_chirho": 0.98,
      "tipnr_id_chirho": "God.1"
    },
    {
      "text_chirho": "Moses",
      "type_chirho": "PERSON",
      "start_chirho": 23,
      "end_chirho": 28,
      "confidence_chirho": 0.99,
      "tipnr_id_chirho": "Moses.1"
    }
  ]
}
```

### Deployment

- Model size after quantization (INT8): ~33MB -- deployable on Cloudflare Workers with WebAssembly
- Inference latency: <10ms per verse on CPU, <2ms on GPU
- Batch processing: Annotate entire Bible (~31,000 verses) in ~30 seconds on A100

---

## References

1. STEPBible Data Repository. Tyndale House, Cambridge. CC BY 4.0. https://github.com/STEPBible/STEPBible-Data
2. Theographic Bible Metadata. Robert Rouse. https://github.com/robertrouse/theographic-bible-metadata
3. MetaV Bible Metadata. https://github.com/Nilpo/bible-metadata
4. BibleNLP Biblical Names Data. https://github.com/BibleNLP/biblical-names-data
5. OpenBible.info Geocoding Data. CC BY. https://github.com/openbibleinfo/Bible-Geocoding-Data
6. Macula Hebrew/Greek Linguistic Datasets. Clear.Bible. CC BY 4.0. https://github.com/Clear-Bible/macula-hebrew
7. dslim/distilbert-NER. Hugging Face. https://huggingface.co/dslim/distilbert-NER
8. "What is it with NLP models and biblical names?" Towards Data Science. https://towardsdatascience.com/what-is-it-with-nlp-models-and-biblical-names-c389cf7a24c9/
9. ScrollMapper Bible Databases. https://github.com/scrollmapper/bible_databases
10. BibleNLP Awesome Bible NLP. https://github.com/BibleNLP/awesome-bible-nlp
11. Viz.Bible Machine Learning Project List. https://viz.bible/machine-learning-ai-and-bible-data-project-list/

---

## Sources Discovered During Research

1. https://github.com/STEPBible/STEPBible-Data
2. https://stepbible.github.io/STEPBible-Data/
3. https://github.com/robertrouse/theographic-bible-metadata
4. https://github.com/Nilpo/bible-metadata
5. https://github.com/BibleNLP/biblical-names-data
6. https://github.com/openbibleinfo/Bible-Geocoding-Data
7. https://github.com/Clear-Bible/macula-hebrew
8. https://github.com/Clear-Bible/macula-greek
9. https://github.com/scrollmapper/bible_databases
10. https://github.com/BibleNLP/awesome-bible-nlp
11. https://viz.bible/machine-learning-ai-and-bible-data-project-list/
12. https://viz.bible/bible-data/
13. https://huggingface.co/dslim/distilbert-NER
14. https://huggingface.co/docs/transformers/tasks/token_classification
15. https://towardsdatascience.com/what-is-it-with-nlp-models-and-biblical-names-c389cf7a24c9/
16. https://tools.bible/tools/macula-greek-and-hebrew-linguistic-datasets
17. https://get.bible/bible-data-sets/
18. https://tyndalehouse.com/research/old-testament-project/
