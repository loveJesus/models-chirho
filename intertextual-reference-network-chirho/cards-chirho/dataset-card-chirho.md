---
language: en
license: cc-by-4.0
tags:
  - bible
  - cross-reference
  - intertextuality
  - treasury-of-scripture-knowledge
size_categories:
  - 100K<n<1M
---

# Intertextual Reference Dataset - chirho

*For God so loved the world that he gave his only begotten Son, that whoever believes in him should not perish but have eternal life. - John 3:16*

## Description

Training data for the Intertextual Reference Network models. Contains two datasets:

### Embedder Dataset (~344K triplets)
- **Source**: Treasury of Scripture Knowledge via OpenBible.info (CC Attribution)
- **Format**: `(anchor_verse, positive_verse, negative_verse)` triplets
- **Splits**: train (275K), val (34K), test (34K)
- **Hard negatives**: Same-book unrelated verses for stronger training signal

### Classifier Dataset (28,612 labeled pairs)
- **Source**: Top cross-reference pairs labeled by Grok xAI API
- **Labels**: 7 connection types (direct_quote, allusion, thematic_parallel, typological, prophecy_fulfillment, parallel_narrative, contrast)
- **Splits**: train (22,889), val (2,861), test (2,862)

### Verse Map
- **31,102** KJV Bible verses in OSIS format (Gen.1.1 through Rev.22.21)
- Source: aruljohn/Bible-kjv (MIT license)

## Citation

Treasury of Scripture Knowledge cross-references from [OpenBible.info](https://a.openbible.info/data/cross-references.zip) (CC Attribution).

Built with love for Jesus by [loveJesus](https://huggingface.co/LoveJesus).
