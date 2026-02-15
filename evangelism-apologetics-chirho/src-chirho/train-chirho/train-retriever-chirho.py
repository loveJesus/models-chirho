# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-retriever-chirho.py
Train MiniLM-L12 retriever for Model 9: Evangelism & Apologetics.

Fine-tunes sentence-transformers/all-MiniLM-L12-v2 on (query, passage) pairs
using MultipleNegativesRankingLoss (MNRL) for semantic retrieval.
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import torch
from sentence_transformers import (
    InputExample,
    SentenceTransformer,
    evaluation,
    losses,
)
from torch.utils.data import DataLoader

# ── Constants ──────────────────────────────────────────────────────────
MODEL_NAME_CHIRHO = "sentence-transformers/all-MiniLM-L12-v2"
BATCH_SIZE_CHIRHO = 32
EPOCHS_CHIRHO = 3
LEARNING_RATE_CHIRHO = 2e-5
WARMUP_STEPS_CHIRHO = 200
EVAL_STEPS_CHIRHO = 500
SEED_CHIRHO = 316  # John 3:16

BASE_DIR_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho")
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho" / "retriever-chirho"
OUTPUT_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "retriever-chirho"
PROGRESS_DB_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/spec-chirho/progress-chirho.sqlite")
AGENT_CODE_CHIRHO = "train-retriever-chirho"


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


