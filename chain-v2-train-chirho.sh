#!/bin/bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# Chain v2 retraining: glosser → parser → upload
# Run this AFTER variant classifier finishes

set -e

VENV_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/.venv-chirho/bin/python3"
BASE_DIR_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho"
VARIANT_PID_CHIRHO=32528

echo "============================================================"
echo "V2 Chained Training Pipeline"
echo "============================================================"
echo "Started at: $(date)"
echo ""

# Step 0: Wait for variant classifier training to finish
if kill -0 $VARIANT_PID_CHIRHO 2>/dev/null; then
    echo "Waiting for variant classifier (PID $VARIANT_PID_CHIRHO) to finish..."
    while kill -0 $VARIANT_PID_CHIRHO 2>/dev/null; do
        sleep 30
        echo "  Still waiting... $(date)"
    done
    echo "Variant classifier training finished at: $(date)"
    echo "Waiting 10s for MPS memory to clear..."
    sleep 10
else
    echo "Variant classifier already finished."
fi
echo ""

# Step 1: Train Glosser v2
echo "============================================================"
echo "STEP 1: Training Glosser v2"
echo "============================================================"
echo "Start time: $(date)"
cd "$BASE_DIR_CHIRHO/biblical-language-tutor-chirho"
$VENV_CHIRHO src-chirho/train-chirho/train-glosser-chirho.py
echo "Glosser v2 training completed at: $(date)"
echo ""

# Step 2: Train Parser v2
echo "============================================================"
echo "STEP 2: Training Parser v2"
echo "============================================================"
echo "Start time: $(date)"
$VENV_CHIRHO src-chirho/train-chirho/train-parser-chirho.py
echo "Parser v2 training completed at: $(date)"
echo ""

# Step 3: Upload retrained models to HuggingFace
echo "============================================================"
echo "STEP 3: Uploading models to HuggingFace"
echo "============================================================"
echo "Start time: $(date)"

# Upload variant classifier
cd "$BASE_DIR_CHIRHO/manuscript-variant-analyzer-chirho"
if [ -f src-chirho/upload-hf-chirho.py ]; then
    echo "Uploading variant classifier..."
    $VENV_CHIRHO src-chirho/upload-hf-chirho.py
fi

# Upload glosser
cd "$BASE_DIR_CHIRHO/biblical-language-tutor-chirho"
if [ -f src-chirho/upload-hf-chirho.py ]; then
    echo "Uploading glosser + parser..."
    $VENV_CHIRHO src-chirho/upload-hf-chirho.py
fi

echo ""
echo "============================================================"
echo "All v2 training and uploads complete!"
echo "Finished at: $(date)"
echo "============================================================"
