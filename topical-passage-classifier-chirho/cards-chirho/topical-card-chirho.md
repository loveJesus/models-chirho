---
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16
license: mit
language:
  - en
tags:
  - sentence-transformers
  - semantic-search
  - bible
  - topical-search
  - kjv
  - information-retrieval
  - embedding
datasets:
  - LoveJesus/biblical-topical-dataset-chirho
pipeline_tag: sentence-similarity
model-index:
  - name: biblical-topical-search-chirho
    results:
      - task:
          type: information-retrieval
          name: Topical Bible Passage Retrieval
        metrics:
          - type: cosine_similarity
            value: 0.639
            name: Top Cosine Similarity (prayer and intercession)
---

# Topical Passage Classifier - Model 7 (biblical-topical-search-chirho)

A fine-tuned sentence-transformer model for **semantic topical Bible passage retrieval**. Given a natural language topic or question, the model retrieves the most relevant KJV Bible passages by embedding both queries and verses into a shared 384-dimensional vector space.

## Model Details

| Property | Value |
|----------|-------|
| **Base Model** | `sentence-transformers/all-MiniLM-L6-v2` |
| **Parameters** | 22M |
| **Embedding Dimensions** | 384 |
| **Model Size** | 87MB |
| **Loss Function** | MultipleNegativesRankingLoss (in-batch negatives) |
| **Training Data** | 30,000+ verse-topic pairs from KJV Bible |
| **Data Sources** | Nave's Topical Bible + TSK cross-references |
| **Epochs** | 5 |
| **Learning Rate** | 2e-5 |
| **Warmup** | 10% of total steps |
| **HuggingFace Repo** | [LoveJesus/biblical-topical-search-chirho](https://huggingface.co/LoveJesus/biblical-topical-search-chirho) |

## How It Works

The model takes a topical query (e.g., "salvation through faith") and encodes it into the same embedding space as Bible verses. Relevant passages are retrieved by computing cosine similarity between the query embedding and all verse embeddings, then ranking by score.

**Training approach:**

1. Each training example is a `(topic_text, verse_text)` or `(verse_A, verse_B)` positive pair
2. `MultipleNegativesRankingLoss` uses other positives within the same batch as hard negatives
3. No explicit negative mining is required -- the in-batch negative strategy naturally pushes unrelated pairs apart
4. An `InformationRetrievalEvaluator` (NDCG@10, MRR@10, MAP@10) is used for validation every 500 steps

## Retrieval Performance

Example queries and their top-1 retrieved passages with cosine similarity scores:

| Query | Top Retrieved Passage | Cosine Similarity |
|-------|----------------------|-------------------|
| "salvation through faith" | "For by grace are ye saved through faith; and that not of yourselves: it is the gift of God." (Eph 2:8) | **0.619** |
| "passages about creation" | "In the beginning God created the heaven and the earth." (Gen 1:1) | **0.570** |
| "prayer and intercession" | "Pray without ceasing." (1 Thess 5:17) | **0.639** |

Additional test queries demonstrate strong cross-topic retrieval:

- "What does the Bible say about forgiveness?" correctly surfaces 1 John 1:9
- "verses about love" correctly surfaces John 3:16

## Usage

### Quick Start: Topical Search

```python
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

from sentence_transformers import SentenceTransformer, util

# Load the fine-tuned model
model_chirho = SentenceTransformer("LoveJesus/biblical-topical-search-chirho")

# Encode a topical query
query_chirho = "What does the Bible say about forgiveness?"
query_embedding_chirho = model_chirho.encode(query_chirho)

# Encode candidate passages
passages_chirho = [
    "If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness.",
    "In the beginning God created the heaven and the earth.",
    "Pray without ceasing.",
]
passage_embeddings_chirho = model_chirho.encode(passages_chirho)

# Compute cosine similarity and rank
scores_chirho = util.cos_sim(query_embedding_chirho, passage_embeddings_chirho)[0]
ranked_chirho = scores_chirho.argsort(descending=True)

for rank_chirho in range(len(passages_chirho)):
    idx_chirho = ranked_chirho[rank_chirho].item()
    print(f"  #{rank_chirho + 1} ({scores_chirho[idx_chirho]:.3f}): {passages_chirho[idx_chirho]}")
```

### Building a Full Bible Search Index

```python
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

import json
import numpy as np
from sentence_transformers import SentenceTransformer, util

model_chirho = SentenceTransformer("LoveJesus/biblical-topical-search-chirho")

# Load your KJV verse corpus (one verse per line, JSON with "reference" and "text" fields)
verses_chirho = []
with open("kjv-verses-chirho.jsonl", "r") as f_chirho:
    for line_chirho in f_chirho:
        verses_chirho.append(json.loads(line_chirho))

# Pre-compute all verse embeddings (do this once, then cache)
verse_texts_chirho = [v_chirho["text_chirho"] for v_chirho in verses_chirho]
verse_embeddings_chirho = model_chirho.encode(verse_texts_chirho, show_progress_bar=True, batch_size=64)

# Save embeddings for reuse
np.save("verse-embeddings-chirho.npy", verse_embeddings_chirho)

# Search function
def search_bible_chirho(query_chirho: str, top_k_chirho: int = 10):
    query_emb_chirho = model_chirho.encode(query_chirho)
    scores_chirho = util.cos_sim(query_emb_chirho, verse_embeddings_chirho)[0]
    top_indices_chirho = scores_chirho.argsort(descending=True)[:top_k_chirho]
    results_chirho = []
    for idx_chirho in top_indices_chirho:
        results_chirho.append({
            "reference_chirho": verses_chirho[idx_chirho.item()]["reference_chirho"],
            "text_chirho": verses_chirho[idx_chirho.item()]["text_chirho"],
            "score_chirho": scores_chirho[idx_chirho.item()].item(),
        })
    return results_chirho

# Example
results_chirho = search_bible_chirho("the armor of God")
for r_chirho in results_chirho:
    print(f"  {r_chirho['reference_chirho']} ({r_chirho['score_chirho']:.3f}): {r_chirho['text_chirho'][:80]}...")
```

## Training Data

The training dataset consists of 30,000+ positive pairs in two formats:

1. **Topic-to-verse pairs** (`query_chirho`, `positive_chirho`): A natural language topic description paired with a relevant KJV Bible verse. Derived from **Nave's Topical Bible**, which categorizes Bible verses under ~5,000 topical headings.

2. **Verse-to-verse pairs**: Two thematically related KJV verses paired together. Derived from the **Treasury of Scripture Knowledge (TSK)** cross-reference system, which links verses that share theological themes.

Data is stored in JSONL format with fields `query_chirho` and `positive_chirho`, split into training (`train-topical-chirho.jsonl`) and validation (`val-topical-chirho.jsonl`) sets.

**Dataset repository:** [LoveJesus/biblical-topical-dataset-chirho](https://huggingface.co/datasets/LoveJesus/biblical-topical-dataset-chirho)

## Architecture

```
Input (topic query or verse text)
    |
    v
all-MiniLM-L6-v2 Transformer Encoder (6 layers, 12 heads, 22M params)
    |
    v
Mean Pooling over token embeddings
    |
    v
384-dimensional normalized embedding vector
    |
    v
Cosine similarity for retrieval ranking
```

The base model (`all-MiniLM-L6-v2`) was pre-trained on 1B+ sentence pairs from diverse sources. Fine-tuning on biblical topic-verse pairs adapts the embedding space so that topical queries and their relevant Bible passages are close together.

## Evaluation

Validation uses an `InformationRetrievalEvaluator` that constructs a synthetic IR task from held-out topic-verse pairs:

- **Queries**: The topic/query side of each validation pair
- **Corpus**: The verse/positive side of each validation pair
- **Relevant docs**: Each query maps to exactly one correct corpus entry

Metrics computed at k=10:
- **NDCG@10** (Normalized Discounted Cumulative Gain)
- **MRR@10** (Mean Reciprocal Rank)
- **MAP@10** (Mean Average Precision)

Best model checkpoint is saved based on evaluator performance (evaluated every 500 training steps).

## Limitations

- **KJV only**: Trained exclusively on King James Version text. Performance on other Bible translations may vary.
- **English only**: Does not support queries or passages in other languages.
- **Topical retrieval, not QA**: The model retrieves relevant passages but does not generate answers or explanations.
- **Coverage**: Performance depends on overlap with Nave's Topical Bible and TSK cross-reference categories. Highly novel or abstract queries may yield less precise results.
- **Cosine scores are relative**: Absolute similarity values should be compared within a query's ranked results, not across different queries.
- **Assistive tool**: This model is designed to assist Bible study, not to replace careful reading and pastoral guidance.

## Intended Use

- **Bible study assistance**: Quickly find passages relevant to a topic being studied
- **Sermon preparation**: Discover verses related to a sermon theme
- **Topical indexing**: Build topic-organized collections of Bible passages
- **Cross-reference discovery**: Find thematically related passages across books of the Bible
- **Application backends**: Power semantic search features in Bible study applications

## Training Environment

- **Framework**: `sentence-transformers` with PyTorch
- **Device support**: CUDA GPU, Apple MPS, or CPU (auto-detected)
- **Batch size**: 64 (CUDA) / 16 (MPS/CPU)
- **Optimizer**: AdamW with linear warmup schedule
- **Best model selection**: Automatic via `save_best_model=True`

## Related Models

| Model | Repository | Task |
|-------|-----------|------|
| Theological Classifier | [LoveJesus/theologian-classifier-chirho](https://huggingface.co/LoveJesus/theologian-classifier-chirho) | Orthodox/heterodox classification |
| Theological Embedder | [LoveJesus/theologian-embedder-chirho](https://huggingface.co/LoveJesus/theologian-embedder-chirho) | Theological embedding space |
| Theological Explainer | [LoveJesus/theologian-explainer-chirho](https://huggingface.co/LoveJesus/theologian-explainer-chirho) | Natural language explanations |

## License

MIT

## Citation

```bibtex
@misc{lovejesus2026topicalsearch,
  title={Biblical Topical Search: Fine-tuned MiniLM for Semantic Bible Passage Retrieval},
  author={loveJesus},
  year={2026},
  publisher={HuggingFace},
  url={https://huggingface.co/LoveJesus/biblical-topical-search-chirho}
}
```
