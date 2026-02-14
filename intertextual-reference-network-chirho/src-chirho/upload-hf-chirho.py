# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
upload-hf-chirho.py
Upload trained models and dataset to HuggingFace Hub.
Repos: LoveJesus/intertextual-{embedder,classifier,dataset}-chirho
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


def upload_embedder_chirho(api_chirho: HfApi):
    """Upload MiniLM-L12 intertextual embedder."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/intertextual-embedder-chirho"
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
        commit_message="Upload MiniLM-L12 intertextual embedder",
    )

    card_path_chirho = CARDS_DIR_CHIRHO / "embedder-card-chirho.md"
    if card_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(card_path_chirho),
            path_in_repo="README.md",
            repo_id=repo_id_chirho,
            token=HF_TOKEN_CHIRHO,
            commit_message="Add model card",
        )

    print(f"  Embedder uploaded: https://huggingface.co/{repo_id_chirho}")


def upload_classifier_chirho(api_chirho: HfApi):
    """Upload RoBERTa-base connection type classifier."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/intertextual-classifier-chirho"
    model_path_chirho = MODELS_DIR_CHIRHO / "classifier-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Classifier not found at {model_path_chirho}, skipping.")
        return

    print(f"\nUploading classifier to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="model")

    api_chirho.upload_folder(
        folder_path=str(model_path_chirho),
        repo_id=repo_id_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message="Upload RoBERTa-base intertextual classifier",
    )

    card_path_chirho = CARDS_DIR_CHIRHO / "classifier-card-chirho.md"
    if card_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(card_path_chirho),
            path_in_repo="README.md",
            repo_id=repo_id_chirho,
            token=HF_TOKEN_CHIRHO,
            commit_message="Add model card",
        )

    print(f"  Classifier uploaded: https://huggingface.co/{repo_id_chirho}")


def upload_dataset_chirho(api_chirho: HfApi):
    """Upload dataset to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/intertextual-dataset-chirho"

    if not DATA_DIR_CHIRHO.exists():
        print(f"  Dataset not found at {DATA_DIR_CHIRHO}, skipping.")
        return

    print(f"\nUploading dataset to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="dataset")

    # Upload embedder splits
    for split_chirho in ["train-embedder-chirho.jsonl", "val-embedder-chirho.jsonl", "test-embedder-chirho.jsonl"]:
        file_path_chirho = DATA_DIR_CHIRHO / split_chirho
        if file_path_chirho.exists():
            api_chirho.upload_file(
                path_or_fileobj=str(file_path_chirho),
                path_in_repo=f"embedder/{split_chirho}",
                repo_id=repo_id_chirho,
                repo_type="dataset",
                token=HF_TOKEN_CHIRHO,
                commit_message=f"Upload embedder {split_chirho}",
            )

    # Upload classifier splits
    for split_chirho in ["train-classifier-chirho.jsonl", "val-classifier-chirho.jsonl", "test-classifier-chirho.jsonl"]:
        file_path_chirho = DATA_DIR_CHIRHO / split_chirho
        if file_path_chirho.exists():
            api_chirho.upload_file(
                path_or_fileobj=str(file_path_chirho),
                path_in_repo=f"classifier/{split_chirho}",
                repo_id=repo_id_chirho,
                repo_type="dataset",
                token=HF_TOKEN_CHIRHO,
                commit_message=f"Upload classifier {split_chirho}",
            )

    # Upload verse map
    verse_map_chirho = DATA_DIR_CHIRHO / "verse-map-chirho.json"
    if verse_map_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(verse_map_chirho),
            path_in_repo="verse-map-chirho.json",
            repo_id=repo_id_chirho,
            repo_type="dataset",
            token=HF_TOKEN_CHIRHO,
            commit_message="Upload verse map",
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
    print("HuggingFace Upload - Intertextual Reference Network")
    print("=" * 60)
    print(f"User: {HF_USER_CHIRHO}")

    api_chirho = HfApi()

    targets_chirho = sys.argv[1:] if len(sys.argv) > 1 else ["all"]

    if "all" in targets_chirho or "embedder" in targets_chirho:
        upload_embedder_chirho(api_chirho)

    if "all" in targets_chirho or "classifier" in targets_chirho:
        upload_classifier_chirho(api_chirho)

    if "all" in targets_chirho or "dataset" in targets_chirho:
        upload_dataset_chirho(api_chirho)

    print("\n" + "=" * 60)
    print("Upload complete!")
    print(f"  Models: https://huggingface.co/{HF_USER_CHIRHO}")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
