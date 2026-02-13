<!-- For God so loved the world that he gave his only begotten Son, -->
<!-- that whoever believes in him should not perish but have eternal life. - John 3:16 -->

# Theological Guardrails (theological-guardrails-chirho)

AI-powered theological orthodoxy classification using a three-model pipeline.

## Quick Start

### 1. Install Dependencies

```bash
# Python dependencies
pip install -r requirements-chirho.txt

# Bun dependencies (for data scripts)
bun install
```

### 2. Collect Data

```bash
bun run gather-creeds-chirho
bun run gather-heresies-chirho
bun run gather-scripture-chirho
```

### 3. Generate Dataset

```bash
# Source API keys
source ../.env-chirho

# Generate 500 seed examples
bun run seed-generator-chirho

# Augment to ~22,500 examples
bun run augment-chirho

# Validate dataset
bun run validate-chirho
```

### 4. Train Models

```bash
# Train classifier (DeBERTa-v3-large, ~2-4 hrs on M4 Pro)
python src-chirho/train-chirho/train-classifier-chirho.py

# Train embedder (MiniLM-L12, ~20 min)
python src-chirho/train-chirho/train-embedder-chirho.py

# Train explainer (Flan-T5-base, ~1-3 hrs)
python src-chirho/train-chirho/train-explainer-chirho.py
```

### 5. Run Demo

```bash
python src-chirho/inference-chirho/demo-chirho.py
# Open http://localhost:7860
```

## Architecture

| Model | Base | Task | VRAM |
|-------|------|------|------|
| Classifier | DeBERTa-v3-large | Multi-label classification | ~10GB |
| Embedder | MiniLM-L12-v2 | Contrastive embeddings | ~2GB |
| Explainer | Flan-T5-base | Explanation generation | ~8GB |

All trainable locally on Apple M4 Pro (48GB unified memory) via MPS.

## Orthodoxy Basis

First **six** ecumenical councils:
1. Nicaea I (325) - Arianism
2. Constantinople I (381) - Pneumatomachianism
3. Ephesus (431) - Nestorianism
4. Chalcedon (451) - Monophysitism
5. Constantinople II (553) - Three Chapters
6. Constantinople III (681) - Monothelitism

## License

MIT
