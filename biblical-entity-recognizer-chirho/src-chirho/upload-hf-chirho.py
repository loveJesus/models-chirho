# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
upload-hf-chirho.py
Upload the trained Biblical Entity Recognizer model and dataset to HuggingFace Hub.
Repos: LoveJesus/biblical-entity-recognizer-chirho
       LoveJesus/biblical-ner-dataset-chirho
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
MODELS_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "ner-chirho"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"


def upload_model_chirho(api_chirho: HfApi):
    """Upload DistilBERT NER model to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/biblical-entity-recognizer-chirho"
    model_path_chirho = MODELS_DIR_CHIRHO / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Model not found at {model_path_chirho}, skipping.")
        return

    print(f"\nUploading NER model to {repo_id_chirho}...")
    create_repo(repo_id_chirho, token=HF_TOKEN_CHIRHO, exist_ok=True, repo_type="model")

    # Upload model files
    api_chirho.upload_folder(
        folder_path=str(model_path_chirho),
        repo_id=repo_id_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message="Upload DistilBERT biblical entity recognizer (NER)",
    )

    # Create and upload model card
    model_card_chirho = f"""---
language: en
license: mit
tags:
  - token-classification
  - ner
  - bible
  - biblical
  - named-entity-recognition
  - distilbert
datasets:
  - {HF_USER_CHIRHO}/biblical-ner-dataset-chirho
pipeline_tag: token-classification
---

# Biblical Entity Recognizer (Chirho)

A DistilBERT-based Named Entity Recognition model fine-tuned on KJV Bible text
to recognize six types of biblical entities.

## Entity Types

| Tag | Description | Example |
|-----|-------------|---------|
| PERSON | Biblical persons | Moses, David, Paul |
| DIVINE | Names/titles of God | God, LORD, Jesus Christ, Holy Spirit |
| PEOPLE_GROUP | Nations and groups | Israelites, Philistines, Pharisees |
| PLACE | Geographical locations | Jerusalem, Bethlehem, Egypt |
| EVENT | Biblical events/feasts | Passover, Pentecost, Sabbath |
| ARTIFACT | Sacred objects | Urim, Thummim |

## Usage

```python
from transformers import pipeline

ner_pipeline = pipeline(
    "token-classification",
    model="{repo_id_chirho}",
    aggregation_strategy="simple",
)

text = "And Moses said unto the LORD in the land of Egypt"
entities = ner_pipeline(text)
for entity in entities:
    print(f"{{entity['word']}}: {{entity['entity_group']}} ({{entity['score']:.3f}})")
```

## Training

- **Base model**: distilbert-base-uncased
- **Dataset**: ~31,000 KJV verses with BIO-tagged entities
- **Entity sources**: STEPBible TIPNR + curated divine names
- **Split**: 80/10/10 by book (not verse) to prevent data leakage
- **Framework**: HuggingFace Transformers

## License

MIT

For God so loved the world that he gave his only begotten Son,
that whoever believes in him should not perish but have eternal life. - John 3:16
"""

    # Write model card locally then upload
    card_path_chirho = model_path_chirho / "README.md"
    with open(card_path_chirho, "w") as f_chirho:
        f_chirho.write(model_card_chirho)

    api_chirho.upload_file(
        path_or_fileobj=str(card_path_chirho),
        path_in_repo="README.md",
        repo_id=repo_id_chirho,
        token=HF_TOKEN_CHIRHO,
        commit_message="Add model card",
    )

    print(f"  Model uploaded: https://huggingface.co/{repo_id_chirho}")


def upload_dataset_chirho(api_chirho: HfApi):
    """Upload NER dataset to HuggingFace."""
    repo_id_chirho = f"{HF_USER_CHIRHO}/biblical-ner-dataset-chirho"

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
            print(f"  Uploaded {split_chirho}")

    # Upload metadata
    metadata_path_chirho = DATA_DIR_CHIRHO / "metadata-chirho.json"
    if metadata_path_chirho.exists():
        api_chirho.upload_file(
            path_or_fileobj=str(metadata_path_chirho),
            path_in_repo="data/metadata-chirho.json",
            repo_id=repo_id_chirho,
            repo_type="dataset",
            token=HF_TOKEN_CHIRHO,
            commit_message="Upload dataset metadata",
        )

    # Dataset card
    dataset_card_chirho = f"""---
language: en
license: cc-by-4.0
tags:
  - ner
  - bible
  - biblical
  - named-entity-recognition
  - token-classification
task_categories:
  - token-classification
---

# Biblical NER Dataset (Chirho)

BIO-tagged Named Entity Recognition dataset built from the King James Version (KJV)
Bible text with entity annotations from STEPBible TIPNR data and curated divine name lists.

## Format

JSONL with fields:
- `tokens_chirho`: List of word tokens
- `ner_tags_chirho`: List of BIO tags (one per token)
- `reference_chirho`: Bible verse reference

## Entity Types

- **PERSON**: Biblical persons (Moses, David, Paul, etc.)
- **DIVINE**: Names and titles of God (God, LORD, Jesus Christ, Holy Spirit, etc.)
- **PEOPLE_GROUP**: Nations and ethnic groups (Israelites, Philistines, etc.)
- **PLACE**: Geographical locations (Jerusalem, Egypt, Bethlehem, etc.)
- **EVENT**: Biblical events and feasts (Passover, Pentecost, Sabbath, etc.)
- **ARTIFACT**: Sacred objects (Urim, Thummim, etc.)

## Labels (BIO scheme)

O, B-PERSON, I-PERSON, B-DIVINE, I-DIVINE, B-PEOPLE_GROUP, I-PEOPLE_GROUP,
B-PLACE, I-PLACE, B-EVENT, I-EVENT, B-ARTIFACT, I-ARTIFACT

## Split Strategy

Split 80/10/10 by **book** (not by verse) to prevent data leakage.

## Sources

- **Text**: King James Version from ScrollMapper bible_databases (Public Domain)
- **Entities**: STEPBible TIPNR (CC BY) + curated divine names list

For God so loved the world that he gave his only begotten Son,
that whoever believes in him should not perish but have eternal life. - John 3:16
"""

    card_path_chirho = DATA_DIR_CHIRHO / "README.md"
    with open(card_path_chirho, "w") as f_chirho:
        f_chirho.write(dataset_card_chirho)

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
    print("HuggingFace Upload - Biblical Entity Recognizer")
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
    print(f"  Model: https://huggingface.co/{HF_USER_CHIRHO}/biblical-entity-recognizer-chirho")
    print(f"  Dataset: https://huggingface.co/datasets/{HF_USER_CHIRHO}/biblical-ner-dataset-chirho")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
