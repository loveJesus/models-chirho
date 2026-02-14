#!/bin/bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# train-on-pod-chirho.sh
# Run this on a RunPod A100/H200/B200 pod after uploading data + scripts.
# Usage: bash runpod-chirho/train-on-pod-chirho.sh

set -euo pipefail

echo "============================================"
echo "Biblical Language Tutor - RunPod Training"
echo "============================================"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'unknown')"
echo "VRAM: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader 2>/dev/null || echo 'unknown')"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q transformers datasets torch accelerate evaluate \
    sentencepiece protobuf sacrebleu pyyaml safetensors \
    huggingface-hub python-dotenv numpy scikit-learn

# Verify data exists
DATA_DIR_CHIRHO="data-chirho/processed-chirho"
if [ ! -f "$DATA_DIR_CHIRHO/train-parser-chirho.jsonl" ]; then
    echo "ERROR: Parser training data not found at $DATA_DIR_CHIRHO/"
    echo "Upload JSONL files first: scp data-chirho/processed-chirho/*.jsonl pod:data-chirho/processed-chirho/"
    exit 1
fi

PARSER_COUNT_CHIRHO=$(wc -l < "$DATA_DIR_CHIRHO/train-parser-chirho.jsonl")
GLOSSER_COUNT_CHIRHO=$(wc -l < "$DATA_DIR_CHIRHO/train-glosser-chirho.jsonl")
echo "Parser train examples: $PARSER_COUNT_CHIRHO"
echo "Glosser train examples: $GLOSSER_COUNT_CHIRHO"

# Train parser
echo ""
echo "============================================"
echo "Training Parser (mT5-small)..."
echo "============================================"
python src-chirho/train-chirho/train-parser-chirho.py

# Train glosser
echo ""
echo "============================================"
echo "Training Glosser (mT5-small)..."
echo "============================================"
python src-chirho/train-chirho/train-glosser-chirho.py

# Evaluate
echo ""
echo "============================================"
echo "Running Evaluation..."
echo "============================================"
python src-chirho/eval-chirho/evaluate-chirho.py

# Push to HuggingFace (if HF_TOKEN_CHIRHO is set)
if [ -n "${HF_TOKEN_CHIRHO:-}" ]; then
    echo ""
    echo "============================================"
    echo "Uploading to HuggingFace..."
    echo "============================================"
    python src-chirho/upload-hf-chirho.py
else
    echo ""
    echo "HF_TOKEN_CHIRHO not set — skipping HuggingFace upload."
    echo "Models saved locally in models-chirho/{parser,glosser}-chirho/best-chirho/"
fi

echo ""
echo "============================================"
echo "Training complete!"
echo "============================================"
echo "Parser:  models-chirho/parser-chirho/best-chirho/"
echo "Glosser: models-chirho/glosser-chirho/best-chirho/"
echo "Results: spec-chirho/eval-results-chirho.json"
