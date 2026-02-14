---
language: en
license: mit
tags:
  - sentence-transformers
  - bible
  - cross-reference
  - semantic-search
  - intertextuality
pipeline_tag: sentence-similarity
library_name: sentence-transformers
base_model: sentence-transformers/all-MiniLM-L12-v2
datasets:
  - LoveJesus/intertextual-dataset-chirho
---

# Intertextual Embedder (MiniLM-L12) - chirho

*For God so loved the world that he gave his only begotten Son, that whoever believes in him should not perish but have eternal life. - John 3:16*

## Description

A sentence transformer fine-tuned for **biblical verse similarity** and **cross-reference discovery**. Given a verse text, it produces a 384-dimensional embedding that places semantically related verses close together in vector space.

## Training

- **Base model**: sentence-transformers/all-MiniLM-L12-v2
- **Loss**: Triplet loss (cosine distance, margin=0.5)
- **Data**: 344,798 triplets from the Treasury of Scripture Knowledge (OpenBible.info)
  - Anchor: verse A, Positive: cross-referenced verse B, Negative: hard negative (same-book unrelated verse)
- **Epochs**: 3
- **Batch size**: 64
- **Device**: Apple MPS (M4 Pro)

## Evaluation

- **Triplet ranking accuracy**: 86.75% (positive cross-ref ranked higher than negative)
- **Separation gap**: 0.4213
- **Pearson cosine**: 0.6271
- **Spearman cosine**: 0.6326

## Usage

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("LoveJesus/intertextual-embedder-chirho")

verses = [
    "In the beginning God created the heaven and the earth.",
    "In the beginning was the Word, and the Word was with God, and the Word was God.",
    "And the children of Israel went into the midst of the sea upon the dry ground.",
]

embeddings = model.encode(verses)
# embeddings[0] will be closest to embeddings[1] (Gen 1:1 <-> John 1:1)
```

## Part of models-chirho

This model is part of the [Intertextual Reference Network](https://huggingface.co/LoveJesus) pipeline, paired with:
- **Classifier**: [LoveJesus/intertextual-classifier-chirho](https://huggingface.co/LoveJesus/intertextual-classifier-chirho)
- **Dataset**: [LoveJesus/intertextual-dataset-chirho](https://huggingface.co/datasets/LoveJesus/intertextual-dataset-chirho)

Built with love for Jesus by [loveJesus](https://huggingface.co/LoveJesus).
