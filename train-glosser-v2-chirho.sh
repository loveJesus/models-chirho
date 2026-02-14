#!/bin/bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# Train glosser v2 and upload to HuggingFace
# Run this after chain-after-glosser-chirho.sh completes (parser training finishes)
set -e

VENV_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/.venv-chirho/bin/python3"
BASE_DIR_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho"
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

echo "============================================================"
echo "Glosser v2 Training + Upload"
echo "============================================================"
echo "Started at: $(date)"

# Wait for parser/chain to finish first
echo "Waiting for parser/chain process to finish..."
while pgrep -f "train-parser-chirho" > /dev/null 2>&1; do
    sleep 60
    echo "  Still waiting for parser... $(date)"
done
while pgrep -f "chain-after-glosser-chirho" > /dev/null 2>&1; do
    sleep 30
    echo "  Still waiting for chain... $(date)"
done
echo "Parser/chain finished at: $(date)"
sleep 15

# Train Glosser v2
echo ""
echo "============================================================"
echo "Training Glosser v2"
echo "============================================================"
echo "Start time: $(date)"
cd "$BASE_DIR_CHIRHO/biblical-language-tutor-chirho"
$VENV_CHIRHO src-chirho/train-chirho/train-glosser-chirho.py
echo "Glosser v2 training completed at: $(date)"

# Upload glosser + parser v2
echo ""
echo "============================================================"
echo "Uploading glosser + parser v2 to HuggingFace"
echo "============================================================"
if [ -f src-chirho/upload-hf-chirho.py ]; then
    echo "Uploading glosser + parser v2..."
    $VENV_CHIRHO src-chirho/upload-hf-chirho.py
fi

echo ""
echo "============================================================"
echo "All done! Finished at: $(date)"
echo "============================================================"
