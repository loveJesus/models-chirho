---
language:
  - en
tags:
  - sentence-transformers
  - bible
  - cross-translation
  - semantic-similarity
  - embeddings
license: mit
datasets:
  - LoveJesus/biblical-embedding-dataset-chirho
pipeline_tag: sentence-similarity
---

<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

# Cross-Translation Bible Embeddings

A sentence transformer fine-tuned to create a shared embedding space where semantically
equivalent Bible verses across different translations map to nearby vectors.

## Usage

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer("LoveJesus/biblical-cross-translation-chirho")

verses = [
    "[KJV] In the beginning God created the heaven and the earth.",
    "[BBE] At the first God made the heaven and the earth.",
    "[KJV] And the earth was without form, and void;",
]

embeddings = model.encode(verses)
similarities = cos_sim(embeddings, embeddings)
print(similarities)
# Gen 1:1 KJV vs Gen 1:1 BBE: ~0.95 (same verse, different translation)
# Gen 1:1 KJV vs Gen 1:2 KJV: ~0.30 (different verses)
```

## Training

- **Base model**: paraphrase-multilingual-MiniLM-L12-v2 (118M params, 384-dim)
- **Training**: Contrastive learning (CosineSimilarityLoss) on ~300K verse pairs
- **Translations**: KJV, ASV, YLT, BBE, WEB (all public domain)
- **Positive pairs**: Same verse in different translations
- **Negative pairs**: Different verses from the same translation

## Part of bible.systems

This is model 5 of 5 in the [bible.systems](https://bible.systems) ML pipeline.

---
*For God so loved the world...* — John 3:16
