# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""Upload topical passage classifier model and dataset to HuggingFace Hub."""

import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import HfApi, create_repo

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

HF_TOKEN_CHIRHO = os.environ.get("HF_TOKEN_CHIRHO", "")
PROJECT_DIR_CHIRHO = Path(__file__).parent.parent


def upload_chirho():
    """Upload model and dataset to HuggingFace."""
    if not HF_TOKEN_CHIRHO:
        print("ERROR: HF_TOKEN_CHIRHO not set in .env file")
        print("Set it to your HuggingFace write token to upload.")
        return

    api_chirho = HfApi(token=HF_TOKEN_CHIRHO)

    # Upload topical search model
    model_dir_chirho = (
        PROJECT_DIR_CHIRHO / "models-chirho" / "topical-chirho" / "best-chirho"
    )
    if model_dir_chirho.exists():
        repo_id_chirho = "LoveJesus/biblical-topical-search-chirho"
        print(f"Uploading model to {repo_id_chirho}...")
        create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True)
        api_chirho.upload_folder(
            folder_path=str(model_dir_chirho),
            repo_id=repo_id_chirho,
            commit_message="Upload topical passage search model (all-MiniLM-L6-v2 fine-tuned)",
        )
        print(f"  Done: https://huggingface.co/{repo_id_chirho}")
    else:
        print(f"Model not found at {model_dir_chirho}")
        print("Run training first: python src-chirho/train-chirho/train-topical-chirho.py")

    # Upload dataset
    dataset_repo_chirho = "LoveJesus/biblical-topical-dataset-chirho"
    data_dir_chirho = PROJECT_DIR_CHIRHO / "data-chirho" / "processed-chirho"
    if data_dir_chirho.exists():
        print(f"\nUploading dataset to {dataset_repo_chirho}...")
        create_repo(
            dataset_repo_chirho,
            token=HF_TOKEN_CHIRHO,
            repo_type="dataset",
            exist_ok=True,
        )
        api_chirho.upload_folder(
            folder_path=str(data_dir_chirho),
            repo_id=dataset_repo_chirho,
            repo_type="dataset",
            commit_message="Upload topical passage search dataset (Nave's + TSK cross-refs)",
        )
        print(f"  Done: https://huggingface.co/datasets/{dataset_repo_chirho}")
    else:
        print(f"Dataset not found at {data_dir_chirho}")
        print("Run the data pipeline first: bun run build-all-chirho")

    print("\nAll uploads complete!")


if __name__ == "__main__":
    upload_chirho()
