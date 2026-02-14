# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
evaluate-chirho.py
Evaluates the fine-tuned topical passage classifier on the test set.

Computes:
  - NDCG@10: Normalized Discounted Cumulative Gain at 10
  - MRR: Mean Reciprocal Rank
  - MAP: Mean Average Precision
  - Qualitative search for "forgiveness", "prayer", "creation"

Compares fine-tuned model against base all-MiniLM-L6-v2 (no fine-tuning).
"""

import json
import os
import sys
from collections import defaultdict

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from sklearn.metrics import ndcg_score


def load_test_data_chirho(test_path_chirho: str, max_samples_chirho: int = 10000):
    """Load test set and build IR evaluation data structures."""
    queries_chirho = {}
    corpus_chirho = {}
    relevant_docs_chirho = defaultdict(set)

    with open(test_path_chirho, "r", encoding="utf-8") as f_chirho:
        idx_chirho = 0
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            if idx_chirho >= max_samples_chirho:
                break
            obj_chirho = json.loads(line_chirho)
            query_chirho = obj_chirho.get("query_chirho", "")
            positive_chirho = obj_chirho.get("positive_chirho", "")
            if not query_chirho or not positive_chirho:
                continue

            query_id_chirho = f"q{idx_chirho}"
            corpus_id_chirho = f"c{idx_chirho}"

            queries_chirho[query_id_chirho] = query_chirho
            corpus_chirho[corpus_id_chirho] = positive_chirho
            relevant_docs_chirho[query_id_chirho].add(corpus_id_chirho)

            idx_chirho += 1

    return queries_chirho, corpus_chirho, relevant_docs_chirho


def compute_retrieval_metrics_chirho(
    model_chirho: SentenceTransformer,
    queries_chirho: dict,
    corpus_chirho: dict,
    relevant_docs_chirho: dict,
    k_chirho: int = 10,
    batch_size_chirho: int = 64,
):
    """Compute NDCG@k, MRR@k, MAP@k for the given model and data."""
    query_ids_chirho = list(queries_chirho.keys())
    corpus_ids_chirho = list(corpus_chirho.keys())

    query_texts_chirho = [queries_chirho[qid_chirho] for qid_chirho in query_ids_chirho]
    corpus_texts_chirho = [corpus_chirho[cid_chirho] for cid_chirho in corpus_ids_chirho]

    print(f"  Encoding {len(query_texts_chirho)} queries...")
    query_embeddings_chirho = model_chirho.encode(
        query_texts_chirho, batch_size=batch_size_chirho, show_progress_bar=True
    )

    print(f"  Encoding {len(corpus_texts_chirho)} corpus docs...")
    corpus_embeddings_chirho = model_chirho.encode(
        corpus_texts_chirho, batch_size=batch_size_chirho, show_progress_bar=True
    )

    # Compute similarity matrix
    print("  Computing similarities...")
    sim_matrix_chirho = cos_sim(query_embeddings_chirho, corpus_embeddings_chirho)

    # Metrics accumulators
    ndcg_scores_chirho = []
    mrr_scores_chirho = []
    map_scores_chirho = []

    for i_chirho, qid_chirho in enumerate(query_ids_chirho):
        scores_chirho = sim_matrix_chirho[i_chirho].cpu().numpy()
        relevant_set_chirho = relevant_docs_chirho.get(qid_chirho, set())

        # Create relevance labels for all corpus docs
        relevance_chirho = np.array([
            1.0 if corpus_ids_chirho[j_chirho] in relevant_set_chirho else 0.0
            for j_chirho in range(len(corpus_ids_chirho))
        ])

        # Ranked indices by similarity (descending)
        ranked_indices_chirho = np.argsort(scores_chirho)[::-1]

        # NDCG@k
        top_k_relevance_chirho = relevance_chirho[ranked_indices_chirho[:k_chirho]]
        ideal_relevance_chirho = np.sort(relevance_chirho)[::-1][:k_chirho]

        if ideal_relevance_chirho.sum() > 0:
            ndcg_val_chirho = ndcg_score(
                [ideal_relevance_chirho], [top_k_relevance_chirho]
            )
            ndcg_scores_chirho.append(ndcg_val_chirho)

        # MRR@k
        mrr_val_chirho = 0.0
        for rank_chirho in range(min(k_chirho, len(ranked_indices_chirho))):
            doc_idx_chirho = ranked_indices_chirho[rank_chirho]
            if corpus_ids_chirho[doc_idx_chirho] in relevant_set_chirho:
                mrr_val_chirho = 1.0 / (rank_chirho + 1)
                break
        mrr_scores_chirho.append(mrr_val_chirho)

        # MAP@k
        num_relevant_chirho = 0
        precision_sum_chirho = 0.0
        for rank_chirho in range(min(k_chirho, len(ranked_indices_chirho))):
            doc_idx_chirho = ranked_indices_chirho[rank_chirho]
            if corpus_ids_chirho[doc_idx_chirho] in relevant_set_chirho:
                num_relevant_chirho += 1
                precision_sum_chirho += num_relevant_chirho / (rank_chirho + 1)
        map_val_chirho = (
            precision_sum_chirho / min(len(relevant_set_chirho), k_chirho)
            if relevant_set_chirho
            else 0.0
        )
        map_scores_chirho.append(map_val_chirho)

    results_chirho = {
        "ndcg_at_10_chirho": float(np.mean(ndcg_scores_chirho)) if ndcg_scores_chirho else 0.0,
        "mrr_at_10_chirho": float(np.mean(mrr_scores_chirho)),
        "map_at_10_chirho": float(np.mean(map_scores_chirho)),
    }

    return results_chirho


def qualitative_search_chirho(
    model_chirho: SentenceTransformer,
    corpus_texts_chirho: list,
    model_label_chirho: str,
):
    """Run qualitative topical search queries and show top-5 results."""
    search_queries_chirho = [
        "forgiveness",
        "prayer",
        "creation",
        "love and compassion",
        "salvation through faith",
    ]

    print(f"\n  Qualitative Search ({model_label_chirho}):")
    print("  " + "-" * 56)

    corpus_embeddings_chirho = model_chirho.encode(
        corpus_texts_chirho, batch_size=64, show_progress_bar=False
    )
    query_embeddings_chirho = model_chirho.encode(
        search_queries_chirho, show_progress_bar=False
    )

    sim_matrix_chirho = cos_sim(query_embeddings_chirho, corpus_embeddings_chirho)

    for i_chirho, query_chirho in enumerate(search_queries_chirho):
        scores_chirho = sim_matrix_chirho[i_chirho]
        top_indices_chirho = scores_chirho.argsort(descending=True)[:5]

        print(f"\n  Query: \"{query_chirho}\"")
        for rank_chirho, idx_chirho in enumerate(top_indices_chirho):
            idx_val_chirho = idx_chirho.item()
            score_val_chirho = scores_chirho[idx_val_chirho].item()
            text_preview_chirho = corpus_texts_chirho[idx_val_chirho][:90]
            print(f"    #{rank_chirho + 1} ({score_val_chirho:.3f}): {text_preview_chirho}...")


def main_chirho():
    """Run full evaluation."""
    print("=" * 60)
    print("Topical Passage Classifier Evaluation")
    print("=" * 60)

    # Paths
    model_dir_chirho = os.path.join(
        os.path.dirname(__file__), "../../models-chirho/topical-chirho/best-chirho"
    )
    test_path_chirho = os.path.join(
        os.path.dirname(__file__), "../../data-chirho/processed-chirho/test-topical-chirho.jsonl"
    )

    if not os.path.exists(test_path_chirho):
        print(f"ERROR: Test data not found at {test_path_chirho}")
        sys.exit(1)

    # Detect device
    if torch.cuda.is_available():
        device_chirho = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = "mps"
    else:
        device_chirho = "cpu"
    print(f"Device: {device_chirho}")

    # Load test data
    print("\nLoading test data...")
    queries_chirho, corpus_chirho, relevant_docs_chirho = load_test_data_chirho(
        test_path_chirho, max_samples_chirho=5000
    )
    print(f"  Queries: {len(queries_chirho)}")
    print(f"  Corpus: {len(corpus_chirho)}")

    # Collect unique corpus texts for qualitative search
    corpus_texts_list_chirho = list(corpus_chirho.values())

    # ============================================================
    # Evaluate base model (no fine-tuning)
    # ============================================================
    print("\n" + "=" * 60)
    print("Evaluating BASE model (all-MiniLM-L6-v2, no fine-tuning)...")
    print("=" * 60)

    base_model_chirho = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2", device=device_chirho
    )

    base_results_chirho = compute_retrieval_metrics_chirho(
        base_model_chirho, queries_chirho, corpus_chirho, relevant_docs_chirho
    )

    print(f"\n  Base Model Results:")
    print(f"    NDCG@10: {base_results_chirho['ndcg_at_10_chirho']:.4f}")
    print(f"    MRR@10:  {base_results_chirho['mrr_at_10_chirho']:.4f}")
    print(f"    MAP@10:  {base_results_chirho['map_at_10_chirho']:.4f}")

    qualitative_search_chirho(
        base_model_chirho, corpus_texts_list_chirho, "Base Model"
    )

    del base_model_chirho
    if device_chirho == "cuda":
        torch.cuda.empty_cache()

    # ============================================================
    # Evaluate fine-tuned model
    # ============================================================
    if not os.path.exists(model_dir_chirho):
        print(f"\nFine-tuned model not found at {model_dir_chirho}")
        print("Skipping fine-tuned evaluation. Run training first.")
        return

    print("\n" + "=" * 60)
    print("Evaluating FINE-TUNED model...")
    print("=" * 60)

    finetuned_model_chirho = SentenceTransformer(model_dir_chirho, device=device_chirho)

    finetuned_results_chirho = compute_retrieval_metrics_chirho(
        finetuned_model_chirho, queries_chirho, corpus_chirho, relevant_docs_chirho
    )

    print(f"\n  Fine-tuned Model Results:")
    print(f"    NDCG@10: {finetuned_results_chirho['ndcg_at_10_chirho']:.4f}")
    print(f"    MRR@10:  {finetuned_results_chirho['mrr_at_10_chirho']:.4f}")
    print(f"    MAP@10:  {finetuned_results_chirho['map_at_10_chirho']:.4f}")

    qualitative_search_chirho(
        finetuned_model_chirho, corpus_texts_list_chirho, "Fine-tuned Model"
    )

    # ============================================================
    # Comparison
    # ============================================================
    print("\n" + "=" * 60)
    print("Comparison: Base vs Fine-tuned")
    print("=" * 60)

    metrics_chirho = ["ndcg_at_10_chirho", "mrr_at_10_chirho", "map_at_10_chirho"]
    labels_chirho = ["NDCG@10", "MRR@10", "MAP@10"]
    targets_chirho = [0.85, 0.80, 0.70]

    print(f"  {'Metric':<12} {'Base':>8} {'Finetuned':>10} {'Delta':>8} {'Target':>8} {'Status':>8}")
    print(f"  {'-' * 56}")

    for metric_chirho, label_chirho, target_chirho in zip(
        metrics_chirho, labels_chirho, targets_chirho
    ):
        base_val_chirho = base_results_chirho[metric_chirho]
        ft_val_chirho = finetuned_results_chirho[metric_chirho]
        delta_chirho = ft_val_chirho - base_val_chirho
        met_target_chirho = ft_val_chirho >= target_chirho

        status_chirho = "PASS" if met_target_chirho else "MISS"
        delta_sign_chirho = "+" if delta_chirho >= 0 else ""

        print(
            f"  {label_chirho:<12} {base_val_chirho:>8.4f} {ft_val_chirho:>10.4f} "
            f"{delta_sign_chirho}{delta_chirho:>7.4f} {target_chirho:>8.2f} {status_chirho:>8}"
        )

    # Save results
    results_output_chirho = {
        "base_model_chirho": base_results_chirho,
        "finetuned_model_chirho": finetuned_results_chirho,
        "improvements_chirho": {
            metric_chirho: finetuned_results_chirho[metric_chirho] - base_results_chirho[metric_chirho]
            for metric_chirho in metrics_chirho
        },
    }

    results_path_chirho = os.path.join(
        os.path.dirname(__file__), "../../data-chirho/processed-chirho/eval-results-chirho.json"
    )
    with open(results_path_chirho, "w", encoding="utf-8") as f_chirho:
        json.dump(results_output_chirho, f_chirho, indent=2)
    print(f"\n  Results saved to: {results_path_chirho}")

    print("\nEvaluation complete!")


if __name__ == "__main__":
    main_chirho()
