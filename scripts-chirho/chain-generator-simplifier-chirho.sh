#!/bin/bash
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

# Chain script: Wait for generator on RunPod, download, upload, then retrain simplifier
# This handles the RunPod side after the generator finishes

set -e

BASE_DIR_CHIRHO="/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho"
VENV_CHIRHO="$BASE_DIR_CHIRHO/.venv-chirho/bin/python3"
SSH_HOST_CHIRHO="213.181.111.149"
SSH_PORT_CHIRHO="11943"
SSH_OPTS_CHIRHO="-o StrictHostKeyChecking=no -o ConnectTimeout=10"
source "$BASE_DIR_CHIRHO/.env"

LOCAL_GEN_DIR_CHIRHO="$BASE_DIR_CHIRHO/evangelism-apologetics-chirho/models-chirho/generator-chirho/best-chirho"
REMOTE_GEN_DIR_CHIRHO="/workspace/models/generator-chirho/best-chirho"
SIMPLIFIER_DATA_DIR_CHIRHO="$BASE_DIR_CHIRHO/passage-difficulty-simplifier-chirho/data-chirho/processed-chirho"
LOCAL_SIMP_DIR_CHIRHO="$BASE_DIR_CHIRHO/passage-difficulty-simplifier-chirho/models-chirho/simplifier-chirho/best-chirho"

# =============================================
# STEP 1: Wait for generator training to complete
# =============================================
echo "=== Waiting for generator training on RunPod ==="
while true; do
    has_model_chirho=$(ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO \
        "ls ${REMOTE_GEN_DIR_CHIRHO}/adapter_config.json 2>/dev/null && echo 'DONE'" 2>/dev/null)

    if echo "$has_model_chirho" | grep -q "DONE"; then
        echo ""
        echo "=== GENERATOR TRAINING COMPLETE! ==="
        break
    fi

    progress_chirho=$(ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO \
        'cat /proc/525/fd/2 2>/dev/null | grep -oP "\d+/1992 \[.*?\]" | tail -1' 2>/dev/null)
    echo -ne "\r  Generator: $progress_chirho   "
    sleep 120
done

# =============================================
# STEP 2: Download generator LoRA adapter
# =============================================
echo ""
echo "=== Downloading LoRA adapter ==="
mkdir -p "$LOCAL_GEN_DIR_CHIRHO"
scp $SSH_OPTS_CHIRHO -P $SSH_PORT_CHIRHO -r \
    "root@${SSH_HOST_CHIRHO}:${REMOTE_GEN_DIR_CHIRHO}/" "$LOCAL_GEN_DIR_CHIRHO/"
echo "  Downloaded to: $LOCAL_GEN_DIR_CHIRHO"

# Copy README
cp "$BASE_DIR_CHIRHO/evangelism-apologetics-chirho/models-chirho/generator-chirho/README-chirho.md" \
   "$LOCAL_GEN_DIR_CHIRHO/README.md"

# =============================================
# STEP 3: Upload generator to HuggingFace
# =============================================
echo ""
echo "=== Uploading generator to HuggingFace ==="
$VENV_CHIRHO -c "
import os
from huggingface_hub import HfApi, create_repo
token_chirho = os.environ.get('HF_TOKEN_CHIRHO', '')
api_chirho = HfApi()
repo_id_chirho = 'LoveJesus/evangelism-generator-chirho'
create_repo(repo_id_chirho, token=token_chirho, exist_ok=True, private=False)
api_chirho.upload_folder(
    folder_path='$LOCAL_GEN_DIR_CHIRHO',
    repo_id=repo_id_chirho,
    token=token_chirho,
    commit_message='Upload Qwen3-14B LoRA generator for Model 9: Evangelism & Apologetics',
)
print(f'  Done: https://huggingface.co/{repo_id_chirho}')
"

# =============================================
# STEP 4: Upload simplifier data and training script to RunPod
# =============================================
echo ""
echo "=== Uploading simplifier data to RunPod ==="
ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO \
    "mkdir -p /workspace/simplifier-chirho/data-chirho/processed-chirho"

for split_chirho in train-simplifier-chirho.jsonl val-simplifier-chirho.jsonl; do
    echo "  Uploading $split_chirho..."
    scp $SSH_OPTS_CHIRHO -P $SSH_PORT_CHIRHO \
        "$SIMPLIFIER_DATA_DIR_CHIRHO/$split_chirho" \
        "root@${SSH_HOST_CHIRHO}:/workspace/simplifier-chirho/data-chirho/processed-chirho/$split_chirho"
done

