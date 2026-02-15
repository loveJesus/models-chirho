# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-generator-chirho.py
Train Qwen3-4B-Instruct with LoRA for Model 9: Evangelism & Apologetics.

Fine-tunes the generator to produce Scripture-grounded apologetics responses
using instruction-response pairs from the collected corpus.
"""

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from peft import LoraConfig, TaskType, get_peft_model, PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)

# ── Constants ──────────────────────────────────────────────────────────
MODEL_NAME_CHIRHO = "Qwen/Qwen3-4B-Instruct"
MAX_LENGTH_CHIRHO = 1024
LEARNING_RATE_CHIRHO = 1e-4
EPOCHS_CHIRHO = 3
BATCH_SIZE_CHIRHO = 4
GRADIENT_ACCUMULATION_CHIRHO = 4
WARMUP_RATIO_CHIRHO = 0.05
LORA_R_CHIRHO = 16
LORA_ALPHA_CHIRHO = 32
LORA_DROPOUT_CHIRHO = 0.05
SEED_CHIRHO = 316  # John 3:16

BASE_DIR_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho")
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho" / "generator-chirho"
OUTPUT_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "generator-chirho"
PROGRESS_DB_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/spec-chirho/progress-chirho.sqlite")
AGENT_CODE_CHIRHO = "train-generator-chirho"

SYSTEM_PROMPT_CHIRHO = (
    "You are a knowledgeable Christian apologist and evangelist. "
    "Answer questions with Scripture references, sound reasoning, "
    "and a heart for sharing the Gospel of Jesus Christ. "
    "All answers should be grounded in biblical truth (2 Timothy 3:16). "
    "Be respectful, thorough, and always point to Christ."
)


def log_progress_chirho(action_chirho, result_chirho, overview_chirho):
    """Log progress to SQLite."""
    try:
        conn_chirho = sqlite3.connect(str(PROGRESS_DB_CHIRHO))
        cursor_chirho = conn_chirho.cursor()
        cursor_chirho.execute("""
            INSERT INTO steps_taken_chirho
            (agent_code_chirho, timestamp_start_chirho, timestamp_end_chirho,
             action_taken_chirho, result_of_action_chirho, overview_of_result_chirho)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            AGENT_CODE_CHIRHO,
            datetime.now(timezone.utc).isoformat(),
            datetime.now(timezone.utc).isoformat(),
            action_chirho, result_chirho, overview_chirho,
        ))
        conn_chirho.commit()
        conn_chirho.close()
    except Exception as e_chirho:
        print(f"  Warning: Could not log progress: {e_chirho}")


class InstructDatasetChirho(torch.utils.data.Dataset):
    """Dataset for instruction-tuning with chat template."""

    def __init__(self, filepath_chirho, tokenizer_chirho, max_length_chirho=MAX_LENGTH_CHIRHO):
        self.examples_chirho = []

        with open(filepath_chirho, "r", encoding="utf-8") as f_chirho:
            for line_chirho in f_chirho:
                line_chirho = line_chirho.strip()
                if not line_chirho:
                    continue
                entry_chirho = json.loads(line_chirho)
                instruction_chirho = entry_chirho.get("instruction_chirho", "").strip()
                response_chirho = entry_chirho.get("response_chirho", "").strip()

                if not instruction_chirho or not response_chirho:
                    continue

                # Build chat messages
                messages_chirho = [
                    {"role": "system", "content": SYSTEM_PROMPT_CHIRHO},
                    {"role": "user", "content": instruction_chirho},
                    {"role": "assistant", "content": response_chirho},
                ]

                # Apply chat template
                try:
                    text_chirho = tokenizer_chirho.apply_chat_template(
                        messages_chirho,
                        tokenize=False,
                        add_generation_prompt=False,
                    )
                except Exception:
                    # Fallback for models without chat template
                    text_chirho = (
                        f"<|system|>{SYSTEM_PROMPT_CHIRHO}<|end|>"
                        f"<|user|>{instruction_chirho}<|end|>"
                        f"<|assistant|>{response_chirho}<|end|>"
                    )

                encoding_chirho = tokenizer_chirho(
                    text_chirho,
                    truncation=True,
                    max_length=max_length_chirho,
                    padding=False,
                    return_tensors=None,
                )

                input_ids_chirho = encoding_chirho["input_ids"]
                # Labels = input_ids (causal LM), mask padding tokens
                labels_chirho = input_ids_chirho.copy()

                self.examples_chirho.append({
                    "input_ids": input_ids_chirho,
                    "attention_mask": encoding_chirho["attention_mask"],
                    "labels": labels_chirho,
                })

        print(f"  Loaded {len(self.examples_chirho)} examples from {filepath_chirho}")

    def __len__(self):
        return len(self.examples_chirho)

    def __getitem__(self, idx_chirho):
        return self.examples_chirho[idx_chirho]


