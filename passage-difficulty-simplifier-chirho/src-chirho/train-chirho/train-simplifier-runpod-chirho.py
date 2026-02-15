# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-simplifier-runpod-chirho.py
Uploads simplifier data to RunPod H200 and runs flan-t5-base training.
"""

import os
import subprocess
import sys
import time

SSH_HOST_CHIRHO = "213.181.111.149"
SSH_PORT_CHIRHO = "11943"
SSH_OPTS_CHIRHO = "-o StrictHostKeyChecking=no -o ConnectTimeout=10"

BASE_DIR_CHIRHO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR_CHIRHO = os.path.join(BASE_DIR_CHIRHO, "data-chirho", "processed-chirho")
TRAIN_SCRIPT_CHIRHO = os.path.join(BASE_DIR_CHIRHO, "src-chirho", "train-chirho", "train-simplifier-chirho.py")


def run_ssh_chirho(cmd_chirho: str, check_chirho: bool = True) -> str:
    """Run command on RunPod via SSH."""
    full_cmd_chirho = f"ssh {SSH_OPTS_CHIRHO} -p {SSH_PORT_CHIRHO} root@{SSH_HOST_CHIRHO} '{cmd_chirho}'"
    result_chirho = subprocess.run(full_cmd_chirho, shell=True, capture_output=True, text=True)
    if check_chirho and result_chirho.returncode != 0:
        print(f"SSH ERROR: {result_chirho.stderr}")
    return result_chirho.stdout.strip()


def scp_upload_chirho(local_path_chirho: str, remote_path_chirho: str):
    """Upload file to RunPod via SCP."""
    cmd_chirho = f"scp {SSH_OPTS_CHIRHO} -P {SSH_PORT_CHIRHO} '{local_path_chirho}' root@{SSH_HOST_CHIRHO}:{remote_path_chirho}"
    subprocess.run(cmd_chirho, shell=True, check=True)


def main_chirho():
    print("=" * 60)
    print("Simplifier Retraining on RunPod H200")
    print("flan-t5-base (248M params)")
    print("=" * 60)

    # Create remote directories
    print("\n1. Creating remote directories...")
    run_ssh_chirho("mkdir -p /workspace/simplifier-chirho/data-chirho/processed-chirho")
    run_ssh_chirho("mkdir -p /workspace/simplifier-chirho/models-chirho/simplifier-chirho")

    # Upload data files
    print("\n2. Uploading data files...")
    for split_chirho in ["train-simplifier-chirho.jsonl", "val-simplifier-chirho.jsonl"]:
        local_file_chirho = os.path.join(DATA_DIR_CHIRHO, split_chirho)
        if os.path.exists(local_file_chirho):
            print(f"  Uploading {split_chirho}...")
            scp_upload_chirho(local_file_chirho, f"/workspace/simplifier-chirho/data-chirho/processed-chirho/{split_chirho}")
        else:
            print(f"  WARNING: {local_file_chirho} not found!")

    # Create the RunPod training script
    print("\n3. Creating RunPod training script...")
    runpod_script_chirho = '''#!/usr/bin/env python3
# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""RunPod flan-t5-base simplifier training."""

import json
import os
from pathlib import Path

import numpy as np
import torch
from datasets import Dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

DATA_DIR_CHIRHO = Path("/workspace/simplifier-chirho/data-chirho/processed-chirho")
OUTPUT_DIR_CHIRHO = Path("/workspace/simplifier-chirho/models-chirho/simplifier-chirho")
BEST_DIR_CHIRHO = OUTPUT_DIR_CHIRHO / "best-chirho"
MODEL_NAME_CHIRHO = "google/flan-t5-base"
MAX_INPUT_LENGTH_CHIRHO = 256
MAX_TARGET_LENGTH_CHIRHO = 256


