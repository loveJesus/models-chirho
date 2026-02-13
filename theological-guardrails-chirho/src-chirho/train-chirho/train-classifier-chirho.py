# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-classifier-chirho.py
Fine-tunes DeBERTa-v3-large for multi-label theological statement classification.
Supports MPS (Apple Silicon) for local training on M4 Pro.
Optimized with dynamic padding for 3-5x faster training.
"""

import json
import os
from pathlib import Path

import numpy as np
import torch
import yaml
from datasets import Dataset
from sklearn.metrics import f1_score, precision_score, recall_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)

# Paths
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH_CHIRHO = BASE_DIR_CHIRHO / "src-chirho" / "train-chirho" / "config-chirho.yaml"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
OUTPUT_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "classifier-chirho"


def load_config_chirho() -> dict:
    """Load training configuration."""
    with open(CONFIG_PATH_CHIRHO, "r") as f_chirho:
        return yaml.safe_load(f_chirho)


def load_dataset_chirho(split_name_chirho: str, labels_chirho: list[str]) -> Dataset:
    """Load JSONL dataset and convert to HuggingFace Dataset."""
    file_path_chirho = DATA_DIR_CHIRHO / f"{split_name_chirho}-chirho.jsonl"
    examples_chirho: list[dict] = []

    with open(file_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            item_chirho = json.loads(line_chirho)
            text_chirho = item_chirho.get("text_chirho", "")

            # Build multi-hot label vector
            label_vector_chirho = [0.0] * len(labels_chirho)

            if item_chirho.get("label_chirho") == "orthodox":
                label_vector_chirho[0] = 1.0  # orthodox_chirho is index 0
            else:
                heresy_types_chirho = item_chirho.get("heresy_types_chirho", [])
                for ht_chirho in heresy_types_chirho:
                    label_key_chirho = f"{ht_chirho}_chirho"
                    if label_key_chirho in labels_chirho:
                        idx_chirho = labels_chirho.index(label_key_chirho)
                        label_vector_chirho[idx_chirho] = 1.0

            examples_chirho.append({
                "text_chirho": text_chirho,
                "labels_chirho": label_vector_chirho,
            })

    return Dataset.from_dict({
        "text_chirho": [ex_chirho["text_chirho"] for ex_chirho in examples_chirho],
        "labels": [ex_chirho["labels_chirho"] for ex_chirho in examples_chirho],
    })


class MultiLabelCollatorChirho(DataCollatorWithPadding):
    """Data collator that handles dynamic padding while preserving multi-label float targets."""

    def __call__(self, features_chirho):
        labels_chirho = [f_chirho.pop("labels") for f_chirho in features_chirho]
        batch_chirho = super().__call__(features_chirho)
        batch_chirho["labels"] = torch.tensor(labels_chirho, dtype=torch.float32)
        return batch_chirho


def compute_metrics_chirho(eval_pred_chirho):
    """Compute multi-label F1, precision, recall."""
    logits_chirho, labels_chirho = eval_pred_chirho
    predictions_chirho = (torch.sigmoid(torch.tensor(logits_chirho)) > 0.5).numpy().astype(int)
    labels_np_chirho = labels_chirho.astype(int)

    f1_macro_chirho = f1_score(
        labels_np_chirho, predictions_chirho, average="macro", zero_division=0
    )
    f1_micro_chirho = f1_score(
        labels_np_chirho, predictions_chirho, average="micro", zero_division=0
    )
    precision_chirho = precision_score(
        labels_np_chirho, predictions_chirho, average="macro", zero_division=0
    )
    recall_chirho = recall_score(
        labels_np_chirho, predictions_chirho, average="macro", zero_division=0
    )

    return {
        "f1_macro_chirho": f1_macro_chirho,
        "f1_micro_chirho": f1_micro_chirho,
        "precision_chirho": precision_chirho,
        "recall_chirho": recall_chirho,
    }


def main_chirho():
    """Main training loop for the theological classifier."""
    print("=" * 60)
    print("Theological Classifier Training (DeBERTa-v3-large)")
    print("=" * 60)

    config_chirho = load_config_chirho()
    classifier_config_chirho = config_chirho["classifier_chirho"]
    labels_chirho = classifier_config_chirho["labels_chirho"]

    # Device selection
    if torch.backends.mps.is_available():
        device_chirho = "mps"
        print("Using Apple MPS (Metal Performance Shaders)")
    elif torch.cuda.is_available():
        device_chirho = "cuda"
        print("Using CUDA GPU")
    else:
        device_chirho = "cpu"
        print("Using CPU")

    model_name_chirho = classifier_config_chirho["model_name_chirho"]
    num_labels_chirho = classifier_config_chirho["num_labels_chirho"]
    max_length_chirho = classifier_config_chirho["max_length_chirho"]
    print(f"Model: {model_name_chirho}")
    print(f"Labels ({num_labels_chirho}): {labels_chirho}")
    print(f"Max length: {max_length_chirho} (with dynamic padding)")

    # Load tokenizer and model
    print("\nLoading tokenizer and model...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(model_name_chirho, use_fast=False)
    model_chirho = AutoModelForSequenceClassification.from_pretrained(
        model_name_chirho,
        num_labels=num_labels_chirho,
        problem_type="multi_label_classification",
    )

    # Load datasets
    print("Loading datasets...")
    train_dataset_chirho = load_dataset_chirho("train", labels_chirho)
    val_dataset_chirho = load_dataset_chirho("val", labels_chirho)

    print(f"  Train: {len(train_dataset_chirho)} examples")
    print(f"  Validation: {len(val_dataset_chirho)} examples")

    # Tokenize with truncation only (no padding - handled dynamically by collator)
    def tokenize_function_chirho(examples_chirho):
        return tokenizer_chirho(
            examples_chirho["text_chirho"],
            truncation=True,
            max_length=max_length_chirho,
        )

    print("Tokenizing datasets...")
    train_dataset_chirho = train_dataset_chirho.map(
        tokenize_function_chirho, batched=True, remove_columns=["text_chirho"]
    )
    val_dataset_chirho = val_dataset_chirho.map(
        tokenize_function_chirho, batched=True, remove_columns=["text_chirho"]
    )

    # Data collator with dynamic padding
    data_collator_chirho = MultiLabelCollatorChirho(tokenizer=tokenizer_chirho)

    # Training arguments
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    training_args_chirho = TrainingArguments(
        output_dir=str(OUTPUT_DIR_CHIRHO),
        num_train_epochs=classifier_config_chirho["num_epochs_chirho"],
        per_device_train_batch_size=classifier_config_chirho["batch_size_chirho"],
        per_device_eval_batch_size=classifier_config_chirho["batch_size_chirho"] * 2,
        learning_rate=classifier_config_chirho["learning_rate_chirho"],
        weight_decay=classifier_config_chirho["weight_decay_chirho"],
        warmup_steps=110,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro_chirho",
        greater_is_better=True,
        logging_steps=50,
        save_total_limit=3,
        fp16=False,  # MPS doesn't support fp16 well; use default precision
        dataloader_pin_memory=False if device_chirho == "mps" else True,
        report_to="none",
        seed=42,
    )

    # Trainer
    trainer_chirho = Trainer(
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_dataset_chirho,
        eval_dataset=val_dataset_chirho,
        data_collator=data_collator_chirho,
        compute_metrics=compute_metrics_chirho,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    )

    # Train
    print("\nStarting training...")
    train_result_chirho = trainer_chirho.train()

    print("\nTraining complete!")
    print(f"  Training loss: {train_result_chirho.training_loss:.4f}")

    # Evaluate
    print("\nEvaluating on validation set...")
    eval_results_chirho = trainer_chirho.evaluate()
    print(f"  F1 (macro): {eval_results_chirho.get('eval_f1_macro_chirho', 'N/A')}")
    print(f"  F1 (micro): {eval_results_chirho.get('eval_f1_micro_chirho', 'N/A')}")
    print(f"  Precision: {eval_results_chirho.get('eval_precision_chirho', 'N/A')}")
    print(f"  Recall: {eval_results_chirho.get('eval_recall_chirho', 'N/A')}")

    # Save best model
    best_model_dir_chirho = OUTPUT_DIR_CHIRHO / "best-chirho"
    trainer_chirho.save_model(str(best_model_dir_chirho))
    tokenizer_chirho.save_pretrained(str(best_model_dir_chirho))

    # Save label mapping
    label_map_chirho = {i: label_chirho for i, label_chirho in enumerate(labels_chirho)}
    with open(best_model_dir_chirho / "label-map-chirho.json", "w") as f_chirho:
        json.dump(label_map_chirho, f_chirho, indent=2)

    print(f"\nModel saved to: {best_model_dir_chirho}")
    print("Label map saved to: label-map-chirho.json")


if __name__ == "__main__":
    main_chirho()
