# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-embedder-chirho.py
Trains a MiniLM-L12 sentence transformer for theological embeddings
using contrastive (triplet) learning. Orthodox statements as anchors,
heresies as negatives.
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


def load_examples_chirho(split_name_chirho: str) -> list[dict]:
    """Load JSONL examples."""
    file_path_chirho = DATA_DIR_CHIRHO / f"{split_name_chirho}-chirho.jsonl"
    examples_chirho = []
    with open(file_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if line_chirho.strip():
                examples_chirho.append(json.loads(line_chirho))
    return examples_chirho


def build_triplets_chirho(
    examples_chirho: list[dict],
) -> list[InputExample]:
    """Build triplet examples: (anchor=orthodox, positive=orthodox, negative=heterodox)."""
    orthodox_chirho = [
        ex_chirho for ex_chirho in examples_chirho if ex_chirho.get("label_chirho") == "orthodox"
    ]
    heterodox_chirho = [
        ex_chirho for ex_chirho in examples_chirho if ex_chirho.get("label_chirho") == "heterodox"
    ]

    if not orthodox_chirho or not heterodox_chirho:
        raise ValueError("Need both orthodox and heterodox examples for triplet training")

    triplets_chirho = []
    # For each orthodox pair, create a triplet with a heterodox negative
    for i_chirho in range(len(orthodox_chirho)):
        for j_chirho in range(i_chirho + 1, min(i_chirho + 5, len(orthodox_chirho))):
            # Pick a heterodox negative
            neg_idx_chirho = (i_chirho + j_chirho) % len(heterodox_chirho)

            anchor_chirho = orthodox_chirho[i_chirho]["text_chirho"]
            positive_chirho = orthodox_chirho[j_chirho]["text_chirho"]
            negative_chirho = heterodox_chirho[neg_idx_chirho]["text_chirho"]

            triplets_chirho.append(
                InputExample(texts=[anchor_chirho, positive_chirho, negative_chirho])
            )

    # Also create heresy-type-aware triplets
    # Group heresies by type for intra-heresy similarity
    heresy_groups_chirho: dict[str, list[str]] = {}
    for ex_chirho in heterodox_chirho:
        for ht_chirho in ex_chirho.get("heresy_types_chirho", []):
            if ht_chirho not in heresy_groups_chirho:
                heresy_groups_chirho[ht_chirho] = []
            heresy_groups_chirho[ht_chirho].append(ex_chirho["text_chirho"])

    # Heresy anchor + same heresy positive + orthodox negative
    for heresy_type_chirho, texts_chirho in heresy_groups_chirho.items():
        for i_chirho in range(len(texts_chirho)):
            for j_chirho in range(i_chirho + 1, min(i_chirho + 3, len(texts_chirho))):
                orth_idx_chirho = (i_chirho + j_chirho) % len(orthodox_chirho)
                triplets_chirho.append(
                    InputExample(
                        texts=[
                            texts_chirho[i_chirho],
                            texts_chirho[j_chirho],
                            orthodox_chirho[orth_idx_chirho]["text_chirho"],
                        ]
                    )
                )

    return triplets_chirho


def build_eval_pairs_chirho(
    examples_chirho: list[dict],
) -> list[InputExample]:
    """Build evaluation pairs with similarity scores."""
    orthodox_chirho = [
        ex_chirho for ex_chirho in examples_chirho if ex_chirho.get("label_chirho") == "orthodox"
    ]
    heterodox_chirho = [
        ex_chirho for ex_chirho in examples_chirho if ex_chirho.get("label_chirho") == "heterodox"
    ]

    pairs_chirho = []

    # Orthodox-orthodox pairs (high similarity)
    for i_chirho in range(min(100, len(orthodox_chirho))):
        j_chirho = (i_chirho + 1) % len(orthodox_chirho)
        pairs_chirho.append(
            InputExample(
                texts=[
                    orthodox_chirho[i_chirho]["text_chirho"],
                    orthodox_chirho[j_chirho]["text_chirho"],
                ],
                label=0.8,
            )
        )

    # Orthodox-heterodox pairs (low similarity)
    for i_chirho in range(min(100, len(heterodox_chirho))):
        orth_idx_chirho = i_chirho % len(orthodox_chirho)
        pairs_chirho.append(
            InputExample(
                texts=[
                    orthodox_chirho[orth_idx_chirho]["text_chirho"],
                    heterodox_chirho[i_chirho]["text_chirho"],
                ],
                label=0.2,
            )
        )

    return pairs_chirho


def main_chirho():
    """Main training loop for the theological embedder."""
    print("=" * 60)
    print("Theological Embedder Training (MiniLM-L12)")
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
    print("Loading training data...")
    train_examples_chirho = load_examples_chirho("train")
    val_examples_chirho = load_examples_chirho("val")

    print(f"  Train examples: {len(train_examples_chirho)}")
    print(f"  Val examples: {len(val_examples_chirho)}")

    # Build triplets for training
    print("Building triplets...")
    train_triplets_chirho = build_triplets_chirho(train_examples_chirho)
    print(f"  Training triplets: {len(train_triplets_chirho)}")

    # Build eval pairs
    print("Building evaluation pairs...")
    eval_pairs_chirho = build_eval_pairs_chirho(val_examples_chirho)
    print(f"  Evaluation pairs: {len(eval_pairs_chirho)}")

    # Data loader
    train_dataloader_chirho = DataLoader(
        train_triplets_chirho,
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
        name="theological-similarity-chirho",
    )

    # Output directory
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    # Train
    print(f"\nStarting training for {embedder_config_chirho['num_epochs_chirho']} epochs...")
    model_chirho.fit(
        train_objectives=[(train_dataloader_chirho, train_loss_chirho)],
        evaluator=evaluator_chirho,
        epochs=embedder_config_chirho["num_epochs_chirho"],
        evaluation_steps=500,
        warmup_steps=100,
        output_path=str(OUTPUT_DIR_CHIRHO / "best-chirho"),
        save_best_model=True,
        show_progress_bar=True,
    )

    print(f"\nTraining complete! Model saved to: {OUTPUT_DIR_CHIRHO / 'best-chirho'}")

    # Quick evaluation
    print("\nFinal evaluation:")
    final_score_chirho = evaluator_chirho(model_chirho)
    print(f"  Embedding similarity score: {final_score_chirho:.4f}")


if __name__ == "__main__":
    main_chirho()
