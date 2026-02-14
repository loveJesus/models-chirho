# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-classifier-chirho.py
Fine-tunes RoBERTa-base for single-label cross-reference type classification (7 classes).
Input: verse pair (verse_a [SEP] verse_b) → connection type.
Supports MPS (Apple Silicon), resume from checkpoint.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import yaml
from datasets import Dataset
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report
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

# Connection type label mapping
LABELS_CHIRHO = [
    "direct_quote",
    "allusion",
    "thematic_parallel",
    "typological",
    "prophecy_fulfillment",
    "parallel_narrative",
    "contrast",
]

LABEL2ID_CHIRHO = {label_chirho: i_chirho for i_chirho, label_chirho in enumerate(LABELS_CHIRHO)}
ID2LABEL_CHIRHO = {i_chirho: label_chirho for i_chirho, label_chirho in enumerate(LABELS_CHIRHO)}


class WeightedTrainerChirho(Trainer):
    """Trainer with class-weighted CrossEntropyLoss for imbalanced data."""

    def __init__(self, class_weights_chirho=None, **kwargs_chirho):
        super().__init__(**kwargs_chirho)
        self.class_weights_chirho = class_weights_chirho

    def compute_loss(self, model_chirho, inputs_chirho, return_outputs=False, **kwargs_chirho):
        labels_chirho = inputs_chirho.pop("labels")
        outputs_chirho = model_chirho(**inputs_chirho)
        logits_chirho = outputs_chirho.logits
        if self.class_weights_chirho is not None:
            weights_chirho = self.class_weights_chirho.to(logits_chirho.device)
            loss_fn_chirho = nn.CrossEntropyLoss(weight=weights_chirho)
        else:
            loss_fn_chirho = nn.CrossEntropyLoss()
        loss_chirho = loss_fn_chirho(logits_chirho, labels_chirho)
        return (loss_chirho, outputs_chirho) if return_outputs else loss_chirho


def load_config_chirho() -> dict:
    """Load training configuration."""
    with open(CONFIG_PATH_CHIRHO, "r") as f_chirho:
        return yaml.safe_load(f_chirho)


