# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-simplifier-chirho.py
Fine-tunes google/flan-t5-base for dual-task Bible processing:
  1. Difficulty Scoring:  "rate difficulty: [verse]" -> "reading_level: X | ..."
  2. Simplification:      "simplify: [complex verse]" -> "[simplified verse]"

Multi-task learning: both tasks mixed in the same training run.
Uses Seq2SeqTrainer with DataCollatorForSeq2Seq.

Output: models-chirho/simplifier-chirho/best-chirho/
"""

import json
import os
import sys
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

# ─── Paths ───
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
OUTPUT_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "simplifier-chirho"
BEST_DIR_CHIRHO = OUTPUT_DIR_CHIRHO / "best-chirho"

# ─── Config ───
MODEL_NAME_CHIRHO = "google/flan-t5-base"
MAX_INPUT_LENGTH_CHIRHO = 256
MAX_TARGET_LENGTH_CHIRHO = 256
LEARNING_RATE_CHIRHO = 2e-4
NUM_EPOCHS_CHIRHO = 5
WARMUP_RATIO_CHIRHO = 0.1
BATCH_SIZE_CHIRHO = 12
LOGGING_STEPS_CHIRHO = 100


def detect_device_chirho() -> str:
    """Detect best available device: cuda > mps > cpu."""
    if torch.cuda.is_available():
        gpu_name_chirho = torch.cuda.get_device_name(0)
        print(f"Using CUDA GPU: {gpu_name_chirho}")
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print("Using Apple MPS")
        return "mps"
    else:
        print("Using CPU (training will be slow)")
        return "cpu"


def load_jsonl_chirho(file_path_chirho: Path) -> list[dict]:
    """Load JSONL file into list of dicts."""
    examples_chirho = []
    with open(file_path_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            obj_chirho = json.loads(line_chirho)
            examples_chirho.append(
                {
                    "input_text_chirho": obj_chirho["input_chirho"],
                    "target_text_chirho": obj_chirho["target_chirho"],
                    "task_chirho": obj_chirho.get("task_chirho", "unknown"),
                }
            )
    return examples_chirho


def preprocess_function_chirho(
    examples_chirho: dict,
    tokenizer_chirho: AutoTokenizer,
) -> dict:
    """Tokenize inputs and targets for Seq2Seq training."""
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
    """Compute metrics for both tasks."""
    predictions_chirho, labels_chirho = eval_preds_chirho

    # Replace -100 and out-of-range values (robust overflow safety for transformers 5.x)
    pad_id_chirho = int(tokenizer_chirho.pad_token_id or 0)
    vocab_size_chirho = tokenizer_chirho.vocab_size

    # Clip predictions to valid token ID range, then cast to int64 (not int32 to avoid overflow)
    predictions_chirho = np.clip(predictions_chirho, 0, vocab_size_chirho - 1).astype(np.int64)

    # Replace -100 in labels (padding)
    labels_chirho = np.where(labels_chirho != -100, labels_chirho, pad_id_chirho)
    labels_chirho = np.clip(labels_chirho, 0, vocab_size_chirho - 1).astype(np.int64)

    # Decode predictions
    decoded_preds_chirho = tokenizer_chirho.batch_decode(
        predictions_chirho.tolist(), skip_special_tokens=True
    )
    decoded_labels_chirho = tokenizer_chirho.batch_decode(
        labels_chirho.tolist(), skip_special_tokens=True
    )

    # Strip whitespace
    decoded_preds_chirho = [p_chirho.strip() for p_chirho in decoded_preds_chirho]
    decoded_labels_chirho = [l_chirho.strip() for l_chirho in decoded_labels_chirho]

    # Separate by task (check if target contains "difficulty:" pattern)
    diff_correct_chirho = 0
    diff_total_chirho = 0
    simp_total_chirho = 0
    simp_exact_chirho = 0

    for pred_chirho, label_chirho in zip(decoded_preds_chirho, decoded_labels_chirho):
        if "difficulty:" in label_chirho:
            # Difficulty scoring: check if difficulty label matches
            diff_total_chirho += 1
            pred_diff_chirho = ""
            label_diff_chirho = ""

            import re

            pred_match_chirho = re.search(r"difficulty:\s*(\w+)", pred_chirho)
            label_match_chirho = re.search(r"difficulty:\s*(\w+)", label_chirho)

            if pred_match_chirho:
                pred_diff_chirho = pred_match_chirho.group(1)
            if label_match_chirho:
                label_diff_chirho = label_match_chirho.group(1)

            if pred_diff_chirho == label_diff_chirho:
                diff_correct_chirho += 1
        else:
            # Simplification: track exact match and length ratio
            simp_total_chirho += 1
            if pred_chirho.lower() == label_chirho.lower():
                simp_exact_chirho += 1

    metrics_chirho = {}

    if diff_total_chirho > 0:
        metrics_chirho["difficulty_accuracy_chirho"] = diff_correct_chirho / diff_total_chirho

    if simp_total_chirho > 0:
        metrics_chirho["simplification_exact_match_chirho"] = simp_exact_chirho / simp_total_chirho

    # Overall metric for model selection
    diff_acc_chirho = metrics_chirho.get("difficulty_accuracy_chirho", 0.0)
    simp_em_chirho = metrics_chirho.get("simplification_exact_match_chirho", 0.0)
    metrics_chirho["combined_score_chirho"] = 0.4 * diff_acc_chirho + 0.6 * simp_em_chirho

    return metrics_chirho


def main_chirho():
    """Main training function."""
    print("=" * 60)
    print("Passage Difficulty Scorer & Simplifier Training")
    print("Flan-T5-base Multi-Task Fine-tuning")
    print("=" * 60)

    device_chirho = detect_device_chirho()

    # Adjust batch size for device
    batch_size_chirho = BATCH_SIZE_CHIRHO
    if device_chirho == "cuda":
        batch_size_chirho = 32
    elif device_chirho == "mps":
        batch_size_chirho = 16
    else:
        batch_size_chirho = 8

    gradient_accumulation_chirho = max(1, 16 // batch_size_chirho)

    print(f"\nConfig:")
    print(f"  Model: {MODEL_NAME_CHIRHO}")
    print(f"  Batch size: {batch_size_chirho}")
    print(f"  Gradient accumulation: {gradient_accumulation_chirho}")
    print(f"  Effective batch size: {batch_size_chirho * gradient_accumulation_chirho}")
    print(f"  Epochs: {NUM_EPOCHS_CHIRHO}")
    print(f"  Learning rate: {LEARNING_RATE_CHIRHO}")
    print(f"  Warmup ratio: {WARMUP_RATIO_CHIRHO}")

    # ─── Load tokenizer and model ───
    print("\nLoading model and tokenizer...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(MODEL_NAME_CHIRHO)
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME_CHIRHO)

    # Move model to device
    if device_chirho == "cuda":
        model_chirho = model_chirho.to("cuda")
    elif device_chirho == "mps":
        model_chirho = model_chirho.to("mps")

    param_count_chirho = sum(p_chirho.numel() for p_chirho in model_chirho.parameters())
    trainable_count_chirho = sum(
        p_chirho.numel() for p_chirho in model_chirho.parameters() if p_chirho.requires_grad
    )
    print(f"  Parameters: {param_count_chirho:,} total, {trainable_count_chirho:,} trainable")

    # ─── Load datasets ───
    print("\nLoading datasets...")
    train_path_chirho = DATA_DIR_CHIRHO / "train-simplifier-chirho.jsonl"
    val_path_chirho = DATA_DIR_CHIRHO / "val-simplifier-chirho.jsonl"

    train_raw_chirho = load_jsonl_chirho(train_path_chirho)
    val_raw_chirho = load_jsonl_chirho(val_path_chirho)

    print(f"  Train: {len(train_raw_chirho)} examples")
    print(f"  Val: {len(val_raw_chirho)} examples")

    # Show task distribution
    train_diff_chirho = sum(1 for e_chirho in train_raw_chirho if e_chirho["task_chirho"] == "difficulty_scoring")
    train_simp_chirho = sum(1 for e_chirho in train_raw_chirho if e_chirho["task_chirho"] == "simplification")
    print(f"  Train tasks: difficulty={train_diff_chirho}, simplification={train_simp_chirho}")

    val_diff_chirho = sum(1 for e_chirho in val_raw_chirho if e_chirho["task_chirho"] == "difficulty_scoring")
    val_simp_chirho = sum(1 for e_chirho in val_raw_chirho if e_chirho["task_chirho"] == "simplification")
    print(f"  Val tasks: difficulty={val_diff_chirho}, simplification={val_simp_chirho}")

    # ─── Create HuggingFace datasets ───
    train_dataset_chirho = Dataset.from_list(train_raw_chirho)
    val_dataset_chirho = Dataset.from_list(val_raw_chirho)

    # Tokenize
    print("\nTokenizing...")
    train_tokenized_chirho = train_dataset_chirho.map(
        lambda examples_chirho: preprocess_function_chirho(examples_chirho, tokenizer_chirho),
        batched=True,
        remove_columns=train_dataset_chirho.column_names,
        desc="Tokenizing train",
    )
    val_tokenized_chirho = val_dataset_chirho.map(
        lambda examples_chirho: preprocess_function_chirho(examples_chirho, tokenizer_chirho),
        batched=True,
        remove_columns=val_dataset_chirho.column_names,
        desc="Tokenizing val",
    )

    print(f"  Train tokenized: {len(train_tokenized_chirho)} examples")
    print(f"  Val tokenized: {len(val_tokenized_chirho)} examples")

    # ─── Data collator ───
    data_collator_chirho = DataCollatorForSeq2Seq(
        tokenizer=tokenizer_chirho,
        model=model_chirho,
        padding=True,
        max_length=MAX_INPUT_LENGTH_CHIRHO,
        label_pad_token_id=-100,
    )

    # ─── Training arguments ───
    use_bf16_chirho = device_chirho == "cuda" and torch.cuda.is_bf16_supported()
    use_fp16_chirho = device_chirho == "cuda" and not use_bf16_chirho

    training_args_chirho = Seq2SeqTrainingArguments(
        output_dir=str(OUTPUT_DIR_CHIRHO),
        num_train_epochs=NUM_EPOCHS_CHIRHO,
        per_device_train_batch_size=batch_size_chirho,
        per_device_eval_batch_size=batch_size_chirho,
        gradient_accumulation_steps=gradient_accumulation_chirho,
        learning_rate=LEARNING_RATE_CHIRHO,
        warmup_ratio=WARMUP_RATIO_CHIRHO,
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
        logging_steps=LOGGING_STEPS_CHIRHO,
        logging_first_step=True,
        report_to="none",
        bf16=use_bf16_chirho,
        fp16=use_fp16_chirho,
        dataloader_num_workers=2 if device_chirho != "mps" else 0,
        remove_unused_columns=True,
        label_smoothing_factor=0.1,
    )

    # ─── Trainer ───
    trainer_chirho = Seq2SeqTrainer(
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_tokenized_chirho,
        eval_dataset=val_tokenized_chirho,
        processing_class=tokenizer_chirho,
        data_collator=data_collator_chirho,
        compute_metrics=lambda eval_preds_chirho: compute_metrics_chirho(
            eval_preds_chirho, tokenizer_chirho
        ),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    # ─── Train ───
    print("\n" + "=" * 60)
    print("Starting training...")
    print("=" * 60)

    train_result_chirho = trainer_chirho.train()

    # ─── Save best model ───
    print(f"\nSaving best model to {BEST_DIR_CHIRHO}...")
    BEST_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)
    trainer_chirho.save_model(str(BEST_DIR_CHIRHO))
    tokenizer_chirho.save_pretrained(str(BEST_DIR_CHIRHO))

    # ─── Print training metrics ───
    print("\n" + "=" * 60)
    print("Training Results:")
    print(f"  Train loss: {train_result_chirho.training_loss:.4f}")
    print(f"  Train runtime: {train_result_chirho.metrics.get('train_runtime', 0):.1f}s")
    print(f"  Samples/second: {train_result_chirho.metrics.get('train_samples_per_second', 0):.1f}")

    # ─── Evaluate ───
    print("\nRunning evaluation...")
    eval_result_chirho = trainer_chirho.evaluate()
    print(f"  Eval loss: {eval_result_chirho.get('eval_loss', 'N/A')}")
    for key_chirho, val_chirho in eval_result_chirho.items():
        if key_chirho != "eval_loss":
            print(f"  {key_chirho}: {val_chirho}")

    # ─── Inference test ───
    print("\n" + "=" * 60)
    print("Inference Test:")
    print("=" * 60)

    # Move model to device for inference
    model_chirho = model_chirho.to(device_chirho if device_chirho != "mps" else "cpu")
    model_chirho.eval()

    test_inputs_chirho = [
        "rate difficulty: In the beginning God created the heaven and the earth.",
        "rate difficulty: For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        "simplify: And the LORD God formed man of the dust of the ground, and breathed into his nostrils the breath of life; and man became a living soul.",
        "simplify: For all have sinned, and come short of the glory of God;",
        "simplify: Wherefore, as by one man sin entered into the world, and death by sin; and so death passed upon all men, for that all have sinned:",
    ]

    for test_input_chirho in test_inputs_chirho:
        inputs_chirho = tokenizer_chirho(
            test_input_chirho,
            return_tensors="pt",
            max_length=MAX_INPUT_LENGTH_CHIRHO,
            truncation=True,
        )

        # Move inputs to same device as model
        input_device_chirho = device_chirho if device_chirho != "mps" else "cpu"
        inputs_chirho = {
            k_chirho: v_chirho.to(input_device_chirho)
            for k_chirho, v_chirho in inputs_chirho.items()
        }

        with torch.no_grad():
            outputs_chirho = model_chirho.generate(
                **inputs_chirho,
                max_length=MAX_TARGET_LENGTH_CHIRHO,
                num_beams=4,
                early_stopping=True,
            )

        output_text_chirho = tokenizer_chirho.decode(
            outputs_chirho[0], skip_special_tokens=True
        )

        # Truncate long input for display
        display_input_chirho = test_input_chirho[:80]
        if len(test_input_chirho) > 80:
            display_input_chirho += "..."
        print(f"\n  Input:  {display_input_chirho}")
        print(f"  Output: {output_text_chirho}")

    print("\n" + "=" * 60)
    print("Training complete!")
    print(f"Model saved to: {BEST_DIR_CHIRHO}")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
