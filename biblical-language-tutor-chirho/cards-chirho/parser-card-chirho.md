---
language:
  - he
  - el
license: mit
tags:
  - biblical-hebrew
  - biblical-greek
  - morphology
  - parsing
  - mt5
  - seq2seq
datasets:
  - LoveJesus/biblical-tutor-dataset-chirho
pipeline_tag: text2text-generation
---

# Biblical Morphological Parser (mT5-small)

*For God so loved the world that he gave his only begotten Son, that whoever believes in him should not perish but have eternal life. - John 3:16*

## What This Does

This model parses biblical Hebrew and Greek words into their morphological components: part of speech, stem, lemma, tense, person, gender, number, and English gloss.

## Usage

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("LoveJesus/biblical-parser-chirho")
model = AutoModelForSeq2SeqLM.from_pretrained("LoveJesus/biblical-parser-chirho")

# Parse a Hebrew word
input_text = 'parse [hebrew]: בָּרָא [GEN 1:1] context: בְּרֵאשִׁית אֱלֹהִים'
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=128)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
# Expected: "class:verb | stem:qal | lemma:ברא | morph:... | person:3 | gender:m | number:s | gloss:he created"

# Parse a Greek word
input_text = 'parse [greek]: λόγος [JHN 1:1] context: ἐν ἀρχῇ ἦν'
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=128)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Input Format

```
parse [{language}]: {word} [{verse_ref}] context: {surrounding_words}
```

- `{language}`: `hebrew` or `greek`
- `{word}`: The biblical word in original script
- `{verse_ref}`: Book chapter:verse reference
- `{surrounding_words}`: 2 words before and after for disambiguation

## Output Format

Pipe-separated morphological tags:
```
class:{pos} | stem:{stem} | lemma:{lemma} | morph:{code} | person:{p} | gender:{g} | number:{n} | gloss:{english}
```

## Training Data

- **Macula Hebrew** (Clear-Bible): ~425K OT words with morphology and glosses
- **Macula Greek SBLGNT** (Clear-Bible): ~138K NT words with morphology and glosses
- Subsampled to ~200K words (100K per language), stratified by book

## Model Details

| Property | Value |
|----------|-------|
| Base model | google/mt5-small (300M params) |
| Architecture | Encoder-decoder (Seq2Seq) |
| Languages | Biblical Hebrew, Koine Greek |
| Training | 5 epochs, lr=3e-4, batch=32 |
| Hardware | NVIDIA A100/H200 GPU |

## Limitations

- Trained on Macula morphological annotations — may not match all scholarly traditions
- Handles individual words, not full syntactic analysis
- Performance may vary on words not well-represented in training data

---

Built with love for Jesus. Published by [LoveJesus](https://huggingface.co/LoveJesus).
Part of the [bible.systems](https://bible.systems) project.
