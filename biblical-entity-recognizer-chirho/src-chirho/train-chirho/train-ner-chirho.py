# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-ner-chirho.py
Fine-tunes DistilBERT for token classification (NER) on biblical text.
Recognizes 6 entity types: PERSON, DIVINE, PEOPLE_GROUP, PLACE, EVENT, ARTIFACT.

Uses BIO tagging scheme with 13 labels:
  O, B-PERSON, I-PERSON, B-DIVINE, I-DIVINE, B-PEOPLE_GROUP, I-PEOPLE_GROUP,
  B-PLACE, I-PLACE, B-EVENT, I-EVENT, B-ARTIFACT, I-ARTIFACT

Supports MPS (Apple Silicon), CUDA, and CPU training.
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
import yaml
from datasets import Dataset
from seqeval.metrics import (
    classification_report,
    f1_score as seqeval_f1_score,
    precision_score as seqeval_precision_score,
    recall_score as seqeval_recall_score,
)
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    DataCollatorForTokenClassification,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)

# Paths
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH_CHIRHO = BASE_DIR_CHIRHO / "config-chirho.yaml"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
OUTPUT_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "ner-chirho"


def load_config_chirho() -> dict:
    """Load training configuration from YAML."""
    with open(CONFIG_PATH_CHIRHO, "r") as f_chirho:
        return yaml.safe_load(f_chirho)


