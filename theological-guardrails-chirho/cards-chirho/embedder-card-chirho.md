<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

---
license: mit
language:
  - en
tags:
  - theology
  - sentence-transformers
  - embeddings
  - contrastive-learning
  - sentence-similarity
datasets:
  - loveJesus/theologian-dataset-chirho
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# Theologian Embedder (theologian-embedder-chirho)

A fine-tuned **MiniLM-L12-v2** sentence transformer that creates a theological embedding space, clustering orthodox statements together and separating them from heterodox ones.

Part of the [Theological Guardrails Pipeline](https://huggingface.co/loveJesus/theologian-classifier-chirho).

## How It Works

Trained via **contrastive learning** (triplet loss):
- **Anchor**: Orthodox theological statement
- **Positive**: Similar orthodox statement
- **Negative**: Heterodox / heretical statement

The resulting embedding space groups orthodox statements together while pushing heterodox statements far away.

## Evaluation Results

| Metric | Value |
|--------|-------|
| Orthodox-Orthodox avg similarity | 0.8881 |
| Heterodox-Heterodox avg similarity | 0.6126 |
| Orthodox-Heterodox avg similarity | -0.7174 |
| Separation gap | 1.6055 |
| Pearson correlation | 0.970 |

## Usage

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("loveJesus/theologian-embedder-chirho")

orthodox = model.encode("Christ is fully God and fully man, two natures in one person.")
heretical = model.encode("Jesus was merely a created being.")

similarity = np.dot(orthodox, heretical) / (np.linalg.norm(orthodox) * np.linalg.norm(heretical))
print(f"Similarity: {similarity:.3f}")  # Should be low/negative
```

## Use Cases

- **Zero-shot heresy detection**: Compare new statements against orthodox centroid
- **Semantic search**: Find theologically similar statements
- **Clustering**: Group theological positions by similarity
- **Anomaly detection**: Flag statements that are far from known orthodox/heterodox clusters

## Architecture

- **Base model**: `sentence-transformers/all-MiniLM-L12-v2`
- **Training**: Triplet loss with online hard mining
- **Embedding dimension**: 384
- **Training data**: ~22,500 theological statements from the theologian-dataset-chirho

## Orthodoxy Basis

First **six** ecumenical councils (Nicaea I through Constantinople III).

## Limitations

- Trained on English theological texts only
- Best at detecting heresies covered in the training data
- Embedding similarity is a signal, not a definitive classification
- Should be used alongside the classifier and explainer for best results

## Related Models

| Model | Task |
|-------|------|
| [theologian-classifier-chirho](https://huggingface.co/loveJesus/theologian-classifier-chirho) | Multi-label heresy classification (RoBERTa-large) |
| [theologian-explainer-chirho](https://huggingface.co/loveJesus/theologian-explainer-chirho) | Explanation generation (Flan-T5-base) |
| [theologian-dataset-chirho](https://huggingface.co/datasets/loveJesus/theologian-dataset-chirho) | Training dataset |

## License

MIT

## Citation

```bibtex
@misc{lovejesus2026theologianembedder,
  title={Theologian Embedder: Contrastive Theological Embedding Space},
  author={loveJesus},
  year={2026},
  publisher={HuggingFace},
  url={https://huggingface.co/loveJesus/theologian-embedder-chirho}
}
```
