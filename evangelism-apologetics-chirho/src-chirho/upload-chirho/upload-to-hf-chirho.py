# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
upload-to-hf-chirho.py
Upload Model 9 components to HuggingFace Hub.

Uploads:
  1. Intent Classifier (RoBERTa-base)
  2. Retriever (MiniLM-L12-v2)
  3. Generator (Qwen3-4B LoRA adapter)
  4. Dataset (training corpus)
"""

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi, create_repo

# ── Constants ──────────────────────────────────────────────────────────
BASE_DIR_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho")
MODELS_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho"
PROGRESS_DB_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/spec-chirho/progress-chirho.sqlite")
AGENT_CODE_CHIRHO = "upload-hf-chirho"

HF_USER_CHIRHO = "LoveJesus"
HF_TOKEN_CHIRHO = os.environ.get("HF_TOKEN_CHIRHO", "")

REPOS_CHIRHO = {
    "intent-classifier": {
        "repo_id_chirho": f"{HF_USER_CHIRHO}/evangelism-intent-classifier-chirho",
        "local_dir_chirho": MODELS_DIR_CHIRHO / "intent-classifier-chirho" / "best-chirho",
        "description_chirho": "RoBERTa-base intent classifier for evangelism & apologetics (5 categories)",
    },
    "retriever": {
        "repo_id_chirho": f"{HF_USER_CHIRHO}/evangelism-retriever-chirho",
        "local_dir_chirho": MODELS_DIR_CHIRHO / "retriever-chirho" / "best-chirho",
        "description_chirho": "MiniLM-L12 retriever for apologetics passage retrieval",
    },
    "generator": {
        "repo_id_chirho": f"{HF_USER_CHIRHO}/evangelism-generator-chirho",
        "local_dir_chirho": MODELS_DIR_CHIRHO / "generator-chirho" / "best-chirho",
        "description_chirho": "Qwen3-14B LoRA adapter for generating apologetics responses (base: Qwen/Qwen3-14B)",
    },
    "dataset": {
        "repo_id_chirho": f"{HF_USER_CHIRHO}/evangelism-dataset-chirho",
        "local_dir_chirho": DATA_DIR_CHIRHO / "processed-chirho",
        "description_chirho": "Training dataset for evangelism & apologetics models",
    },
}


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


def upload_component_chirho(name_chirho, config_chirho, api_chirho):
    """Upload a single component to HuggingFace."""
    repo_id_chirho = config_chirho["repo_id_chirho"]
    local_dir_chirho = config_chirho["local_dir_chirho"]

    print(f"\n  Uploading {name_chirho} -> {repo_id_chirho}")

    if not local_dir_chirho.exists():
        print(f"    SKIP: {local_dir_chirho} does not exist")
        return False

    # Create repo if needed
    repo_type_chirho = "dataset" if name_chirho == "dataset" else "model"
    try:
        create_repo(
            repo_id_chirho,
            token=HF_TOKEN_CHIRHO,
            repo_type=repo_type_chirho,
            exist_ok=True,
            private=False,
        )
    except Exception as e_chirho:
        print(f"    Warning creating repo: {e_chirho}")

    # Upload
    api_chirho.upload_folder(
        folder_path=str(local_dir_chirho),
        repo_id=repo_id_chirho,
        repo_type=repo_type_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message=f"Upload {name_chirho} for Model 9: Evangelism & Apologetics",
    )

    print(f"    Done: https://huggingface.co/{repo_id_chirho}")
    return True


def main_chirho():
    """Upload all Model 9 components to HuggingFace."""
    print("=" * 60)
    print("Model 9: Upload to HuggingFace")
    print("=" * 60)

    if not HF_TOKEN_CHIRHO:
        # Try loading from .env
        env_path_chirho = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/.env")
        if env_path_chirho.exists():
            with open(env_path_chirho) as f_chirho:
                for line_chirho in f_chirho:
                    if line_chirho.startswith("HF_TOKEN_CHIRHO="):
                        token_chirho = line_chirho.strip().split("=", 1)[1].strip('"').strip("'")
                        os.environ["HF_TOKEN_CHIRHO"] = token_chirho
                        globals()["HF_TOKEN_CHIRHO"] = token_chirho
                        break

    api_chirho = HfApi()

    uploaded_chirho = 0
    for name_chirho, config_chirho in REPOS_CHIRHO.items():
        success_chirho = upload_component_chirho(name_chirho, config_chirho, api_chirho)
        if success_chirho:
            uploaded_chirho += 1
            log_progress_chirho(
                f"Uploaded {name_chirho} to HuggingFace",
                f"Repo: {config_chirho['repo_id_chirho']}",
                f"Successfully uploaded from {config_chirho['local_dir_chirho']}",
            )

    print(f"\n{'=' * 60}")
    print(f"Upload complete: {uploaded_chirho}/{len(REPOS_CHIRHO)} components")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
