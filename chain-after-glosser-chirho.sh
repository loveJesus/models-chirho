#!/bin/bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# Chain: wait for glosser → run parser → upload all
set -e

VENV_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/.venv-chirho/bin/python3"
BASE_DIR_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho"
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

echo "============================================================"
echo "Post-Glosser Chain: Parser + Upload"
echo "============================================================"
echo "Started at: $(date)"

# Wait for glosser to finish
echo "Waiting for glosser process to finish..."
while pgrep -f "train-glosser-chirho" > /dev/null 2>&1; do
    sleep 60
    echo "  Still waiting... $(date)"
done
echo "Glosser finished at: $(date)"
sleep 15

# Train Parser v2
echo ""
echo "============================================================"
echo "Training Parser v2"
echo "============================================================"
echo "Start time: $(date)"
cd "$BASE_DIR_CHIRHO/biblical-language-tutor-chirho"
$VENV_CHIRHO src-chirho/train-chirho/train-parser-chirho.py
echo "Parser v2 training completed at: $(date)"

# Upload all retrained models
echo ""
echo "============================================================"
echo "Uploading models to HuggingFace"
echo "============================================================"

cd "$BASE_DIR_CHIRHO/manuscript-variant-analyzer-chirho"
if [ -f src-chirho/upload-hf-chirho.py ]; then
    echo "Uploading variant classifier v2..."
    $VENV_CHIRHO src-chirho/upload-hf-chirho.py
fi

cd "$BASE_DIR_CHIRHO/biblical-language-tutor-chirho"
if [ -f src-chirho/upload-hf-chirho.py ]; then
    echo "Uploading glosser + parser v2..."
    $VENV_CHIRHO src-chirho/upload-hf-chirho.py
fi

echo ""
echo "============================================================"
echo "All done! Finished at: $(date)"
echo "============================================================"
