# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
upload-hf-chirho.py
Upload trained Flan-T5-small dual-task model and dataset to HuggingFace Hub.
Repos: LoveJesus/passage-difficulty-simplifier-chirho (model)
       LoveJesus/passage-difficulty-simplifier-dataset-chirho (dataset)
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


def upload_model_chirho(api_chirho: HfApi):
    """Upload Flan-T5-small dual-task model to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/passage-difficulty-simplifier-chirho"
    model_path_chirho = MODELS_DIR_CHIRHO / "simplifier-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Model not found at {model_path_chirho}, skipping.")
        return

    print(f"\nUploading model to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="model")

    # Upload model files
    api_chirho.upload_folder(
        folder_path=str(model_path_chirho),
        repo_id=repo_id_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message="Upload Flan-T5-small passage difficulty scorer & simplifier",
    )

    # Upload model card
    card_path_chirho = CARDS_DIR_CHIRHO / "simplifier-card-chirho.md"
    if card_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(card_path_chirho),
            path_in_repo="README.md",
            repo_id=repo_id_chirho,
            token=HF_TOKEN_CHIRHO,
            commit_message="Add model card",
        )

    print(f"  Model uploaded: https://huggingface.co/{repo_id_chirho}")


def upload_dataset_chirho(api_chirho: HfApi):
    """Upload dataset to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/passage-difficulty-simplifier-dataset-chirho"

    if not DATA_DIR_CHIRHO.exists():
        print(f"  Dataset not found at {DATA_DIR_CHIRHO}, skipping.")
        return

    print(f"\nUploading dataset to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="dataset")

    # Upload data files
    for split_chirho in [
        "train-simplifier-chirho.jsonl",
        "val-simplifier-chirho.jsonl",
        "test-simplifier-chirho.jsonl",
    ]:
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
    """Upload model and dataset to HuggingFace Hub."""
    print("=" * 60)
    print("HuggingFace Upload - Passage Difficulty Scorer & Simplifier")
    print("=" * 60)
    print(f"User: {HF_USER_CHIRHO}")

    api_chirho = HfApi()

    # Parse args for selective upload
    targets_chirho = sys.argv[1:] if len(sys.argv) > 1 else ["all"]

    if "all" in targets_chirho or "model" in targets_chirho:
        upload_model_chirho(api_chirho)

    if "all" in targets_chirho or "dataset" in targets_chirho:
        upload_dataset_chirho(api_chirho)

    print("\n" + "=" * 60)
    print("Upload complete!")
    print(f"  Model: https://huggingface.co/{HF_USER_CHIRHO}/passage-difficulty-simplifier-chirho")
    print(f"  Dataset: https://huggingface.co/datasets/{HF_USER_CHIRHO}/passage-difficulty-simplifier-dataset-chirho")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
