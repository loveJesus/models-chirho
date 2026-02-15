# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
evaluate-chirho.py
Comprehensive evaluation of the Biblical Entity Recognizer NER model.
Runs on the held-out test set and computes:
  - Per-entity-type F1, precision, recall
  - Overall (micro/macro) F1
  - Confusion-matrix-style breakdown
  - Sample predictions with highlighted entities
"""

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
import yaml
from seqeval.metrics import classification_report as seqeval_report
from seqeval.metrics import f1_score as seqeval_f1
from transformers import AutoModelForTokenClassification, AutoTokenizer

# Paths
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH_CHIRHO = BASE_DIR_CHIRHO / "config-chirho.yaml"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
MODELS_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "ner-chirho"


def load_config_chirho() -> dict:
    """Load configuration."""
    with open(CONFIG_PATH_CHIRHO, "r") as f_chirho:
        return yaml.safe_load(f_chirho)


def load_test_data_chirho() -> list[dict]:
    """Load test JSONL data."""
    test_path_chirho = DATA_DIR_CHIRHO / "test-chirho.jsonl"
    examples_chirho = []
    with open(test_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if line_chirho.strip():
                examples_chirho.append(json.loads(line_chirho))
    return examples_chirho


def predict_sentence_chirho(
    tokens_chirho: list[str],
    model_chirho,
    tokenizer_chirho,
    id2label_chirho: dict,
    device_chirho: torch.device,
    max_length_chirho: int = 128,
) -> list[str]:
    """
    Run NER inference on a list of pre-tokenized words.
    Returns predicted BIO tags aligned to the original tokens.
    """
    # Tokenize with word-level split
    encoding_chirho = tokenizer_chirho(
        tokens_chirho,
        is_split_into_words=True,
        return_tensors="pt",
        truncation=True,
        max_length=max_length_chirho,
    )
    encoding_chirho = {
        k_chirho: v_chirho.to(device_chirho)
        for k_chirho, v_chirho in encoding_chirho.items()
    }

    # Predict
    with torch.no_grad():
        outputs_chirho = model_chirho(**encoding_chirho)
        logits_chirho = outputs_chirho.logits
        predictions_chirho = torch.argmax(logits_chirho, dim=2)[0].cpu().tolist()
        confidences_chirho = torch.softmax(logits_chirho, dim=2)[0].cpu().numpy()

    # Align predictions back to original tokens
    word_ids_chirho = encoding_chirho["input_ids"][0].cpu().tolist()
    word_id_map_chirho = tokenizer_chirho(
        tokens_chirho,
        is_split_into_words=True,
        truncation=True,
        max_length=max_length_chirho,
    ).word_ids()

    aligned_preds_chirho = ["O"] * len(tokens_chirho)
    aligned_confs_chirho = [0.0] * len(tokens_chirho)
    seen_word_ids_chirho = set()

    for idx_chirho, word_id_chirho in enumerate(word_id_map_chirho):
        if word_id_chirho is None:
            continue
        if word_id_chirho in seen_word_ids_chirho:
            continue
        seen_word_ids_chirho.add(word_id_chirho)

        if word_id_chirho < len(tokens_chirho):
            pred_id_chirho = predictions_chirho[idx_chirho]
            aligned_preds_chirho[word_id_chirho] = id2label_chirho.get(pred_id_chirho, "O")
            aligned_confs_chirho[word_id_chirho] = float(np.max(confidences_chirho[idx_chirho]))

    return aligned_preds_chirho


def extract_entities_chirho(
    tokens_chirho: list[str],
    tags_chirho: list[str],
) -> list[dict]:
    """Extract entity spans from BIO-tagged tokens."""
    entities_chirho = []
    current_entity_chirho = None
    current_tokens_chirho = []
    current_start_chirho = -1

    for i_chirho, (token_chirho, tag_chirho) in enumerate(zip(tokens_chirho, tags_chirho)):
        if tag_chirho.startswith("B-"):
            # Flush previous entity
            if current_entity_chirho:
                entities_chirho.append({
                    "text_chirho": " ".join(current_tokens_chirho),
                    "type_chirho": current_entity_chirho,
                    "start_chirho": current_start_chirho,
                    "end_chirho": i_chirho - 1,
                })

            current_entity_chirho = tag_chirho[2:]
            current_tokens_chirho = [token_chirho]
            current_start_chirho = i_chirho

        elif tag_chirho.startswith("I-") and current_entity_chirho == tag_chirho[2:]:
            current_tokens_chirho.append(token_chirho)

        else:
            if current_entity_chirho:
                entities_chirho.append({
                    "text_chirho": " ".join(current_tokens_chirho),
                    "type_chirho": current_entity_chirho,
                    "start_chirho": current_start_chirho,
                    "end_chirho": i_chirho - 1,
                })
                current_entity_chirho = None
                current_tokens_chirho = []

    # Flush final entity
    if current_entity_chirho:
        entities_chirho.append({
            "text_chirho": " ".join(current_tokens_chirho),
            "type_chirho": current_entity_chirho,
            "start_chirho": current_start_chirho,
            "end_chirho": len(tokens_chirho) - 1,
        })

    return entities_chirho


def compute_confusion_matrix_chirho(
    all_true_chirho: list[list[str]],
    all_pred_chirho: list[list[str]],
    entity_types_chirho: list[str],
) -> dict:
    """
    Compute entity-level confusion counts.
    For each true entity, check what it was predicted as.
    """
    confusion_chirho = defaultdict(lambda: defaultdict(int))

    for true_seq_chirho, pred_seq_chirho in zip(all_true_chirho, all_pred_chirho):
        true_entities_chirho = extract_entities_chirho(
            [str(i_chirho) for i_chirho in range(len(true_seq_chirho))],  # dummy tokens as strings
            true_seq_chirho,
        )
        pred_entities_chirho = extract_entities_chirho(
            [str(i_chirho) for i_chirho in range(len(pred_seq_chirho))],
            pred_seq_chirho,
        )

        # Build span-to-type maps
        pred_span_map_chirho = {}
        for ent_chirho in pred_entities_chirho:
            span_key_chirho = (ent_chirho["start_chirho"], ent_chirho["end_chirho"])
            pred_span_map_chirho[span_key_chirho] = ent_chirho["type_chirho"]

        for ent_chirho in true_entities_chirho:
            span_key_chirho = (ent_chirho["start_chirho"], ent_chirho["end_chirho"])
            true_type_chirho = ent_chirho["type_chirho"]

            if span_key_chirho in pred_span_map_chirho:
                pred_type_chirho = pred_span_map_chirho[span_key_chirho]
                confusion_chirho[true_type_chirho][pred_type_chirho] += 1
            else:
                confusion_chirho[true_type_chirho]["MISSED"] += 1

    return dict(confusion_chirho)


def print_confusion_matrix_chirho(
    confusion_chirho: dict,
    entity_types_chirho: list[str],
):
    """Print a formatted confusion matrix."""
    all_cols_chirho = entity_types_chirho + ["MISSED"]

    # Header
    header_chirho = f"{'True \\ Pred':<16}"
    for col_chirho in all_cols_chirho:
        header_chirho += f"{col_chirho:>14}"
    print(header_chirho)
    print("-" * len(header_chirho))

    for true_type_chirho in entity_types_chirho:
        row_chirho = f"{true_type_chirho:<16}"
        row_data_chirho = confusion_chirho.get(true_type_chirho, {})
        for col_chirho in all_cols_chirho:
            count_chirho = row_data_chirho.get(col_chirho, 0)
            row_chirho += f"{count_chirho:>14}"
        print(row_chirho)


def print_sample_predictions_chirho(
    test_data_chirho: list[dict],
    model_chirho,
    tokenizer_chirho,
    id2label_chirho: dict,
    device_chirho: torch.device,
    num_samples_chirho: int = 15,
):
    """Print sample predictions with highlighted entities."""
    print("\n" + "=" * 60)
    print("SAMPLE PREDICTIONS")
    print("=" * 60)

    # Select samples that have entities
    entity_examples_chirho = [
        ex_chirho for ex_chirho in test_data_chirho
        if any(t_chirho != "O" for t_chirho in ex_chirho["ner_tags_chirho"])
    ]

    # Spread samples across the data
    step_chirho = max(1, len(entity_examples_chirho) // num_samples_chirho)
    samples_chirho = []
    for i_chirho in range(0, len(entity_examples_chirho), step_chirho):
        samples_chirho.append(entity_examples_chirho[i_chirho])
        if len(samples_chirho) >= num_samples_chirho:
            break

    for i_chirho, example_chirho in enumerate(samples_chirho):
        tokens_chirho = example_chirho["tokens_chirho"]
        true_tags_chirho = example_chirho["ner_tags_chirho"]
        reference_chirho = example_chirho.get("reference_chirho", f"example-{i_chirho}")

        # Predict
        pred_tags_chirho = predict_sentence_chirho(
            tokens_chirho, model_chirho, tokenizer_chirho, id2label_chirho, device_chirho
        )

        # Extract entities
        true_entities_chirho = extract_entities_chirho(tokens_chirho, true_tags_chirho)
        pred_entities_chirho = extract_entities_chirho(tokens_chirho, pred_tags_chirho)

        print(f"\n  [{i_chirho + 1}] {reference_chirho}")
        print(f"      Text: {' '.join(tokens_chirho[:30])}{'...' if len(tokens_chirho) > 30 else ''}")

        if true_entities_chirho:
            true_str_chirho = ", ".join(
                f"{e_chirho['text_chirho']}({e_chirho['type_chirho']})" for e_chirho in true_entities_chirho
            )
            print(f"      True:  {true_str_chirho}")

        if pred_entities_chirho:
            pred_str_chirho = ", ".join(
                f"{e_chirho['text_chirho']}({e_chirho['type_chirho']})" for e_chirho in pred_entities_chirho
            )
            print(f"      Pred:  {pred_str_chirho}")

        # Compare
        true_set_chirho = {
            (e_chirho["text_chirho"], e_chirho["type_chirho"]) for e_chirho in true_entities_chirho
        }
        pred_set_chirho = {
            (e_chirho["text_chirho"], e_chirho["type_chirho"]) for e_chirho in pred_entities_chirho
        }

        correct_chirho = true_set_chirho & pred_set_chirho
        missed_chirho = true_set_chirho - pred_set_chirho
        extra_chirho = pred_set_chirho - true_set_chirho

        status_parts_chirho = []
        if correct_chirho:
            status_parts_chirho.append(f"correct={len(correct_chirho)}")
        if missed_chirho:
            status_parts_chirho.append(f"missed={len(missed_chirho)}")
        if extra_chirho:
            status_parts_chirho.append(f"extra={len(extra_chirho)}")

        print(f"      Status: {', '.join(status_parts_chirho) if status_parts_chirho else 'no entities'}")


def main_chirho():
    """Run full evaluation on the test set."""
    print("=" * 60)
    print("Biblical Entity Recognizer - Evaluation")
    print("=" * 60)

    config_chirho = load_config_chirho()
    ner_config_chirho = config_chirho["ner_chirho"]
    labels_chirho = ner_config_chirho["labels_chirho"]
    entity_types_chirho = ner_config_chirho["entity_types_chirho"]

    # Build label maps
    id2label_chirho = {i_chirho: label_chirho for i_chirho, label_chirho in enumerate(labels_chirho)}

    # Check model exists
    model_path_chirho = MODELS_DIR_CHIRHO / "best-chirho"
    if not model_path_chirho.exists():
        print(f"\nModel not found at {model_path_chirho}")
        print("Run training first: python src-chirho/train-chirho/train-ner-chirho.py")
        return

    # Device
    if torch.backends.mps.is_available():
        device_chirho = torch.device("mps")
        print("Using Apple MPS")
    elif torch.cuda.is_available():
        device_chirho = torch.device("cuda")
        print(f"Using CUDA: {torch.cuda.get_device_name(0)}")
    else:
        device_chirho = torch.device("cpu")
        print("Using CPU")

    # Load model
    print(f"\nLoading model from {model_path_chirho}...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(str(model_path_chirho))
    model_chirho = AutoModelForTokenClassification.from_pretrained(str(model_path_chirho))
    model_chirho.to(device_chirho)
    model_chirho.eval()

    # Load test data
    print("Loading test data...")
    test_data_chirho = load_test_data_chirho()
    print(f"  Test examples: {len(test_data_chirho)}")

    # Run predictions on all test data
    print("\nRunning inference on test set...")
    all_true_tags_chirho = []
    all_pred_tags_chirho = []

    for i_chirho, example_chirho in enumerate(test_data_chirho):
        if i_chirho > 0 and i_chirho % 500 == 0:
            print(f"  Progress: {i_chirho}/{len(test_data_chirho)}")

        tokens_chirho = example_chirho["tokens_chirho"]
        true_tags_chirho = example_chirho["ner_tags_chirho"]

        pred_tags_chirho = predict_sentence_chirho(
            tokens_chirho, model_chirho, tokenizer_chirho, id2label_chirho, device_chirho
        )

        all_true_tags_chirho.append(true_tags_chirho)
        all_pred_tags_chirho.append(pred_tags_chirho)

    # Compute seqeval metrics
    print("\n" + "=" * 60)
    print("ENTITY-LEVEL METRICS (seqeval)")
    print("=" * 60)

    overall_f1_chirho = seqeval_f1(all_true_tags_chirho, all_pred_tags_chirho)
    print(f"\n  Overall F1: {overall_f1_chirho:.4f}")

    # Detailed classification report
    report_chirho = seqeval_report(
        all_true_tags_chirho, all_pred_tags_chirho, digits=4
    )
    print(f"\n{report_chirho}")

    # Confusion matrix
    print("\n" + "=" * 60)
    print("CONFUSION MATRIX (entity-level)")
    print("=" * 60)

    confusion_chirho = compute_confusion_matrix_chirho(
        all_true_tags_chirho, all_pred_tags_chirho, entity_types_chirho
    )
    print_confusion_matrix_chirho(confusion_chirho, entity_types_chirho)

    # Sample predictions
    print_sample_predictions_chirho(
        test_data_chirho, model_chirho, tokenizer_chirho, id2label_chirho, device_chirho
    )

    # Target check
    target_f1_chirho = config_chirho.get("evaluation_chirho", {}).get("target_f1_chirho", 0.80)
    status_chirho = "PASS" if overall_f1_chirho >= target_f1_chirho else "FAIL"

    print("\n" + "=" * 60)
    print(f"Target F1 >= {target_f1_chirho}: {status_chirho} (got {overall_f1_chirho:.4f})")
    print("=" * 60)
    print("\nEvaluation complete!")


if __name__ == "__main__":
    main_chirho()
