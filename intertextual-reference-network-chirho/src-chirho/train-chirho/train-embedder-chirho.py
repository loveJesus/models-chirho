# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-embedder-chirho.py
Trains a MiniLM-L12 sentence transformer for biblical verse similarity
using contrastive (triplet) learning on 344K cross-reference pairs.
"""

import json
from pathlib import Path

import torch
import yaml
from sentence_transformers import (
    InputExample,
    SentenceTransformer,
    losses,
    evaluation,
)
from torch.utils.data import DataLoader

# Paths
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH_CHIRHO = BASE_DIR_CHIRHO / "src-chirho" / "train-chirho" / "config-chirho.yaml"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
OUTPUT_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "embedder-chirho"


def load_config_chirho() -> dict:
    """Load training configuration."""
    with open(CONFIG_PATH_CHIRHO, "r") as f_chirho:
        return yaml.safe_load(f_chirho)


def load_triplets_chirho(split_name_chirho: str) -> list[dict]:
    """Load JSONL triplets."""
    file_path_chirho = DATA_DIR_CHIRHO / f"{split_name_chirho}-embedder-chirho.jsonl"
    triplets_chirho = []
    with open(file_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if line_chirho.strip():
                triplets_chirho.append(json.loads(line_chirho))
    return triplets_chirho


def build_input_examples_chirho(
    triplets_chirho: list[dict],
) -> list[InputExample]:
    """Convert triplet dicts to InputExample objects for sentence-transformers."""
    examples_chirho = []
    for t_chirho in triplets_chirho:
        anchor_chirho = t_chirho["anchor_text_chirho"]
        positive_chirho = t_chirho["positive_text_chirho"]
        negative_chirho = t_chirho["negative_text_chirho"]

        if anchor_chirho and positive_chirho and negative_chirho:
            examples_chirho.append(
                InputExample(texts=[anchor_chirho, positive_chirho, negative_chirho])
            )
    return examples_chirho


def build_eval_pairs_chirho(
    triplets_chirho: list[dict],
    max_pairs_chirho: int = 2000,
) -> list[InputExample]:
    """Build evaluation pairs with similarity scores from triplets."""
    pairs_chirho = []

    for t_chirho in triplets_chirho[:max_pairs_chirho]:
        # Positive pair (high similarity)
        pairs_chirho.append(
            InputExample(
                texts=[t_chirho["anchor_text_chirho"], t_chirho["positive_text_chirho"]],
                label=0.8,
            )
        )
        # Negative pair (low similarity)
        pairs_chirho.append(
            InputExample(
                texts=[t_chirho["anchor_text_chirho"], t_chirho["negative_text_chirho"]],
                label=0.2,
            )
        )

    return pairs_chirho


def main_chirho():
    """Main training loop for the intertextual embedder."""
    print("=" * 60)
    print("Intertextual Reference Embedder Training (MiniLM-L12)")
    print("=" * 60)

    config_chirho = load_config_chirho()
    embedder_config_chirho = config_chirho["embedder_chirho"]

    model_name_chirho = embedder_config_chirho["model_name_chirho"]
    print(f"Model: {model_name_chirho}")

    # Device
    if torch.backends.mps.is_available():
        device_chirho = "mps"
        print("Using Apple MPS")
    elif torch.cuda.is_available():
        device_chirho = "cuda"
        print("Using CUDA")
    else:
        device_chirho = "cpu"
        print("Using CPU")

    # Load model
    print("\nLoading sentence transformer model...")
    model_chirho = SentenceTransformer(model_name_chirho, device=device_chirho)

    # Load data
    print("Loading training triplets...")
    train_triplets_chirho = load_triplets_chirho("train")
    val_triplets_chirho = load_triplets_chirho("val")

    print(f"  Train triplets: {len(train_triplets_chirho)}")
    print(f"  Val triplets: {len(val_triplets_chirho)}")

    # Build InputExamples
    print("Building training examples...")
    train_examples_chirho = build_input_examples_chirho(train_triplets_chirho)
    print(f"  Training examples: {len(train_examples_chirho)}")

    # Build eval pairs
    print("Building evaluation pairs...")
    eval_pairs_chirho = build_eval_pairs_chirho(val_triplets_chirho)
    print(f"  Evaluation pairs: {len(eval_pairs_chirho)}")

    # Data loader
    train_dataloader_chirho = DataLoader(
        train_examples_chirho,
        shuffle=True,
        batch_size=embedder_config_chirho["batch_size_chirho"],
    )

    # Loss function: Triplet loss
    train_loss_chirho = losses.TripletLoss(
        model=model_chirho,
        distance_metric=losses.TripletDistanceMetric.COSINE,
        triplet_margin=embedder_config_chirho["margin_chirho"],
    )

    # Evaluator
    eval_sentences1_chirho = [ex_chirho.texts[0] for ex_chirho in eval_pairs_chirho]
    eval_sentences2_chirho = [ex_chirho.texts[1] for ex_chirho in eval_pairs_chirho]
    eval_scores_chirho = [ex_chirho.label for ex_chirho in eval_pairs_chirho]

    evaluator_chirho = evaluation.EmbeddingSimilarityEvaluator(
        eval_sentences1_chirho,
        eval_sentences2_chirho,
        eval_scores_chirho,
        name="intertextual-similarity-chirho",
    )

    # Output directory
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    # Train
    num_epochs_chirho = embedder_config_chirho["num_epochs_chirho"]
    print(f"\nStarting training for {num_epochs_chirho} epochs...")
    print(f"  Batch size: {embedder_config_chirho['batch_size_chirho']}")
    print(f"  Triplet margin: {embedder_config_chirho['margin_chirho']}")
    print(f"  Learning rate: {embedder_config_chirho['learning_rate_chirho']}")

    model_chirho.fit(
        train_objectives=[(train_dataloader_chirho, train_loss_chirho)],
        evaluator=evaluator_chirho,
        epochs=num_epochs_chirho,
        evaluation_steps=1000,
        warmup_steps=200,
        output_path=str(OUTPUT_DIR_CHIRHO / "best-chirho"),
        save_best_model=True,
        show_progress_bar=True,
    )

    print(f"\nTraining complete! Model saved to: {OUTPUT_DIR_CHIRHO / 'best-chirho'}")

    # Final evaluation
    print("\nFinal evaluation:")
    final_score_chirho = evaluator_chirho(model_chirho)
    if isinstance(final_score_chirho, dict):
        for key_chirho, val_chirho in final_score_chirho.items():
            print(f"  {key_chirho}: {val_chirho:.4f}")
    else:
        print(f"  Embedding similarity score: {final_score_chirho:.4f}")


if __name__ == "__main__":
    main_chirho()
