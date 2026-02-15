#!/bin/bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# Chain script: After classifier training completes, upload to HF and start topical retraining
# Usage: Run this in background while classifier training is in progress

set -e

BASE_DIR_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho"
VENV_CHIRHO="$BASE_DIR_CHIRHO/.venv-chirho/bin/python3"
source "$BASE_DIR_CHIRHO/.env"

# =============================================
# STEP 1: Wait for classifier training to finish
# =============================================
CLASSIFIER_BEST_CHIRHO="$BASE_DIR_CHIRHO/intertextual-reference-network-chirho/models-chirho/classifier-chirho/best-chirho"
echo "=== Waiting for intertextual classifier retraining to complete ==="
echo "Watching: $CLASSIFIER_BEST_CHIRHO/model.safetensors"

# The training script saves the best model at the end - check if file was modified recently
INITIAL_SIZE_CHIRHO=$(stat -f%z "$CLASSIFIER_BEST_CHIRHO/model.safetensors" 2>/dev/null || echo "0")
while true; do
    CURRENT_SIZE_CHIRHO=$(stat -f%z "$CLASSIFIER_BEST_CHIRHO/model.safetensors" 2>/dev/null || echo "0")
    # Check if the model file size changed (means a new model was saved)
    if [ "$CURRENT_SIZE_CHIRHO" != "$INITIAL_SIZE_CHIRHO" ] && [ "$CURRENT_SIZE_CHIRHO" != "0" ]; then
        # Wait a bit more to ensure writing is complete
        sleep 10
        FINAL_SIZE_CHIRHO=$(stat -f%z "$CLASSIFIER_BEST_CHIRHO/model.safetensors" 2>/dev/null || echo "0")
        if [ "$FINAL_SIZE_CHIRHO" = "$CURRENT_SIZE_CHIRHO" ]; then
            echo "  Classifier model updated! Size: $FINAL_SIZE_CHIRHO bytes"
            break
        fi
    fi
    echo -ne "\r  Waiting... (current size: $CURRENT_SIZE_CHIRHO, initial: $INITIAL_SIZE_CHIRHO)   "
    sleep 30
done

# =============================================
# STEP 2: Upload retrained classifier to HuggingFace
# =============================================
echo ""
echo "=== Uploading retrained intertextual classifier ==="
$VENV_CHIRHO -c "
import os
from huggingface_hub import HfApi

token_chirho = os.environ.get('HF_TOKEN_CHIRHO', '')
api_chirho = HfApi()
repo_id_chirho = 'LoveJesus/intertextual-classifier-chirho'

api_chirho.upload_folder(
    folder_path='$CLASSIFIER_BEST_CHIRHO',
    repo_id=repo_id_chirho,
    token=token_chirho,
    commit_message='Retrain with balanced data (19K examples) + WeightedTrainer for class imbalance fix',
)
print(f'  Uploaded: https://huggingface.co/{repo_id_chirho}')
"

# =============================================
# STEP 3: Start topical search retraining (MiniLM-L12-v2)
# =============================================
echo ""
echo "=== Starting topical search retraining (MiniLM-L12-v2) ==="
cd "$BASE_DIR_CHIRHO"
$VENV_CHIRHO topical-passage-classifier-chirho/src-chirho/train-chirho/train-topical-chirho.py 2>&1

# =============================================
# STEP 4: Upload retrained topical model
# =============================================
echo ""
echo "=== Uploading retrained topical search model ==="
TOPICAL_BEST_CHIRHO="$BASE_DIR_CHIRHO/topical-passage-classifier-chirho/models-chirho/topical-chirho/best-chirho"
$VENV_CHIRHO -c "
import os
from huggingface_hub import HfApi

token_chirho = os.environ.get('HF_TOKEN_CHIRHO', '')
api_chirho = HfApi()
repo_id_chirho = 'LoveJesus/biblical-topical-search-chirho'

api_chirho.upload_folder(
    folder_path='$TOPICAL_BEST_CHIRHO',
    repo_id=repo_id_chirho,
    token=token_chirho,
    commit_message='Retrain with MiniLM-L12-v2 (upgrade from L6-v2)',
)
print(f'  Uploaded: https://huggingface.co/{repo_id_chirho}')
"

echo ""
echo "=== CHAIN COMPLETE ==="
echo "  1. Intertextual classifier retrained and uploaded"
echo "  2. Topical search retrained (L12) and uploaded"
