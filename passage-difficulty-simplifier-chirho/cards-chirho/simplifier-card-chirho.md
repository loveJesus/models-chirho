---
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16
license: mit
language:
  - en
tags:
  - text2text-generation
  - flan-t5
  - bible
  - simplification
  - readability
  - difficulty-scoring
  - multi-task
  - seq2seq
datasets:
  - LoveJesus/passage-difficulty-simplifier-dataset-chirho
pipeline_tag: text2text-generation
base_model: google/flan-t5-small
model-index:
  - name: passage-difficulty-simplifier-chirho
    results: []
---

# Passage Difficulty Scorer & Plain-Language Simplifier (Model 8)

A fine-tuned **google/flan-t5-small** (80M parameters) for dual-task Bible passage processing: (1) reading difficulty scoring and (2) archaic-to-modern English simplification. Both tasks are learned jointly through multi-task training on the same model.

## Model Description

This model takes Bible passages as input and performs one of two tasks, selected by a natural language prefix:

### Task 1: Difficulty Scoring

Analyzes a Bible passage and produces a structured difficulty assessment.

- **Prefix**: `rate difficulty:`
- **Output format**: `reading_level: [1-12] | vocab_complexity: [low/medium/high] | archaic_forms: [count] | difficulty: [easy/medium/hard]`

### Task 2: Simplification

Converts archaic or complex Bible passages into plain modern English.

- **Prefix**: `simplify:`
- **Output**: Plain-language paraphrase of the input verse

## Training Details

| Parameter | Value |
|---|---|
| **Base model** | `google/flan-t5-small` (80M params) |
| **Architecture** | Encoder-Decoder (T5) |
| **Training approach** | Full fine-tuning, multi-task |
| **Trainer** | `Seq2SeqTrainer` with `DataCollatorForSeq2Seq` |
| **Epochs** | 5 |
| **Batch size** | 32 (A100 GPU) |
| **Effective batch size** | 32 (gradient accumulation = 1 on A100) |
| **Learning rate** | 3e-4 |
| **LR scheduler** | Cosine with 10% warmup |
| **Weight decay** | 0.01 |
| **Label smoothing** | 0.1 |
| **Mixed precision** | bf16 (A100) |
| **Max input length** | 256 tokens |
| **Max target length** | 256 tokens |
| **Early stopping** | Patience = 2, monitoring `eval_loss` |
| **Best model selection** | Lowest `eval_loss` |
| **Generation (eval)** | `predict_with_generate=True`, beam search |

### Dataset

Trained on approximately **120K+ examples** combining both tasks, split by Bible book to prevent verse-level leakage (80/10/10 by book):

| Task | Target Count | Description |
|---|---|---|
| Difficulty scoring | ~64K | Verses from 6 translations with algorithmically computed labels |
| Simplification | ~96K | Cross-translation pairs mapping complex to simple English |

#### Translations Used

