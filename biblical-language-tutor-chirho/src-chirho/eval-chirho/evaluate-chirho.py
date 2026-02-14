# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
evaluate-chirho.py
Comprehensive evaluation of both parser and glosser models.

Parser metrics:
  - Exact match rate (target >75%)
  - Per-tag F1 (target >90%)
  - Per-language breakdown (Hebrew vs Greek)

Glosser metrics:
  - BLEU score (target >50)
  - Word-level accuracy (target >70%)
  - Qualitative examples (Gen 1:1, John 1:1, John 3:16)
"""

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Paths
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
PARSER_MODEL_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "parser-chirho" / "best-chirho"
GLOSSER_MODEL_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "glosser-chirho" / "best-chirho"


def detect_device_chirho() -> str:
    """Auto-detect best available device."""
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_test_data_chirho(prefix_chirho: str) -> list[dict]:
    """Load test JSONL file."""
    path_chirho = DATA_DIR_CHIRHO / f"test-{prefix_chirho}-chirho.jsonl"
    data_chirho = []
    with open(path_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            if line_chirho.strip():
                data_chirho.append(json.loads(line_chirho))
    return data_chirho


def generate_predictions_chirho(
    model_chirho, tokenizer_chirho, inputs_chirho: list[str],
    max_length_chirho: int, device_chirho: str, batch_size_chirho: int = 32
) -> list[str]:
    """Generate predictions in batches."""
    model_chirho.eval()
    all_preds_chirho = []

    for i_chirho in range(0, len(inputs_chirho), batch_size_chirho):
        batch_inputs_chirho = inputs_chirho[i_chirho:i_chirho + batch_size_chirho]
        encoded_chirho = tokenizer_chirho(
            batch_inputs_chirho, return_tensors="pt",
            max_length=max_length_chirho, truncation=True, padding=True,
        )
        encoded_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in encoded_chirho.items()}

        with torch.no_grad():
            output_ids_chirho = model_chirho.generate(
                **encoded_chirho, max_length=max_length_chirho
            )

        decoded_chirho = tokenizer_chirho.batch_decode(output_ids_chirho, skip_special_tokens=True)
        all_preds_chirho.extend(decoded_chirho)

        if (i_chirho // batch_size_chirho) % 10 == 0:
            print(f"    Processed {i_chirho + len(batch_inputs_chirho)}/{len(inputs_chirho)}")

    return all_preds_chirho


def evaluate_parser_chirho(device_chirho: str) -> dict:
    """Evaluate the morphological parser."""
    print("\n" + "=" * 60)
    print("PARSER EVALUATION")
    print("=" * 60)

    if not PARSER_MODEL_DIR_CHIRHO.exists():
        print("  Parser model not found. Skipping.")
        return {}

    print("Loading parser model...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(str(PARSER_MODEL_DIR_CHIRHO))
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(str(PARSER_MODEL_DIR_CHIRHO))
    model_chirho.to(device_chirho)

    print("Loading test data...")
    test_data_chirho = load_test_data_chirho("parser")
    print(f"  Test examples: {len(test_data_chirho)}")

    inputs_chirho = [d_chirho["input_chirho"] for d_chirho in test_data_chirho]
    targets_chirho = [d_chirho["target_chirho"] for d_chirho in test_data_chirho]
    langs_chirho = [d_chirho.get("lang_chirho", "unknown") for d_chirho in test_data_chirho]

    print("Generating predictions...")
    preds_chirho = generate_predictions_chirho(
        model_chirho, tokenizer_chirho, inputs_chirho, 128, device_chirho
    )

    # Exact match
    exact_matches_chirho = sum(
        1 for p_chirho, t_chirho in zip(preds_chirho, targets_chirho)
        if p_chirho.strip() == t_chirho.strip()
    )
    exact_match_rate_chirho = exact_matches_chirho / len(preds_chirho)

    # Per-tag F1
    tag_tp_chirho = defaultdict(int)
    tag_fp_chirho = defaultdict(int)
    tag_fn_chirho = defaultdict(int)

    for pred_chirho, target_chirho in zip(preds_chirho, targets_chirho):
        pred_tags_chirho = set(t_chirho.strip() for t_chirho in pred_chirho.split("|") if ":" in t_chirho)
        target_tags_chirho = set(t_chirho.strip() for t_chirho in target_chirho.split("|") if ":" in t_chirho)

        for tag_chirho in target_tags_chirho:
            key_chirho = tag_chirho.split(":")[0]
            if tag_chirho in pred_tags_chirho:
                tag_tp_chirho[key_chirho] += 1
            else:
                tag_fn_chirho[key_chirho] += 1

        for tag_chirho in pred_tags_chirho:
            key_chirho = tag_chirho.split(":")[0]
            if tag_chirho not in target_tags_chirho:
                tag_fp_chirho[key_chirho] += 1

    # Compute per-tag F1
    all_tags_chirho = set(list(tag_tp_chirho.keys()) + list(tag_fn_chirho.keys()) + list(tag_fp_chirho.keys()))
    tag_f1s_chirho = {}
    for tag_chirho in sorted(all_tags_chirho):
        tp_chirho = tag_tp_chirho[tag_chirho]
        fp_chirho = tag_fp_chirho[tag_chirho]
        fn_chirho = tag_fn_chirho[tag_chirho]
        precision_chirho = tp_chirho / (tp_chirho + fp_chirho) if (tp_chirho + fp_chirho) > 0 else 0
        recall_chirho = tp_chirho / (tp_chirho + fn_chirho) if (tp_chirho + fn_chirho) > 0 else 0
        f1_chirho = (
            2 * precision_chirho * recall_chirho / (precision_chirho + recall_chirho)
            if (precision_chirho + recall_chirho) > 0 else 0
        )
        tag_f1s_chirho[tag_chirho] = f1_chirho

    avg_tag_f1_chirho = np.mean(list(tag_f1s_chirho.values())) if tag_f1s_chirho else 0

    # Per-language breakdown
    lang_exact_chirho = defaultdict(lambda: {"correct_chirho": 0, "total_chirho": 0})
    for pred_chirho, target_chirho, lang_chirho in zip(preds_chirho, targets_chirho, langs_chirho):
        lang_exact_chirho[lang_chirho]["total_chirho"] += 1
        if pred_chirho.strip() == target_chirho.strip():
            lang_exact_chirho[lang_chirho]["correct_chirho"] += 1

    # Print results
    print(f"\n  Exact Match Rate: {exact_match_rate_chirho:.1%} (target: >75%)")
    target_met_chirho = "[PASS]" if exact_match_rate_chirho >= 0.75 else "[BELOW TARGET]"
    print(f"    {target_met_chirho}")

    print(f"\n  Average Tag F1: {avg_tag_f1_chirho:.1%} (target: >90%)")
    target_met_chirho = "[PASS]" if avg_tag_f1_chirho >= 0.90 else "[BELOW TARGET]"
    print(f"    {target_met_chirho}")

    print("\n  Per-tag F1:")
    for tag_chirho, f1_chirho in sorted(tag_f1s_chirho.items()):
        print(f"    {tag_chirho}: {f1_chirho:.3f}")

    print("\n  Per-language exact match:")
    for lang_chirho, counts_chirho in lang_exact_chirho.items():
        rate_chirho = counts_chirho["correct_chirho"] / counts_chirho["total_chirho"] if counts_chirho["total_chirho"] > 0 else 0
        print(f"    {lang_chirho}: {rate_chirho:.1%} ({counts_chirho['correct_chirho']}/{counts_chirho['total_chirho']})")

    # Qualitative examples
    print("\n  Sample predictions:")
    for i_chirho in range(min(5, len(preds_chirho))):
        print(f"\n    Input:    {inputs_chirho[i_chirho][:80]}...")
        print(f"    Predicted: {preds_chirho[i_chirho][:80]}...")
        print(f"    Expected:  {targets_chirho[i_chirho][:80]}...")
        match_chirho = "MATCH" if preds_chirho[i_chirho].strip() == targets_chirho[i_chirho].strip() else "MISMATCH"
        print(f"    [{match_chirho}]")

    return {
        "exact_match_chirho": exact_match_rate_chirho,
        "avg_tag_f1_chirho": avg_tag_f1_chirho,
        "per_tag_f1_chirho": tag_f1s_chirho,
        "per_language_chirho": {
            lang_chirho: counts_chirho["correct_chirho"] / counts_chirho["total_chirho"]
            for lang_chirho, counts_chirho in lang_exact_chirho.items()
            if counts_chirho["total_chirho"] > 0
        },
    }


def evaluate_glosser_chirho(device_chirho: str) -> dict:
    """Evaluate the interlinear glosser."""
    print("\n" + "=" * 60)
    print("GLOSSER EVALUATION")
    print("=" * 60)

    if not GLOSSER_MODEL_DIR_CHIRHO.exists():
        print("  Glosser model not found. Skipping.")
        return {}

    print("Loading glosser model...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(str(GLOSSER_MODEL_DIR_CHIRHO))
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(str(GLOSSER_MODEL_DIR_CHIRHO))
    model_chirho.to(device_chirho)

    print("Loading test data...")
    test_data_chirho = load_test_data_chirho("glosser")
    print(f"  Test examples: {len(test_data_chirho)}")

    inputs_chirho = [d_chirho["input_chirho"] for d_chirho in test_data_chirho]
    targets_chirho = [d_chirho["target_chirho"] for d_chirho in test_data_chirho]

    print("Generating predictions...")
    preds_chirho = generate_predictions_chirho(
        model_chirho, tokenizer_chirho, inputs_chirho, 256, device_chirho, batch_size_chirho=16
    )

    # BLEU
    try:
        import sacrebleu
        bleu_result_chirho = sacrebleu.corpus_bleu(preds_chirho, [targets_chirho])
        bleu_score_chirho = bleu_result_chirho.score
    except ImportError:
        bleu_score_chirho = 0.0
        print("  (sacrebleu not installed, skipping BLEU)")

    # Word-level accuracy
    correct_words_chirho = 0
    total_words_chirho = 0
    for pred_chirho, target_chirho in zip(preds_chirho, targets_chirho):
        pred_glosses_chirho = [g_chirho.strip().lower() for g_chirho in pred_chirho.split("|")]
        target_glosses_chirho = [g_chirho.strip().lower() for g_chirho in target_chirho.split("|")]

        for i_chirho, tgt_chirho in enumerate(target_glosses_chirho):
            total_words_chirho += 1
            if i_chirho < len(pred_glosses_chirho) and pred_glosses_chirho[i_chirho] == tgt_chirho:
                correct_words_chirho += 1

    word_accuracy_chirho = correct_words_chirho / total_words_chirho if total_words_chirho > 0 else 0

    # Print results
    print(f"\n  BLEU Score: {bleu_score_chirho:.1f} (target: >50)")
    target_met_chirho = "[PASS]" if bleu_score_chirho >= 50 else "[BELOW TARGET]"
    print(f"    {target_met_chirho}")

    print(f"\n  Word Accuracy: {word_accuracy_chirho:.1%} (target: >70%)")
    target_met_chirho = "[PASS]" if word_accuracy_chirho >= 0.70 else "[BELOW TARGET]"
    print(f"    {target_met_chirho}")

    # Qualitative examples
    print("\n  Sample predictions:")
    for i_chirho in range(min(5, len(preds_chirho))):
        print(f"\n    Input:    {inputs_chirho[i_chirho][:100]}...")
        print(f"    Predicted: {preds_chirho[i_chirho][:100]}...")
        print(f"    Expected:  {targets_chirho[i_chirho][:100]}...")

    # Key verse tests
    print("\n  --- Key Verse Tests ---")
    key_verses_chirho = [
        'gloss [hebrew]: בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ [GEN 1:1]',
        'gloss [greek]: Ἐν ἀρχῇ ἦν ὁ λόγος καὶ ὁ λόγος ἦν πρὸς τὸν θεόν καὶ θεὸς ἦν ὁ λόγος [JHN 1:1]',
        'gloss [greek]: Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον ὥστε τὸν υἱὸν τὸν μονογενῆ ἔδωκεν [JHN 3:16]',
    ]

    for verse_input_chirho in key_verses_chirho:
        encoded_chirho = tokenizer_chirho(
            verse_input_chirho, return_tensors="pt", max_length=256, truncation=True
        )
        encoded_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in encoded_chirho.items()}

        with torch.no_grad():
            output_ids_chirho = model_chirho.generate(**encoded_chirho, max_length=256)

        output_chirho = tokenizer_chirho.decode(output_ids_chirho[0], skip_special_tokens=True)
        print(f"\n    Input:  {verse_input_chirho}")
        print(f"    Gloss:  {output_chirho}")

    return {
        "bleu_chirho": bleu_score_chirho,
        "word_accuracy_chirho": word_accuracy_chirho,
    }


def main_chirho():
    """Run full evaluation suite."""
    print("=" * 60)
    print("Biblical Language Tutor — Full Evaluation")
    print("=" * 60)

    device_chirho = detect_device_chirho()
    print(f"Device: {device_chirho}")

    parser_results_chirho = evaluate_parser_chirho(device_chirho)
    glosser_results_chirho = evaluate_glosser_chirho(device_chirho)

    # Summary
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    if parser_results_chirho:
        em_chirho = parser_results_chirho.get("exact_match_chirho", 0)
        f1_chirho = parser_results_chirho.get("avg_tag_f1_chirho", 0)
        print(f"  Parser:  exact_match={em_chirho:.1%}, tag_f1={f1_chirho:.1%}")
    else:
        print("  Parser:  NOT EVALUATED")

    if glosser_results_chirho:
        bleu_chirho = glosser_results_chirho.get("bleu_chirho", 0)
        wa_chirho = glosser_results_chirho.get("word_accuracy_chirho", 0)
        print(f"  Glosser: bleu={bleu_chirho:.1f}, word_accuracy={wa_chirho:.1%}")
    else:
        print("  Glosser: NOT EVALUATED")

    # Save results
    results_path_chirho = BASE_DIR_CHIRHO / "spec-chirho" / "eval-results-chirho.json"
    results_path_chirho.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path_chirho, "w") as f_chirho:
        json.dump({
            "parser_chirho": parser_results_chirho,
            "glosser_chirho": glosser_results_chirho,
        }, f_chirho, indent=2, default=str)
    print(f"\n  Results saved to: {results_path_chirho}")


if __name__ == "__main__":
    main_chirho()
