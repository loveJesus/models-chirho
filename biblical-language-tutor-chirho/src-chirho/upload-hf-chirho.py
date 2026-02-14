# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
upload-hf-chirho.py
Upload trained parser, glosser models and dataset to HuggingFace Hub.
Repos: LoveJesus/biblical-{parser,glosser,tutor-dataset}-chirho
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import HfApi, create_repo

# Load .env (check project-level and parent-level)
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR_CHIRHO / ".env")
load_dotenv(BASE_DIR_CHIRHO.parent / ".env-chirho")

HF_TOKEN_CHIRHO = os.getenv("HF_TOKEN_CHIRHO")
if not HF_TOKEN_CHIRHO:
    print("ERROR: HF_TOKEN_CHIRHO not found in .env or parent .env-chirho")
    sys.exit(1)

HF_USER_CHIRHO = "LoveJesus"
MODELS_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
CARDS_DIR_CHIRHO = BASE_DIR_CHIRHO / "cards-chirho"


def upload_parser_chirho(api_chirho: HfApi):
    """Upload mT5-small morphological parser."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/biblical-parser-chirho"
    model_path_chirho = MODELS_DIR_CHIRHO / "parser-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Parser not found at {model_path_chirho}, skipping.")
        return

    print(f"\nUploading parser to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="model")

    api_chirho.upload_folder(
        folder_path=str(model_path_chirho),
        repo_id=repo_id_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message="Upload mT5-small biblical morphological parser",
    )

    card_path_chirho = CARDS_DIR_CHIRHO / "parser-card-chirho.md"
    if card_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(card_path_chirho),
            path_in_repo="README.md",
            repo_id=repo_id_chirho,
            token=HF_TOKEN_CHIRHO,
            commit_message="Add model card",
        )

    print(f"  Parser uploaded: https://huggingface.co/{repo_id_chirho}")


def upload_glosser_chirho(api_chirho: HfApi):
    """Upload mT5-small interlinear glosser."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/biblical-glosser-chirho"
    model_path_chirho = MODELS_DIR_CHIRHO / "glosser-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Glosser not found at {model_path_chirho}, skipping.")
        return

    print(f"\nUploading glosser to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="model")

    api_chirho.upload_folder(
        folder_path=str(model_path_chirho),
        repo_id=repo_id_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message="Upload mT5-small biblical interlinear glosser",
    )

    card_path_chirho = CARDS_DIR_CHIRHO / "glosser-card-chirho.md"
    if card_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(card_path_chirho),
            path_in_repo="README.md",
            repo_id=repo_id_chirho,
            token=HF_TOKEN_CHIRHO,
            commit_message="Add model card",
        )

    print(f"  Glosser uploaded: https://huggingface.co/{repo_id_chirho}")


def upload_dataset_chirho(api_chirho: HfApi):
    """Upload training dataset to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/biblical-tutor-dataset-chirho"

    if not DATA_DIR_CHIRHO.exists():
        print(f"  Dataset not found at {DATA_DIR_CHIRHO}, skipping.")
        return

    print(f"\nUploading dataset to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="dataset")

    # Upload parser splits
    for split_chirho in ["train-parser-chirho.jsonl", "val-parser-chirho.jsonl", "test-parser-chirho.jsonl"]:
        file_path_chirho = DATA_DIR_CHIRHO / split_chirho
        if file_path_chirho.exists():
            api_chirho.upload_file(
                path_or_fileobj=str(file_path_chirho),
                path_in_repo=f"parser/{split_chirho}",
                repo_id=repo_id_chirho,
                repo_type="dataset",
                token=HF_TOKEN_CHIRHO,
                commit_message=f"Upload parser {split_chirho}",
            )

    # Upload glosser splits
    for split_chirho in ["train-glosser-chirho.jsonl", "val-glosser-chirho.jsonl", "test-glosser-chirho.jsonl"]:
        file_path_chirho = DATA_DIR_CHIRHO / split_chirho
        if file_path_chirho.exists():
            api_chirho.upload_file(
                path_or_fileobj=str(file_path_chirho),
                path_in_repo=f"glosser/{split_chirho}",
                repo_id=repo_id_chirho,
                repo_type="dataset",
                token=HF_TOKEN_CHIRHO,
                commit_message=f"Upload glosser {split_chirho}",
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
    print("HuggingFace Upload - Biblical Language Tutor")
    print("=" * 60)
    print(f"User: {HF_USER_CHIRHO}")

    api_chirho = HfApi()

    targets_chirho = sys.argv[1:] if len(sys.argv) > 1 else ["all"]

    if "all" in targets_chirho or "parser" in targets_chirho:
        upload_parser_chirho(api_chirho)

    if "all" in targets_chirho or "glosser" in targets_chirho:
        upload_glosser_chirho(api_chirho)

    if "all" in targets_chirho or "dataset" in targets_chirho:
        upload_dataset_chirho(api_chirho)

    print("\n" + "=" * 60)
    print("Upload complete!")
    print(f"  Models: https://huggingface.co/{HF_USER_CHIRHO}")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
