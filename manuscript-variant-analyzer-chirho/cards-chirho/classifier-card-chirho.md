---
language: el
tags:
  - textual-criticism
  - biblical-manuscripts
  - variant-classification
  - greek
  - mt5
license: cc-by-4.0
datasets:
  - LoveJesus/biblical-variant-dataset-chirho
---

<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

# Biblical Manuscript Variant Classifier (mT5-small)

Classifies New Testament Greek manuscript variants by type using an mT5-small seq2seq model.

## Variant Types
- **substitution**: Different word forms across critical editions
- **omission**: Word present in some editions but not others
- **addition**: Extra words in some editions
- **spelling**: Minor orthographic variants

## Usage

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("LoveJesus/biblical-variant-classifier-chirho")
model = AutoModelForSeq2SeqLM.from_pretrained("LoveJesus/biblical-variant-classifier-chirho")

input_text = "classify variant [greek]: βαπτίζω [MAT.3.11] editions: NTS context: ἐγὼ μὲν ὑμᾶς βαπτίζω"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=128)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Results (v2)

Trained on Apple M4 Pro (MPS), mT5-small (300M params), 9 epochs:

| Metric | Score |
|---|---|
| Eval loss (best) | **0.0868** (epoch 9) |
| Variant type accuracy | **98.87%** |
| Exact match (full output) | 37.5% |
| Training steps | 9,558 |

### Per-Epoch Progression

| Epoch | Loss | Exact Match | Type Accuracy |
|-------|------|-------------|---------------|
| 1 | 0.8033 | 0% | 69.3% |
| 2 | 0.2577 | 1.0% | 67.5% |
| 3 | 0.1465 | 12.1% | 94.5% |
| 4 | 0.1159 | 25.9% | 96.0% |
| 5 | 0.1039 | 29.3% | 98.3% |
| 6 | 0.0963 | 32.7% | 98.8% |
| 7 | 0.0914 | 34.7% | 97.8% |
| 8 | 0.0888 | 35.6% | 98.8% |
| 9 | 0.0868 | **37.5%** | **98.9%** |

## Training Data

Derived from STEPBible TAGNT (Translators Amalgamated Greek NT), which marks each NT word
with its presence across 6 critical editions: NA27/28, Textus Receptus, SBLGNT, Byzantine,
Westcott-Hort, and THGNT.

- Training set: 8,497 examples
- Validation set: 1,062 examples
- Test set: 1,062 examples

## Part of bible.systems

This is model 4 of 8 in the [bible.systems](https://bible.systems) ML pipeline.

---
*For God so loved the world...* — John 3:16
