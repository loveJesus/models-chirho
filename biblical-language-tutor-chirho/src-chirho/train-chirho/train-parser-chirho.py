# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-parser-chirho.py
Fine-tunes mT5-small for morphological parsing of biblical Hebrew and Greek.

Input:  "parse [hebrew]: בָּרָא [GEN 1:1] context: בְּרֵאשִׁית אֱלֹהִים"
Output: "class:verb | stem:qal | lemma:ברא | morph:... | person:3 | gender:m | number:s | gloss:he created"

Supports: CUDA (A100/H200/B200), MPS (Apple Silicon), CPU fallback.
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
import yaml
from datasets import Dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

# Paths
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH_CHIRHO = BASE_DIR_CHIRHO / "src-chirho" / "train-chirho" / "config-chirho.yaml"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
OUTPUT_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "parser-chirho"


def load_config_chirho() -> dict:
    """Load training configuration."""
    with open(CONFIG_PATH_CHIRHO, "r") as f_chirho:
        return yaml.safe_load(f_chirho)


def detect_device_chirho() -> str:
    """Auto-detect best available device."""
    if torch.cuda.is_available():
        device_name_chirho = torch.cuda.get_device_name(0)
        print(f"Using CUDA GPU: {device_name_chirho}")
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print("Using Apple MPS (Metal Performance Shaders)")
        return "mps"
    else:
        print("Using CPU (this will be slow)")
        return "cpu"


