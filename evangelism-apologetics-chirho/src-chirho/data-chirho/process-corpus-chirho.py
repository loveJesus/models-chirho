# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
Process and merge all raw corpus data into training-ready datasets for Model 9.

Components:
1. Intent Classifier: Labeled examples across 5 categories
2. Retriever: (query, passage) pairs for fine-tuning MiniLM-L12
3. Generator: Instruction-response pairs for Qwen3-4B LoRA fine-tuning

Input: raw-chirho/ subdirectories (evidence, fathers, miracles, sermons, dialogues, apologetics)
Output: processed-chirho/ training splits
"""

import json
import os
import random
import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────
BASE_DIR_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho")
RAW_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "raw-chirho"
PROCESSED_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
PROGRESS_DB_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/spec-chirho/progress-chirho.sqlite")
AGENT_CODE_CHIRHO = "process-corpus-chirho"
SEED_CHIRHO = 316  # John 3:16

INTENT_CATEGORIES_CHIRHO = [
    "evangelism_dialogue",
    "apologetics_qa",
    "creation_science",
    "historical_evidence",
    "miracle_testimony",
]


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
            action_chirho,
            result_chirho,
            overview_chirho,
        ))
        conn_chirho.commit()
        conn_chirho.close()
    except Exception as e_chirho:
        print(f"  Warning: Could not log progress: {e_chirho}")


def load_jsonl_chirho(filepath_chirho):
    """Load all entries from a JSONL file."""
    entries_chirho = []
    if not filepath_chirho.exists():
        return entries_chirho
    with open(filepath_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            line_chirho = line_chirho.strip()
            if line_chirho:
                try:
                    entries_chirho.append(json.loads(line_chirho))
                except json.JSONDecodeError:
                    continue
    return entries_chirho


def load_all_raw_chirho():
    """Load all raw corpus data from all subdirectories."""
    corpus_chirho = {
        "evidence_chirho": [],
        "fathers_chirho": [],
        "miracles_chirho": [],
        "sermons_chirho": [],
        "dialogues_chirho": [],
        "apologetics_chirho": [],
    }

    # Load evidence files
    evidence_dir_chirho = RAW_DIR_CHIRHO / "evidence-chirho"
    if evidence_dir_chirho.exists():
        for f_chirho in evidence_dir_chirho.glob("*.jsonl"):
            corpus_chirho["evidence_chirho"].extend(load_jsonl_chirho(f_chirho))

    # Load church fathers
    fathers_dir_chirho = RAW_DIR_CHIRHO / "fathers-chirho"
    if fathers_dir_chirho.exists():
        for f_chirho in fathers_dir_chirho.glob("*.jsonl"):
            corpus_chirho["fathers_chirho"].extend(load_jsonl_chirho(f_chirho))

    # Load miracle testimonies
    miracles_dir_chirho = RAW_DIR_CHIRHO / "miracles-chirho"
    if miracles_dir_chirho.exists():
        for f_chirho in miracles_dir_chirho.glob("*.jsonl"):
            corpus_chirho["miracles_chirho"].extend(load_jsonl_chirho(f_chirho))

    # Load sermons
    sermons_dir_chirho = RAW_DIR_CHIRHO / "sermons-chirho"
    if sermons_dir_chirho.exists():
        for f_chirho in sermons_dir_chirho.glob("*.jsonl"):
            corpus_chirho["sermons_chirho"].extend(load_jsonl_chirho(f_chirho))

    # Load dialogues
    dialogues_dir_chirho = RAW_DIR_CHIRHO / "dialogues-chirho"
    if dialogues_dir_chirho.exists():
        for f_chirho in dialogues_dir_chirho.glob("*.jsonl"):
            corpus_chirho["dialogues_chirho"].extend(load_jsonl_chirho(f_chirho))

    # Load apologetics Q&A
    apologetics_dir_chirho = RAW_DIR_CHIRHO / "apologetics-chirho"
    if apologetics_dir_chirho.exists():
        for f_chirho in apologetics_dir_chirho.glob("*.jsonl"):
            corpus_chirho["apologetics_chirho"].extend(load_jsonl_chirho(f_chirho))

    return corpus_chirho


CREATION_KEYWORDS_CHIRHO = [
    "evolution", "creationism", "creation ", "young earth", "old earth",
    "dinosaur", "fossil", "big bang", "age of the earth", "genesis 1",
    "days of creation", "flood", "noah's ark", "noah's flood",
    "intelligent design", "irreducible complexity", "fine-tuning",
    "carbon dating", "radiometric", "geolog", "cambrian", "missing link",
    "human origins", "adam and eve real", "origin of life",
    "theistic evolution", "gap theory", "day-age",
]

HISTORICAL_KEYWORDS_CHIRHO = [
    "manuscript", "dead sea scroll", "archaeology", "archaeolog",
    "historical jesus", "josephus", "tacitus", "pliny",
    "early church", "church father", "council of nicaea", "canon",
    "gnostic gospel", "textual criticism", "reliability of the bible",
    "bible been changed", "bible contradictions", "bible reliable",
    "eyewitness", "apostle", "martyrdom", "resurrection evidence",
    "empty tomb", "crusade", "inquisition", "reformation",
    "constantine", "apocrypha", "book of enoch",
]

MIRACLE_KEYWORDS_CHIRHO = [
    "miracle", "healing", "supernatural", "demon", "exorcism",
    "angel", "vision", "prophecy fulfilled", "prayer answered",
    "sign", "wonder", "raise", "raised from", "near-death",
    "tongue", "gift of the spirit", "cessationism", "continuationism",
]

EVANGELISM_KEYWORDS_CHIRHO = [
    "how to be saved", "what must i do to be saved", "plan of salvation",
    "share my faith", "share the gospel", "witnessing", "evangelis",
    "how to become a christian", "accept christ", "accept jesus",
    "born again", "repent", "what is the gospel", "get saved",
    "invite jesus", "sinner's prayer", "receive christ",
]


def _keyword_classify_chirho(text_chirho):
    """Classify by keywords in question/claim text."""
    text_lower_chirho = text_chirho.lower()

    for kw_chirho in EVANGELISM_KEYWORDS_CHIRHO:
        if kw_chirho in text_lower_chirho:
            return "evangelism_dialogue"

    for kw_chirho in CREATION_KEYWORDS_CHIRHO:
        if kw_chirho in text_lower_chirho:
            return "creation_science"

    for kw_chirho in HISTORICAL_KEYWORDS_CHIRHO:
        if kw_chirho in text_lower_chirho:
            return "historical_evidence"

    for kw_chirho in MIRACLE_KEYWORDS_CHIRHO:
        if kw_chirho in text_lower_chirho:
            return "miracle_testimony"

    return None


def classify_intent_chirho(entry_chirho, source_type_chirho):
    """Determine the intent category for an entry."""
    category_chirho = entry_chirho.get("category_chirho", "").lower()

    # Direct category mapping
    if source_type_chirho == "dialogues_chirho":
        return "evangelism_dialogue"

    if category_chirho in ("creation_science", "intelligent_design", "biology",
                           "geology", "radiometric", "cosmological", "human_origins",
                           "prophecy_fulfillment"):
        return "creation_science"

    if category_chirho in ("historical_evidence", "early_church_apologetics"):
        return "historical_evidence"

    if category_chirho in ("miracle_testimony", "health_faith"):
        return "miracle_testimony"

    # For generic apologetics_qa entries, try keyword-based classification
    # to redistribute into more specific categories
    if category_chirho == "apologetics_qa" or source_type_chirho == "apologetics_chirho":
        text_chirho = entry_chirho.get("question_chirho", "")
        if not text_chirho:
            text_chirho = entry_chirho.get("claim_chirho", "")
        if text_chirho:
            kw_intent_chirho = _keyword_classify_chirho(text_chirho)
            if kw_intent_chirho:
                return kw_intent_chirho

    if category_chirho in ("apologetics_qa", "existence_of_god", "jesus_christ",
                           "bible_reliability", "problem_of_evil", "science_faith",
                           "world_religions", "heaven_hell", "christian_living",
                           "common_objections", "ethics", "church_history",
                           "modern_challenges", "sermon"):
        return "apologetics_qa"

    if source_type_chirho == "evidence_chirho":
        return "creation_science"
    if source_type_chirho == "fathers_chirho":
        return "historical_evidence"
    if source_type_chirho == "miracles_chirho":
        return "miracle_testimony"
    if source_type_chirho in ("apologetics_chirho", "sermons_chirho"):
        return "apologetics_qa"

    return "apologetics_qa"  # default


def build_intent_classifier_data_chirho(corpus_chirho):
    """Build labeled data for the intent classifier (RoBERTa-base)."""
    print("\n━━━ Building Intent Classifier Data ━━━")
    examples_chirho = []

    for source_type_chirho, entries_chirho in corpus_chirho.items():
        for entry_chirho in entries_chirho:
            intent_chirho = classify_intent_chirho(entry_chirho, source_type_chirho)

            # Extract text to classify
            text_chirho = ""
            if "question_chirho" in entry_chirho:
                text_chirho = entry_chirho["question_chirho"]
            elif "claim_chirho" in entry_chirho:
                text_chirho = entry_chirho["claim_chirho"]
            elif "argument_chirho" in entry_chirho:
                text_chirho = entry_chirho["argument_chirho"]
            elif "title_chirho" in entry_chirho:
                text_chirho = entry_chirho["title_chirho"]
            elif "topic_chirho" in entry_chirho:
                text_chirho = entry_chirho.get("question_chirho", entry_chirho.get("topic_chirho", ""))

            # For dialogues, use the first seeker turn
            if source_type_chirho == "dialogues_chirho" and "turns_chirho" in entry_chirho:
                turns_chirho = entry_chirho["turns_chirho"]
                seeker_turns_chirho = [t_chirho for t_chirho in turns_chirho
                                       if t_chirho.get("role_chirho") == "seeker"]
                if seeker_turns_chirho:
                    text_chirho = seeker_turns_chirho[0].get("text_chirho", "")

            if text_chirho and len(text_chirho) > 10:
                examples_chirho.append({
                    "text_chirho": text_chirho.strip(),
                    "label_chirho": intent_chirho,
                })

    # Deduplicate by text hash
    seen_chirho = set()
    unique_chirho = []
    for ex_chirho in examples_chirho:
        hash_chirho = hashlib.md5(ex_chirho["text_chirho"].encode()).hexdigest()
        if hash_chirho not in seen_chirho:
            seen_chirho.add(hash_chirho)
            unique_chirho.append(ex_chirho)

    # Print distribution
    from collections import Counter
    dist_chirho = Counter(ex_chirho["label_chirho"] for ex_chirho in unique_chirho)
    print(f"  Total unique examples: {len(unique_chirho)}")
    for label_chirho, count_chirho in sorted(dist_chirho.items()):
        print(f"    {label_chirho}: {count_chirho}")

    return unique_chirho


def build_retriever_data_chirho(corpus_chirho):
    """Build (query, passage) pairs for retriever fine-tuning (MiniLM-L12)."""
    print("\n━━━ Building Retriever Data ━━━")
    pairs_chirho = []

    # From apologetics Q&A
    for entry_chirho in corpus_chirho.get("apologetics_chirho", []):
        question_chirho = entry_chirho.get("question_chirho", "")
        answer_chirho = entry_chirho.get("answer_chirho", "")
        if question_chirho and answer_chirho and len(answer_chirho) > 50:
            # Truncate very long answers for retriever training
            passage_chirho = answer_chirho[:1000]
            pairs_chirho.append({
                "query_chirho": question_chirho.strip(),
                "passage_chirho": passage_chirho.strip(),
                "category_chirho": classify_intent_chirho(entry_chirho, "apologetics_chirho"),
            })

    # From evidence entries
    for source_chirho in ["evidence_chirho", "miracles_chirho"]:
        for entry_chirho in corpus_chirho.get(source_chirho, []):
            claim_chirho = entry_chirho.get("claim_chirho", "")
            evidence_chirho = entry_chirho.get("evidence_chirho", "")
            if claim_chirho and evidence_chirho:
                pairs_chirho.append({
                    "query_chirho": claim_chirho.strip(),
                    "passage_chirho": evidence_chirho.strip()[:1000],
                    "category_chirho": classify_intent_chirho(entry_chirho, source_chirho),
                })

    # From church fathers
    for entry_chirho in corpus_chirho.get("fathers_chirho", []):
        argument_chirho = entry_chirho.get("argument_chirho", "")
        relevance_chirho = entry_chirho.get("relevance_chirho", "")
        context_chirho = entry_chirho.get("context_chirho", "")
        if argument_chirho and (relevance_chirho or context_chirho):
            passage_chirho = f"{context_chirho} {relevance_chirho}".strip()[:1000]
            pairs_chirho.append({
                "query_chirho": argument_chirho.strip(),
                "passage_chirho": passage_chirho,
                "category_chirho": "historical_evidence",
            })

    # From dialogues (question -> answer pairs)
    for entry_chirho in corpus_chirho.get("dialogues_chirho", []):
        question_chirho = entry_chirho.get("question_chirho", "")
        answer_chirho = entry_chirho.get("answer_chirho", "")
        if question_chirho and answer_chirho and len(answer_chirho) > 50:
            pairs_chirho.append({
                "query_chirho": question_chirho.strip(),
                "passage_chirho": answer_chirho.strip()[:1000],
                "category_chirho": "evangelism_dialogue",
            })

    # From sermons (title/scripture -> sermon excerpt)
    for entry_chirho in corpus_chirho.get("sermons_chirho", []):
        title_chirho = entry_chirho.get("title_chirho", "")
        text_chirho = entry_chirho.get("text_chirho", "")
        scripture_ref_chirho = entry_chirho.get("scripture_reference_chirho", "")
        if title_chirho and text_chirho and len(text_chirho) > 200:
            query_chirho = title_chirho
            if scripture_ref_chirho:
                query_chirho += f" ({scripture_ref_chirho})"
            # Use first 1000 chars of sermon as passage
            pairs_chirho.append({
                "query_chirho": query_chirho.strip(),
                "passage_chirho": text_chirho[:1000].strip(),
                "category_chirho": "apologetics_qa",
            })

    print(f"  Total retriever pairs: {len(pairs_chirho)}")
    return pairs_chirho


def build_generator_data_chirho(corpus_chirho):
    """Build instruction-response pairs for generator fine-tuning (Qwen3-4B LoRA)."""
    print("\n━━━ Building Generator Data ━━━")
    instructions_chirho = []

    # From apologetics Q&A -> direct instruction pairs
    for entry_chirho in corpus_chirho.get("apologetics_chirho", []):
        question_chirho = entry_chirho.get("question_chirho", "")
        answer_chirho = entry_chirho.get("answer_chirho", "")
        scripture_chirho = entry_chirho.get("scripture_chirho", [])

        if question_chirho and answer_chirho and len(answer_chirho) > 50:
            # Add scripture references to the response
            response_chirho = answer_chirho.strip()
            if scripture_chirho:
                refs_chirho = ", ".join(scripture_chirho[:5])
                response_chirho += f"\n\nKey Scripture: {refs_chirho}"

            instructions_chirho.append({
                "instruction_chirho": question_chirho.strip(),
                "response_chirho": response_chirho,
                "category_chirho": classify_intent_chirho(entry_chirho, "apologetics_chirho"),
            })

    # From evidence entries -> "What is the evidence for X?"
    for source_chirho in ["evidence_chirho", "miracles_chirho"]:
        for entry_chirho in corpus_chirho.get(source_chirho, []):
            claim_chirho = entry_chirho.get("claim_chirho", "")
            evidence_chirho = entry_chirho.get("evidence_chirho", "")
            scripture_chirho = entry_chirho.get("scripture_chirho", [])
            rebuttal_chirho = entry_chirho.get("rebuttal_chirho", "")

            if claim_chirho and evidence_chirho:
                # Create the instruction
                instruction_chirho = f"What is the evidence for: {claim_chirho}"

                # Build comprehensive response
                response_parts_chirho = [evidence_chirho.strip()]
                if rebuttal_chirho:
                    response_parts_chirho.append(f"\nResponse to objections: {rebuttal_chirho}")
                if scripture_chirho:
                    refs_chirho = ", ".join(scripture_chirho[:5])
                    response_parts_chirho.append(f"\nScripture: {refs_chirho}")

                instructions_chirho.append({
                    "instruction_chirho": instruction_chirho,
                    "response_chirho": "\n".join(response_parts_chirho),
                    "category_chirho": classify_intent_chirho(entry_chirho, source_chirho),
                })

    # From church fathers -> "What did the early church teach about X?"
    for entry_chirho in corpus_chirho.get("fathers_chirho", []):
        father_chirho = entry_chirho.get("father_chirho", "")
        argument_chirho = entry_chirho.get("argument_chirho", "")
        context_chirho = entry_chirho.get("context_chirho", "")
        relevance_chirho = entry_chirho.get("relevance_chirho", "")
        scripture_chirho = entry_chirho.get("scripture_chirho", [])

        if argument_chirho and father_chirho:
            instruction_chirho = f"What did {father_chirho} teach about: {argument_chirho}"
            response_parts_chirho = []
            if context_chirho:
                response_parts_chirho.append(context_chirho)
            if relevance_chirho:
                response_parts_chirho.append(f"\nModern relevance: {relevance_chirho}")
            if scripture_chirho:
                refs_chirho = ", ".join(scripture_chirho[:5])
                response_parts_chirho.append(f"\nScripture (primary authority): {refs_chirho}")
            response_parts_chirho.append(
                "\nNote: Church fathers are secondary to Scripture. The Bible is the final authority."
            )

            instructions_chirho.append({
                "instruction_chirho": instruction_chirho,
                "response_chirho": "\n".join(response_parts_chirho),
                "category_chirho": "historical_evidence",
            })

    # From dialogues -> conversation training
    for entry_chirho in corpus_chirho.get("dialogues_chirho", []):
        # Handle simple question/answer format
        question_chirho = entry_chirho.get("question_chirho", "")
        answer_chirho = entry_chirho.get("answer_chirho", "")
        if question_chirho and answer_chirho and len(answer_chirho) > 50:
            response_chirho = answer_chirho.strip()
            scripture_chirho = entry_chirho.get("scripture_chirho", [])
            if scripture_chirho:
                refs_chirho = ", ".join(scripture_chirho[:5])
                response_chirho += f"\n\nScripture: {refs_chirho}"
            instructions_chirho.append({
                "instruction_chirho": question_chirho.strip(),
                "response_chirho": response_chirho,
                "category_chirho": "evangelism_dialogue",
            })
            continue

        # Handle multi-turn dialogue format
        turns_chirho = entry_chirho.get("turns_chirho", [])
        if len(turns_chirho) >= 2:
            seeker_text_chirho = []
            evangelist_text_chirho = []
            for turn_chirho in turns_chirho:
                if turn_chirho.get("role_chirho") == "seeker":
                    seeker_text_chirho.append(turn_chirho.get("text_chirho", ""))
                elif turn_chirho.get("role_chirho") == "evangelist":
                    evangelist_text_chirho.append(turn_chirho.get("text_chirho", ""))

            if seeker_text_chirho and evangelist_text_chirho:
                instruction_chirho = seeker_text_chirho[0].strip()
                response_chirho = "\n\n".join(evangelist_text_chirho).strip()

                instructions_chirho.append({
                    "instruction_chirho": instruction_chirho,
                    "response_chirho": response_chirho,
                    "category_chirho": "evangelism_dialogue",
                })

    # From sermons -> "Summarize/explain" instructions
    for entry_chirho in corpus_chirho.get("sermons_chirho", []):
        title_chirho = entry_chirho.get("title_chirho", "")
        text_chirho = entry_chirho.get("text_chirho", "")
        scripture_ref_chirho = entry_chirho.get("scripture_reference_chirho", "")

        if title_chirho and text_chirho and len(text_chirho) > 200:
            # Use first 2000 chars as response (sermon excerpt)
            instruction_chirho = f"What does the Bible teach about: {title_chirho}"
            if scripture_ref_chirho:
                instruction_chirho += f" (based on {scripture_ref_chirho})"

            instructions_chirho.append({
                "instruction_chirho": instruction_chirho,
                "response_chirho": text_chirho[:2000].strip(),
                "category_chirho": "apologetics_qa",
            })

    print(f"  Total generator instruction pairs: {len(instructions_chirho)}")
    from collections import Counter
    dist_chirho = Counter(i_chirho["category_chirho"] for i_chirho in instructions_chirho)
    for cat_chirho, count_chirho in sorted(dist_chirho.items()):
        print(f"    {cat_chirho}: {count_chirho}")

    return instructions_chirho


def split_and_save_chirho(data_chirho, name_chirho, train_ratio_chirho=0.8, val_ratio_chirho=0.1):
    """Split data into train/val/test and save as JSONL."""
    random.seed(SEED_CHIRHO)
    random.shuffle(data_chirho)

    n_chirho = len(data_chirho)
    train_end_chirho = int(n_chirho * train_ratio_chirho)
    val_end_chirho = int(n_chirho * (train_ratio_chirho + val_ratio_chirho))

    splits_chirho = {
        "train": data_chirho[:train_end_chirho],
        "val": data_chirho[train_end_chirho:val_end_chirho],
        "test": data_chirho[val_end_chirho:],
    }

    output_dir_chirho = PROCESSED_DIR_CHIRHO / name_chirho
    output_dir_chirho.mkdir(parents=True, exist_ok=True)

    for split_name_chirho, split_data_chirho in splits_chirho.items():
        filepath_chirho = output_dir_chirho / f"{split_name_chirho}-chirho.jsonl"
        with open(filepath_chirho, "w", encoding="utf-8") as f_chirho:
            for entry_chirho in split_data_chirho:
                f_chirho.write(json.dumps(entry_chirho, ensure_ascii=False) + "\n")
        print(f"    {split_name_chirho}: {len(split_data_chirho)} examples → {filepath_chirho.name}")

    return splits_chirho


def main_chirho():
    """Main processing pipeline."""
    print("=" * 60)
    print("Model 9: Evangelism & Apologetics — Corpus Processing Pipeline")
    print("=" * 60)

    # Ensure output dir exists
    PROCESSED_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    # Load all raw data
    print("\n━━━ Loading Raw Corpus ━━━")
    corpus_chirho = load_all_raw_chirho()
    total_raw_chirho = sum(len(v_chirho) for v_chirho in corpus_chirho.values())
    print(f"  Total raw entries loaded: {total_raw_chirho}")
    for source_chirho, entries_chirho in corpus_chirho.items():
        print(f"    {source_chirho}: {len(entries_chirho)}")

    if total_raw_chirho == 0:
        print("\n  ERROR: No raw data found. Run the compilation scripts first.")
        return

    # Build each component's training data
    intent_data_chirho = build_intent_classifier_data_chirho(corpus_chirho)
    retriever_data_chirho = build_retriever_data_chirho(corpus_chirho)
    generator_data_chirho = build_generator_data_chirho(corpus_chirho)

    # Split and save
    print("\n━━━ Saving Training Splits ━━━")

    if intent_data_chirho:
        print("\n  Intent Classifier:")
        split_intent_chirho = split_and_save_chirho(intent_data_chirho, "intent-classifier-chirho")

    if retriever_data_chirho:
        print("\n  Retriever:")
        split_retriever_chirho = split_and_save_chirho(retriever_data_chirho, "retriever-chirho")

    if generator_data_chirho:
        print("\n  Generator:")
        split_generator_chirho = split_and_save_chirho(generator_data_chirho, "generator-chirho")

    # Summary
    print("\n" + "=" * 60)
    print("CORPUS PROCESSING COMPLETE")
    print("=" * 60)
    print(f"  Raw entries: {total_raw_chirho}")
    print(f"  Intent classifier examples: {len(intent_data_chirho)}")
    print(f"  Retriever pairs: {len(retriever_data_chirho)}")
    print(f"  Generator instructions: {len(generator_data_chirho)}")
    print(f"  Output directory: {PROCESSED_DIR_CHIRHO}")

    # Log to progress DB
    log_progress_chirho(
        f"Process Model 9 corpus: {total_raw_chirho} raw entries → "
        f"{len(intent_data_chirho)} intent + {len(retriever_data_chirho)} retriever + "
        f"{len(generator_data_chirho)} generator",
        f"Training splits saved to {PROCESSED_DIR_CHIRHO}",
        "Corpus processing pipeline complete. Ready for model training.",
    )


if __name__ == "__main__":
    main_chirho()
