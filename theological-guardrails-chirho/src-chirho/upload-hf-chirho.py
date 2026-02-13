# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
upload-hf-chirho.py
Upload trained models and dataset to HuggingFace Hub.
Repos: LoveJesus/theologian-{classifier,embedder,explainer,dataset}-chirho
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import HfApi, create_repo

# Load .env
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR_CHIRHO / ".env")

HF_TOKEN_CHIRHO = os.getenv("HF_TOKEN_CHIRHO")
if not HF_TOKEN_CHIRHO:
    print("ERROR: HF_TOKEN_CHIRHO not found in .env")
    sys.exit(1)

HF_USER_CHIRHO = "LoveJesus"
MODELS_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
CARDS_DIR_CHIRHO = BASE_DIR_CHIRHO / "cards-chirho"


def upload_classifier_chirho(api_chirho: HfApi):
    """Upload RoBERTa-large classifier to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/theologian-classifier-chirho"
    model_path_chirho = MODELS_DIR_CHIRHO / "classifier-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Classifier not found at {model_path_chirho}, skipping.")
        return

    print(f"\nUploading classifier to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="model")

    # Upload model files
    api_chirho.upload_folder(
        folder_path=str(model_path_chirho),
        repo_id=repo_id_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message="Upload RoBERTa-large theological classifier (F1=0.9971)",
    )

    # Upload README (model card)
    card_path_chirho = CARDS_DIR_CHIRHO / "model-card-chirho.md"
    if card_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(card_path_chirho),
            path_in_repo="README.md",
            repo_id=repo_id_chirho,
            token=HF_TOKEN_CHIRHO,
            commit_message="Add model card",
        )

    print(f"  Classifier uploaded: https://huggingface.co/{repo_id_chirho}")


def upload_embedder_chirho(api_chirho: HfApi):
    """Upload MiniLM-L12 embedder to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/theologian-embedder-chirho"
    model_path_chirho = MODELS_DIR_CHIRHO / "embedder-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Embedder not found at {model_path_chirho}, skipping.")
        return

    print(f"\nUploading embedder to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="model")

    api_chirho.upload_folder(
        folder_path=str(model_path_chirho),
        repo_id=repo_id_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message="Upload MiniLM-L12 theological embedder (Pearson=0.970)",
    )

    # Upload README (model card)
    card_path_chirho = CARDS_DIR_CHIRHO / "embedder-card-chirho.md"
    if card_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(card_path_chirho),
            path_in_repo="README.md",
            repo_id=repo_id_chirho,
            token=HF_TOKEN_CHIRHO,
            commit_message="Add embedder model card",
        )

    print(f"  Embedder uploaded: https://huggingface.co/{repo_id_chirho}")


def upload_explainer_chirho(api_chirho: HfApi):
    """Upload Flan-T5-base explainer to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/theologian-explainer-chirho"
    model_path_chirho = MODELS_DIR_CHIRHO / "explainer-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Explainer not found at {model_path_chirho}, skipping.")
        return

    print(f"\nUploading explainer to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="model")

    api_chirho.upload_folder(
        folder_path=str(model_path_chirho),
        repo_id=repo_id_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message="Upload Flan-T5-base theological explainer",
    )

    # Upload README (model card)
    card_path_chirho = CARDS_DIR_CHIRHO / "explainer-card-chirho.md"
    if card_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(card_path_chirho),
            path_in_repo="README.md",
            repo_id=repo_id_chirho,
            token=HF_TOKEN_CHIRHO,
            commit_message="Add explainer model card",
        )

    print(f"  Explainer uploaded: https://huggingface.co/{repo_id_chirho}")


def upload_dataset_chirho(api_chirho: HfApi):
    """Upload dataset to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/theologian-dataset-chirho"

    if not DATA_DIR_CHIRHO.exists():
        print(f"  Dataset not found at {DATA_DIR_CHIRHO}, skipping.")
        return

    print(f"\nUploading dataset to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="dataset")

    # Upload data files
    for split_chirho in ["train-chirho.jsonl", "val-chirho.jsonl", "test-chirho.jsonl"]:
        file_path_chirho = DATA_DIR_CHIRHO / split_chirho
        if file_path_chirho.exists():
            api_chirho.upload_file(
                path_or_fileobj=str(file_path_chirho),
                path_in_repo=f"data/{split_chirho}",
                repo_id=repo_id_chirho,
                repo_type="dataset",
                token=HF_TOKEN_CHIRHO,
                commit_message=f"Upload {split_chirho}",
            )

    # Upload dataset card
    card_path_chirho = CARDS_DIR_CHIRHO / "dataset-card-chirho.md"
    if card_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(card_path_chirho),
            path_in_repo="README.md",
            repo_id=repo_id_chirho,
            repo_type="dataset",
            token=HF_TOKEN_CHIRHO,
            commit_message="Add dataset card",
        )

    print(f"  Dataset uploaded: https://huggingface.co/datasets/{repo_id_chirho}")


def main_chirho():
    """Upload all models and dataset to HuggingFace Hub."""
    print("=" * 60)
    print("HuggingFace Upload - Theological Guardrails Pipeline")
    print("=" * 60)
    print(f"User: {HF_USER_CHIRHO}")

    api_chirho = HfApi()

    # Parse args for selective upload
    targets_chirho = sys.argv[1:] if len(sys.argv) > 1 else ["all"]

    if "all" in targets_chirho or "classifier" in targets_chirho:
        upload_classifier_chirho(api_chirho)

    if "all" in targets_chirho or "embedder" in targets_chirho:
        upload_embedder_chirho(api_chirho)

    if "all" in targets_chirho or "explainer" in targets_chirho:
        upload_explainer_chirho(api_chirho)

    if "all" in targets_chirho or "dataset" in targets_chirho:
        upload_dataset_chirho(api_chirho)

    print("\n" + "=" * 60)
    print("Upload complete!")
    print(f"  Models: https://huggingface.co/{HF_USER_CHIRHO}")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
