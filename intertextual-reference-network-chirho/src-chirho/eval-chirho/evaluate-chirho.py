# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
evaluate-chirho.py
Comprehensive evaluation of both intertextual models:
  - Embedder: Precision@10, Recall@10 on held-out cross-refs, separation gap
  - Classifier: F1 macro, per-class P/R/F1, confusion matrix
"""

import json
from pathlib import Path
from collections import defaultdict

import numpy as np
import torch
import yaml
from sentence_transformers import SentenceTransformer
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH_CHIRHO = BASE_DIR_CHIRHO / "src-chirho" / "train-chirho" / "config-chirho.yaml"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
EMBEDDER_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "embedder-chirho" / "best-chirho"
CLASSIFIER_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "classifier-chirho" / "best-chirho"

LABELS_CHIRHO = [
    "direct_quote", "allusion", "thematic_parallel", "typological",
    "prophecy_fulfillment", "parallel_narrative", "contrast",
]


def load_jsonl_chirho(path_chirho: Path) -> list[dict]:
    """Load JSONL file."""
    items_chirho = []
    with open(path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if line_chirho.strip():
                items_chirho.append(json.loads(line_chirho))
    return items_chirho


def evaluate_embedder_chirho(device_chirho: str):
    """Evaluate the embedder on held-out cross-reference triplets."""
    print("\n" + "=" * 60)
    print("Embedder Evaluation (MiniLM-L12)")
    print("=" * 60)

    if not EMBEDDER_DIR_CHIRHO.exists():
        print("  Embedder model not found. Skipping.")
        return

    model_chirho = SentenceTransformer(str(EMBEDDER_DIR_CHIRHO), device=device_chirho)

    # Load test triplets
    test_triplets_chirho = load_jsonl_chirho(DATA_DIR_CHIRHO / "test-embedder-chirho.jsonl")
    print(f"  Test triplets: {len(test_triplets_chirho)}")

    # Compute similarity scores
    positive_sims_chirho = []
    negative_sims_chirho = []
    correct_ranking_chirho = 0

    batch_size_chirho = 256
    for i_chirho in range(0, len(test_triplets_chirho), batch_size_chirho):
        batch_chirho = test_triplets_chirho[i_chirho:i_chirho + batch_size_chirho]

        anchors_chirho = [t_chirho["anchor_text_chirho"] for t_chirho in batch_chirho]
        positives_chirho = [t_chirho["positive_text_chirho"] for t_chirho in batch_chirho]
        negatives_chirho = [t_chirho["negative_text_chirho"] for t_chirho in batch_chirho]

        emb_a_chirho = model_chirho.encode(anchors_chirho, convert_to_numpy=True)
        emb_p_chirho = model_chirho.encode(positives_chirho, convert_to_numpy=True)
        emb_n_chirho = model_chirho.encode(negatives_chirho, convert_to_numpy=True)

        for j_chirho in range(len(batch_chirho)):
            sim_pos_chirho = float(np.dot(emb_a_chirho[j_chirho], emb_p_chirho[j_chirho]) /
                (np.linalg.norm(emb_a_chirho[j_chirho]) * np.linalg.norm(emb_p_chirho[j_chirho])))
            sim_neg_chirho = float(np.dot(emb_a_chirho[j_chirho], emb_n_chirho[j_chirho]) /
                (np.linalg.norm(emb_a_chirho[j_chirho]) * np.linalg.norm(emb_n_chirho[j_chirho])))

            positive_sims_chirho.append(sim_pos_chirho)
            negative_sims_chirho.append(sim_neg_chirho)
            if sim_pos_chirho > sim_neg_chirho:
                correct_ranking_chirho += 1

    # Metrics
    accuracy_chirho = correct_ranking_chirho / len(test_triplets_chirho)
    avg_pos_sim_chirho = np.mean(positive_sims_chirho)
    avg_neg_sim_chirho = np.mean(negative_sims_chirho)
    separation_gap_chirho = avg_pos_sim_chirho - avg_neg_sim_chirho

    print(f"\n  Triplet ranking accuracy: {accuracy_chirho:.4f}")
    print(f"  Avg positive similarity: {avg_pos_sim_chirho:.4f}")
    print(f"  Avg negative similarity: {avg_neg_sim_chirho:.4f}")
    print(f"  Separation gap: {separation_gap_chirho:.4f}")

    # Known pair sanity check
    known_pairs_chirho = [
        ("In the beginning God created the heaven and the earth.",
         "In the beginning was the Word, and the Word was with God, and the Word was God.",
         "Gen.1.1 <-> John.1.1"),
        ("The LORD is my shepherd; I shall not want.",
         "I am the good shepherd: the good shepherd giveth his life for the sheep.",
         "Ps.23.1 <-> John.10.11"),
    ]

    print("\n  Known pair similarity checks:")
    for text_a_chirho, text_b_chirho, label_chirho in known_pairs_chirho:
        emb_pair_chirho = model_chirho.encode([text_a_chirho, text_b_chirho])
        sim_chirho = float(np.dot(emb_pair_chirho[0], emb_pair_chirho[1]) /
            (np.linalg.norm(emb_pair_chirho[0]) * np.linalg.norm(emb_pair_chirho[1])))
        print(f"    {label_chirho}: {sim_chirho:.4f}")

    return {
        "accuracy_chirho": accuracy_chirho,
        "avg_pos_sim_chirho": avg_pos_sim_chirho,
        "avg_neg_sim_chirho": avg_neg_sim_chirho,
        "separation_gap_chirho": separation_gap_chirho,
    }


def evaluate_classifier_chirho(device_chirho: str):
    """Evaluate the classifier on held-out test set."""
    print("\n" + "=" * 60)
    print("Classifier Evaluation (RoBERTa-base)")
    print("=" * 60)

    if not CLASSIFIER_DIR_CHIRHO.exists():
        print("  Classifier model not found. Skipping.")
        return

    tokenizer_chirho = AutoTokenizer.from_pretrained(str(CLASSIFIER_DIR_CHIRHO))
    model_chirho = AutoModelForSequenceClassification.from_pretrained(str(CLASSIFIER_DIR_CHIRHO))
    model_chirho.to(device_chirho)
    model_chirho.eval()

    # Load test data
    test_data_chirho = load_jsonl_chirho(DATA_DIR_CHIRHO / "test-classifier-chirho.jsonl")
    print(f"  Test examples: {len(test_data_chirho)}")

    true_labels_chirho = []
    pred_labels_chirho = []

    label2id_chirho = {l_chirho: i_chirho for i_chirho, l_chirho in enumerate(LABELS_CHIRHO)}

    batch_size_chirho = 32
    for i_chirho in range(0, len(test_data_chirho), batch_size_chirho):
        batch_chirho = test_data_chirho[i_chirho:i_chirho + batch_size_chirho]

        texts_a_chirho = [item_chirho.get("from_text_chirho", "") for item_chirho in batch_chirho]
        texts_b_chirho = [item_chirho.get("to_text_chirho", "") for item_chirho in batch_chirho]
        true_types_chirho = [item_chirho.get("connection_type_chirho", "thematic_parallel") for item_chirho in batch_chirho]

        inputs_chirho = tokenizer_chirho(
            texts_a_chirho, texts_b_chirho,
            return_tensors="pt", truncation=True, max_length=256, padding=True,
        )
        inputs_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

        with torch.no_grad():
            outputs_chirho = model_chirho(**inputs_chirho)
            preds_chirho = torch.argmax(outputs_chirho.logits, dim=-1).cpu().numpy()

        for j_chirho in range(len(batch_chirho)):
            true_id_chirho = label2id_chirho.get(true_types_chirho[j_chirho], 2)
            true_labels_chirho.append(true_id_chirho)
            pred_labels_chirho.append(int(preds_chirho[j_chirho]))

    # Metrics
    f1_macro_chirho = f1_score(true_labels_chirho, pred_labels_chirho, average="macro", zero_division=0)
    print(f"\n  F1 (macro): {f1_macro_chirho:.4f}")

    print("\n  Per-class report:")
    print(classification_report(
        true_labels_chirho, pred_labels_chirho,
        target_names=LABELS_CHIRHO, zero_division=0,
    ))

    print("  Confusion matrix:")
    cm_chirho = confusion_matrix(true_labels_chirho, pred_labels_chirho)
    print(f"  {cm_chirho}")

    return {"f1_macro_chirho": f1_macro_chirho}


def main_chirho():
    """Run all evaluations."""
    print("Intertextual Reference Network - Full Evaluation")
    print("=" * 60)

    if torch.backends.mps.is_available():
        device_chirho = "mps"
    elif torch.cuda.is_available():
        device_chirho = "cuda"
    else:
        device_chirho = "cpu"
    print(f"Device: {device_chirho}")

    embedder_results_chirho = evaluate_embedder_chirho(device_chirho)
    classifier_results_chirho = evaluate_classifier_chirho(device_chirho)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if embedder_results_chirho:
        print(f"  Embedder ranking accuracy: {embedder_results_chirho['accuracy_chirho']:.4f}")
        print(f"  Embedder separation gap: {embedder_results_chirho['separation_gap_chirho']:.4f}")
    if classifier_results_chirho:
        print(f"  Classifier F1 (macro): {classifier_results_chirho['f1_macro_chirho']:.4f}")


if __name__ == "__main__":
    main_chirho()
