---
language:
  - he
  - el
  - en
license: mit
tags:
  - biblical-hebrew
  - biblical-greek
  - morphology
  - interlinear
  - glossing
size_categories:
  - 100K<n<1M
---

# Biblical Language Tutor Dataset

*For God so loved the world that he gave his only begotten Son, that whoever believes in him should not perish but have eternal life. - John 3:16*

## Description

Training data for the Biblical Language Tutor pipeline: morphological parsing and interlinear glossing of biblical Hebrew and Greek. Derived from the Macula Hebrew and Greek treebanks (Clear-Bible).

## Dataset Structure

### Parser Dataset (~200K examples)

JSONL format with fields:
- `input_chirho`: Parse instruction with word, reference, and context
- `target_chirho`: Pipe-separated morphological tags
- `ref_chirho`: Verse reference
- `lang_chirho`: `hebrew` or `greek`

### Glosser Dataset (~31K examples)

JSONL format with fields:
- `input_chirho`: Gloss instruction with full verse text and reference
- `target_chirho`: Word-by-word English glosses separated by ` | `
- `ref_chirho`: Verse reference
- `lang_chirho`: `hebrew` or `greek`
- `word_count_chirho`: Number of words in the verse

## Source Data

- **Macula Hebrew** (Clear-Bible/macula-hebrew): Full OT morphology + glosses
- **Macula Greek SBLGNT** (Clear-Bible/macula-greek): Full NT morphology + glosses

## Splits

| Split | Parser | Glosser |
|-------|--------|---------|
| Train | ~160K  | ~25K    |
| Val   | ~20K   | ~3K     |
| Test  | ~20K   | ~3K     |

---

Built with love for Jesus. Published by [LoveJesus](https://huggingface.co/LoveJesus).
