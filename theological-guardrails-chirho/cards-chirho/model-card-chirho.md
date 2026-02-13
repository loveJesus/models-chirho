---
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16
license: mit
language:
  - en
tags:
  - theology
  - classification
  - text-classification
  - sentence-transformers
  - text2text-generation
  - guardrails
datasets:
  - loveJesus/theologian-dataset-chirho
pipeline_tag: text-classification
---

# Theological Guardrails Pipeline (models-chirho)

A three-model AI pipeline for classifying theological statements as **orthodox**, **heterodox**, or **denominational distinctive** based on the first six ecumenical councils of Christianity.

## Models

| Model | Architecture | Task |
|-------|-------------|------|
| `theologian-classifier-chirho` | RoBERTa-large | Multi-label heresy classification |
| `theologian-embedder-chirho` | MiniLM-L12-v2 | Theological embedding space |
| `theologian-explainer-chirho` | Flan-T5-base | Natural language explanations |

## Orthodoxy Basis

Core orthodoxy defined by the first **six** ecumenical councils:

1. **Nicaea I** (325 AD) - Christ is God, consubstantial with the Father
2. **Constantinople I** (381 AD) - Holy Spirit is God, full Trinitarian doctrine
3. **Ephesus** (431 AD) - Christ is one person, Mary is Theotokos
4. **Chalcedon** (451 AD) - Two natures, fully God and fully man
5. **Constantinople II** (553 AD) - Reinforces Chalcedon
6. **Constantinople III** (681 AD) - Two wills in Christ

## Heresies Detected

Arianism, Pelagianism, Gnosticism, Modalism, Docetism, Nestorianism, Marcionism, Apollinarianism, Monothelitism, Semi-Pelagianism, Adoptionism, Patripassianism

## Denominational Handling

Intra-Christian disagreements (predestination, baptism mode, spiritual gifts, eucharistic theology, etc.) are labeled as **denominational distinctives**, NOT heresy.

## Usage

```python
from pipeline_chirho import TheologianPipelineChirho

pipeline = TheologianPipelineChirho()
result = pipeline.analyze_chirho("Jesus is a created being.")

print(result.overall_label_chirho)    # "heterodox"
print(result.top_heresies_chirho)     # ["arianism_chirho"]
print(result.confidence_chirho)       # 0.95
print(result.explanation_chirho)      # "This statement reflects Arianism..."
```

## Limitations

- This is an **assistive tool**, not a replacement for theological education
- May struggle with highly nuanced or novel theological formulations
- Trained primarily on English-language theological texts
- Performance varies by heresy type (see evaluation results)

## Training

- **Classifier**: Fine-tuned RoBERTa-large with multi-label head, BCELoss
- **Embedder**: Contrastive learning with triplet loss on MiniLM-L12
- **Explainer**: Fine-tuned Flan-T5-base for instruction-following explanation

## License

MIT

## Citation

```bibtex
@misc{lovejesus2025theologicanguardrails,
  title={Theological Guardrails: AI-Powered Orthodox Doctrine Classification},
  author={loveJesus},
  year={2026},
  publisher={HuggingFace},
  url={https://huggingface.co/loveJesus/theologian-classifier-chirho}
}
```