def load_pairs_chirho(filepath_chirho):
    """Load (query, passage) pairs from JSONL."""
    pairs_chirho = []
    with open(filepath_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            line_chirho = line_chirho.strip()
            if not line_chirho:
                continue
            entry_chirho = json.loads(line_chirho)
            query_chirho = entry_chirho.get("query_chirho", "").strip()
            passage_chirho = entry_chirho.get("passage_chirho", "").strip()
            if query_chirho and passage_chirho and len(passage_chirho) > 20:
                pairs_chirho.append((query_chirho, passage_chirho))
    return pairs_chirho


def build_train_examples_chirho(pairs_chirho):
    """Convert (query, passage) pairs to InputExamples for MNRL."""
    examples_chirho = []
    for query_chirho, passage_chirho in pairs_chirho:
        examples_chirho.append(
            InputExample(texts=[query_chirho, passage_chirho])
        )
    return examples_chirho


def build_eval_pairs_chirho(pairs_chirho, max_pairs_chirho=2000):
    """Build evaluation pairs with similarity scores."""
    import random
    random.seed(SEED_CHIRHO)

    eval_sentences1_chirho = []
    eval_sentences2_chirho = []
    eval_scores_chirho = []

    # Positive pairs (matching query-passage)
    subset_chirho = pairs_chirho[:max_pairs_chirho]
    for query_chirho, passage_chirho in subset_chirho:
        eval_sentences1_chirho.append(query_chirho)
        eval_sentences2_chirho.append(passage_chirho)
        eval_scores_chirho.append(0.85)

    # Negative pairs (mismatched query-passage)
    shuffled_passages_chirho = [p_chirho for _, p_chirho in subset_chirho]
    random.shuffle(shuffled_passages_chirho)
    for i_chirho, (query_chirho, _) in enumerate(subset_chirho):
        neg_passage_chirho = shuffled_passages_chirho[i_chirho]
        # Avoid accidental positive match
        if neg_passage_chirho == subset_chirho[i_chirho][1]:
            continue
        eval_sentences1_chirho.append(query_chirho)
        eval_sentences2_chirho.append(neg_passage_chirho)
        eval_scores_chirho.append(0.15)

    return eval_sentences1_chirho, eval_sentences2_chirho, eval_scores_chirho


def main_chirho():
    """Train the apologetics retriever."""
    print("=" * 60)
    print("Model 9: Retriever Training (MiniLM-L12-v2 + MNRL)")
    print("=" * 60)

    # Check data exists
    train_path_chirho = DATA_DIR_CHIRHO / "train-chirho.jsonl"
    val_path_chirho = DATA_DIR_CHIRHO / "val-chirho.jsonl"

    if not train_path_chirho.exists():
        print(f"ERROR: Training data not found at {train_path_chirho}")
        print("Run process-corpus-chirho.py first to generate retriever data.")
        return

    # Detect device
    if torch.backends.mps.is_available():
        device_chirho = "mps"
    elif torch.cuda.is_available():
        device_chirho = "cuda"
    else:
        device_chirho = "cpu"
    print(f"Device: {device_chirho}")

    # Load model
    print(f"\nLoading model: {MODEL_NAME_CHIRHO}")
    model_chirho = SentenceTransformer(MODEL_NAME_CHIRHO, device=device_chirho)

    # Load data
    print("Loading training pairs...")
    train_pairs_chirho = load_pairs_chirho(train_path_chirho)
    val_pairs_chirho = load_pairs_chirho(val_path_chirho)

    print(f"  Train pairs: {len(train_pairs_chirho)}")
    print(f"  Val pairs:   {len(val_pairs_chirho)}")

    # Build training examples
    print("Building training examples...")
    train_examples_chirho = build_train_examples_chirho(train_pairs_chirho)
    print(f"  Training examples: {len(train_examples_chirho)}")

    # Build evaluation
    print("Building evaluation pairs...")
    eval_s1_chirho, eval_s2_chirho, eval_scores_chirho = build_eval_pairs_chirho(val_pairs_chirho)
    print(f"  Evaluation pairs: {len(eval_s1_chirho)}")

    evaluator_chirho = evaluation.EmbeddingSimilarityEvaluator(
        eval_s1_chirho,
        eval_s2_chirho,
        eval_scores_chirho,
        name="apologetics-retriever-chirho",
    )

    # Data loader
    train_dataloader_chirho = DataLoader(
        train_examples_chirho,
        shuffle=True,
        batch_size=BATCH_SIZE_CHIRHO,
    )

    # Loss: Multiple Negatives Ranking Loss (MNRL)
    # In-batch negatives: each passage paired with other queries as negatives
    train_loss_chirho = losses.MultipleNegativesRankingLoss(model=model_chirho)

    # Output directory
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)
    best_dir_chirho = OUTPUT_DIR_CHIRHO / "best-chirho"

    # Train
    print(f"\n{'=' * 60}")
    print("TRAINING")
    print(f"{'=' * 60}")
    print(f"  Epochs: {EPOCHS_CHIRHO}")
    print(f"  Batch size: {BATCH_SIZE_CHIRHO}")
    print(f"  Learning rate: {LEARNING_RATE_CHIRHO}")
    print(f"  Loss: MultipleNegativesRankingLoss (MNRL)")

    log_progress_chirho(
        f"Start retriever training: {MODEL_NAME_CHIRHO}, {len(train_pairs_chirho)} pairs, {EPOCHS_CHIRHO} epochs",
        "Training started",
        f"Device: {device_chirho}, batch_size={BATCH_SIZE_CHIRHO}, lr={LEARNING_RATE_CHIRHO}, loss=MNRL",
    )

    model_chirho.fit(
        train_objectives=[(train_dataloader_chirho, train_loss_chirho)],
        evaluator=evaluator_chirho,
        epochs=EPOCHS_CHIRHO,
        evaluation_steps=EVAL_STEPS_CHIRHO,
        warmup_steps=WARMUP_STEPS_CHIRHO,
        output_path=str(best_dir_chirho),
        save_best_model=True,
        show_progress_bar=True,
        optimizer_params={"lr": LEARNING_RATE_CHIRHO},
    )

    # Final evaluation
    print(f"\n{'=' * 60}")
    print("EVALUATION")
    print(f"{'=' * 60}")

    final_score_chirho = evaluator_chirho(model_chirho)
    if isinstance(final_score_chirho, dict):
        for key_chirho, val_chirho in final_score_chirho.items():
            print(f"  {key_chirho}: {val_chirho:.4f}")
    else:
        print(f"  Embedding similarity (Pearson): {final_score_chirho:.4f}")

    # Log completion
    score_str_chirho = f"{final_score_chirho:.4f}" if isinstance(final_score_chirho, (int, float)) else str(final_score_chirho)
    log_progress_chirho(
        f"Retriever training complete: score={score_str_chirho}",
        f"Model saved to {best_dir_chirho}",
        f"Pairs={len(train_pairs_chirho)}, Epochs={EPOCHS_CHIRHO}",
    )

    print(f"\n  Model saved to: {best_dir_chirho}")
    print(f"\n{'=' * 60}")
    print("TRAINING COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main_chirho()
