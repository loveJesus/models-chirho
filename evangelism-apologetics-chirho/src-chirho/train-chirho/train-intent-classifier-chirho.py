# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-intent-classifier-chirho.py
Train RoBERTa-base intent classifier for Model 9: Evangelism & Apologetics.

Classifies user queries into 5 categories:
  - evangelism_dialogue
  - apologetics_qa
  - creation_science
  - historical_evidence
  - miracle_testimony

Uses WeightedTrainerChirho for class imbalance handling.
"""

import json
import os
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import classification_report, f1_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)

# ── Constants ──────────────────────────────────────────────────────────
MODEL_NAME_CHIRHO = "roberta-base"
MAX_LENGTH_CHIRHO = 128
LEARNING_RATE_CHIRHO = 2e-5
EPOCHS_CHIRHO = 5
BATCH_SIZE_CHIRHO = 16
WARMUP_RATIO_CHIRHO = 0.1
SEED_CHIRHO = 316  # John 3:16

BASE_DIR_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho")
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho" / "intent-classifier-chirho"
OUTPUT_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "intent-classifier-chirho"
PROGRESS_DB_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/spec-chirho/progress-chirho.sqlite")
AGENT_CODE_CHIRHO = "train-intent-classifier-chirho"

LABEL_MAP_CHIRHO = {
    "evangelism_dialogue": 0,
    "apologetics_qa": 1,
    "creation_science": 2,
    "historical_evidence": 3,
    "miracle_testimony": 4,
}
ID_TO_LABEL_CHIRHO = {v_chirho: k_chirho for k_chirho, v_chirho in LABEL_MAP_CHIRHO.items()}


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


class IntentDatasetChirho(torch.utils.data.Dataset):
    """Dataset for intent classification."""

    def __init__(self, filepath_chirho, tokenizer_chirho, max_length_chirho=MAX_LENGTH_CHIRHO):
        self.encodings_chirho = {"input_ids": [], "attention_mask": []}
        self.labels_chirho = []

        with open(filepath_chirho, "r", encoding="utf-8") as f_chirho:
            for line_chirho in f_chirho:
                line_chirho = line_chirho.strip()
                if not line_chirho:
                    continue
                entry_chirho = json.loads(line_chirho)
                text_chirho = entry_chirho["text_chirho"]
                label_chirho = LABEL_MAP_CHIRHO.get(entry_chirho["label_chirho"])

                if label_chirho is None:
                    continue

                encoding_chirho = tokenizer_chirho(
                    text_chirho,
                    truncation=True,
                    max_length=max_length_chirho,
                    padding="max_length",
                    return_tensors="pt",
                )
                self.encodings_chirho["input_ids"].append(encoding_chirho["input_ids"].squeeze())
                self.encodings_chirho["attention_mask"].append(encoding_chirho["attention_mask"].squeeze())
                self.labels_chirho.append(label_chirho)

        self.encodings_chirho["input_ids"] = torch.stack(self.encodings_chirho["input_ids"])
        self.encodings_chirho["attention_mask"] = torch.stack(self.encodings_chirho["attention_mask"])
        self.labels_chirho = torch.tensor(self.labels_chirho, dtype=torch.long)

    def __len__(self):
        return len(self.labels_chirho)

    def __getitem__(self, idx_chirho):
        return {
            "input_ids": self.encodings_chirho["input_ids"][idx_chirho],
            "attention_mask": self.encodings_chirho["attention_mask"][idx_chirho],
            "labels": self.labels_chirho[idx_chirho],
        }


class WeightedTrainerChirho(Trainer):
    """Trainer with inverse-frequency class weights for imbalanced data."""

    def __init__(self, class_weights_chirho=None, **kwargs_chirho):
        super().__init__(**kwargs_chirho)
        self._class_weights_chirho = class_weights_chirho

    def compute_loss(self, model_chirho, inputs_chirho, return_outputs=False, **kwargs_chirho):
        labels_chirho = inputs_chirho.pop("labels")
        outputs_chirho = model_chirho(**inputs_chirho)
        logits_chirho = outputs_chirho.logits

        if self._class_weights_chirho is not None:
            weight_chirho = self._class_weights_chirho.to(logits_chirho.device)
            loss_fn_chirho = torch.nn.CrossEntropyLoss(weight=weight_chirho)
        else:
            loss_fn_chirho = torch.nn.CrossEntropyLoss()

        loss_chirho = loss_fn_chirho(logits_chirho, labels_chirho)
        return (loss_chirho, outputs_chirho) if return_outputs else loss_chirho


def compute_metrics_chirho(eval_pred_chirho):
    """Compute classification metrics."""
    logits_chirho, labels_chirho = eval_pred_chirho
    preds_chirho = np.argmax(logits_chirho, axis=-1)

    macro_f1_chirho = f1_score(labels_chirho, preds_chirho, average="macro")
    weighted_f1_chirho = f1_score(labels_chirho, preds_chirho, average="weighted")

    return {
        "macro_f1": macro_f1_chirho,
        "weighted_f1": weighted_f1_chirho,
    }


def compute_class_weights_chirho(dataset_chirho):
    """Compute inverse-frequency class weights."""
    labels_chirho = dataset_chirho.labels_chirho.numpy()
    counts_chirho = Counter(labels_chirho)
    total_chirho = len(labels_chirho)
    num_classes_chirho = len(LABEL_MAP_CHIRHO)

    weights_chirho = []
    for i_chirho in range(num_classes_chirho):
        count_chirho = counts_chirho.get(i_chirho, 1)
        weights_chirho.append(total_chirho / (num_classes_chirho * count_chirho))

    return torch.tensor(weights_chirho, dtype=torch.float32)


def main_chirho():
    """Train the intent classifier."""
    print("=" * 60)
    print("Model 9: Intent Classifier Training (RoBERTa-base)")
    print("=" * 60)

    # Check data exists
    train_path_chirho = DATA_DIR_CHIRHO / "train-chirho.jsonl"
    val_path_chirho = DATA_DIR_CHIRHO / "val-chirho.jsonl"
    test_path_chirho = DATA_DIR_CHIRHO / "test-chirho.jsonl"

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
    tokenizer_chirho = AutoTokenizer.from_pretrained(MODEL_NAME_CHIRHO)

    # Load datasets
    print("Loading datasets...")
    train_dataset_chirho = IntentDatasetChirho(train_path_chirho, tokenizer_chirho)
    val_dataset_chirho = IntentDatasetChirho(val_path_chirho, tokenizer_chirho)
    test_dataset_chirho = IntentDatasetChirho(test_path_chirho, tokenizer_chirho)

    print(f"  Train: {len(train_dataset_chirho)} examples")
    print(f"  Val:   {len(val_dataset_chirho)} examples")
    print(f"  Test:  {len(test_dataset_chirho)} examples")

    # Print label distribution
    train_labels_chirho = train_dataset_chirho.labels_chirho.numpy()
    dist_chirho = Counter(train_labels_chirho)
    print("\n  Label distribution (train):")
    for label_id_chirho in sorted(dist_chirho.keys()):
        label_name_chirho = ID_TO_LABEL_CHIRHO[label_id_chirho]
        count_chirho = dist_chirho[label_id_chirho]
        pct_chirho = 100.0 * count_chirho / len(train_labels_chirho)
        print(f"    {label_name_chirho}: {count_chirho} ({pct_chirho:.1f}%)")

    # Compute class weights
    class_weights_chirho = compute_class_weights_chirho(train_dataset_chirho)
    print(f"\n  Class weights: {class_weights_chirho.tolist()}")

    # Load model
    print(f"\nLoading model: {MODEL_NAME_CHIRHO}")
    model_chirho = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME_CHIRHO,
        num_labels=len(LABEL_MAP_CHIRHO),
        id2label=ID_TO_LABEL_CHIRHO,
        label2id=LABEL_MAP_CHIRHO,
    )

    # Training arguments
    output_dir_chirho = str(OUTPUT_DIR_CHIRHO)
    training_args_chirho = TrainingArguments(
        output_dir=output_dir_chirho,
        num_train_epochs=EPOCHS_CHIRHO,
        per_device_train_batch_size=BATCH_SIZE_CHIRHO,
        per_device_eval_batch_size=BATCH_SIZE_CHIRHO * 2,
        learning_rate=LEARNING_RATE_CHIRHO,
        warmup_ratio=WARMUP_RATIO_CHIRHO,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        save_total_limit=2,
        seed=SEED_CHIRHO,
        fp16=False,  # MPS compatibility
        dataloader_pin_memory=False,  # MPS compatibility
        logging_steps=50,
        report_to="none",
    )

    # Create trainer
    trainer_chirho = WeightedTrainerChirho(
        class_weights_chirho=class_weights_chirho,
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_dataset_chirho,
        eval_dataset=val_dataset_chirho,
        processing_class=tokenizer_chirho,
        compute_metrics=compute_metrics_chirho,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    # Train
    print("\n" + "=" * 60)
    print("TRAINING")
    print("=" * 60)

    log_progress_chirho(
        f"Start intent classifier training: {MODEL_NAME_CHIRHO}, {len(train_dataset_chirho)} examples, {EPOCHS_CHIRHO} epochs",
        "Training started",
        f"Device: {device_chirho}, batch_size={BATCH_SIZE_CHIRHO}, lr={LEARNING_RATE_CHIRHO}",
    )

    train_result_chirho = trainer_chirho.train()

    # Evaluate on test set
    print("\n" + "=" * 60)
    print("EVALUATION (Test Set)")
    print("=" * 60)

    test_results_chirho = trainer_chirho.evaluate(test_dataset_chirho)
    print(f"\n  Test macro F1:    {test_results_chirho.get('eval_macro_f1', 0):.4f}")
    print(f"  Test weighted F1: {test_results_chirho.get('eval_weighted_f1', 0):.4f}")
    print(f"  Test loss:        {test_results_chirho.get('eval_loss', 0):.4f}")

    # Detailed classification report
    test_preds_chirho = trainer_chirho.predict(test_dataset_chirho)
    pred_labels_chirho = np.argmax(test_preds_chirho.predictions, axis=-1)
    true_labels_chirho = test_preds_chirho.label_ids

    target_names_chirho = [ID_TO_LABEL_CHIRHO[i_chirho] for i_chirho in range(len(LABEL_MAP_CHIRHO))]
    print("\n  Detailed Classification Report:")
    print(classification_report(true_labels_chirho, pred_labels_chirho, target_names=target_names_chirho))

    # Save best model
    best_dir_chirho = OUTPUT_DIR_CHIRHO / "best-chirho"
    trainer_chirho.save_model(str(best_dir_chirho))
    tokenizer_chirho.save_pretrained(str(best_dir_chirho))

    # Save label map
    label_map_path_chirho = best_dir_chirho / "label-map-chirho.json"
    with open(label_map_path_chirho, "w") as f_chirho:
        json.dump({"label2id_chirho": LABEL_MAP_CHIRHO, "id2label_chirho": ID_TO_LABEL_CHIRHO}, f_chirho, indent=2)

    print(f"\n  Best model saved to: {best_dir_chirho}")

    # Log completion
    log_progress_chirho(
        f"Intent classifier training complete: macro_f1={test_results_chirho.get('eval_macro_f1', 0):.4f}",
        f"Model saved to {best_dir_chirho}",
        f"Weighted F1={test_results_chirho.get('eval_weighted_f1', 0):.4f}, "
        f"Loss={test_results_chirho.get('eval_loss', 0):.4f}",
    )

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
