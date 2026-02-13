<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

---
license: mit
language:
  - en
tags:
  - theology
  - classification
  - text-classification
  - heresy-detection
size_categories:
  - 10K<n<100K
task_categories:
  - text-classification
---

# Theologian Dataset (theologian-dataset-chirho)

A curated dataset of theological statements labeled as orthodox, heterodox, or denominational distinctive, designed for training theological guardrails models.

## Dataset Description

- **Size**: ~22,500 examples
- **Format**: JSONL
- **Splits**: Train (80%), Validation (10%), Test (10%)
- **Languages**: English

## Schema

```json
{
  "text_chirho": "Statement text",
  "label_chirho": "orthodox | heterodox | denominational_distinctive",
  "heresy_types_chirho": ["arianism", "pelagianism", ...],
  "confidence_chirho": 0.95,
  "explanation_chirho": "Why this is classified this way",
  "scripture_refs_chirho": ["John 1:1", "Colossians 1:15"],
  "creed_refs_chirho": ["nicene_creed"],
  "domain_chirho": "christology",
  "denominational_note_chirho": null
}
```

## Heresy Types

| Label | Description | Council |
|-------|-------------|---------|
| arianism | Christ is created, not God | Nicaea (325) |
| pelagianism | No original sin, salvation by works | Ephesus (431) |
| gnosticism | Material world is evil, secret knowledge saves | Early church |
| modalism | God is one person in three modes | Constantinople I (381) |
| docetism | Christ only appeared human | Chalcedon (451) |
| nestorianism | Two persons in Christ | Ephesus (431) |
| marcionism | OT God is evil, reject OT | Early church |
| apollinarianism | Christ lacks human mind | Constantinople I (381) |
| monothelitism | Christ has only one will | Constantinople III (681) |
| semi_pelagianism | Humans initiate salvation | Orange (529) |
| adoptionism | Jesus adopted as Son | Multiple synods |
| patripassianism | Father suffered on cross | Early church |

## Sources

- Historical creeds (Nicene, Apostles', Chalcedonian, Athanasian) - Public domain
- Church council definitions - Public domain
- Westminster and Heidelberg Catechisms - Public domain
- World English Bible (scripture) - Public domain
- LLM-generated paraphrases and augmentations (from 500 curated seeds)

## License

MIT