def load_jsonl_chirho(file_path_chirho):
    examples_chirho = []
    with open(file_path_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            obj_chirho = json.loads(line_chirho)
            examples_chirho.append({
                "input_text_chirho": obj_chirho["input_chirho"],
                "target_text_chirho": obj_chirho["target_chirho"],
                "task_chirho": obj_chirho.get("task_chirho", "unknown"),
            })
    return examples_chirho


def preprocess_function_chirho(examples_chirho, tokenizer_chirho):
    model_inputs_chirho = tokenizer_chirho(
        examples_chirho["input_text_chirho"],
        max_length=MAX_INPUT_LENGTH_CHIRHO,
        truncation=True,
        padding=False,
    )
    labels_chirho = tokenizer_chirho(
        text_target=examples_chirho["target_text_chirho"],
        max_length=MAX_TARGET_LENGTH_CHIRHO,
        truncation=True,
        padding=False,
    )
    model_inputs_chirho["labels"] = labels_chirho["input_ids"]
    return model_inputs_chirho


def compute_metrics_chirho(eval_preds_chirho, tokenizer_chirho):
    import re
    predictions_chirho, labels_chirho = eval_preds_chirho
    pad_id_chirho = int(tokenizer_chirho.pad_token_id or 0)
    vocab_size_chirho = tokenizer_chirho.vocab_size
    predictions_chirho = np.clip(predictions_chirho, 0, vocab_size_chirho - 1).astype(np.int64)
    labels_chirho = np.where(labels_chirho != -100, labels_chirho, pad_id_chirho)
    labels_chirho = np.clip(labels_chirho, 0, vocab_size_chirho - 1).astype(np.int64)
    decoded_preds_chirho = tokenizer_chirho.batch_decode(predictions_chirho.tolist(), skip_special_tokens=True)
    decoded_labels_chirho = tokenizer_chirho.batch_decode(labels_chirho.tolist(), skip_special_tokens=True)
    decoded_preds_chirho = [p.strip() for p in decoded_preds_chirho]
    decoded_labels_chirho = [l.strip() for l in decoded_labels_chirho]

    diff_correct_chirho = 0
    diff_total_chirho = 0
    simp_total_chirho = 0
    simp_exact_chirho = 0

    for pred_chirho, label_chirho in zip(decoded_preds_chirho, decoded_labels_chirho):
        if "difficulty:" in label_chirho:
            diff_total_chirho += 1
            pred_match_chirho = re.search(r"difficulty:\\s*(\\w+)", pred_chirho)
            label_match_chirho = re.search(r"difficulty:\\s*(\\w+)", label_chirho)
            if pred_match_chirho and label_match_chirho and pred_match_chirho.group(1) == label_match_chirho.group(1):
                diff_correct_chirho += 1
        else:
            simp_total_chirho += 1
            if pred_chirho.lower() == label_chirho.lower():
                simp_exact_chirho += 1

    metrics_chirho = {}
    if diff_total_chirho > 0:
        metrics_chirho["difficulty_accuracy_chirho"] = diff_correct_chirho / diff_total_chirho
    if simp_total_chirho > 0:
        metrics_chirho["simplification_exact_match_chirho"] = simp_exact_chirho / simp_total_chirho
    diff_acc_chirho = metrics_chirho.get("difficulty_accuracy_chirho", 0.0)
    simp_em_chirho = metrics_chirho.get("simplification_exact_match_chirho", 0.0)
    metrics_chirho["combined_score_chirho"] = 0.4 * diff_acc_chirho + 0.6 * simp_em_chirho
    return metrics_chirho


def main_chirho():
    print("=" * 60)
    print("Simplifier Training - flan-t5-base on RunPod H200")
    print("=" * 60)

    device_chirho = "cuda"
    gpu_name_chirho = torch.cuda.get_device_name(0)
    print(f"GPU: {gpu_name_chirho}")

    batch_size_chirho = 32
    gradient_accumulation_chirho = 1

    print(f"Model: {MODEL_NAME_CHIRHO}")
    print(f"Batch size: {batch_size_chirho}")

    tokenizer_chirho = AutoTokenizer.from_pretrained(MODEL_NAME_CHIRHO)
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME_CHIRHO).to("cuda")

    param_count_chirho = sum(p.numel() for p in model_chirho.parameters())
    print(f"Parameters: {param_count_chirho:,}")

    train_raw_chirho = load_jsonl_chirho(DATA_DIR_CHIRHO / "train-simplifier-chirho.jsonl")
    val_raw_chirho = load_jsonl_chirho(DATA_DIR_CHIRHO / "val-simplifier-chirho.jsonl")
    print(f"Train: {len(train_raw_chirho)} examples")
    print(f"Val: {len(val_raw_chirho)} examples")

    train_dataset_chirho = Dataset.from_list(train_raw_chirho)
    val_dataset_chirho = Dataset.from_list(val_raw_chirho)

    train_tokenized_chirho = train_dataset_chirho.map(
        lambda e: preprocess_function_chirho(e, tokenizer_chirho),
        batched=True,
        remove_columns=train_dataset_chirho.column_names,
    )
    val_tokenized_chirho = val_dataset_chirho.map(
        lambda e: preprocess_function_chirho(e, tokenizer_chirho),
        batched=True,
        remove_columns=val_dataset_chirho.column_names,
    )

    data_collator_chirho = DataCollatorForSeq2Seq(
        tokenizer=tokenizer_chirho, model=model_chirho,
        padding=True, max_length=MAX_INPUT_LENGTH_CHIRHO, label_pad_token_id=-100,
    )

    training_args_chirho = Seq2SeqTrainingArguments(
        output_dir=str(OUTPUT_DIR_CHIRHO),
        num_train_epochs=5,
        per_device_train_batch_size=batch_size_chirho,
        per_device_eval_batch_size=batch_size_chirho,
        gradient_accumulation_steps=gradient_accumulation_chirho,
        learning_rate=2e-4,
        warmup_ratio=0.1,
        weight_decay=0.01,
        lr_scheduler_type="cosine",
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        predict_with_generate=True,
        generation_max_length=MAX_TARGET_LENGTH_CHIRHO,
        logging_steps=100,
        logging_first_step=True,
        report_to="none",
        bf16=True,
        dataloader_num_workers=4,
        remove_unused_columns=True,
        label_smoothing_factor=0.1,
    )

    trainer_chirho = Seq2SeqTrainer(
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_tokenized_chirho,
        eval_dataset=val_tokenized_chirho,
        processing_class=tokenizer_chirho,
        data_collator=data_collator_chirho,
        compute_metrics=lambda ep: compute_metrics_chirho(ep, tokenizer_chirho),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    train_result_chirho = trainer_chirho.train()

    BEST_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)
    trainer_chirho.save_model(str(BEST_DIR_CHIRHO))
    tokenizer_chirho.save_pretrained(str(BEST_DIR_CHIRHO))

    print(f"\\nTraining loss: {train_result_chirho.training_loss:.4f}")

    eval_result_chirho = trainer_chirho.evaluate()
    print(f"Eval loss: {eval_result_chirho.get('eval_loss', 'N/A')}")
    for k, v in eval_result_chirho.items():
        if k != "eval_loss":
            print(f"  {k}: {v}")

    print(f"\\nModel saved to: {BEST_DIR_CHIRHO}")
    print("TRAINING COMPLETE")


