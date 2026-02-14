---
language: en
license: mit
tags:
  - text-classification
  - bible
  - cross-reference
  - intertextuality
  - roberta
pipeline_tag: text-classification
library_name: transformers
base_model: roberta-base
datasets:
  - LoveJesus/intertextual-dataset-chirho
---

# Intertextual Classifier (RoBERTa-base) - chirho

*For God so loved the world that he gave his only begotten Son, that whoever believes in him should not perish but have eternal life. - John 3:16*

## Description

A RoBERTa-base model fine-tuned for **classifying the type of connection** between pairs of Bible verses. Given two verses (as a sentence pair), it predicts one of 7 connection types.

## Connection Types

| Label | Description | Example |
|-------|-------------|---------|
| `direct_quote` | NT directly quotes OT | Mt 1:23 quotes Is 7:14 |
| `allusion` | Clear reference without direct quotation | Rev 5:5 alludes to Gen 49:9 |
| `thematic_parallel` | Shared theme or motif | Ps 23 parallels Jn 10 |
| `typological` | OT type foreshadows NT antitype | Isaac sacrifice prefigures Christ |
| `prophecy_fulfillment` | OT prophecy fulfilled in NT | Is 53 in Passion narratives |
| `parallel_narrative` | Same event in parallel accounts | Synoptic parallels |
| `contrast` | Deliberate theological contrast | Adam vs Christ (Rom 5) |

## Training

- **Base model**: roberta-base
- **Task**: Single-label classification (7 classes)
- **Data**: 28,612 Grok-labeled cross-reference pairs (class-weighted loss for imbalance)
- **Epochs**: 8 (early stopping patience=3)
- **Batch size**: 16
- **Device**: Apple MPS (M4 Pro)

## Evaluation (Test Set)

- **F1 macro**: 0.42 | **Accuracy**: 70% | **Weighted F1**: 0.72

| Class | Precision | Recall | F1 |
|-------|-----------|--------|-----|
| thematic_parallel | 0.91 | 0.76 | **0.83** |
| direct_quote | 0.48 | 0.66 | **0.56** |
| typological | 0.28 | 0.52 | **0.37** |
| parallel_narrative | 0.26 | 0.55 | **0.36** |
| prophecy_fulfillment | 0.30 | 0.44 | **0.35** |
| allusion | 0.28 | 0.27 | **0.28** |
| contrast | 0.13 | 0.24 | **0.17** |

*Note: Class imbalance (75.9% thematic_parallel) limits macro F1. Weighted F1 of 0.72 better reflects practical performance.*

## Usage

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="LoveJesus/intertextual-classifier-chirho")

result = classifier({
    "text": "Therefore the Lord himself shall give you a sign; Behold, a virgin shall conceive",
    "text_pair": "Now all this was done, that it might be fulfilled which was spoken of the Lord by the prophet"
})
# → prophecy_fulfillment
```

## Part of models-chirho

Paired with [LoveJesus/intertextual-embedder-chirho](https://huggingface.co/LoveJesus/intertextual-embedder-chirho) for full cross-reference discovery.

Built with love for Jesus by [loveJesus](https://huggingface.co/LoveJesus).
