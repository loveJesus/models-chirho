<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

---
license: mit
language:
  - en
tags:
  - theology
  - text2text-generation
  - explanation
  - flan-t5
datasets:
  - loveJesus/theologian-dataset-chirho
pipeline_tag: text2text-generation
---

# Theologian Explainer (theologian-explainer-chirho)

A fine-tuned **Flan-T5-base** model that generates human-readable explanations of why a theological statement is classified as orthodox, heterodox, or a denominational distinctive.

Part of the [Theological Guardrails Pipeline](https://huggingface.co/loveJesus/theologian-classifier-chirho).

## How It Works

Given a theological statement, its classification label, and detected heresy types, the model generates an explanation citing relevant creeds, councils, and scripture.

## Usage

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("loveJesus/theologian-explainer-chirho")
model = AutoModelForSeq2SeqLM.from_pretrained("loveJesus/theologian-explainer-chirho")

input_text = (
    "explain theological classification: Jesus is a created being, "
    "the first of God's creations. | label: heterodox | heresy types: arianism"
)

inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
outputs = model.generate(**inputs, max_length=256, num_beams=4, early_stopping=True)

explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(explanation)
# "This statement reflects Arianism, which teaches that Christ is a created being
#  rather than eternally begotten of the Father. The Council of Nicaea (325 AD)
#  condemned this view, affirming that the Son is 'begotten, not made, of one
#  Being with the Father.'"
```

## Input Format

```
explain theological classification: {statement} | label: {orthodox|heterodox|denominational_distinctive} | heresy types: {comma-separated list or "none"}
```

## Architecture

- **Base model**: `google/flan-t5-base` (248M parameters)
- **Task**: Conditional text generation (seq2seq)
- **Max input length**: 512 tokens
- **Max output length**: 256 tokens
- **Training**: Fine-tuned on ~22,500 theological statement-explanation pairs

## Training Details

- **Epochs**: 8
- **Batch size**: 8
- **Learning rate**: 3e-5
- **Optimizer**: AdamW with weight decay 0.01
- **Hardware**: Apple M4 Pro (48GB, MPS)
- **Best model selection**: Lowest validation loss

## Orthodoxy Basis

First **six** ecumenical councils (Nicaea I through Constantinople III).

## Limitations

- Explanations should be verified by trained theologians
- Quality varies by heresy type and statement complexity
- Best at explaining well-known heresies with clear conciliar definitions
- May produce generic explanations for novel or ambiguous statements
- English only

## Related Models

| Model | Task |
|-------|------|
| [theologian-classifier-chirho](https://huggingface.co/loveJesus/theologian-classifier-chirho) | Multi-label heresy classification (RoBERTa-large) |
| [theologian-embedder-chirho](https://huggingface.co/loveJesus/theologian-embedder-chirho) | Theological embeddings (MiniLM-L12) |
| [theologian-dataset-chirho](https://huggingface.co/datasets/loveJesus/theologian-dataset-chirho) | Training dataset |

## License

MIT

## Citation

```bibtex
@misc{lovejesus2026theologianexplainer,
  title={Theologian Explainer: AI-Generated Theological Classification Explanations},
  author={loveJesus},
  year={2026},
  publisher={HuggingFace},
  url={https://huggingface.co/loveJesus/theologian-explainer-chirho}
}
```
