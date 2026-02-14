# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-embedder-chirho.py
Fine-tunes a sentence transformer for cross-translation Bible verse embeddings.

Uses contrastive learning (CosineSimilarityLoss) on verse pairs:
  - Positive: same verse in different translations (label=1.0)
  - Negative: different verses (label=0.0)

Base model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
  - 118M params, 384-dim embeddings, supports 50+ languages
  - Pre-trained on multilingual paraphrase data

Output: models-chirho/embedder-chirho/best-chirho/
"""

import json
import math
import os
import sys

import torch
from sentence_transformers import (
    InputExample,
    SentenceTransformer,
    evaluation,
    losses,
)
from torch.utils.data import DataLoader


def load_pairs_chirho(file_path_chirho: str) -> list:
    """Load sentence pair JSONL file."""
    examples_chirho = []
    with open(file_path_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            obj_chirho = json.loads(line_chirho)
            examples_chirho.append(
                InputExample(
                    texts=[obj_chirho["sentence1_chirho"], obj_chirho["sentence2_chirho"]],
                    label=float(obj_chirho["label_chirho"]),
                )
            )
    return examples_chirho


def main_chirho():
    """Main training function."""
    print("=" * 60)
    print("Cross-Translation Embedding Training")
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
    model_name_chirho = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    batch_size_chirho = 64 if device_chirho == "cuda" else 16
    epochs_chirho = 3
    lr_chirho = 2e-5
    warmup_ratio_chirho = 0.1

    data_dir_chirho = os.path.join(os.path.dirname(__file__), "../../data-chirho/processed-chirho")
    output_dir_chirho = os.path.join(os.path.dirname(__file__), "../../models-chirho/embedder-chirho")
    best_dir_chirho = os.path.join(output_dir_chirho, "best-chirho")

    print(f"Model: {model_name_chirho}")
    print(f"Batch size: {batch_size_chirho}")
    print(f"Epochs: {epochs_chirho}")
    print(f"Learning rate: {lr_chirho}")

    # Load model
    print("\nLoading model...")
    model_chirho = SentenceTransformer(model_name_chirho, device=device_chirho)

    # Load datasets
    print("Loading datasets...")
    train_path_chirho = os.path.join(data_dir_chirho, "train-embedding-chirho.jsonl")
    val_path_chirho = os.path.join(data_dir_chirho, "val-embedding-chirho.jsonl")

    train_examples_chirho = load_pairs_chirho(train_path_chirho)
    val_examples_chirho = load_pairs_chirho(val_path_chirho)

    print(f"  Train: {len(train_examples_chirho)} pairs")
    print(f"  Validation: {len(val_examples_chirho)} pairs")

    # DataLoader
    train_dataloader_chirho = DataLoader(
        train_examples_chirho,
        shuffle=True,
        batch_size=batch_size_chirho,
    )

    # Loss: Cosine Similarity Loss
    loss_chirho = losses.CosineSimilarityLoss(model_chirho)

    # Evaluator: use validation pairs
    # Split val into positive and negative for evaluation
    eval_sentences1_chirho = []
    eval_sentences2_chirho = []
    eval_scores_chirho = []
    for ex_chirho in val_examples_chirho[:5000]:  # Cap eval at 5K for speed
        eval_sentences1_chirho.append(ex_chirho.texts[0])
        eval_sentences2_chirho.append(ex_chirho.texts[1])
        eval_scores_chirho.append(ex_chirho.label)

    evaluator_chirho = evaluation.EmbeddingSimilarityEvaluator(
        eval_sentences1_chirho,
        eval_sentences2_chirho,
        eval_scores_chirho,
        name="val-chirho",
        write_csv=True,
    )

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
        evaluation_steps=1000,
        save_best_model=True,
        show_progress_bar=True,
    )

    # Quick inference test
    print("\nInference test:")
    test_verses_chirho = [
        "[KJV] In the beginning God created the heaven and the earth.",
        "[ASV] In the beginning God created the heavens and the earth.",
        "[BBE] At the first God made the heaven and the earth.",
        "[KJV] And the earth was without form, and void;",
    ]

    embeddings_chirho = model_chirho.encode(test_verses_chirho)
    from sentence_transformers.util import cos_sim

    sim_matrix_chirho = cos_sim(embeddings_chirho, embeddings_chirho)

    print("  Similarity matrix (Gen 1:1 x3, Gen 1:2 x1):")
    labels_chirho = ["KJV 1:1", "ASV 1:1", "BBE 1:1", "KJV 1:2"]
    for i_chirho, label_i_chirho in enumerate(labels_chirho):
        row_chirho = " ".join(
            f"{sim_matrix_chirho[i_chirho][j_chirho].item():.3f}"
            for j_chirho in range(len(labels_chirho))
        )
        print(f"    {label_i_chirho}: {row_chirho}")

    print("\nTraining complete!")
    print(f"Model saved to: {best_dir_chirho}")


if __name__ == "__main__":
    main_chirho()
