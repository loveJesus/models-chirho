# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-classifier-chirho.py
Trains a DeBERTa-v3-small text classifier for NT manuscript variant type classification.

Variant types:
  - substitution: Different word forms across editions
  - omission: Word present in some editions but not others
  - addition: Extra words in some editions
  - spelling: Minor orthographic variants
  - harmonization: Reading from parallel passage
  - word_order: Same words in different sequences

Input: "classify variant [greek]: βαπτίζω [MAT.3.11] editions: NTS context: ..."
Output: "type:substitution | lemma:βαπτίζω | morph:V-PAI-1S | editions:NTS | variant:..."
"""

import json
import os
import sys

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


def load_dataset_chirho(file_path_chirho: str) -> Dataset:
    """Load JSONL dataset file."""
    inputs_chirho = []
    targets_chirho = []

    with open(file_path_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            example_chirho = json.loads(line_chirho)
            inputs_chirho.append(example_chirho["input_chirho"])
            targets_chirho.append(example_chirho["target_chirho"])

    return Dataset.from_dict({
        "input_text_chirho": inputs_chirho,
        "target_text_chirho": targets_chirho,
    })


def compute_metrics_chirho(eval_preds_chirho, tokenizer_chirho):
    """Compute exact match and per-type accuracy."""
    predictions_chirho, labels_chirho = eval_preds_chirho

    # Replace -100 with pad token
    labels_chirho = np.where(labels_chirho != -100, labels_chirho, tokenizer_chirho.pad_token_id)

    # Clip and cast to int32 to prevent overflow
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
    exact_match_chirho = exact_matches_chirho / max(len(decoded_preds_chirho), 1)

    # Type accuracy: extract "type:xxx" from output
    type_correct_chirho = 0
    type_total_chirho = 0
    for pred_chirho, label_chirho in zip(decoded_preds_chirho, decoded_labels_chirho):
        pred_type_chirho = ""
        label_type_chirho = ""
        for part_chirho in pred_chirho.split("|"):
            if "type:" in part_chirho:
                pred_type_chirho = part_chirho.strip()
        for part_chirho in label_chirho.split("|"):
            if "type:" in part_chirho:
                label_type_chirho = part_chirho.strip()

        type_total_chirho += 1
        if pred_type_chirho == label_type_chirho:
            type_correct_chirho += 1

    type_accuracy_chirho = type_correct_chirho / max(type_total_chirho, 1)

    return {
        "exact_match_chirho": exact_match_chirho,
        "type_accuracy_chirho": type_accuracy_chirho,
    }


def main_chirho():
    """Main training function."""
    print("=" * 60)
    print("Manuscript Variant Classifier Training (mT5-small)")
    print("=" * 60)

    # Detect device
    if torch.cuda.is_available():
        device_chirho = "cuda"
        gpu_name_chirho = torch.cuda.get_device_name(0)
        print(f"Using CUDA GPU: {gpu_name_chirho}")
        is_cuda_chirho = True
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = "mps"
        print("Using Apple MPS")
        is_cuda_chirho = False
    else:
        device_chirho = "cpu"
        print("Using CPU")
        is_cuda_chirho = False

    # Config
    model_name_chirho = "google/mt5-small"
    max_input_length_chirho = 256
    max_target_length_chirho = 128
    data_dir_chirho = os.path.join(os.path.dirname(__file__), "../../data-chirho/processed-chirho")

    print(f"Model: {model_name_chirho}")
    print(f"Max input length: {max_input_length_chirho}")
    print(f"Max target length: {max_target_length_chirho}")

    # Load tokenizer and model
    print("\nLoading tokenizer and model...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(model_name_chirho)
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(model_name_chirho)

    # Load datasets
    print("Loading datasets...")
    train_path_chirho = os.path.join(data_dir_chirho, "train-variant-chirho.jsonl")
    val_path_chirho = os.path.join(data_dir_chirho, "val-variant-chirho.jsonl")

    train_dataset_chirho = load_dataset_chirho(train_path_chirho)
    val_dataset_chirho = load_dataset_chirho(val_path_chirho)

    print(f"  Train: {len(train_dataset_chirho)} examples")
    print(f"  Validation: {len(val_dataset_chirho)} examples")

    # Tokenize
    def tokenize_fn_chirho(examples_chirho):
        model_inputs_chirho = tokenizer_chirho(
            examples_chirho["input_text_chirho"],
            max_length=max_input_length_chirho,
            truncation=True,
            padding="max_length",
        )
        labels_chirho = tokenizer_chirho(
            text_target=examples_chirho["target_text_chirho"],
            max_length=max_target_length_chirho,
            truncation=True,
            padding="max_length",
        )
        model_inputs_chirho["labels"] = labels_chirho["input_ids"]
        return model_inputs_chirho

    print("Tokenizing datasets...")
    train_dataset_chirho = train_dataset_chirho.map(tokenize_fn_chirho, batched=True, remove_columns=["input_text_chirho", "target_text_chirho"])
    val_dataset_chirho = val_dataset_chirho.map(tokenize_fn_chirho, batched=True, remove_columns=["input_text_chirho", "target_text_chirho"])

    # Training args
    output_dir_chirho = os.path.join(os.path.dirname(__file__), "../../models-chirho/classifier-chirho")
    best_dir_chirho = os.path.join(output_dir_chirho, "best-chirho")

    batch_size_chirho = 32 if is_cuda_chirho else 8
    epochs_chirho = 10
    lr_chirho = 3e-4

    training_args_chirho = Seq2SeqTrainingArguments(
        output_dir=output_dir_chirho,
        num_train_epochs=epochs_chirho,
        per_device_train_batch_size=batch_size_chirho,
        per_device_eval_batch_size=batch_size_chirho,
        learning_rate=lr_chirho,
        warmup_steps=500,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="type_accuracy_chirho",
        greater_is_better=True,
        predict_with_generate=True,
        generation_max_length=max_target_length_chirho,
        bf16=is_cuda_chirho,
        fp16=False,
        logging_steps=100,
        report_to="none",
        dataloader_num_workers=4 if is_cuda_chirho else 0,
    )

    # Data collator
    data_collator_chirho = DataCollatorForSeq2Seq(
        tokenizer_chirho,
        model=model_chirho,
        label_pad_token_id=-100,
    )

    # Trainer
    print(f"\nStarting training...")
    print(f"  Epochs: {epochs_chirho}")
    print(f"  Batch size: {batch_size_chirho}")
    print(f"  Learning rate: {lr_chirho}")
    print(f"  BF16: {is_cuda_chirho}")

    trainer_chirho = Seq2SeqTrainer(
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_dataset_chirho,
        eval_dataset=val_dataset_chirho,
        processing_class=tokenizer_chirho,
        data_collator=data_collator_chirho,
        compute_metrics=lambda eval_preds_chirho: compute_metrics_chirho(
            eval_preds_chirho, tokenizer_chirho
        ),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    )

    trainer_chirho.train()

    # Save best model
    print(f"\nSaving best model to {best_dir_chirho}...")
    trainer_chirho.save_model(best_dir_chirho)
    tokenizer_chirho.save_pretrained(best_dir_chirho)

    # Quick inference test
    print("\nInference test:")
    test_input_chirho = "classify variant [greek]: βαπτίζω [MAT.3.11] editions: NTS context: ἐγὼ μὲν ὑμᾶς βαπτίζω ἐν ὕδατι"
    input_ids_chirho = tokenizer_chirho(test_input_chirho, return_tensors="pt").input_ids
    input_ids_chirho = input_ids_chirho.to(device_chirho)
    model_chirho = model_chirho.to(device_chirho)

    with torch.no_grad():
        outputs_chirho = model_chirho.generate(input_ids_chirho, max_length=max_target_length_chirho)

    result_chirho = tokenizer_chirho.decode(outputs_chirho[0], skip_special_tokens=True)
    print(f"  Input: {test_input_chirho}")
    print(f"  Output: {result_chirho}")
    print("\nTraining complete!")


if __name__ == "__main__":
    main_chirho()