def load_jsonl_chirho(file_path_chirho: Path) -> Dataset:
    """Load JSONL file into HuggingFace Dataset."""
    inputs_chirho = []
    targets_chirho = []

    with open(file_path_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            item_chirho = json.loads(line_chirho)
            inputs_chirho.append(item_chirho["input_chirho"])
            targets_chirho.append(item_chirho["target_chirho"])

    return Dataset.from_dict({
        "input_text_chirho": inputs_chirho,
        "target_text_chirho": targets_chirho,
    })


def compute_metrics_chirho(eval_preds_chirho, tokenizer_chirho):
    """Compute exact match and per-tag F1."""
    predictions_chirho, labels_chirho = eval_preds_chirho

    # Replace -100 with pad token for decoding
    labels_chirho = np.where(labels_chirho != -100, labels_chirho, tokenizer_chirho.pad_token_id)

    # Clip token IDs to valid vocab range and cast to int32
    # (mT5 generate() can produce out-of-range float IDs that overflow C int conversion)
    vocab_size_chirho = tokenizer_chirho.vocab_size
    predictions_chirho = np.nan_to_num(predictions_chirho, nan=0.0)
    predictions_chirho = np.clip(predictions_chirho, 0, vocab_size_chirho - 1).astype(np.int32)
    labels_chirho = np.clip(labels_chirho, 0, vocab_size_chirho - 1).astype(np.int32)

    decoded_preds_chirho = tokenizer_chirho.batch_decode(predictions_chirho, skip_special_tokens=True)
    decoded_labels_chirho = tokenizer_chirho.batch_decode(labels_chirho, skip_special_tokens=True)

    # Exact match
    exact_matches_chirho = sum(
        1 for pred_chirho, label_chirho in zip(decoded_preds_chirho, decoded_labels_chirho)
        if pred_chirho.strip() == label_chirho.strip()
    )
    exact_match_chirho = exact_matches_chirho / len(decoded_preds_chirho) if decoded_preds_chirho else 0

    # Per-tag F1: parse "key:value | key:value" and compute tag-level accuracy
    tag_correct_chirho = 0
    tag_total_chirho = 0

    for pred_chirho, label_chirho in zip(decoded_preds_chirho, decoded_labels_chirho):
        pred_tags_chirho = set(t_chirho.strip() for t_chirho in pred_chirho.split("|"))
        label_tags_chirho = set(t_chirho.strip() for t_chirho in label_chirho.split("|"))

        for tag_chirho in label_tags_chirho:
            tag_total_chirho += 1
            if tag_chirho in pred_tags_chirho:
                tag_correct_chirho += 1

    tag_f1_chirho = tag_correct_chirho / tag_total_chirho if tag_total_chirho > 0 else 0

    return {
        "exact_match_chirho": exact_match_chirho,
        "tag_f1_chirho": tag_f1_chirho,
    }


def main_chirho():
    """Main training loop for the morphological parser."""
    print("=" * 60)
    print("Biblical Morphological Parser Training (mT5-small)")
    print("=" * 60)

    config_chirho = load_config_chirho()
    parser_config_chirho = config_chirho["parser_chirho"]

    # Device
    device_chirho = detect_device_chirho()
    is_cuda_chirho = device_chirho == "cuda"
    is_mps_chirho = device_chirho == "mps"

    model_name_chirho = parser_config_chirho["model_name_chirho"]
    max_input_length_chirho = parser_config_chirho["max_input_length_chirho"]
    max_target_length_chirho = parser_config_chirho["max_target_length_chirho"]

    print(f"Model: {model_name_chirho}")
    print(f"Max input length: {max_input_length_chirho}")
    print(f"Max target length: {max_target_length_chirho}")

    # Load tokenizer and model
    print("\nLoading tokenizer and model...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(model_name_chirho)
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(model_name_chirho)

    # Load datasets
    print("Loading datasets...")
    train_dataset_chirho = load_jsonl_chirho(DATA_DIR_CHIRHO / "train-parser-chirho.jsonl")
    val_dataset_chirho = load_jsonl_chirho(DATA_DIR_CHIRHO / "val-parser-chirho.jsonl")

    print(f"  Train: {len(train_dataset_chirho)} examples")
    print(f"  Validation: {len(val_dataset_chirho)} examples")

    # Subsample training set for MPS speed
    max_train_chirho = parser_config_chirho.get("max_train_samples_chirho", 0)
    if max_train_chirho and len(train_dataset_chirho) > max_train_chirho:
        train_dataset_chirho = train_dataset_chirho.shuffle(seed=42).select(range(max_train_chirho))
        print(f"  Train subsampled to: {len(train_dataset_chirho)} examples")

    # Subsample eval set for speed (predict_with_generate is slow)
    max_eval_chirho = parser_config_chirho.get("max_eval_samples_chirho", 0)
    if max_eval_chirho and len(val_dataset_chirho) > max_eval_chirho:
        val_dataset_chirho = val_dataset_chirho.shuffle(seed=42).select(range(max_eval_chirho))
        print(f"  Eval subsampled to: {len(val_dataset_chirho)} examples")

    # Tokenize
    def tokenize_function_chirho(examples_chirho):
        model_inputs_chirho = tokenizer_chirho(
            examples_chirho["input_text_chirho"],
            max_length=max_input_length_chirho,
            truncation=True,
            padding=False,
        )
        labels_chirho = tokenizer_chirho(
            text_target=examples_chirho["target_text_chirho"],
            max_length=max_target_length_chirho,
            truncation=True,
            padding=False,
        )
        model_inputs_chirho["labels"] = labels_chirho["input_ids"]
        return model_inputs_chirho

    print("Tokenizing datasets...")
    train_dataset_chirho = train_dataset_chirho.map(
        tokenize_function_chirho,
        batched=True,
        remove_columns=["input_text_chirho", "target_text_chirho"],
    )
    val_dataset_chirho = val_dataset_chirho.map(
        tokenize_function_chirho,
        batched=True,
        remove_columns=["input_text_chirho", "target_text_chirho"],
    )

    # Data collator (pads dynamically)
    data_collator_chirho = DataCollatorForSeq2Seq(
        tokenizer=tokenizer_chirho,
        model=model_chirho,
        padding=True,
    )

    # Training arguments
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    # Determine precision: bf16 on CUDA (A100/H200/B200), fp32 on MPS/CPU
    use_bf16_chirho = is_cuda_chirho and parser_config_chirho.get("bf16_chirho", True)
    batch_size_chirho = parser_config_chirho["batch_size_chirho"]

    # Reduce batch size on MPS (less VRAM)
    if is_mps_chirho:
        batch_size_chirho = min(batch_size_chirho, 8)
        print(f"  MPS detected: reducing batch size to {batch_size_chirho}")

    training_args_chirho = Seq2SeqTrainingArguments(
        output_dir=str(OUTPUT_DIR_CHIRHO),
        num_train_epochs=parser_config_chirho["num_epochs_chirho"],
        per_device_train_batch_size=batch_size_chirho,
        per_device_eval_batch_size=batch_size_chirho * 2,
        learning_rate=parser_config_chirho["learning_rate_chirho"],
        weight_decay=parser_config_chirho["weight_decay_chirho"],
        warmup_steps=parser_config_chirho["warmup_steps_chirho"],
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="exact_match_chirho",
        greater_is_better=True,
        predict_with_generate=True,
        generation_max_length=max_target_length_chirho,
        logging_steps=100,
        save_total_limit=3,
        bf16=use_bf16_chirho,
        fp16=False,
        dataloader_pin_memory=not is_mps_chirho,
        report_to="none",
        seed=42,
        gradient_accumulation_steps=1 if is_cuda_chirho else 4,
    )

    # Trainer
    trainer_chirho = Seq2SeqTrainer(
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_dataset_chirho,
        eval_dataset=val_dataset_chirho,
        data_collator=data_collator_chirho,
        compute_metrics=lambda eval_preds_chirho: compute_metrics_chirho(
            eval_preds_chirho, tokenizer_chirho
        ),
        callbacks=[
            EarlyStoppingCallback(
                early_stopping_patience=parser_config_chirho["early_stopping_patience_chirho"]
            )
        ],
    )

    # Resume from checkpoint if requested
    resume_from_chirho = None
    if "--resume" in sys.argv:
        checkpoints_chirho = sorted(OUTPUT_DIR_CHIRHO.glob("checkpoint-*"))
        if checkpoints_chirho:
            resume_from_chirho = str(checkpoints_chirho[-1])
            print(f"\nResuming from checkpoint: {resume_from_chirho}")
        else:
            print("\nNo checkpoint found, starting fresh.")

    # Train
    print("\nStarting training...")
    print(f"  Epochs: {parser_config_chirho['num_epochs_chirho']}")
    print(f"  Batch size: {batch_size_chirho}")
    print(f"  Learning rate: {parser_config_chirho['learning_rate_chirho']}")
    print(f"  BF16: {use_bf16_chirho}")

    train_result_chirho = trainer_chirho.train(resume_from_checkpoint=resume_from_chirho)

    print("\nTraining complete!")
    print(f"  Training loss: {train_result_chirho.training_loss:.4f}")

    # Evaluate
    print("\nEvaluating on validation set...")
    eval_results_chirho = trainer_chirho.evaluate()
    print(f"  Exact match: {eval_results_chirho.get('eval_exact_match_chirho', 'N/A')}")
    print(f"  Tag F1: {eval_results_chirho.get('eval_tag_f1_chirho', 'N/A')}")

    # Save best model
    best_model_dir_chirho = OUTPUT_DIR_CHIRHO / "best-chirho"
    trainer_chirho.save_model(str(best_model_dir_chirho))
    tokenizer_chirho.save_pretrained(str(best_model_dir_chirho))

    print(f"\nModel saved to: {best_model_dir_chirho}")

    # Quick inference test
    print("\n--- Quick Inference Test ---")
    model_chirho.eval()

    test_inputs_chirho = [
        'parse [hebrew]: בָּרָא [GEN 1:1] context: בְּרֵאשִׁית אֱלֹהִים',
        'parse [greek]: λόγος [JHN 1:1] context: ἐν ἀρχῇ ἦν',
    ]

    for test_input_chirho in test_inputs_chirho:
        input_ids_chirho = tokenizer_chirho(
            test_input_chirho, return_tensors="pt", max_length=max_input_length_chirho, truncation=True
        ).input_ids

        input_ids_chirho = input_ids_chirho.to(device_chirho)

        with torch.no_grad():
            output_ids_chirho = model_chirho.generate(
                input_ids_chirho, max_length=max_target_length_chirho
            )

        output_text_chirho = tokenizer_chirho.decode(output_ids_chirho[0], skip_special_tokens=True)
        print(f"  Input:  {test_input_chirho}")
        print(f"  Output: {output_text_chirho}")
        print()


if __name__ == "__main__":
    main_chirho()
