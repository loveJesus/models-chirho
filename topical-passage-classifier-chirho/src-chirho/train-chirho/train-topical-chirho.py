# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-topical-chirho.py
Fine-tunes all-MiniLM-L6-v2 for semantic topical Bible search.

Uses MultipleNegativesRankingLoss with in-batch negatives:
  - Each batch contains (query, positive) pairs
  - Other positives in the batch serve as hard negatives
  - No explicit negative mining needed

Training data: (topic_text, verse_text) and (verse_A, verse_B) positive pairs
from Nave's Topical Bible and TSK cross-references.

Base model: sentence-transformers/all-MiniLM-L6-v2
  - 22M params, 384-dim embeddings, fast inference
  - Pre-trained on 1B+ sentence pairs

Output: models-chirho/topical-chirho/best-chirho/
"""

import json
import os
import random
import sys

import torch
from sentence_transformers import (
    InputExample,
    SentenceTransformer,
    evaluation,
    losses,
)
from torch.utils.data import DataLoader


def load_topical_pairs_chirho(file_path_chirho: str) -> list:
    """Load topical query-positive JSONL file into InputExample list."""
    examples_chirho = []
    with open(file_path_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            obj_chirho = json.loads(line_chirho)
            query_chirho = obj_chirho.get("query_chirho", "")
            positive_chirho = obj_chirho.get("positive_chirho", "")
            if query_chirho and positive_chirho:
                examples_chirho.append(
                    InputExample(texts=[query_chirho, positive_chirho])
                )
    return examples_chirho


def build_ir_evaluator_chirho(
    val_path_chirho: str, max_eval_chirho: int = 5000
) -> evaluation.InformationRetrievalEvaluator:
    """
    Build an InformationRetrievalEvaluator from validation data.

    Creates a synthetic IR task:
    - queries: the query/topic side of each pair
    - corpus: the positive/verse side of each pair
    - relevant_docs: maps each query to its matching corpus entry
    """
    queries_chirho = {}
    corpus_chirho = {}
    relevant_docs_chirho = {}

    with open(val_path_chirho, "r", encoding="utf-8") as f_chirho:
        idx_chirho = 0
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            if idx_chirho >= max_eval_chirho:
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
            relevant_docs_chirho[query_id_chirho] = {corpus_id_chirho}

            idx_chirho += 1

    print(f"  IR Evaluator: {len(queries_chirho)} queries, {len(corpus_chirho)} corpus docs")

    evaluator_chirho = evaluation.InformationRetrievalEvaluator(
        queries=queries_chirho,
        corpus=corpus_chirho,
        relevant_docs=relevant_docs_chirho,
        name="val-topical-chirho",
        show_progress_bar=True,
        ndcg_at_k=[10],
        mrr_at_k=[10],
        map_at_k=[10],
        write_csv=True,
    )

    return evaluator_chirho


def main_chirho():
    """Main training function."""
    print("=" * 60)
    print("Topical Passage Classifier Training")
    print("=" * 60)

    # Detect device
    if torch.cuda.is_available():
        device_chirho = "cuda"
        gpu_name_chirho = torch.cuda.get_device_name(0)
        print(f"Using CUDA GPU: {gpu_name_chirho}")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = "mps"
        print("Using Apple MPS")
    else:
        device_chirho = "cpu"
        print("Using CPU")

    # Config
    model_name_chirho = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size_chirho = 64 if device_chirho == "cuda" else 16
    epochs_chirho = 5
    lr_chirho = 2e-5
    warmup_ratio_chirho = 0.1

    data_dir_chirho = os.path.join(
        os.path.dirname(__file__), "../../data-chirho/processed-chirho"
    )
    output_dir_chirho = os.path.join(
        os.path.dirname(__file__), "../../models-chirho/topical-chirho"
    )
    best_dir_chirho = os.path.join(output_dir_chirho, "best-chirho")

    print(f"Model: {model_name_chirho}")
    print(f"Batch size: {batch_size_chirho}")
    print(f"Epochs: {epochs_chirho}")
    print(f"Learning rate: {lr_chirho}")
    print(f"Loss: MultipleNegativesRankingLoss (in-batch negatives)")

    # Load model
    print("\nLoading model...")
    model_chirho = SentenceTransformer(model_name_chirho, device=device_chirho)

    # Load datasets
    print("Loading datasets...")
    train_path_chirho = os.path.join(data_dir_chirho, "train-topical-chirho.jsonl")
    val_path_chirho = os.path.join(data_dir_chirho, "val-topical-chirho.jsonl")

    if not os.path.exists(train_path_chirho):
        print(f"ERROR: Training data not found at {train_path_chirho}")
        print("Run the data pipeline first: bun run build-all-chirho")
        sys.exit(1)

    train_examples_chirho = load_topical_pairs_chirho(train_path_chirho)
    print(f"  Train: {len(train_examples_chirho)} pairs")

    if not os.path.exists(val_path_chirho):
        print(f"WARNING: Validation data not found at {val_path_chirho}")
        print("Training without evaluation...")
        evaluator_chirho = None
    else:
        print("Building IR evaluator from validation data...")
        evaluator_chirho = build_ir_evaluator_chirho(val_path_chirho)

    # DataLoader
    train_dataloader_chirho = DataLoader(
        train_examples_chirho,
        shuffle=True,
        batch_size=batch_size_chirho,
    )

    # Loss: MultipleNegativesRankingLoss
    # Each (query, positive) pair uses other batch positives as negatives
    loss_chirho = losses.MultipleNegativesRankingLoss(model_chirho)

    # Training
    warmup_steps_chirho = int(
        len(train_dataloader_chirho) * epochs_chirho * warmup_ratio_chirho
    )

    print(f"\nStarting training...")
    print(f"  Steps per epoch: {len(train_dataloader_chirho)}")
    print(f"  Warmup steps: {warmup_steps_chirho}")
    print(f"  Total steps: {len(train_dataloader_chirho) * epochs_chirho}")

    model_chirho.fit(
        train_objectives=[(train_dataloader_chirho, loss_chirho)],
        evaluator=evaluator_chirho,
        epochs=epochs_chirho,
        warmup_steps=warmup_steps_chirho,
        optimizer_params={"lr": lr_chirho},
        output_path=best_dir_chirho,
        evaluation_steps=500,
        save_best_model=True,
        show_progress_bar=True,
    )

    # Quick inference test: topical search
    print("\n" + "=" * 60)
    print("Inference test: Topical Search")
    print("=" * 60)

    test_queries_chirho = [
        "What does the Bible say about forgiveness?",
        "verses about love",
        "passages about creation",
        "prayer and intercession",
        "salvation through faith",
    ]

    test_passages_chirho = [
        "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        "In the beginning God created the heaven and the earth.",
        "If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness.",
        "Pray without ceasing.",
        "For by grace are ye saved through faith; and that not of yourselves: it is the gift of God.",
        "The LORD is my shepherd; I shall not want.",
        "Be ye angry, and sin not: let not the sun go down upon your wrath.",
        "And God said, Let there be light: and there was light.",
        "Bear ye one another's burdens, and so fulfil the law of Christ.",
        "But the fruit of the Spirit is love, joy, peace, longsuffering, gentleness, goodness, faith.",
    ]

    query_embeddings_chirho = model_chirho.encode(test_queries_chirho)
    passage_embeddings_chirho = model_chirho.encode(test_passages_chirho)

    from sentence_transformers.util import cos_sim

    sim_matrix_chirho = cos_sim(query_embeddings_chirho, passage_embeddings_chirho)

    for i_chirho, query_chirho in enumerate(test_queries_chirho):
        scores_chirho = sim_matrix_chirho[i_chirho]
        ranked_indices_chirho = scores_chirho.argsort(descending=True)
        print(f"\nQuery: \"{query_chirho}\"")
        for rank_chirho in range(min(3, len(test_passages_chirho))):
            idx_chirho = ranked_indices_chirho[rank_chirho].item()
            score_chirho = scores_chirho[idx_chirho].item()
            passage_preview_chirho = test_passages_chirho[idx_chirho][:80]
            print(f"  #{rank_chirho + 1} ({score_chirho:.3f}): {passage_preview_chirho}...")

    print("\n" + "=" * 60)
    print("Training complete!")
    print(f"Model saved to: {best_dir_chirho}")


if __name__ == "__main__":
    main_chirho()