| Translation | Style | Role |
|---|---|---|
| KJV (King James Version) | Formal, archaic | Complex source |
| ASV (American Standard Version) | Formal, dated | Complex source |
| YLT (Young's Literal Translation) | Ultra-literal | Complex source |
| Darby Bible | Literal, dated | Complex source / Difficulty scoring |
| BBE (Bible in Basic English) | 850-word vocabulary, ~Grade 4 | Simple target |
| OEB (Open English Bible) | Modern, public domain | Simple target |

#### Simplification Pairs

| Complex Source | Simple Target |
|---|---|
| KJV | BBE |
| KJV | OEB |
| ASV | BBE |
| YLT | OEB |

#### Data Source

Bible text sourced from **ScrollMapper Bible Databases** (public domain translations on GitHub).

#### Difficulty Scoring Labels

Labels are computed algorithmically from textual features:

- **Reading level** (1-12): Approximate Flesch-Kincaid grade level analog, adjusted for archaic vocabulary and uncommon word ratio
- **Vocabulary complexity** (low/medium/high): Ratio of words outside a ~3,000-word common English vocabulary
- **Archaic forms** (count): Number of archaic English words detected (thee, thou, hath, doth, -eth/-est verb endings, etc.)
- **Difficulty** (easy/medium/hard): Composite score from reading level, vocabulary complexity, and archaic form count

## Usage

### Quick Start: Simplification

```python
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer_chirho = AutoTokenizer.from_pretrained("LoveJesus/passage-difficulty-simplifier-chirho")
model_chirho = AutoModelForSeq2SeqLM.from_pretrained("LoveJesus/passage-difficulty-simplifier-chirho")

input_text_chirho = "simplify: And the LORD God formed man of the dust of the ground, and breathed into his nostrils the breath of life; and man became a living soul."

inputs_chirho = tokenizer_chirho(input_text_chirho, return_tensors="pt", max_length=256, truncation=True)
outputs_chirho = model_chirho.generate(**inputs_chirho, max_length=256, num_beams=4, early_stopping=True)
result_chirho = tokenizer_chirho.decode(outputs_chirho[0], skip_special_tokens=True)

print(result_chirho)
# Expected: A simplified, modern English version of the verse
```

### Quick Start: Difficulty Scoring

```python
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

tokenizer_chirho = AutoTokenizer.from_pretrained("LoveJesus/passage-difficulty-simplifier-chirho")
model_chirho = AutoModelForSeq2SeqLM.from_pretrained("LoveJesus/passage-difficulty-simplifier-chirho")

input_text_chirho = "rate difficulty: For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."

inputs_chirho = tokenizer_chirho(input_text_chirho, return_tensors="pt", max_length=256, truncation=True)
outputs_chirho = model_chirho.generate(**inputs_chirho, max_length=256, num_beams=4, early_stopping=True)
raw_output_chirho = tokenizer_chirho.decode(outputs_chirho[0], skip_special_tokens=True)

print(raw_output_chirho)
# Expected: "reading_level: X | vocab_complexity: Y | archaic_forms: Z | difficulty: W"

# Parse structured output
reading_level_chirho = re.search(r"reading_level:\s*(\d+)", raw_output_chirho)
difficulty_chirho = re.search(r"difficulty:\s*(\w+)", raw_output_chirho)
vocab_chirho = re.search(r"vocab_complexity:\s*(\w+)", raw_output_chirho)
archaic_chirho = re.search(r"archaic_forms:\s*(\d+)", raw_output_chirho)

if reading_level_chirho:
    print(f"Reading Level: Grade {reading_level_chirho.group(1)}")
if difficulty_chirho:
    print(f"Difficulty: {difficulty_chirho.group(1)}")
if vocab_chirho:
    print(f"Vocabulary Complexity: {vocab_chirho.group(1)}")
if archaic_chirho:
    print(f"Archaic Forms: {archaic_chirho.group(1)}")
```

### Batch Inference

```python
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer_chirho = AutoTokenizer.from_pretrained("LoveJesus/passage-difficulty-simplifier-chirho")
model_chirho = AutoModelForSeq2SeqLM.from_pretrained("LoveJesus/passage-difficulty-simplifier-chirho")
model_chirho.eval()

verses_chirho = [
    "simplify: Verily, verily, I say unto thee, Except a man be born again, he cannot see the kingdom of God.",
    "simplify: Wherefore, as by one man sin entered into the world, and death by sin; and so death passed upon all men, for that all have sinned:",
    "rate difficulty: In the beginning God created the heaven and the earth.",
    "rate difficulty: Jesus wept.",
]

inputs_chirho = tokenizer_chirho(verses_chirho, return_tensors="pt", max_length=256, truncation=True, padding=True)

with torch.no_grad():
    outputs_chirho = model_chirho.generate(**inputs_chirho, max_length=256, num_beams=4, early_stopping=True)

results_chirho = tokenizer_chirho.batch_decode(outputs_chirho, skip_special_tokens=True)

for verse_chirho, result_chirho in zip(verses_chirho, results_chirho):
    print(f"Input:  {verse_chirho}")
    print(f"Output: {result_chirho}\n")
```

## Evaluation

### Metrics

| Task | Metric | Description |
|---|---|---|
| Difficulty Scoring | `difficulty_accuracy_chirho` | Exact match on easy/medium/hard label |
| Difficulty Scoring | Reading level MAE | Mean absolute error on grade level (1-12) |
| Difficulty Scoring | Vocab complexity accuracy | Exact match on low/medium/high |
| Simplification | BLEU | Corpus-level BLEU score (sacrebleu) |
| Simplification | BERTScore F1 | Semantic similarity to reference simplifications |
| Simplification | Exact match | Proportion of predictions matching reference exactly |
| Combined | `combined_score_chirho` | 0.4 * difficulty_accuracy + 0.6 * simplification_exact_match |

### Results

Trained for 5 epochs (19,075 steps) on NVIDIA A100 SXM 80GB in ~80 minutes. Best model selected by lowest eval loss.

| Metric | Score |
|---|---|
| Eval loss (best) | **2.341** (epoch 4) |
| Difficulty accuracy | **91.96%** |
| Simplification exact match | 0.35% |
| Combined score | 0.3699 |
| Training throughput | 128.3 samples/sec |
| Training runtime | 4,758 seconds |

**Per-epoch progression:**

| Epoch | Eval Loss | Difficulty Acc | Simp Exact | Combined |
|---|---|---|---|---|
| 1 | 2.441 | 85.55% | 0.24% | 0.3436 |
| 2 | 2.373 | 89.21% | 0.32% | 0.3587 |
| 3 | 2.348 | 90.19% | 0.33% | 0.3628 |
| 4 | 2.341 | 91.74% | 0.32% | 0.3689 |
| 5 | 2.342 | 91.96% | 0.35% | 0.3699 |

**Notes:**
- Difficulty scoring is the model's strong suit at 91.96% accuracy on easy/medium/hard classification
- Simplification exact match is expectedly low since there are many valid paraphrases of any verse
- The model produces fluent, readable simplifications even when they don't match the reference exactly
- Combined score weights: 0.4 * difficulty_accuracy + 0.6 * simplification_exact_match

## Try It Live

**[Interactive Demo on HuggingFace Spaces](https://huggingface.co/spaces/LoveJesus/passage-difficulty-simplifier-chirho)**

The Gradio-powered demo provides two tabs:
- **Simplify**: Enter any Bible verse and receive a plain-language version
- **Difficulty**: Enter a verse and get reading level, vocabulary complexity, archaic form count, and overall difficulty

## Limitations

- Trained exclusively on Bible text; does not generalize to other literary or domain-specific texts
- Simplification quality varies by verse length and complexity; very long passages may be truncated
- Difficulty scoring labels are algorithmically generated (not human-annotated), which introduces systematic biases
- Small model (80M params) trades accuracy for speed and accessibility
- Simplification targets (BBE, OEB) have their own translation biases; outputs reflect those stylistic choices
- Archaic form detection relies on a fixed word list and may miss uncommon archaic constructions
- The model does not preserve verse references or theological nuance; it is a readability tool, not a study Bible

## Intended Use

- Bible study tools that need plain-language paraphrasing of archaic translations
- Reading level assessment for curriculum planning or children's ministry materials
- Accessibility applications that present Bible text at appropriate reading levels
- Research into text simplification for historical English

## Out-of-Scope Use

- Replacing authoritative Bible translations for doctrinal study
- General-purpose text simplification outside of biblical literature
- Machine translation between languages (this model operates only in English)

## Model Architecture

```
google/flan-t5-small (Encoder-Decoder)
  Encoder: 6 layers, 8 heads, d_model=512
  Decoder: 6 layers, 8 heads, d_model=512
  Total parameters: ~80M (all trainable, full fine-tuning)
  Vocabulary: SentencePiece, 32,128 tokens
```

## Repository Structure

```
passage-difficulty-simplifier-chirho/
  src-chirho/
    train-chirho/train-simplifier-chirho.py    # Training script
    eval-chirho/evaluate-chirho.py             # Evaluation script
    data-chirho/build-simplifier-dataset-chirho.ts  # Dataset builder (Bun/TS)
    data-chirho/download-translations-chirho.ts     # Translation downloader
    upload-hf-chirho.py                        # HuggingFace upload script
  space-chirho/
    app.py                                     # Gradio demo application
  data-chirho/
    raw-chirho/                                # Raw Bible CSVs
    processed-chirho/                          # JSONL train/val/test splits
  models-chirho/
    simplifier-chirho/best-chirho/             # Best checkpoint
  cards-chirho/
    simplifier-card-chirho.md                  # This model card
  config-chirho.yaml                           # Training configuration
  spec-chirho/
    progress-chirho.sqlite                     # Agent progress log
```

## Training Reproducibility

```bash
# 1. Download Bible translations
cd passage-difficulty-simplifier-chirho
bun run src-chirho/data-chirho/download-translations-chirho.ts

# 2. Build dual-task dataset
bun run src-chirho/data-chirho/build-simplifier-dataset-chirho.ts

# 3. Train model
python src-chirho/train-chirho/train-simplifier-chirho.py

# 4. Evaluate
python src-chirho/eval-chirho/evaluate-chirho.py

# 5. Upload to HuggingFace
python src-chirho/upload-hf-chirho.py
```

## License

MIT

## Citation

```bibtex
@misc{lovejesus2026passagedifficultysimplifier,
  title={Passage Difficulty Scorer & Plain-Language Simplifier: Multi-Task Flan-T5 for Bible Readability},
  author={loveJesus},
  year={2026},
  publisher={HuggingFace},
  url={https://huggingface.co/LoveJesus/passage-difficulty-simplifier-chirho}
}
```

---

Built with love for Jesus. Published by [loveJesus](https://huggingface.co/LoveJesus).
