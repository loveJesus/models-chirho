# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
download-gotquestions-chirho.py

Downloads the GotQuestions.org Bible Q&A dataset from HuggingFace
(vericudebuget/Bible-responses-dataset-gotquestions) and structures
each Q&A pair into JSONL format for the evangelism-apologetics pipeline.
"""

import json
import re
import statistics
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DATASET_ID_CHIRHO = "vericudebuget/Bible-responses-dataset-gotquestions"
SOURCE_CHIRHO = "GotQuestions.org"
CATEGORY_CHIRHO = "apologetics_qa"

OUTPUT_DIR_CHIRHO = Path(
    "/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/"
    "models-chirho/evangelism-apologetics-chirho/data-chirho/"
    "raw-chirho/apologetics-chirho"
)
OUTPUT_FILE_CHIRHO = OUTPUT_DIR_CHIRHO / "gotquestions-chirho.jsonl"

PROGRESS_DB_CHIRHO = Path(
    "/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/"
    "models-chirho/spec-chirho/progress-chirho.sqlite"
)

AGENT_CODE_CHIRHO = "opus-download-gq-chirho"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def clean_response_chirho(raw_text_chirho: str) -> str:
    """Strip residual HTML tags and normalise whitespace from a response."""
    # Remove HTML tags
    cleaned_chirho = re.sub(r"<[^>]+>", "", raw_text_chirho)
    # Collapse multiple whitespace / newlines into single spaces
    cleaned_chirho = re.sub(r"\s+", " ", cleaned_chirho).strip()
    return cleaned_chirho


def slug_from_question_chirho(question_chirho: str) -> str:
    """Derive a GotQuestions.org-style URL slug from the question text."""
    slug_chirho = question_chirho.lower().strip().rstrip("?").strip()
    slug_chirho = re.sub(r"[^a-z0-9\s-]", "", slug_chirho)
    slug_chirho = re.sub(r"\s+", "-", slug_chirho)
    return f"https://www.gotquestions.org/{slug_chirho}.html"


def log_progress_chirho(
    action_chirho: str,
    result_chirho: str,
    overview_chirho: str,
    timestamp_start_chirho: str | None = None,
) -> None:
    """Insert a row into the progress-chirho.sqlite log table."""
    import sqlite3

    timestamp_end_chirho = time.strftime("%Y-%m-%d %H:%M:%S")
    if timestamp_start_chirho is None:
        timestamp_start_chirho = timestamp_end_chirho

    conn_chirho = sqlite3.connect(str(PROGRESS_DB_CHIRHO))
    cur_chirho = conn_chirho.cursor()
    cur_chirho.execute(
        """
        INSERT INTO steps_taken_chirho (
            agent_code_chirho,
            timestamp_start_chirho,
            timestamp_end_chirho,
            action_taken_chirho,
            result_of_action_chirho,
            overview_of_result_chirho
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            AGENT_CODE_CHIRHO,
            timestamp_start_chirho,
            timestamp_end_chirho,
            action_chirho,
            result_chirho,
            overview_chirho,
        ),
    )
    conn_chirho.commit()
    conn_chirho.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main_chirho() -> None:
    timestamp_start_chirho = time.strftime("%Y-%m-%d %H:%M:%S")

    # --- 1. Download dataset from HuggingFace ---
    print(f"[*] Loading dataset: {DATASET_ID_CHIRHO}")
    try:
        from datasets import load_dataset
    except ImportError:
        print(
            "[!] 'datasets' library not installed. "
            "Run: pip install datasets",
            file=sys.stderr,
        )
        sys.exit(1)

    dataset_chirho = load_dataset(DATASET_ID_CHIRHO, split="train")
    total_raw_chirho = len(dataset_chirho)
    print(f"[*] Downloaded {total_raw_chirho} raw entries")

    # --- 2. Structure into JSONL records ---
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    records_written_chirho = 0
    answer_lengths_chirho: list[int] = []
    skipped_chirho = 0

    with open(OUTPUT_FILE_CHIRHO, "w", encoding="utf-8") as fout_chirho:
        for idx_chirho, row_chirho in enumerate(dataset_chirho):
            question_chirho = (row_chirho.get("prompt") or "").strip()
            raw_answer_chirho = row_chirho.get("response") or ""
            answer_chirho = clean_response_chirho(raw_answer_chirho)

            # Skip entries with empty question or trivially short answer
            if not question_chirho or len(answer_chirho) < 20:
                skipped_chirho += 1
                continue

            url_chirho = slug_from_question_chirho(question_chirho)

            record_chirho = {
                "question_chirho": question_chirho,
                "answer_chirho": answer_chirho,
                "source_chirho": SOURCE_CHIRHO,
                "category_chirho": CATEGORY_CHIRHO,
                "url_chirho": url_chirho,
            }

            fout_chirho.write(json.dumps(record_chirho, ensure_ascii=False) + "\n")
            answer_lengths_chirho.append(len(answer_chirho))
            records_written_chirho += 1

    # --- 3. Print statistics ---
    print()
    print("=" * 60)
    print("  GotQuestions Download Complete")
    print("=" * 60)
    print(f"  Raw entries downloaded:     {total_raw_chirho}")
    print(f"  Records written to JSONL:   {records_written_chirho}")
    print(f"  Skipped (empty/too short):  {skipped_chirho}")
    print()

    if answer_lengths_chirho:
        avg_len_chirho = statistics.mean(answer_lengths_chirho)
        median_len_chirho = statistics.median(answer_lengths_chirho)
        min_len_chirho = min(answer_lengths_chirho)
        max_len_chirho = max(answer_lengths_chirho)
        print(f"  Avg answer length (chars):  {avg_len_chirho:,.1f}")
        print(f"  Median answer length:       {median_len_chirho:,.1f}")
        print(f"  Min answer length:          {min_len_chirho:,}")
        print(f"  Max answer length:          {max_len_chirho:,}")
    print()
    print(f"  Output file: {OUTPUT_FILE_CHIRHO}")
    print("=" * 60)

    # --- 4. Log to progress DB ---
    try:
        log_progress_chirho(
            action_chirho=(
                f"Downloaded GotQuestions dataset ({DATASET_ID_CHIRHO}) "
                f"from HuggingFace and converted to JSONL"
            ),
            result_chirho=(
                f"Wrote {records_written_chirho} Q&A pairs to "
                f"{OUTPUT_FILE_CHIRHO} (skipped {skipped_chirho}). "
                f"Avg answer length: {avg_len_chirho:,.1f} chars."
            ),
            overview_chirho=(
                "Successfully downloaded and structured the GotQuestions "
                "apologetics Q&A dataset. Data is ready for the "
                "evangelism-apologetics pipeline. HTML tags cleaned, "
                "whitespace normalised, URL slugs derived from questions."
            ),
            timestamp_start_chirho=timestamp_start_chirho,
        )
        print("[*] Progress logged to spec-chirho/progress-chirho.sqlite")
    except Exception as err_chirho:
        print(f"[!] Could not log progress: {err_chirho}", file=sys.stderr)


if __name__ == "__main__":
    main_chirho()
