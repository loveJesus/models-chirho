---
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16
license: mit
language:
  - en
tags:
  - token-classification
  - ner
  - bible
  - biblical
  - named-entity-recognition
  - distilbert
  - kjv
  - bio-tagging
datasets:
  - LoveJesus/biblical-ner-dataset-chirho
pipeline_tag: token-classification
model-index:
  - name: biblical-entity-recognizer-chirho
    results:
      - task:
          type: token-classification
          name: Named Entity Recognition
        dataset:
          type: LoveJesus/biblical-ner-dataset-chirho
          name: Biblical NER Dataset (Chirho)
        metrics:
          - type: f1
            value: 0.9810
            name: F1
          - type: precision
            value: 0.9778
            name: Precision
          - type: recall
            value: 0.9843
            name: Recall
---

# Biblical Entity Recognizer (Chirho) - Model 6

A DistilBERT-based Named Entity Recognition model fine-tuned on 200K+ annotated tokens from the King James Version (KJV) Bible to recognize six types of biblical entities using BIO tagging.

**Repo**: [LoveJesus/biblical-entity-recognizer-chirho](https://huggingface.co/LoveJesus/biblical-entity-recognizer-chirho)

## Model Overview

| Property | Value |
|----------|-------|
| **Base Model** | `distilbert-base-uncased` |
| **Parameters** | ~66M |
| **Task** | Token Classification (NER) |
| **Tagging Scheme** | BIO (Beginning-Inside-Outside) |
| **Number of Labels** | 13 |
| **Entity Types** | 6 |
| **Max Sequence Length** | 128 tokens |
| **Framework** | HuggingFace Transformers |
| **License** | MIT |

## Entity Types

| Entity Type | BIO Tags | Description | Examples |
|-------------|----------|-------------|----------|
| PERSON | B-PERSON, I-PERSON | Biblical persons and figures | Moses, David, Paul, Mary |
| DIVINE | B-DIVINE, I-DIVINE | Names and titles of God | God, LORD, Jesus Christ, Holy Spirit |
| PEOPLE_GROUP | B-PEOPLE_GROUP, I-PEOPLE_GROUP | Nations, tribes, and groups | Israelites, Philistines, Pharisees, Corinthians |
| PLACE | B-PLACE, I-PLACE | Geographical locations | Jerusalem, Bethlehem, Egypt, Gethsemane |
| EVENT | B-EVENT, I-EVENT | Biblical events and feasts | Passover, Pentecost, Sabbath |
| ARTIFACT | B-ARTIFACT, I-ARTIFACT | Sacred objects and instruments | Urim, Thummim |

### Full Label Set (13 Labels)

```
O, B-PERSON, I-PERSON, B-DIVINE, I-DIVINE, B-PEOPLE_GROUP, I-PEOPLE_GROUP,
B-PLACE, I-PLACE, B-EVENT, I-EVENT, B-ARTIFACT, I-ARTIFACT
```

## Evaluation Results

| Metric | Score |
|--------|-------|
| **F1** | **0.9810** |
| **Precision** | 97.78% |
| **Recall** | 98.43% |
| **Best Epoch** | 4 |

Entity-level metrics are computed using the `seqeval` library, which evaluates complete entity spans rather than individual token labels, providing a rigorous assessment of recognition quality.

## Usage

### Quick Start: Pipeline API

```python
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

from transformers import pipeline

ner_pipeline_chirho = pipeline(
    "token-classification",
    model="LoveJesus/biblical-entity-recognizer-chirho",
    aggregation_strategy="simple",
)

text_chirho = "And Moses said unto the LORD in the land of Egypt"
entities_chirho = ner_pipeline_chirho(text_chirho)

for entity_chirho in entities_chirho:
    print(f"{entity_chirho['word']}: {entity_chirho['entity_group']} ({entity_chirho['score']:.3f})")
# Moses: PERSON (0.998)
# LORD: DIVINE (0.999)
# Egypt: PLACE (0.997)
```

### Manual Inference

```python
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

tokenizer_chirho = AutoTokenizer.from_pretrained("LoveJesus/biblical-entity-recognizer-chirho")
model_chirho = AutoModelForTokenClassification.from_pretrained("LoveJesus/biblical-entity-recognizer-chirho")

text_chirho = "Then Jesus went with them unto a place called Gethsemane."
inputs_chirho = tokenizer_chirho(text_chirho, return_tensors="pt", truncation=True, max_length=128)

with torch.no_grad():
    outputs_chirho = model_chirho(**inputs_chirho)
    predictions_chirho = torch.argmax(outputs_chirho.logits, dim=2)

tokens_chirho = tokenizer_chirho.convert_ids_to_tokens(inputs_chirho["input_ids"][0])
pred_ids_chirho = predictions_chirho[0].tolist()
id2label_chirho = model_chirho.config.id2label

for token_chirho, pred_id_chirho in zip(tokens_chirho, pred_ids_chirho):
    label_chirho = id2label_chirho[pred_id_chirho]
    if label_chirho != "O" and token_chirho not in ["[CLS]", "[SEP]", "[PAD]"]:
        print(f"  {token_chirho}: {label_chirho}")
# jesus: B-PERSON
# gethsemane: B-PLACE
```

### Batch Processing

```python
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

from transformers import pipeline

ner_pipeline_chirho = pipeline(
    "token-classification",
    model="LoveJesus/biblical-entity-recognizer-chirho",
    aggregation_strategy="simple",
)

verses_chirho = [
    "Now when Jesus was born in Bethlehem of Judaea in the days of Herod the king.",
    "And Solomon built the house of the LORD in Jerusalem.",
    "The LORD is my shepherd; I shall not want.",
    "And Paul said unto the Corinthians, Grace be unto you from God our Father.",
]

for verse_chirho in verses_chirho:
    entities_chirho = ner_pipeline_chirho(verse_chirho)
    print(f"\n{verse_chirho}")
    for entity_chirho in entities_chirho:
        print(f"  {entity_chirho['word']}: {entity_chirho['entity_group']} ({entity_chirho['score']:.3f})")
```

## Training Details

### Dataset

| Property | Value |
|----------|-------|
| **Source Text** | King James Version (KJV) Bible |
| **Text Source** | ScrollMapper bible_databases (Public Domain) |
| **Entity Source** | STEPBible TIPNR (CC BY) + curated divine names list |
| **Annotated Tokens** | 200,000+ |
| **Annotation Scheme** | BIO (Beginning-Inside-Outside) |
| **Format** | JSONL with `tokens_chirho`, `ner_tags_chirho`, `reference_chirho` fields |
| **Split Strategy** | 80/10/10 by **book** (not verse) to prevent data leakage |
| **Dataset Repo** | [LoveJesus/biblical-ner-dataset-chirho](https://huggingface.co/datasets/LoveJesus/biblical-ner-dataset-chirho) |

### Hyperparameters

| Parameter | Value |
|-----------|-------|
| **Learning Rate** | 5.0e-5 |
| **Batch Size** | 32 |
| **Epochs** | 5 (best at epoch 4) |
| **Weight Decay** | 0.01 |
| **Warmup Ratio** | 0.1 |
| **Max Sequence Length** | 128 |
| **Seed** | 42 |
| **Optimizer** | AdamW (default Trainer) |
| **Early Stopping Patience** | 3 epochs |
| **Metric for Best Model** | F1 (entity-level) |

### Subword Alignment

When DistilBERT's WordPiece tokenizer splits a word into multiple subword tokens, only the **first subtoken** receives the original BIO label. Subsequent subtokens of the same word receive `-100` (ignored in loss computation). This prevents the model from being penalized on tokens it cannot meaningfully label.

### Hardware Compatibility

The training script supports:
- **Apple MPS** (Metal Performance Shaders) for Apple Silicon Macs
- **CUDA** for NVIDIA GPUs
- **CPU** fallback

## Architecture

```
DistilBERT-base-uncased (66M parameters)
    |
    v
6-layer Transformer Encoder
    |
    v
Token Classification Head (Linear: 768 -> 13)
    |
    v
BIO Label Predictions per Token
```

DistilBERT is a distilled version of BERT that retains 97% of BERT's language understanding while being 60% faster and 40% smaller. It uses 6 transformer layers (vs. BERT's 12), a hidden size of 768, and 12 attention heads.

## Limitations

- **Domain Specificity**: Trained exclusively on KJV Bible text; may not generalize well to modern English biblical translations or extra-biblical religious texts
- **Archaic Language**: Optimized for Early Modern English (KJV) vocabulary and syntax ("thou", "unto", "begat")
- **Entity Coverage**: The six entity categories may not cover all possible biblical entity types (e.g., no separate category for books of the Bible, religious practices, or time periods)
- **Base Model Vocabulary**: DistilBERT was pre-trained on modern English; some rare biblical proper nouns may be heavily subword-tokenized, potentially reducing recognition accuracy for uncommon names
- **Assistive Tool**: This model is intended as an assistive tool for Bible study and research, not as a replacement for careful scriptural reading

## Intended Use

- Bible study applications requiring automatic entity highlighting
- Biblical text analysis and digital humanities research
- Building knowledge graphs of biblical persons, places, and events
- Enhancing Bible search engines with entity-aware queries
- Educational tools for learning biblical geography, persons, and events

## Citation

```bibtex
@misc{lovejesus2026biblicalentityrecognizer,
  title={Biblical Entity Recognizer: DistilBERT NER for KJV Bible Text},
  author={LoveJesus},
  year={2026},
  publisher={HuggingFace},
  url={https://huggingface.co/LoveJesus/biblical-entity-recognizer-chirho}
}
```

## License

MIT

---

For God so loved the world that he gave his only begotten Son,
that whoever believes in him should not perish but have eternal life. - John 3:16
