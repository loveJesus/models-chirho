---
language:
  - he
  - el
license: mit
tags:
  - biblical-hebrew
  - biblical-greek
  - interlinear
  - glossing
  - mt5
  - seq2seq
datasets:
  - LoveJesus/biblical-tutor-dataset-chirho
pipeline_tag: text2text-generation
---

# Biblical Interlinear Glosser (mT5-small)

*For God so loved the world that he gave his only begotten Son, that whoever believes in him should not perish but have eternal life. - John 3:16*

## What This Does

This model produces word-by-word English glosses for biblical Hebrew and Greek verses, creating an interlinear translation.

## Usage

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("LoveJesus/biblical-glosser-chirho")
model = AutoModelForSeq2SeqLM.from_pretrained("LoveJesus/biblical-glosser-chirho")

# Gloss Genesis 1:1
input_text = 'gloss [hebrew]: בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ [GEN 1:1]'
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
# Expected: "In-beginning | created | God | [direct object marker] | the-heavens | and | the-earth"

# Gloss John 1:1
input_text = 'gloss [greek]: Ἐν ἀρχῇ ἦν ὁ λόγος [JHN 1:1]'
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
# Expected: "In | [the] beginning | was | the | Word"
```

## Input Format

```
gloss [{language}]: {verse_text_in_original_script} [{verse_ref}]
```

## Output Format

Word-by-word English glosses separated by ` | `:
```
word1_gloss | word2_gloss | word3_gloss | ...
```

## Training Data

- **Macula Hebrew** (Clear-Bible): ~23K OT verses with word-level glosses
- **Macula Greek SBLGNT** (Clear-Bible): ~8K NT verses with word-level glosses
- Total: ~31K verse-level glossing examples

## Model Details

| Property | Value |
|----------|-------|
| Base model | google/mt5-small (300M params) |
| Architecture | Encoder-decoder (Seq2Seq) |
| Languages | Biblical Hebrew, Koine Greek |
| Training | 8 epochs, lr=3e-4, batch=16 |
| Hardware | NVIDIA A100/H200 GPU |

## Limitations

- Glosses are word-level, not fluent English translations
- Based on Macula glossing conventions — may differ from other interlinear traditions
- Long verses (>30 words) may be truncated due to sequence length limits

---

Built with love for Jesus. Published by [LoveJesus](https://huggingface.co/LoveJesus).
Part of the [bible.systems](https://bible.systems) project.
