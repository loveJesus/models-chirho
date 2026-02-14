#!/usr/bin/env bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# retrain-v2-all-chirho.sh
# Trains all v2 models sequentially on RunPod A100:
#   1. Variant classifier (~15 min)
#   2. Parser v2 (~2 hrs)
#   3. Glosser v2 (~45 min)
# Then pushes models to HuggingFace Hub.

set -euo pipefail

WORKSPACE_CHIRHO="/workspace"
HF_TOKEN_CHIRHO="${HF_TOKEN_CHIRHO:-}"
LOG_CHIRHO="${WORKSPACE_CHIRHO}/training-v2-chirho.log"

echo "============================================" | tee "$LOG_CHIRHO"
echo "V2 Retraining Pipeline - $(date)" | tee -a "$LOG_CHIRHO"
echo "============================================" | tee -a "$LOG_CHIRHO"

# Install dependencies
echo "Installing dependencies..." | tee -a "$LOG_CHIRHO"
pip install -q transformers datasets accelerate sentencepiece protobuf sacrebleu pyyaml huggingface_hub 2>&1 | tail -5 | tee -a "$LOG_CHIRHO"

# ===== 1. VARIANT CLASSIFIER =====
echo "" | tee -a "$LOG_CHIRHO"
echo "===== [1/3] Variant Classifier v2 =====" | tee -a "$LOG_CHIRHO"
VARIANT_DIR_CHIRHO="${WORKSPACE_CHIRHO}/variant-chirho"

if [ -d "${VARIANT_DIR_CHIRHO}/models-chirho/classifier-chirho/best-chirho" ] && [ -f "${VARIANT_DIR_CHIRHO}/models-chirho/classifier-chirho/best-chirho/model.safetensors" ]; then
    echo "Variant classifier already trained, skipping." | tee -a "$LOG_CHIRHO"
else
    cd "$VARIANT_DIR_CHIRHO"
    python src-chirho/train-chirho/train-classifier-chirho.py 2>&1 | tee -a "$LOG_CHIRHO"
    echo "Variant classifier done at $(date)" | tee -a "$LOG_CHIRHO"
fi

# Push variant to HF
if [ -n "$HF_TOKEN_CHIRHO" ]; then
    echo "Pushing variant classifier to HuggingFace..." | tee -a "$LOG_CHIRHO"
    python3 -c "
from huggingface_hub import HfApi
api_chirho = HfApi(token='${HF_TOKEN_CHIRHO}')
api_chirho.upload_folder(
    folder_path='${VARIANT_DIR_CHIRHO}/models-chirho/classifier-chirho/best-chirho',
    repo_id='LoveJesus/biblical-variant-classifier-chirho',
    repo_type='model',
    commit_message='v2 retrained variant classifier with improved data'
)
print('Variant classifier pushed to HF!')
" 2>&1 | tee -a "$LOG_CHIRHO"
fi

# ===== 2. PARSER v2 =====
echo "" | tee -a "$LOG_CHIRHO"
echo "===== [2/3] Parser v2 (530K examples) =====" | tee -a "$LOG_CHIRHO"
TUTOR_DIR_CHIRHO="${WORKSPACE_CHIRHO}/tutor-chirho"

if [ -d "${TUTOR_DIR_CHIRHO}/models-chirho/parser-chirho/best-chirho" ] && [ -f "${TUTOR_DIR_CHIRHO}/models-chirho/parser-chirho/best-chirho/model.safetensors" ]; then
    echo "Parser v2 already trained, skipping." | tee -a "$LOG_CHIRHO"
else
    cd "$TUTOR_DIR_CHIRHO"
    python src-chirho/train-chirho/train-parser-chirho.py 2>&1 | tee -a "$LOG_CHIRHO"
    echo "Parser v2 done at $(date)" | tee -a "$LOG_CHIRHO"
fi

# Push parser to HF
if [ -n "$HF_TOKEN_CHIRHO" ]; then
    echo "Pushing parser v2 to HuggingFace..." | tee -a "$LOG_CHIRHO"
    python3 -c "
from huggingface_hub import HfApi
api_chirho = HfApi(token='${HF_TOKEN_CHIRHO}')
api_chirho.upload_folder(
    folder_path='${TUTOR_DIR_CHIRHO}/models-chirho/parser-chirho/best-chirho',
    repo_id='LoveJesus/biblical-parser-chirho',
    repo_type='model',
    commit_message='v2 parser: 530K examples with Hebrew transliteration'
)
print('Parser v2 pushed to HF!')
" 2>&1 | tee -a "$LOG_CHIRHO"
fi

# ===== 3. GLOSSER v2 =====
echo "" | tee -a "$LOG_CHIRHO"
echo "===== [3/3] Glosser v2 (31K examples) =====" | tee -a "$LOG_CHIRHO"

if [ -d "${TUTOR_DIR_CHIRHO}/models-chirho/glosser-chirho/best-chirho" ] && [ -f "${TUTOR_DIR_CHIRHO}/models-chirho/glosser-chirho/best-chirho/model.safetensors" ]; then
    echo "Glosser v2 already trained, skipping." | tee -a "$LOG_CHIRHO"
else
    cd "$TUTOR_DIR_CHIRHO"
    python src-chirho/train-chirho/train-glosser-chirho.py 2>&1 | tee -a "$LOG_CHIRHO"
    echo "Glosser v2 done at $(date)" | tee -a "$LOG_CHIRHO"
fi

# Push glosser to HF
if [ -n "$HF_TOKEN_CHIRHO" ]; then
    echo "Pushing glosser v2 to HuggingFace..." | tee -a "$LOG_CHIRHO"
    python3 -c "
from huggingface_hub import HfApi
api_chirho = HfApi(token='${HF_TOKEN_CHIRHO}')
api_chirho.upload_folder(
    folder_path='${TUTOR_DIR_CHIRHO}/models-chirho/glosser-chirho/best-chirho',
    repo_id='LoveJesus/biblical-glosser-chirho',
    repo_type='model',
    commit_message='v2 glosser: improved Hebrew transliteration + quality'
)
print('Glosser v2 pushed to HF!')
" 2>&1 | tee -a "$LOG_CHIRHO"
fi

echo "" | tee -a "$LOG_CHIRHO"
echo "============================================" | tee -a "$LOG_CHIRHO"
echo "All v2 training complete at $(date)" | tee -a "$LOG_CHIRHO"
echo "============================================" | tee -a "$LOG_CHIRHO"
