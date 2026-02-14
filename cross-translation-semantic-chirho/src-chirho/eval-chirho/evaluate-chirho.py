# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""Evaluate cross-translation embedding model on test set."""

import json
import os
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from sklearn.metrics import accuracy_score, roc_auc_score


def main_chirho():
    """Run evaluation."""
    print("=" * 60)
    print("Cross-Translation Embedding Evaluation")
    print("=" * 60)

    # Paths
    model_dir_chirho = os.path.join(os.path.dirname(__file__), "../../models-chirho/embedder-chirho/best-chirho")
    test_path_chirho = os.path.join(os.path.dirname(__file__), "../../data-chirho/processed-chirho/test-embedding-chirho.jsonl")

    # Load model
    device_chirho = "cuda" if torch.cuda.is_available() else "mps" if hasattr(torch.backends, "mps") and torch.backends.mps.is_available() else "cpu"
    print(f"Device: {device_chirho}")

    model_chirho = SentenceTransformer(model_dir_chirho, device=device_chirho)

    # Load test data
    examples_chirho = []
    with open(test_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if line_chirho.strip():
                examples_chirho.append(json.loads(line_chirho))

    print(f"Test examples: {len(examples_chirho)}")

    # Compute similarities
    sentences1_chirho = [ex["sentence1_chirho"] for ex in examples_chirho]
    sentences2_chirho = [ex["sentence2_chirho"] for ex in examples_chirho]
    labels_chirho = [ex["label_chirho"] for ex in examples_chirho]

    print("Computing embeddings...")
    embeddings1_chirho = model_chirho.encode(sentences1_chirho, batch_size=64, show_progress_bar=True)
    embeddings2_chirho = model_chirho.encode(sentences2_chirho, batch_size=64, show_progress_bar=True)

    # Cosine similarities
    similarities_chirho = []
    for e1_chirho, e2_chirho in zip(embeddings1_chirho, embeddings2_chirho):
        sim_chirho = cos_sim(e1_chirho, e2_chirho).item()
        similarities_chirho.append(sim_chirho)

    similarities_chirho = np.array(similarities_chirho)
    labels_np_chirho = np.array(labels_chirho)

    # Metrics
    # 1. Mean similarity for positive vs negative pairs
    pos_mask_chirho = labels_np_chirho == 1.0
    neg_mask_chirho = labels_np_chirho == 0.0

    mean_pos_sim_chirho = similarities_chirho[pos_mask_chirho].mean()
    mean_neg_sim_chirho = similarities_chirho[neg_mask_chirho].mean()

    # 2. Classification accuracy at threshold 0.5
    predicted_labels_chirho = (similarities_chirho > 0.5).astype(float)
    accuracy_chirho = accuracy_score(labels_np_chirho, predicted_labels_chirho)

    # 3. ROC AUC
    auc_chirho = roc_auc_score(labels_np_chirho, similarities_chirho)

    # 4. Spearman correlation
    from scipy.stats import spearmanr
    spearman_chirho, _ = spearmanr(similarities_chirho, labels_np_chirho)

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Mean positive similarity: {mean_pos_sim_chirho:.4f}")
    print(f"  Mean negative similarity: {mean_neg_sim_chirho:.4f}")
    print(f"  Separation gap: {mean_pos_sim_chirho - mean_neg_sim_chirho:.4f}")
    print(f"  Classification accuracy (@0.5): {accuracy_chirho:.4f}")
    print(f"  ROC AUC: {auc_chirho:.4f}")
    print(f"  Spearman correlation: {spearman_chirho:.4f}")

    # Sample predictions
    print(f"\nSample positive pairs:")
    pos_indices_chirho = np.where(pos_mask_chirho)[0][:3]
    for idx_chirho in pos_indices_chirho:
        print(f"  Sim={similarities_chirho[idx_chirho]:.3f}: {sentences1_chirho[idx_chirho][:60]}...")
        print(f"         {sentences2_chirho[idx_chirho][:60]}...")

    print(f"\nSample negative pairs:")
    neg_indices_chirho = np.where(neg_mask_chirho)[0][:3]
    for idx_chirho in neg_indices_chirho:
        print(f"  Sim={similarities_chirho[idx_chirho]:.3f}: {sentences1_chirho[idx_chirho][:60]}...")
        print(f"         {sentences2_chirho[idx_chirho][:60]}...")


if __name__ == "__main__":
    main_chirho()