def main_chirho():
    """Train the apologetics generator with LoRA."""
    print("=" * 60)
    print("Model 9: Generator Training (Qwen3-4B + LoRA)")
    print("=" * 60)

    # Check data exists
    train_path_chirho = DATA_DIR_CHIRHO / "train-chirho.jsonl"
    val_path_chirho = DATA_DIR_CHIRHO / "val-chirho.jsonl"

    if not train_path_chirho.exists():
        print(f"ERROR: Training data not found at {train_path_chirho}")
        print("Run process-corpus-chirho.py first to generate training data.")
        sys.exit(1)

    # Detect device
    if torch.backends.mps.is_available():
        device_chirho = "mps"
    elif torch.cuda.is_available():
        device_chirho = "cuda"
    else:
        device_chirho = "cpu"
    print(f"Device: {device_chirho}")

    # Load tokenizer
    print(f"\nLoading tokenizer: {MODEL_NAME_CHIRHO}")
    tokenizer_chirho = AutoTokenizer.from_pretrained(
        MODEL_NAME_CHIRHO,
        trust_remote_code=True,
    )
    if tokenizer_chirho.pad_token is None:
        tokenizer_chirho.pad_token = tokenizer_chirho.eos_token

    # Load datasets
    print("Loading datasets...")
    train_dataset_chirho = InstructDatasetChirho(train_path_chirho, tokenizer_chirho)
    val_dataset_chirho = InstructDatasetChirho(val_path_chirho, tokenizer_chirho)

    print(f"  Train: {len(train_dataset_chirho)} examples")
    print(f"  Val:   {len(val_dataset_chirho)} examples")

    # Load model
    print(f"\nLoading model: {MODEL_NAME_CHIRHO}")

    # Determine dtype based on device
    if device_chirho == "cuda":
        dtype_chirho = torch.bfloat16
    else:
        dtype_chirho = torch.float32  # MPS and CPU need float32

    model_chirho = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME_CHIRHO,
        torch_dtype=dtype_chirho,
        trust_remote_code=True,
        device_map="auto" if device_chirho == "cuda" else None,
    )

    if device_chirho == "mps":
        model_chirho = model_chirho.to("mps")

    # LoRA configuration
    print(f"\nApplying LoRA: r={LORA_R_CHIRHO}, alpha={LORA_ALPHA_CHIRHO}")
    lora_config_chirho = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=LORA_R_CHIRHO,
        lora_alpha=LORA_ALPHA_CHIRHO,
        lora_dropout=LORA_DROPOUT_CHIRHO,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
    )
    model_chirho = get_peft_model(model_chirho, lora_config_chirho)
    model_chirho.print_trainable_parameters()

    # Data collator
    data_collator_chirho = DataCollatorForSeq2Seq(
        tokenizer=tokenizer_chirho,
        padding=True,
        return_tensors="pt",
    )

    # Training arguments
    training_args_chirho = TrainingArguments(
        output_dir=str(OUTPUT_DIR_CHIRHO),
        num_train_epochs=EPOCHS_CHIRHO,
        per_device_train_batch_size=BATCH_SIZE_CHIRHO,
        per_device_eval_batch_size=BATCH_SIZE_CHIRHO,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION_CHIRHO,
        learning_rate=LEARNING_RATE_CHIRHO,
        warmup_ratio=WARMUP_RATIO_CHIRHO,
        weight_decay=0.01,
        eval_strategy="steps",
        eval_steps=500,
        save_strategy="steps",
        save_steps=500,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        save_total_limit=2,
        seed=SEED_CHIRHO,
        fp16=False,  # MPS compatibility
        bf16=(device_chirho == "cuda"),
        dataloader_pin_memory=False,  # MPS compatibility
        logging_steps=25,
        report_to="none",
        gradient_checkpointing=True,
        optim="adamw_torch",
        remove_unused_columns=False,
    )

    # Create trainer
    trainer_chirho = Trainer(
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_dataset_chirho,
        eval_dataset=val_dataset_chirho,
        processing_class=tokenizer_chirho,
        data_collator=data_collator_chirho,
    )

    # Train
    print(f"\n{'=' * 60}")
    print("TRAINING")
    print(f"{'=' * 60}")
    print(f"  Effective batch size: {BATCH_SIZE_CHIRHO * GRADIENT_ACCUMULATION_CHIRHO}")

    log_progress_chirho(
        f"Start generator training: {MODEL_NAME_CHIRHO} + LoRA, {len(train_dataset_chirho)} examples, {EPOCHS_CHIRHO} epochs",
        "Training started",
        f"Device: {device_chirho}, LoRA r={LORA_R_CHIRHO}, alpha={LORA_ALPHA_CHIRHO}, "
        f"effective_batch={BATCH_SIZE_CHIRHO * GRADIENT_ACCUMULATION_CHIRHO}, lr={LEARNING_RATE_CHIRHO}",
    )

    train_result_chirho = trainer_chirho.train()

    # Evaluate
    print(f"\n{'=' * 60}")
    print("EVALUATION")
    print(f"{'=' * 60}")

    eval_results_chirho = trainer_chirho.evaluate()
    print(f"\n  Eval loss: {eval_results_chirho.get('eval_loss', 0):.4f}")
    print(f"  Eval perplexity: {np.exp(eval_results_chirho.get('eval_loss', 0)):.2f}")

    # Save LoRA adapter
    best_dir_chirho = OUTPUT_DIR_CHIRHO / "best-chirho"
    best_dir_chirho.mkdir(parents=True, exist_ok=True)
    model_chirho.save_pretrained(str(best_dir_chirho))
    tokenizer_chirho.save_pretrained(str(best_dir_chirho))

    print(f"\n  LoRA adapter saved to: {best_dir_chirho}")

    # Log completion
    log_progress_chirho(
        f"Generator training complete: eval_loss={eval_results_chirho.get('eval_loss', 0):.4f}",
        f"LoRA adapter saved to {best_dir_chirho}",
        f"Perplexity={np.exp(eval_results_chirho.get('eval_loss', 0)):.2f}, "
        f"Train examples={len(train_dataset_chirho)}, Epochs={EPOCHS_CHIRHO}",
    )

    print(f"\n{'=' * 60}")
    print("TRAINING COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main_chirho()