def load_dataset_chirho(split_name_chirho: str) -> Dataset:
    """Load JSONL dataset and convert to HuggingFace Dataset."""
    file_path_chirho = DATA_DIR_CHIRHO / f"{split_name_chirho}-classifier-chirho.jsonl"
    texts_a_chirho = []
    texts_b_chirho = []
    labels_chirho = []

    with open(file_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            item_chirho = json.loads(line_chirho)
            text_a_chirho = item_chirho.get("from_text_chirho", "")
            text_b_chirho = item_chirho.get("to_text_chirho", "")
            conn_type_chirho = item_chirho.get("connection_type_chirho", "thematic_parallel")

            label_id_chirho = LABEL2ID_CHIRHO.get(conn_type_chirho, LABEL2ID_CHIRHO["thematic_parallel"])

            texts_a_chirho.append(text_a_chirho)
            texts_b_chirho.append(text_b_chirho)
            labels_chirho.append(label_id_chirho)

    return Dataset.from_dict({
        "text_a_chirho": texts_a_chirho,
        "text_b_chirho": texts_b_chirho,
        "label": labels_chirho,
    })


def compute_metrics_chirho(eval_pred_chirho):
    """Compute single-label F1, precision, recall."""
    logits_chirho, labels_chirho = eval_pred_chirho
    predictions_chirho = np.argmax(logits_chirho, axis=-1)

    f1_macro_chirho = f1_score(
        labels_chirho, predictions_chirho, average="macro", zero_division=0
    )
    f1_micro_chirho = f1_score(
        labels_chirho, predictions_chirho, average="micro", zero_division=0
    )
    precision_chirho = precision_score(
        labels_chirho, predictions_chirho, average="macro", zero_division=0
    )
    recall_chirho = recall_score(
        labels_chirho, predictions_chirho, average="macro", zero_division=0
    )

    return {
        "f1_macro_chirho": f1_macro_chirho,
        "f1_micro_chirho": f1_micro_chirho,
        "precision_chirho": precision_chirho,
        "recall_chirho": recall_chirho,
    }


def main_chirho():
    """Main training loop for the connection type classifier."""
    print("=" * 60)
    print("Intertextual Classifier Training (RoBERTa-base)")
    print("=" * 60)

    config_chirho = load_config_chirho()
    cls_config_chirho = config_chirho["classifier_chirho"]

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

    model_name_chirho = cls_config_chirho["model_name_chirho"]
    num_labels_chirho = cls_config_chirho["num_labels_chirho"]
    max_length_chirho = cls_config_chirho["max_length_chirho"]

    print(f"Model: {model_name_chirho}")
    print(f"Labels ({num_labels_chirho}): {LABELS_CHIRHO}")
    print(f"Max length: {max_length_chirho} (with dynamic padding)")

    # Load tokenizer and model
    print("\nLoading tokenizer and model...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(model_name_chirho)
    model_chirho = AutoModelForSequenceClassification.from_pretrained(
        model_name_chirho,
        num_labels=num_labels_chirho,
        id2label=ID2LABEL_CHIRHO,
        label2id=LABEL2ID_CHIRHO,
    )

    # Load datasets
    print("Loading datasets...")
    train_dataset_chirho = load_dataset_chirho("train")
    val_dataset_chirho = load_dataset_chirho("val")

    print(f"  Train: {len(train_dataset_chirho)} examples")
    print(f"  Validation: {len(val_dataset_chirho)} examples")

    # Compute class weights (inverse frequency) for imbalanced data
    label_counts_chirho = Counter(train_dataset_chirho["label"])
    total_samples_chirho = len(train_dataset_chirho)
    num_classes_chirho = len(LABELS_CHIRHO)
    class_weights_chirho = torch.zeros(num_classes_chirho, dtype=torch.float32)
    for class_id_chirho in range(num_classes_chirho):
        count_chirho = label_counts_chirho.get(class_id_chirho, 1)
        class_weights_chirho[class_id_chirho] = total_samples_chirho / (num_classes_chirho * count_chirho)
    print(f"\n  Class weights (inverse freq):")
    for i_chirho, label_chirho in enumerate(LABELS_CHIRHO):
        print(f"    {label_chirho}: {class_weights_chirho[i_chirho]:.3f}")

    # Tokenize — RoBERTa handles sentence pairs with automatic [SEP]
    def tokenize_function_chirho(examples_chirho):
        return tokenizer_chirho(
            examples_chirho["text_a_chirho"],
            examples_chirho["text_b_chirho"],
            truncation=True,
            max_length=max_length_chirho,
        )

    print("Tokenizing datasets...")
    train_dataset_chirho = train_dataset_chirho.map(
        tokenize_function_chirho,
        batched=True,
        remove_columns=["text_a_chirho", "text_b_chirho"],
    )
    val_dataset_chirho = val_dataset_chirho.map(
        tokenize_function_chirho,
        batched=True,
        remove_columns=["text_a_chirho", "text_b_chirho"],
    )

    # Data collator with dynamic padding
    data_collator_chirho = DataCollatorWithPadding(tokenizer=tokenizer_chirho)

    # Training arguments
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    training_args_chirho = TrainingArguments(
        output_dir=str(OUTPUT_DIR_CHIRHO),
        num_train_epochs=cls_config_chirho["num_epochs_chirho"],
        per_device_train_batch_size=cls_config_chirho["batch_size_chirho"],
        per_device_eval_batch_size=cls_config_chirho["batch_size_chirho"] * 2,
        learning_rate=cls_config_chirho["learning_rate_chirho"],
        weight_decay=cls_config_chirho["weight_decay_chirho"],
        warmup_ratio=cls_config_chirho["warmup_ratio_chirho"],
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro_chirho",
        greater_is_better=True,
        logging_steps=50,
        save_total_limit=3,
        fp16=False,  # MPS doesn't support fp16 well
        dataloader_pin_memory=False if device_chirho == "mps" else True,
        report_to="none",
        seed=42,
    )

    # Trainer with class-weighted loss
    trainer_chirho = WeightedTrainerChirho(
        class_weights_chirho=class_weights_chirho,
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_dataset_chirho,
        eval_dataset=val_dataset_chirho,
        data_collator=data_collator_chirho,
        compute_metrics=compute_metrics_chirho,
        callbacks=[
            EarlyStoppingCallback(
                early_stopping_patience=cls_config_chirho["early_stopping_patience_chirho"]
            )
        ],
    )

    # Train (supports --resume)
    resume_from_chirho = None
    if "--resume" in sys.argv:
        checkpoints_chirho = sorted(OUTPUT_DIR_CHIRHO.glob("checkpoint-*"))
        if checkpoints_chirho:
            resume_from_chirho = str(checkpoints_chirho[-1])
            print(f"\nResuming from checkpoint: {resume_from_chirho}")
        else:
            print("\nNo checkpoint found, starting fresh.")

    print("\nStarting training...")
    train_result_chirho = trainer_chirho.train(resume_from_checkpoint=resume_from_chirho)

    print("\nTraining complete!")
    print(f"  Training loss: {train_result_chirho.training_loss:.4f}")

    # Evaluate
    print("\nEvaluating on validation set...")
    eval_results_chirho = trainer_chirho.evaluate()
    print(f"  F1 (macro): {eval_results_chirho.get('eval_f1_macro_chirho', 'N/A')}")
    print(f"  F1 (micro): {eval_results_chirho.get('eval_f1_micro_chirho', 'N/A')}")
    print(f"  Precision: {eval_results_chirho.get('eval_precision_chirho', 'N/A')}")
    print(f"  Recall: {eval_results_chirho.get('eval_recall_chirho', 'N/A')}")

    # Per-class report on test set
    print("\nPer-class classification report (validation):")
    val_predictions_chirho = trainer_chirho.predict(val_dataset_chirho)
    val_preds_chirho = np.argmax(val_predictions_chirho.predictions, axis=-1)
    print(classification_report(
        val_predictions_chirho.label_ids,
        val_preds_chirho,
        target_names=LABELS_CHIRHO,
        zero_division=0,
    ))

    # Save best model
    best_model_dir_chirho = OUTPUT_DIR_CHIRHO / "best-chirho"
    trainer_chirho.save_model(str(best_model_dir_chirho))
    tokenizer_chirho.save_pretrained(str(best_model_dir_chirho))

    # Save label mapping
    label_map_chirho = {str(i_chirho): label_chirho for i_chirho, label_chirho in enumerate(LABELS_CHIRHO)}
    with open(best_model_dir_chirho / "label-map-chirho.json", "w") as f_chirho:
        json.dump(label_map_chirho, f_chirho, indent=2)

    print(f"\nModel saved to: {best_model_dir_chirho}")


if __name__ == "__main__":
    main_chirho()
