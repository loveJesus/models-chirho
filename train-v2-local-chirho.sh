#!/bin/bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# v2 Local Training Chain: Glosser → Parser → Upload
# Optimized for Apple MPS (M4 Pro)
set -e

VENV_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/.venv-chirho/bin/python3"
BASE_DIR_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho"
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

echo "============================================================"
echo "v2 Local Training: Glosser + Parser + Upload"
echo "============================================================"
echo "Started at: $(date)"
echo ""

# Train Glosser v2
echo "============================================================"
echo "Training Glosser v2 (transliteration-enhanced)"
echo "============================================================"
echo "Start time: $(date)"
cd "$BASE_DIR_CHIRHO/biblical-language-tutor-chirho"
$VENV_CHIRHO src-chirho/train-chirho/train-glosser-chirho.py
echo "Glosser v2 training completed at: $(date)"

echo ""

# Train Parser v2
echo "============================================================"
echo "Training Parser v2 (subsampled 150K for MPS)"
echo "============================================================"
echo "Start time: $(date)"
cd "$BASE_DIR_CHIRHO/biblical-language-tutor-chirho"
$VENV_CHIRHO src-chirho/train-chirho/train-parser-chirho.py
echo "Parser v2 training completed at: $(date)"

echo ""

# Upload all retrained models
echo "============================================================"
echo "Uploading models to HuggingFace"
echo "============================================================"

cd "$BASE_DIR_CHIRHO/biblical-language-tutor-chirho"
if [ -f src-chirho/upload-hf-chirho.py ]; then
    echo "Uploading glosser + parser v2..."
    $VENV_CHIRHO src-chirho/upload-hf-chirho.py
fi

echo ""
echo "============================================================"
echo "All done! Finished at: $(date)"
echo "============================================================"
