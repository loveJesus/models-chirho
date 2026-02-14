#!/bin/bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# Chain: wait for parser → run glosser v2 → upload glosser v2
set -e

VENV_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/.venv-chirho/bin/python3"
BASE_DIR_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho"
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

echo "============================================================"
echo "Post-Parser Chain: Glosser v2 Retrain + Upload"
echo "============================================================"
echo "Started at: $(date)"

# Wait for parser to finish
echo "Waiting for parser process to finish..."
while pgrep -f "train-parser-chirho" > /dev/null 2>&1; do
    sleep 60
    echo "  Still waiting... $(date)"
done
echo "Parser finished at: $(date)"

# Wait for MPS memory to clear
echo "Waiting 60s for MPS memory to clear..."
sleep 60

# Train Glosser v2
echo ""
echo "============================================================"
echo "Training Glosser v2"
echo "============================================================"
echo "Start time: $(date)"
cd "$BASE_DIR_CHIRHO/biblical-language-tutor-chirho"
$VENV_CHIRHO src-chirho/train-chirho/train-glosser-chirho.py
echo "Glosser v2 training completed at: $(date)"

# Upload glosser v2 model
echo ""
echo "============================================================"
echo "Uploading Glosser v2 to HuggingFace"
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
