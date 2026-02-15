# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
download-spurgeon-chirho.py

Downloads Charles Spurgeon's complete public-domain sermons (3,561 sermons,
1855-1917) from CCEL (Christian Classics Ethereal Library) plain-text volumes
(sermons01 through sermons63).  Parses each volume into individual sermons
and writes structured JSONL.

All content is public domain (published 1855-1917).
"""

import json
import re
import sqlite3
import sys
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TOTAL_VOLUMES_CHIRHO = 63
CCEL_URL_PATTERN_CHIRHO = (
    "https://www.ccel.org/ccel/s/spurgeon/sermons{vol:02d}/cache/sermons{vol:02d}.txt"
)

USER_AGENT_CHIRHO = (
    "BibleMLModels/1.0 (Academic Research; contact: LoveJesus on HuggingFace)"
)

SOURCE_CHIRHO = "spurgeon_ccel"
CATEGORY_CHIRHO = "sermon"
AUTHOR_CHIRHO = "Charles Haddon Spurgeon"

# Output path relative to this script's location:
#   script is at: .../src-chirho/data-chirho/download-spurgeon-chirho.py
#   output goes to: .../data-chirho/raw-chirho/sermons-chirho/spurgeon-sermons-chirho.jsonl
# That is  ../../data-chirho/raw-chirho/sermons-chirho/ from __file__
SCRIPT_DIR_CHIRHO = Path(__file__).resolve().parent
OUTPUT_DIR_CHIRHO = (
    SCRIPT_DIR_CHIRHO / ".." / ".." / "data-chirho" / "raw-chirho" / "sermons-chirho"
).resolve()
OUTPUT_FILE_CHIRHO = OUTPUT_DIR_CHIRHO / "spurgeon-sermons-chirho.jsonl"

PROGRESS_DB_CHIRHO = (
    SCRIPT_DIR_CHIRHO / ".." / ".." / ".." / "spec-chirho" / "progress-chirho.sqlite"
).resolve()

AGENT_CODE_CHIRHO = "opus-download-spurgeon-chirho"

REQUEST_DELAY_CHIRHO = 2  # seconds between volume downloads (respectful rate limit)
RETRY_DELAY_CHIRHO = 5    # seconds before retrying a failed download
REQUEST_TIMEOUT_CHIRHO = 60  # seconds per HTTP request

# Regex patterns for parsing sermon headers
# IMPORTANT: re.MULTILINE is required so ^ and $ match per-line in split()
SEPARATOR_RE_CHIRHO = re.compile(r"^\s*_{40,}\s*$", re.MULTILINE)
SERMON_NO_RE_CHIRHO = re.compile(r"\(No\.\s*(\d[\d,]*)\)", re.IGNORECASE)
DATE_RE_CHIRHO = re.compile(
    r"Delivered\s+on\s+.*?,\s*(.*?\d{4})",
    re.IGNORECASE,
)
# Match scripture references like: "verse text"--Book Chapter:Verse
SCRIPTURE_RE_CHIRHO = re.compile(
    r'"[^"]*"--(.+?)$', re.MULTILINE
)
# Alternate format: "verse text."--Book Chapter:Verse  (em-dash or en-dash)
SCRIPTURE_ALT_RE_CHIRHO = re.compile(
    r'"[^"]*"[—–-]{1,2}(.+?)$', re.MULTILINE
)
# Location patterns
LOCATION_RE_CHIRHO = re.compile(
    r"(?:At|at)\s+(.+?)(?:\.\s*$|\s*$)", re.MULTILINE
)

# Bible book names for scripture-reference heuristic
BIBLE_BOOKS_RE_CHIRHO = re.compile(
    r"(Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|"
    r"Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|Psalm|Psalms|Proverbs|"
    r"Ecclesiastes|Song|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|"
    r"Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|"
    r"Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|"
    r"Corinthians|Galatians|Ephesians|Philippians|Colossians|"
    r"Thessalonians|Timothy|Titus|Philemon|Hebrews|James|Peter|"
    r"Jude|Revelation)\s+\d+",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Progress logging
# ---------------------------------------------------------------------------
def log_progress_chirho(
    action_chirho: str,
    result_chirho: str,
    overview_chirho: str,
    timestamp_start_chirho: str | None = None,
) -> None:
    """Insert a row into the progress-chirho.sqlite log table."""
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
# CCEL download
# ---------------------------------------------------------------------------
def download_volume_chirho(volume_number_chirho: int) -> str | None:
    """
    Download a single CCEL volume's plain text.

    Retries once after RETRY_DELAY_CHIRHO seconds if the first attempt fails.
    Returns the text content or None on failure.
    """
    url_chirho = CCEL_URL_PATTERN_CHIRHO.format(vol=volume_number_chirho)
    headers_chirho = {"User-Agent": USER_AGENT_CHIRHO}

    for attempt_chirho in range(2):  # attempt 0 = first try, attempt 1 = retry
        try:
            response_chirho = requests.get(
                url_chirho,
                timeout=REQUEST_TIMEOUT_CHIRHO,
                headers=headers_chirho,
            )
            if response_chirho.status_code == 200:
                return response_chirho.text
            else:
                print(
                    f"  [!] Volume {volume_number_chirho:02d}: "
                    f"HTTP {response_chirho.status_code}"
                    f"{' (will retry)' if attempt_chirho == 0 else ''}"
                )
        except requests.RequestException as err_chirho:
            print(
                f"  [!] Volume {volume_number_chirho:02d}: {err_chirho}"
                f"{' (will retry)' if attempt_chirho == 0 else ''}"
            )

        # Retry once after a delay
        if attempt_chirho == 0:
            time.sleep(RETRY_DELAY_CHIRHO)

    return None


# ---------------------------------------------------------------------------
# Sermon parsing helpers
# ---------------------------------------------------------------------------
def extract_title_chirho(header_lines_chirho: list[str]) -> str:
    """
    Extract the sermon title from header lines.

    The title is typically the first substantial non-blank, non-metadata line,
    or the line immediately before "A Sermon".
    """
    # First strategy: find the line just before "A Sermon"
    for i_chirho, line_chirho in enumerate(header_lines_chirho[:30]):
        stripped_chirho = line_chirho.strip()
        if stripped_chirho.lower() == "a sermon":
            # Walk backwards to find the title line(s)
            for j_chirho in range(i_chirho - 1, -1, -1):
                candidate_chirho = header_lines_chirho[j_chirho].strip()
                if candidate_chirho and len(candidate_chirho) > 2:
                    return candidate_chirho
            break

    # Second strategy: first non-empty, non-metadata line
    for line_chirho in header_lines_chirho:
        stripped_chirho = line_chirho.strip()
        if not stripped_chirho:
            continue
        if SEPARATOR_RE_CHIRHO.match(line_chirho):
            continue
        if stripped_chirho.lower().startswith(
            ("title:", "creator", "ccel", "lc ", "practical theology", "worship",
             "times and seasons")
        ):
            continue
        if len(stripped_chirho) > 2 and not stripped_chirho.startswith("("):
            return stripped_chirho

    return "Unknown Sermon"


def extract_location_chirho(header_text_chirho: str) -> str:
    """Extract the location/chapel from the sermon header."""
    location_match_chirho = LOCATION_RE_CHIRHO.search(header_text_chirho)
    if location_match_chirho:
        location_chirho = location_match_chirho.group(1).strip().rstrip(".")
        # Clean up common artifacts
        location_chirho = re.sub(r"\s+", " ", location_chirho)
        return location_chirho

    # Fallback: look for known chapel names
    header_lower_chirho = header_text_chirho.lower()
    if "new park street chapel" in header_lower_chirho:
        return "New Park Street Chapel, Southwark"
    elif "metropolitan tabernacle" in header_lower_chirho:
        return "Metropolitan Tabernacle, Newington"
    elif "exeter hall" in header_lower_chirho:
        return "Exeter Hall, Strand"

    return ""


def parse_volume_chirho(
    raw_text_chirho: str, volume_number_chirho: int
) -> list[dict]:
    """Parse a CCEL volume plain-text file into individual sermon dicts."""
    sermons_chirho: list[dict] = []

    # Split on the underscore separator lines
    sections_chirho = SEPARATOR_RE_CHIRHO.split(raw_text_chirho)

    for section_chirho in sections_chirho:
        # Skip very short sections (headers, footers, empty)
        if len(section_chirho.strip()) < 200:
            continue

        # Check if this looks like a sermon (has "No. X" pattern)
        sermon_no_match_chirho = SERMON_NO_RE_CHIRHO.search(section_chirho[:1500])
        if not sermon_no_match_chirho:
            # Could still be a sermon without the number pattern in some volumes
            if not (
                "a sermon" in section_chirho[:1500].lower()
                or "delivered on" in section_chirho[:1500].lower()
            ):
                continue

        # Extract sermon number
        sermon_number_chirho = 0
        if sermon_no_match_chirho:
            # Handle numbers with commas like "1,000"
            raw_num_chirho = sermon_no_match_chirho.group(1).replace(",", "")
            try:
                sermon_number_chirho = int(raw_num_chirho)
            except ValueError:
                sermon_number_chirho = 0

        # Split into header and body
        lines_chirho = section_chirho.split("\n")

        # Find where the actual body text begins (after the header metadata)
        # The header typically ends after the scripture reference line(s).
        # Scripture references may wrap across 2-3 lines, e.g.:
        #   "Take heed lest
        #    he fall."--1 Corinthians
        #    10:12
        header_end_idx_chirho = 0
        found_scripture_chirho = False

        for i_chirho, line_chirho in enumerate(lines_chirho[:60]):
            # Look for scripture reference pattern (line with "--" or em-dash
            # after a quote)
            if (
                ('--' in line_chirho or '\u2014' in line_chirho
                 or '\u2013' in line_chirho)
                and '"' in line_chirho
            ):
                # The reference might continue onto the next line(s)
                # Check if next lines are continuations (short, with chapter:verse)
                end_chirho = i_chirho + 1
                for k_chirho in range(i_chirho + 1, min(i_chirho + 4, len(lines_chirho))):
                    next_stripped_chirho = lines_chirho[k_chirho].strip()
                    # Continuation lines are typically short and contain
                    # chapter:verse numbers or Bible book names
                    if next_stripped_chirho and len(next_stripped_chirho) < 40:
                        if (re.match(r"^\d+", next_stripped_chirho)
                                or BIBLE_BOOKS_RE_CHIRHO.search(next_stripped_chirho)):
                            end_chirho = k_chirho + 1
                        else:
                            break
                    elif not next_stripped_chirho:
                        # Blank line after the reference -- include it
                        end_chirho = k_chirho + 1
                        break
                    else:
                        break
                header_end_idx_chirho = end_chirho
                found_scripture_chirho = True
                break

            # Also check for lines that contain a Bible book reference
            # (some headers don't have the "--" on the same line as the quote)
            if BIBLE_BOOKS_RE_CHIRHO.search(line_chirho):
                # Check if next line has the chapter:verse continuation
                end_chirho = i_chirho + 1
                for k_chirho in range(i_chirho + 1, min(i_chirho + 3, len(lines_chirho))):
                    next_stripped_chirho = lines_chirho[k_chirho].strip()
                    if next_stripped_chirho and re.match(r"^\d+", next_stripped_chirho) and len(next_stripped_chirho) < 30:
                        end_chirho = k_chirho + 1
                    elif not next_stripped_chirho:
                        end_chirho = k_chirho + 1
                        break
                    else:
                        break
                header_end_idx_chirho = end_chirho
                found_scripture_chirho = True
                break

        if not found_scripture_chirho:
            # Fallback: header is about the first 20 lines
            header_end_idx_chirho = min(20, len(lines_chirho))

        header_text_chirho = "\n".join(lines_chirho[:header_end_idx_chirho])
        body_text_chirho = "\n".join(lines_chirho[header_end_idx_chirho:]).strip()

        # Extract title
        title_chirho = extract_title_chirho(lines_chirho[:header_end_idx_chirho])

        # Extract scripture reference
        # Join header lines into a single string to handle wrapped references
        # e.g. "Take heed lest\n   he fall."--1 Corinthians\n   10:12
        header_joined_chirho = re.sub(r"\s*\n\s*", " ", header_text_chirho)
        scripture_reference_chirho = ""
        # Pattern: "quoted text"--BookName Chapter:Verse
        scripture_joined_match_chirho = re.search(
            r'"[^"]*"\s*--\s*(.+?)(?:\s*$)',
            header_joined_chirho,
        )
        if not scripture_joined_match_chirho:
            # Try em-dash / en-dash variants
            scripture_joined_match_chirho = re.search(
                r'"[^"]*"\s*[—–]\s*(.+?)(?:\s*$)',
                header_joined_chirho,
            )
        if scripture_joined_match_chirho:
            scripture_reference_chirho = scripture_joined_match_chirho.group(1).strip()
            # Clean trailing periods/whitespace
            scripture_reference_chirho = scripture_reference_chirho.rstrip(". ")
        else:
            # Fallback: look for Bible book references in the header
            bible_ref_match_chirho = BIBLE_BOOKS_RE_CHIRHO.search(header_joined_chirho)
            if bible_ref_match_chirho:
                # Grab from the match to the end of that phrase
                start_pos_chirho = bible_ref_match_chirho.start()
                # Extract a reasonable reference string
                ref_candidate_chirho = header_joined_chirho[start_pos_chirho:start_pos_chirho + 80]
                # Trim to just the reference (book + chapter:verse pattern)
                ref_clean_chirho = re.match(
                    r"(\d?\s*[A-Za-z]+\s+\d+(?::\d+(?:-\d+)?)?)",
                    ref_candidate_chirho,
                )
                if ref_clean_chirho:
                    scripture_reference_chirho = ref_clean_chirho.group(1).strip()

        # Extract date
        date_chirho = ""
        date_match_chirho = DATE_RE_CHIRHO.search(header_text_chirho)
        if date_match_chirho:
            date_chirho = date_match_chirho.group(1).strip().rstrip(",. ")

        # Extract location
        location_chirho = extract_location_chirho(header_text_chirho)

        # Clean the body text - remove excessive whitespace but keep paragraphs
        body_text_chirho = re.sub(r"[ \t]+", " ", body_text_chirho)
        body_text_chirho = re.sub(r"\n{3,}", "\n\n", body_text_chirho)
        body_text_chirho = body_text_chirho.strip()

        # Skip if body is too short to be a real sermon
        if len(body_text_chirho) < 500:
            continue

        sermon_record_chirho = {
            "source_chirho": SOURCE_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
            "title_chirho": title_chirho,
            "sermon_number_chirho": sermon_number_chirho,
            "date_chirho": date_chirho,
            "location_chirho": location_chirho,
            "scripture_reference_chirho": scripture_reference_chirho,
            "text_chirho": body_text_chirho,
            "volume_chirho": volume_number_chirho,
            "author_chirho": AUTHOR_CHIRHO,
        }
        sermons_chirho.append(sermon_record_chirho)

    return sermons_chirho


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main_chirho() -> None:
    timestamp_start_chirho = time.strftime("%Y-%m-%d %H:%M:%S")

    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    all_sermons_chirho: list[dict] = []
    volumes_downloaded_chirho = 0
    failed_volumes_chirho: list[int] = []

    # -------------------------------------------------------------------
    # Phase 1: Download all 63 volumes from CCEL
    # -------------------------------------------------------------------
    print("=" * 70)
    print("  Spurgeon Sermon Downloader")
    print("  Source: CCEL (Christian Classics Ethereal Library)")
    print(f"  Volumes: 1-{TOTAL_VOLUMES_CHIRHO} (1855-1917)")
    print(f"  User-Agent: {USER_AGENT_CHIRHO}")
    print("=" * 70)
    print()

    for vol_chirho in range(1, TOTAL_VOLUMES_CHIRHO + 1):
        print(
            f"[*] Downloading volume {vol_chirho:02d}/{TOTAL_VOLUMES_CHIRHO}...",
            end=" ",
            flush=True,
        )

        raw_text_chirho = download_volume_chirho(vol_chirho)

        if raw_text_chirho is None:
            print("FAILED (after retry)")
            failed_volumes_chirho.append(vol_chirho)
        else:
            sermons_in_vol_chirho = parse_volume_chirho(raw_text_chirho, vol_chirho)
            all_sermons_chirho.extend(sermons_in_vol_chirho)
            volumes_downloaded_chirho += 1
            print(f"OK ({len(sermons_in_vol_chirho)} sermons parsed)")

        # Rate limiting: be respectful of CCEL servers
        if vol_chirho < TOTAL_VOLUMES_CHIRHO:
            time.sleep(REQUEST_DELAY_CHIRHO)

    # -------------------------------------------------------------------
    # Phase 2: Deduplicate by (volume, sermon_number, title)
    # -------------------------------------------------------------------
    seen_keys_chirho: set[str] = set()
    unique_sermons_chirho: list[dict] = []
    for sermon_chirho in all_sermons_chirho:
        key_chirho = (
            f"{sermon_chirho['volume_chirho']}-"
            f"{sermon_chirho['sermon_number_chirho']}-"
            f"{sermon_chirho['title_chirho']}"
        )
        if key_chirho not in seen_keys_chirho:
            seen_keys_chirho.add(key_chirho)
            unique_sermons_chirho.append(sermon_chirho)

    # -------------------------------------------------------------------
    # Phase 3: Write JSONL output
    # -------------------------------------------------------------------
    with open(OUTPUT_FILE_CHIRHO, "w", encoding="utf-8") as fout_chirho:
        for sermon_chirho in unique_sermons_chirho:
            fout_chirho.write(
                json.dumps(sermon_chirho, ensure_ascii=False) + "\n"
            )

    total_written_chirho = len(unique_sermons_chirho)

    # -------------------------------------------------------------------
    # Phase 4: Print summary
    # -------------------------------------------------------------------
    print()
    print("=" * 70)
    print("  Spurgeon Sermon Download Complete")
    print("=" * 70)
    print(f"  Volumes downloaded:           {volumes_downloaded_chirho}/{TOTAL_VOLUMES_CHIRHO}")
    print(f"  Total sermons extracted:      {total_written_chirho}")
    print()

    if failed_volumes_chirho:
        print(f"  Failed volumes ({len(failed_volumes_chirho)}):")
        # Format as comma-separated list, wrapped at ~60 chars
        vol_strs_chirho = [str(v_chirho) for v_chirho in failed_volumes_chirho]
        line_chirho = "    "
        for vs_chirho in vol_strs_chirho:
            if len(line_chirho) + len(vs_chirho) + 2 > 70:
                print(line_chirho.rstrip(", "))
                line_chirho = "    "
            line_chirho += vs_chirho + ", "
        if line_chirho.strip():
            print(line_chirho.rstrip(", "))
        print()
    else:
        print("  Failed volumes:               None")
        print()

    if unique_sermons_chirho:
        text_lengths_chirho = [
            len(s_chirho["text_chirho"]) for s_chirho in unique_sermons_chirho
        ]
        total_chars_chirho = sum(text_lengths_chirho)
        avg_len_chirho = total_chars_chirho / len(text_lengths_chirho)
        min_len_chirho = min(text_lengths_chirho)
        max_len_chirho = max(text_lengths_chirho)
        print(f"  Total text (chars):           {total_chars_chirho:,}")
        print(f"  Avg sermon length (chars):    {avg_len_chirho:,.1f}")
        print(f"  Min sermon length:            {min_len_chirho:,}")
        print(f"  Max sermon length:            {max_len_chirho:,}")
        print()

    print(f"  Output file: {OUTPUT_FILE_CHIRHO}")
    print("=" * 70)

    # -------------------------------------------------------------------
    # Phase 5: Log to progress DB
    # -------------------------------------------------------------------
    try:
        log_progress_chirho(
            action_chirho=(
                f"Downloaded Spurgeon sermons from CCEL (volumes 1-{TOTAL_VOLUMES_CHIRHO}). "
                f"Parsed and wrote JSONL."
            ),
            result_chirho=(
                f"Wrote {total_written_chirho} sermons to {OUTPUT_FILE_CHIRHO}. "
                f"Volumes downloaded: {volumes_downloaded_chirho}/{TOTAL_VOLUMES_CHIRHO}. "
                f"Failed volumes: {len(failed_volumes_chirho)}."
            ),
            overview_chirho=(
                f"Downloaded {volumes_downloaded_chirho} CCEL volumes and parsed "
                f"{total_written_chirho} individual sermons. "
                f"Data saved as JSONL for the evangelism-apologetics pipeline. "
                f"All content is public domain (published 1855-1917)."
            ),
            timestamp_start_chirho=timestamp_start_chirho,
        )
        print("[*] Progress logged to spec-chirho/progress-chirho.sqlite")
    except Exception as err_chirho:
        print(f"[!] Could not log progress: {err_chirho}", file=sys.stderr)


if __name__ == "__main__":
    main_chirho()