if __name__ == "__main__":
    main_chirho()
'''

    # Write the script to a temp file and upload
    tmp_script_chirho = "/tmp/train-simplifier-runpod-chirho.py"
    with open(tmp_script_chirho, "w") as f_chirho:
        f_chirho.write(runpod_script_chirho)
    scp_upload_chirho(tmp_script_chirho, "/workspace/simplifier-chirho/train-simplifier-runpod-chirho.py")

    # Install dependencies and start training
    print("\n4. Starting training on RunPod...")
    run_ssh_chirho("pip install -q datasets sentence-transformers 2>/dev/null")

    # Start training in background
    run_ssh_chirho(
        "cd /workspace/simplifier-chirho && "
        "nohup python train-simplifier-runpod-chirho.py > /workspace/simplifier-chirho/training.log 2>&1 &"
    )

    print("\n5. Training started! Monitor with:")
    print(f"  ssh {SSH_OPTS_CHIRHO} -p {SSH_PORT_CHIRHO} root@{SSH_HOST_CHIRHO} 'tail -f /workspace/simplifier-chirho/training.log'")
    print("\n  When done, download with:")
    print(f"  scp -P {SSH_PORT_CHIRHO} -r root@{SSH_HOST_CHIRHO}:/workspace/simplifier-chirho/models-chirho/simplifier-chirho/best-chirho/ .")


if __name__ == "__main__":
    main_chirho()