# Upload training script
scp $SSH_OPTS_CHIRHO -P $SSH_PORT_CHIRHO \
    "$BASE_DIR_CHIRHO/passage-difficulty-simplifier-chirho/src-chirho/train-chirho/train-simplifier-runpod-chirho.py" \
    "root@${SSH_HOST_CHIRHO}:/workspace/simplifier-chirho/train-simplifier-runpod-chirho.py"

# Wait, the train-simplifier-runpod-chirho.py has an embedded script inside it that it uploads.
# Let me just use the embedded script directly
echo "  Creating training script on RunPod..."

ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO 'cat > /workspace/simplifier-chirho/train-chirho.py << '"'"'ENDSCRIPT'"'"'
#!/usr/bin/env python3
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

import json, re, os
from pathlib import Path
import numpy as np
import torch
from datasets import Dataset
from transformers import (
    AutoModelForSeq2SeqLM, AutoTokenizer, DataCollatorForSeq2Seq,
    EarlyStoppingCallback, Seq2SeqTrainer, Seq2SeqTrainingArguments,
)

DATA_DIR_CHIRHO = Path("/workspace/simplifier-chirho/data-chirho/processed-chirho")
OUTPUT_DIR_CHIRHO = Path("/workspace/simplifier-chirho/models-chirho")
BEST_DIR_CHIRHO = OUTPUT_DIR_CHIRHO / "best-chirho"
MODEL_NAME_CHIRHO = "google/flan-t5-base"

def load_jsonl_chirho(fp):
    exs = []
    with open(fp, "r") as f:
        for line in f:
            if not line.strip(): continue
            o = json.loads(line)
            exs.append({"input_text_chirho": o["input_chirho"], "target_text_chirho": o["target_chirho"], "task_chirho": o.get("task_chirho", "unknown")})
    return exs

def preprocess_chirho(examples, tok):
    mi = tok(examples["input_text_chirho"], max_length=256, truncation=True, padding=False)
    labels = tok(text_target=examples["target_text_chirho"], max_length=256, truncation=True, padding=False)
    mi["labels"] = labels["input_ids"]
    return mi

def compute_metrics_chirho(ep, tok):
    preds, labs = ep
    pad = int(tok.pad_token_id or 0)
    vs = tok.vocab_size
    preds = np.clip(preds, 0, vs-1).astype(np.int64)
    labs = np.where(labs != -100, labs, pad)
    labs = np.clip(labs, 0, vs-1).astype(np.int64)
    dp = tok.batch_decode(preds.tolist(), skip_special_tokens=True)
    dl = tok.batch_decode(labs.tolist(), skip_special_tokens=True)
    dp = [p.strip() for p in dp]
    dl = [l.strip() for l in dl]
    dc, dt, st, se = 0, 0, 0, 0
    for p, l in zip(dp, dl):
        if "difficulty:" in l:
            dt += 1
            pm = re.search(r"difficulty:\s*(\w+)", p)
            lm = re.search(r"difficulty:\s*(\w+)", l)
            if pm and lm and pm.group(1) == lm.group(1): dc += 1
        else:
            st += 1
            if p.lower() == l.lower(): se += 1
    m = {}
    if dt > 0: m["difficulty_accuracy_chirho"] = dc / dt
    if st > 0: m["simplification_exact_match_chirho"] = se / st
    m["combined_score_chirho"] = 0.4 * m.get("difficulty_accuracy_chirho", 0) + 0.6 * m.get("simplification_exact_match_chirho", 0)
    return m

print("=" * 60)
print("Simplifier Training - flan-t5-base on RunPod H200")
print("=" * 60)
print(f"GPU: {torch.cuda.get_device_name(0)}")

tok = AutoTokenizer.from_pretrained(MODEL_NAME_CHIRHO)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME_CHIRHO).to("cuda")
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")

tr = load_jsonl_chirho(DATA_DIR_CHIRHO / "train-simplifier-chirho.jsonl")
vl = load_jsonl_chirho(DATA_DIR_CHIRHO / "val-simplifier-chirho.jsonl")
print(f"Train: {len(tr)}, Val: {len(vl)}")

trd = Dataset.from_list(tr).map(lambda e: preprocess_chirho(e, tok), batched=True, remove_columns=["input_text_chirho", "target_text_chirho", "task_chirho"])
vld = Dataset.from_list(vl).map(lambda e: preprocess_chirho(e, tok), batched=True, remove_columns=["input_text_chirho", "target_text_chirho", "task_chirho"])

dc = DataCollatorForSeq2Seq(tokenizer=tok, model=model, padding=True, max_length=256, label_pad_token_id=-100)