def load_ner_dataset_chirho(split_name_chirho: str) -> list[dict]:
    """Load NER JSONL dataset."""
    file_path_chirho = DATA_DIR_CHIRHO / f"{split_name_chirho}-chirho.jsonl"
    examples_chirho = []

    with open(file_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            item_chirho = json.loads(line_chirho)
            examples_chirho.append(item_chirho)

    return examples_chirho


def build_label_maps_chirho(labels_chirho: list[str]) -> tuple[dict, dict]:
    """Build label-to-id and id-to-label mappings."""
    label2id_chirho = {label_chirho: idx_chirho for idx_chirho, label_chirho in enumerate(labels_chirho)}
    id2label_chirho = {idx_chirho: label_chirho for idx_chirho, label_chirho in enumerate(labels_chirho)}
    return label2id_chirho, id2label_chirho


def create_hf_dataset_chirho(
    examples_chirho: list[dict],
    label2id_chirho: dict,
) -> Dataset:
    """Convert list of NER examples into a HuggingFace Dataset."""
    all_tokens_chirho = []
    all_tag_ids_chirho = []

    for example_chirho in examples_chirho:
        tokens_chirho = example_chirho["tokens_chirho"]
        tags_chirho = example_chirho["ner_tags_chirho"]

        # Convert string tags to integer IDs
        tag_ids_chirho = []
        for tag_chirho in tags_chirho:
            if tag_chirho in label2id_chirho:
                tag_ids_chirho.append(label2id_chirho[tag_chirho])
            else:
                tag_ids_chirho.append(label2id_chirho["O"])

        all_tokens_chirho.append(tokens_chirho)
        all_tag_ids_chirho.append(tag_ids_chirho)

    return Dataset.from_dict({
        "tokens_chirho": all_tokens_chirho,
        "ner_tags_chirho": all_tag_ids_chirho,
    })


def tokenize_and_align_labels_chirho(
    examples_chirho,
    tokenizer_chirho,
    max_length_chirho: int,
    label_all_tokens_chirho: bool = False,
):
    """
    Tokenize examples and align NER labels with subword tokens.

    When a word is split into multiple subword tokens by the tokenizer,
    only the first subtoken gets the original label; the rest get -100
    (ignored in loss computation) unless label_all_tokens_chirho is True.
    """
    tokenized_inputs_chirho = tokenizer_chirho(
        examples_chirho["tokens_chirho"],
        truncation=True,
        max_length=max_length_chirho,
        is_split_into_words=True,
    )

    all_labels_chirho = []

    for i_chirho, label_ids_chirho in enumerate(examples_chirho["ner_tags_chirho"]):
        word_ids_chirho = tokenized_inputs_chirho.word_ids(batch_index=i_chirho)
        previous_word_idx_chirho = None
        aligned_labels_chirho = []

        for word_idx_chirho in word_ids_chirho:
            if word_idx_chirho is None:
                # Special tokens ([CLS], [SEP], [PAD]) get -100
                aligned_labels_chirho.append(-100)
            elif word_idx_chirho != previous_word_idx_chirho:
                # First subtoken of a new word gets the label
                if word_idx_chirho < len(label_ids_chirho):
                    aligned_labels_chirho.append(label_ids_chirho[word_idx_chirho])
                else:
                    aligned_labels_chirho.append(-100)
            else:
                # Subsequent subtokens of the same word
                if label_all_tokens_chirho and word_idx_chirho < len(label_ids_chirho):
                    aligned_labels_chirho.append(label_ids_chirho[word_idx_chirho])
                else:
                    aligned_labels_chirho.append(-100)

            previous_word_idx_chirho = word_idx_chirho

        all_labels_chirho.append(aligned_labels_chirho)

    tokenized_inputs_chirho["labels"] = all_labels_chirho
    return tokenized_inputs_chirho


def compute_metrics_chirho(eval_pred_chirho, id2label_chirho: dict):
    """Compute entity-level precision, recall, and F1 using seqeval."""
    predictions_chirho, labels_chirho = eval_pred_chirho
    predictions_chirho = np.argmax(predictions_chirho, axis=2)

    # Convert IDs back to label strings, ignoring -100
    true_labels_chirho = []
    pred_labels_chirho = []

    for prediction_chirho, label_chirho in zip(predictions_chirho, labels_chirho):
        true_seq_chirho = []
        pred_seq_chirho = []

        for pred_id_chirho, label_id_chirho in zip(prediction_chirho, label_chirho):
            if label_id_chirho == -100:
                continue

            true_seq_chirho.append(id2label_chirho.get(label_id_chirho, "O"))
            pred_seq_chirho.append(id2label_chirho.get(pred_id_chirho, "O"))

        true_labels_chirho.append(true_seq_chirho)
        pred_labels_chirho.append(pred_seq_chirho)

    # Compute seqeval metrics
    f1_chirho = seqeval_f1_score(true_labels_chirho, pred_labels_chirho)
    precision_chirho = seqeval_precision_score(true_labels_chirho, pred_labels_chirho)
    recall_chirho = seqeval_recall_score(true_labels_chirho, pred_labels_chirho)

    return {
        "f1_chirho": f1_chirho,
        "precision_chirho": precision_chirho,
        "recall_chirho": recall_chirho,
    }


def run_inference_test_chirho(
    model_chirho,
    tokenizer_chirho,
    id2label_chirho: dict,
    device_chirho: torch.device,
):
    """Run inference on sample biblical texts to verify the trained model."""
    test_sentences_chirho = [
        "In the beginning God created the heaven and the earth.",
        "And Moses said unto the LORD, O my Lord, I am not eloquent.",
        "Then Jesus went with them unto a place called Gethsemane.",
        "And the Philistines gathered together their armies to battle.",
        "Now when Jesus was born in Bethlehem of Judaea in the days of Herod the king.",
        "And Solomon built the house of the LORD in Jerusalem.",
        "The LORD is my shepherd; I shall not want.",
        "And Paul said unto the Corinthians, Grace be unto you from God our Father.",
    ]

    print("\n" + "=" * 60)
    print("INFERENCE TEST")
    print("=" * 60)

    model_chirho.eval()

    for sentence_chirho in test_sentences_chirho:
        # Tokenize
        inputs_chirho = tokenizer_chirho(
            sentence_chirho,
            return_tensors="pt",
            truncation=True,
            max_length=128,
        )
        inputs_chirho = {
            k_chirho: v_chirho.to(device_chirho)
            for k_chirho, v_chirho in inputs_chirho.items()
        }

        # Predict
        with torch.no_grad():
            outputs_chirho = model_chirho(**inputs_chirho)
            predictions_chirho = torch.argmax(outputs_chirho.logits, dim=2)

        # Decode
        tokens_chirho = tokenizer_chirho.convert_ids_to_tokens(
            inputs_chirho["input_ids"][0]
        )
        pred_ids_chirho = predictions_chirho[0].cpu().tolist()

        # Build annotated output
        annotated_parts_chirho = []
        current_entity_chirho = None
        current_tokens_chirho = []

        for token_chirho, pred_id_chirho in zip(tokens_chirho, pred_ids_chirho):
            if token_chirho in ["[CLS]", "[SEP]", "[PAD]"]:
                continue

            label_chirho = id2label_chirho.get(pred_id_chirho, "O")

            if label_chirho.startswith("B-"):
                # Flush previous entity
                if current_entity_chirho:
                    entity_text_chirho = tokenizer_chirho.convert_tokens_to_string(
                        current_tokens_chirho
                    )
                    annotated_parts_chirho.append(
                        f"[{entity_text_chirho}|{current_entity_chirho}]"
                    )

                current_entity_chirho = label_chirho[2:]
                current_tokens_chirho = [token_chirho]

            elif label_chirho.startswith("I-") and current_entity_chirho:
                current_tokens_chirho.append(token_chirho)

            else:
                # Flush previous entity
                if current_entity_chirho:
                    entity_text_chirho = tokenizer_chirho.convert_tokens_to_string(
                        current_tokens_chirho
                    )
                    annotated_parts_chirho.append(
                        f"[{entity_text_chirho}|{current_entity_chirho}]"
                    )
                    current_entity_chirho = None
                    current_tokens_chirho = []

                # Handle subword tokens
                if token_chirho.startswith("##"):
                    if annotated_parts_chirho:
                        annotated_parts_chirho[-1] += token_chirho[2:]
                    else:
                        annotated_parts_chirho.append(token_chirho[2:])
                else:
                    annotated_parts_chirho.append(token_chirho)

        # Flush final entity
        if current_entity_chirho:
            entity_text_chirho = tokenizer_chirho.convert_tokens_to_string(
                current_tokens_chirho
            )
            annotated_parts_chirho.append(
                f"[{entity_text_chirho}|{current_entity_chirho}]"
            )

        print(f"\n  Input: {sentence_chirho}")
        print(f"  Output: {' '.join(annotated_parts_chirho)}")


def main_chirho():
    """Main training loop for biblical NER."""
    print("=" * 60)
    print("Biblical Entity Recognizer - NER Training (DistilBERT)")
    print("=" * 60)

    # Load config
    config_chirho = load_config_chirho()
    ner_config_chirho = config_chirho["ner_chirho"]
    labels_chirho = ner_config_chirho["labels_chirho"]
    label2id_chirho, id2label_chirho = build_label_maps_chirho(labels_chirho)

    # Device selection
    if torch.backends.mps.is_available():
        device_chirho = torch.device("mps")
        device_str_chirho = "mps"
        print("Using Apple MPS (Metal Performance Shaders)")
    elif torch.cuda.is_available():
        device_chirho = torch.device("cuda")
        device_str_chirho = "cuda"
        print(f"Using CUDA GPU: {torch.cuda.get_device_name(0)}")
    else:
        device_chirho = torch.device("cpu")
        device_str_chirho = "cpu"
        print("Using CPU")

    model_name_chirho = ner_config_chirho["model_name_chirho"]
    num_labels_chirho = ner_config_chirho["num_labels_chirho"]
    max_length_chirho = ner_config_chirho["max_length_chirho"]

    print(f"\nModel: {model_name_chirho}")
    print(f"Labels ({num_labels_chirho}): {labels_chirho}")
    print(f"Max length: {max_length_chirho}")

    # Load tokenizer and model
    print("\nLoading tokenizer and model...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(model_name_chirho)
    model_chirho = AutoModelForTokenClassification.from_pretrained(
        model_name_chirho,
        num_labels=num_labels_chirho,
        id2label=id2label_chirho,
        label2id=label2id_chirho,
    )

    # Load datasets
    print("Loading datasets...")
    train_examples_chirho = load_ner_dataset_chirho("train")
    val_examples_chirho = load_ner_dataset_chirho("val")

    print(f"  Train: {len(train_examples_chirho)} examples")
    print(f"  Validation: {len(val_examples_chirho)} examples")

    # Create HF datasets
    train_dataset_chirho = create_hf_dataset_chirho(train_examples_chirho, label2id_chirho)
    val_dataset_chirho = create_hf_dataset_chirho(val_examples_chirho, label2id_chirho)

    # Tokenize and align labels
    print("Tokenizing and aligning labels...")
    train_dataset_chirho = train_dataset_chirho.map(
        lambda examples_chirho: tokenize_and_align_labels_chirho(
            examples_chirho, tokenizer_chirho, max_length_chirho
        ),
        batched=True,
        remove_columns=["tokens_chirho", "ner_tags_chirho"],
    )
    val_dataset_chirho = val_dataset_chirho.map(
        lambda examples_chirho: tokenize_and_align_labels_chirho(
            examples_chirho, tokenizer_chirho, max_length_chirho
        ),
        batched=True,
        remove_columns=["tokens_chirho", "ner_tags_chirho"],
    )

    print(f"  Tokenized train: {len(train_dataset_chirho)} examples")
    print(f"  Tokenized val: {len(val_dataset_chirho)} examples")

    # Data collator
    data_collator_chirho = DataCollatorForTokenClassification(
        tokenizer=tokenizer_chirho,
    )

    # Training arguments
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    training_args_chirho = TrainingArguments(
        output_dir=str(OUTPUT_DIR_CHIRHO),
        num_train_epochs=ner_config_chirho["num_epochs_chirho"],
        per_device_train_batch_size=ner_config_chirho["batch_size_chirho"],
        per_device_eval_batch_size=ner_config_chirho["batch_size_chirho"] * 2,
        learning_rate=ner_config_chirho["learning_rate_chirho"],
        weight_decay=ner_config_chirho["weight_decay_chirho"],
        warmup_ratio=ner_config_chirho["warmup_ratio_chirho"],
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_chirho",
        greater_is_better=True,
        logging_steps=100,
        save_total_limit=3,
        fp16=False,
        dataloader_pin_memory=False if device_str_chirho == "mps" else True,
        report_to="none",
        seed=ner_config_chirho["seed_chirho"],
    )

    # Metrics function (closure over id2label)
    def compute_metrics_wrapper_chirho(eval_pred_chirho):
        return compute_metrics_chirho(eval_pred_chirho, id2label_chirho)

    # Trainer
    trainer_chirho = Trainer(
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_dataset_chirho,
        eval_dataset=val_dataset_chirho,
        data_collator=data_collator_chirho,
        processing_class=tokenizer_chirho,
        compute_metrics=compute_metrics_wrapper_chirho,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
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
    train_result_chirho = trainer_chirho.train(resume_from_checkpoint=resume_from_chirho)

    print("\nTraining complete!")
    print(f"  Training loss: {train_result_chirho.training_loss:.4f}")

    # Evaluate
    print("\nEvaluating on validation set...")
    eval_results_chirho = trainer_chirho.evaluate()
    print(f"  F1: {eval_results_chirho.get('eval_f1_chirho', 'N/A')}")
    print(f"  Precision: {eval_results_chirho.get('eval_precision_chirho', 'N/A')}")
    print(f"  Recall: {eval_results_chirho.get('eval_recall_chirho', 'N/A')}")

    # Save best model
    best_model_dir_chirho = OUTPUT_DIR_CHIRHO / "best-chirho"
    best_model_dir_chirho.mkdir(parents=True, exist_ok=True)
    trainer_chirho.save_model(str(best_model_dir_chirho))
    tokenizer_chirho.save_pretrained(str(best_model_dir_chirho))

    # Save label mapping
    label_map_chirho = {
        "label2id_chirho": label2id_chirho,
        "id2label_chirho": {str(k_chirho): v_chirho for k_chirho, v_chirho in id2label_chirho.items()},
        "labels_chirho": labels_chirho,
    }
    with open(best_model_dir_chirho / "label-map-chirho.json", "w") as f_chirho:
        json.dump(label_map_chirho, f_chirho, indent=2)

    print(f"\nBest model saved to: {best_model_dir_chirho}")
    print("Label map saved to: label-map-chirho.json")

    # Run inference test
    model_chirho.to(device_chirho)
    run_inference_test_chirho(model_chirho, tokenizer_chirho, id2label_chirho, device_chirho)

    print("\n" + "=" * 60)
    print("Training pipeline complete!")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
