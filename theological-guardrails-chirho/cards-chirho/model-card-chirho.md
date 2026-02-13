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

## Try It Live

**[Interactive Demo on HuggingFace Spaces](https://huggingface.co/spaces/LoveJesus/theological-guardrails-chirho)**

## Usage

### Quick Start: Classifier Only

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("LoveJesus/theologian-classifier-chirho")
model = AutoModelForSequenceClassification.from_pretrained("LoveJesus/theologian-classifier-chirho")

text = "Jesus was a created being, the first and greatest of God's creations."
inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)

with torch.no_grad():
    scores = torch.sigmoid(model(**inputs).logits)[0]

labels = ["orthodox", "arianism", "pelagianism", "gnosticism", "modalism",
          "docetism", "nestorianism", "marcionism", "apollinarianism",
          "monothelitism", "semi_pelagianism", "adoptionism", "patripassianism"]

for label, score in zip(labels, scores):
    if score > 0.3:
        print(f"  {label}: {score:.3f}")
# Output: arianism: 0.98
```

### Embedder: Theological Similarity

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("LoveJesus/theologian-embedder-chirho")

orthodox = model.encode("Christ is fully God and fully man, two natures in one person.")
statement = model.encode("Jesus was merely a good moral teacher.")

similarity = np.dot(orthodox, statement) / (np.linalg.norm(orthodox) * np.linalg.norm(statement))
print(f"Similarity to orthodoxy: {similarity:.3f}")  # Low = far from orthodox
```

### Explainer: Why Is It Heretical?

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("LoveJesus/theologian-explainer-chirho")
model = AutoModelForSeq2SeqLM.from_pretrained("LoveJesus/theologian-explainer-chirho")

input_text = ("explain theological classification: Jesus is a created being. "
              "| label: heterodox | heresy types: arianism")
inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
outputs = model.generate(**inputs, max_length=256, num_beams=4, early_stopping=True)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
# "This statement reflects Arianism, which teaches that Christ is a created being..."
```

### Full Pipeline (All 3 Models)

```python
# pip install transformers torch sentence-transformers

from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
import torch, numpy as np

# Load all 3 models
clf_tok = AutoTokenizer.from_pretrained("LoveJesus/theologian-classifier-chirho")
clf_model = AutoModelForSequenceClassification.from_pretrained("LoveJesus/theologian-classifier-chirho")
embedder = SentenceTransformer("LoveJesus/theologian-embedder-chirho")
exp_tok = AutoTokenizer.from_pretrained("LoveJesus/theologian-explainer-chirho")
exp_model = AutoModelForSeq2SeqLM.from_pretrained("LoveJesus/theologian-explainer-chirho")

# Analyze a statement
text = "God is one person who appears in three modes."

# 1. Classify
inputs = clf_tok(text, return_tensors="pt", truncation=True, max_length=256)
with torch.no_grad():
    scores = torch.sigmoid(clf_model(**inputs).logits)[0]
print(f"Modalism score: {scores[4]:.3f}")  # High = detected

# 2. Compare embedding to orthodox centroid
emb = embedder.encode([text])[0]
orthodox_emb = embedder.encode(["We worship one God in Trinity and Trinity in Unity."])[0]
sim = np.dot(emb, orthodox_emb) / (np.linalg.norm(emb) * np.linalg.norm(orthodox_emb))
print(f"Orthodox similarity: {sim:.3f}")

# 3. Explain
exp_input = f"explain theological classification: {text} | label: heterodox | heresy types: modalism"
exp_inputs = exp_tok(exp_input, return_tensors="pt", max_length=512, truncation=True)
exp_out = exp_model.generate(**exp_inputs, max_length=256, num_beams=4)
print(exp_tok.decode(exp_out[0], skip_special_tokens=True))
```

## Evaluation Results

| Model | Metric | Score |
|-------|--------|-------|
| Classifier (RoBERTa-large) | F1 macro | **0.9971** |
| Embedder (MiniLM-L12) | Separation gap | **1.6055** |
| Explainer (Flan-T5-base) | Eval loss | **0.0567** |

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
