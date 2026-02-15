#!/bin/bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# Monitor RunPod generator training, download results, upload to HuggingFace
SSH_HOST_CHIRHO="213.181.111.149"
SSH_PORT_CHIRHO="11943"
SSH_OPTS_CHIRHO="-o StrictHostKeyChecking=no -o ConnectTimeout=10"
LOCAL_DIR_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho/models-chirho/generator-chirho/best-chirho"
REMOTE_DIR_CHIRHO="/workspace/models/generator-chirho/best-chirho"

echo "=== Monitoring generator training on RunPod ==="
echo "SSH: ${SSH_HOST_CHIRHO}:${SSH_PORT_CHIRHO}"

# Wait for training to complete (check for best-chirho directory)
while true; do
    # Check if the best model directory has been created
    has_model=$(ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO \
        "ls ${REMOTE_DIR_CHIRHO}/adapter_config.json 2>/dev/null && echo 'DONE'" 2>/dev/null)

    if echo "$has_model" | grep -q "DONE"; then
        echo ""
        echo "=== TRAINING COMPLETE! ==="
        break
    fi

    # Show progress
    progress=$(ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO \
        'cat /proc/525/fd/2 2>/dev/null | grep -oP "\d+/1992 \[.*?\]" | tail -1' 2>/dev/null)
    echo -ne "\r  Progress: $progress   "
    sleep 60
done

# Download results
echo ""
echo "=== Downloading LoRA adapter ==="
mkdir -p "$LOCAL_DIR_CHIRHO"
scp -o StrictHostKeyChecking=no -P $SSH_PORT_CHIRHO -r \
    "root@${SSH_HOST_CHIRHO}:${REMOTE_DIR_CHIRHO}/" "$LOCAL_DIR_CHIRHO/"

echo "  Downloaded to: $LOCAL_DIR_CHIRHO"
ls -la "$LOCAL_DIR_CHIRHO"

# Copy the pre-made README
cp /Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho/models-chirho/generator-chirho/README-chirho.md \
   "$LOCAL_DIR_CHIRHO/README.md"

# Upload to HuggingFace
echo ""
echo "=== Uploading generator to HuggingFace ==="
source /Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/.env

/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/.venv-chirho/bin/python3 -c "
import os
from huggingface_hub import HfApi, create_repo

token = os.environ.get('HF_TOKEN_CHIRHO', '')
api = HfApi()

repo_id = 'LoveJesus/evangelism-generator-chirho'
create_repo(repo_id, token=token, exist_ok=True, private=False)
api.upload_folder(
    folder_path='$LOCAL_DIR_CHIRHO',
    repo_id=repo_id,
    token=token,
    commit_message='Upload Qwen3-14B LoRA generator for Model 9: Evangelism & Apologetics',
)
print(f'  Done: https://huggingface.co/{repo_id}')
"

echo ""
echo "=== ALL DONE ==="
echo "Generator uploaded to HuggingFace!"