args = Seq2SeqTrainingArguments(
    output_dir=str(OUTPUT_DIR_CHIRHO), num_train_epochs=5, per_device_train_batch_size=32,
    per_device_eval_batch_size=32, learning_rate=2e-4, warmup_ratio=0.1, weight_decay=0.01,
    lr_scheduler_type="cosine", eval_strategy="epoch", save_strategy="epoch", save_total_limit=3,
    load_best_model_at_end=True, metric_for_best_model="eval_loss", greater_is_better=False,
    predict_with_generate=True, generation_max_length=256, logging_steps=100, logging_first_step=True,
    report_to="none", bf16=True, dataloader_num_workers=4, label_smoothing_factor=0.1,
)

trainer = Seq2SeqTrainer(
    model=model, args=args, train_dataset=trd, eval_dataset=vld,
    processing_class=tok, data_collator=dc,
    compute_metrics=lambda ep: compute_metrics_chirho(ep, tok),
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
)

result = trainer.train()
BEST_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)
trainer.save_model(str(BEST_DIR_CHIRHO))
tok.save_pretrained(str(BEST_DIR_CHIRHO))

print(f"\nTraining loss: {result.training_loss:.4f}")
ev = trainer.evaluate()
print(f"Eval loss: {ev.get('eval_loss', 'N/A')}")
for k, v in ev.items():
    if k != "eval_loss": print(f"  {k}: {v}")
print(f"\nModel saved to: {BEST_DIR_CHIRHO}")
print("SIMPLIFIER TRAINING COMPLETE")
ENDSCRIPT'

# =============================================
# STEP 5: Start simplifier training on RunPod
# =============================================
echo ""
echo "=== Starting simplifier training on RunPod ==="
ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO \
    "pip install -q datasets 2>/dev/null; cd /workspace/simplifier-chirho && nohup python train-chirho.py > training.log 2>&1 &"
echo "  Training started in background"

# =============================================
# STEP 6: Monitor simplifier training
# =============================================
echo ""
echo "=== Monitoring simplifier training ==="
while true; do
    done_check_chirho=$(ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO \
        "grep 'SIMPLIFIER TRAINING COMPLETE' /workspace/simplifier-chirho/training.log 2>/dev/null" 2>/dev/null)

    if [ -n "$done_check_chirho" ]; then
        echo ""
        echo "=== SIMPLIFIER TRAINING COMPLETE! ==="
        # Show final metrics
        ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO \
            "tail -20 /workspace/simplifier-chirho/training.log" 2>/dev/null
        break
    fi

    progress_chirho=$(ssh $SSH_OPTS_CHIRHO -p $SSH_PORT_CHIRHO root@$SSH_HOST_CHIRHO \
        "tail -1 /workspace/simplifier-chirho/training.log 2>/dev/null" 2>/dev/null)
    echo -ne "\r  Simplifier: $progress_chirho   "
    sleep 120
done

# =============================================
# STEP 7: Download retrained simplifier
# =============================================
echo ""
echo "=== Downloading retrained simplifier ==="
mkdir -p "$LOCAL_SIMP_DIR_CHIRHO"
scp $SSH_OPTS_CHIRHO -P $SSH_PORT_CHIRHO -r \
    "root@${SSH_HOST_CHIRHO}:/workspace/simplifier-chirho/models-chirho/best-chirho/" "$LOCAL_SIMP_DIR_CHIRHO/"
echo "  Downloaded to: $LOCAL_SIMP_DIR_CHIRHO"

# =============================================
# STEP 8: Upload retrained simplifier to HuggingFace
# =============================================
echo ""
echo "=== Uploading retrained simplifier to HuggingFace ==="
$VENV_CHIRHO -c "
import os
from huggingface_hub import HfApi
token_chirho = os.environ.get('HF_TOKEN_CHIRHO', '')
api_chirho = HfApi()
repo_id_chirho = 'LoveJesus/passage-difficulty-simplifier-chirho'
api_chirho.upload_folder(
    folder_path='$LOCAL_SIMP_DIR_CHIRHO',
    repo_id=repo_id_chirho,
    token=token_chirho,
    commit_message='Retrain with flan-t5-base (248M, upgrade from flan-t5-small 80M)',
)
print(f'  Done: https://huggingface.co/{repo_id_chirho}')
"

echo ""
echo "=== RUNPOD CHAIN COMPLETE ==="
echo "  1. Generator downloaded and uploaded to HuggingFace"
echo "  2. Simplifier retrained with flan-t5-base and uploaded to HuggingFace"
echo ""
echo "  Remember to terminate RunPod pod to stop billing!"
