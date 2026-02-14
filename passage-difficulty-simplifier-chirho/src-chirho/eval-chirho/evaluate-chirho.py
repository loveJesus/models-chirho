# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
evaluate-chirho.py
Evaluate the fine-tuned Flan-T5-small dual-task model on the test set.

Evaluates both tasks separately:
  1. Difficulty Scoring: accuracy on easy/medium/hard categories, reading level MAE
  2. Simplification: BLEU score, qualitative examples (KJV -> simplified)

Also shows qualitative examples for both tasks.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# ─── Paths ───
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
MODEL_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "simplifier-chirho" / "best-chirho"

MAX_INPUT_LENGTH_CHIRHO = 256
MAX_TARGET_LENGTH_CHIRHO = 256
BATCH_SIZE_CHIRHO = 32


def detect_device_chirho() -> str:
    """Detect best available device."""
    if torch.cuda.is_available():
        print(f"Using CUDA: {torch.cuda.get_device_name(0)}")
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print("Using Apple MPS")
        return "mps"
    else:
        print("Using CPU")
        return "cpu"


def load_test_data_chirho(file_path_chirho: Path) -> list[dict]:
    """Load test JSONL file."""
    examples_chirho = []
    with open(file_path_chirho, "r", encoding="utf-8") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            obj_chirho = json.loads(line_chirho)
            examples_chirho.append(obj_chirho)
    return examples_chirho


def generate_predictions_chirho(
    model_chirho,
    tokenizer_chirho,
    inputs_chirho: list[str],
    device_chirho: str,
    batch_size_chirho: int = 32,
) -> list[str]:
    """Generate predictions in batches."""
    all_preds_chirho = []

    for i_chirho in range(0, len(inputs_chirho), batch_size_chirho):
        batch_chirho = inputs_chirho[i_chirho : i_chirho + batch_size_chirho]

        encoded_chirho = tokenizer_chirho(
            batch_chirho,
            return_tensors="pt",
            max_length=MAX_INPUT_LENGTH_CHIRHO,
            truncation=True,
            padding=True,
        )

        encoded_chirho = {
            k_chirho: v_chirho.to(device_chirho)
            for k_chirho, v_chirho in encoded_chirho.items()
        }

        with torch.no_grad():
            outputs_chirho = model_chirho.generate(
                **encoded_chirho,
                max_length=MAX_TARGET_LENGTH_CHIRHO,
                num_beams=4,
                early_stopping=True,
            )

        decoded_chirho = tokenizer_chirho.batch_decode(
            outputs_chirho, skip_special_tokens=True
        )
        all_preds_chirho.extend(decoded_chirho)

        if (i_chirho // batch_size_chirho) % 10 == 0:
            progress_chirho = min(i_chirho + batch_size_chirho, len(inputs_chirho))
            print(f"  Generated {progress_chirho}/{len(inputs_chirho)} predictions...")

    return all_preds_chirho


def evaluate_difficulty_chirho(
    examples_chirho: list[dict], predictions_chirho: list[str]
) -> dict:
    """Evaluate difficulty scoring task."""
    results_chirho = {
        "total_chirho": 0,
        "difficulty_correct_chirho": 0,
        "reading_level_errors_chirho": [],
        "vocab_correct_chirho": 0,
        "confusion_matrix_chirho": Counter(),
    }

    for ex_chirho, pred_chirho in zip(examples_chirho, predictions_chirho):
        target_chirho = ex_chirho["target_chirho"]
        results_chirho["total_chirho"] += 1

        # Extract difficulty label
        pred_diff_match_chirho = re.search(r"difficulty:\s*(\w+)", pred_chirho)
        target_diff_match_chirho = re.search(r"difficulty:\s*(\w+)", target_chirho)

        pred_diff_chirho = pred_diff_match_chirho.group(1) if pred_diff_match_chirho else "unknown"
        target_diff_chirho = target_diff_match_chirho.group(1) if target_diff_match_chirho else "unknown"

        if pred_diff_chirho == target_diff_chirho:
            results_chirho["difficulty_correct_chirho"] += 1

        results_chirho["confusion_matrix_chirho"][(target_diff_chirho, pred_diff_chirho)] += 1

        # Extract reading level
        pred_level_match_chirho = re.search(r"reading_level:\s*(\d+)", pred_chirho)
        target_level_match_chirho = re.search(r"reading_level:\s*(\d+)", target_chirho)

        if pred_level_match_chirho and target_level_match_chirho:
            pred_level_chirho = int(pred_level_match_chirho.group(1))
            target_level_chirho = int(target_level_match_chirho.group(1))
            results_chirho["reading_level_errors_chirho"].append(
                abs(pred_level_chirho - target_level_chirho)
            )

        # Extract vocab complexity
        pred_vocab_match_chirho = re.search(r"vocab_complexity:\s*(\w+)", pred_chirho)
        target_vocab_match_chirho = re.search(r"vocab_complexity:\s*(\w+)", target_chirho)

        if pred_vocab_match_chirho and target_vocab_match_chirho:
            if pred_vocab_match_chirho.group(1) == target_vocab_match_chirho.group(1):
                results_chirho["vocab_correct_chirho"] += 1

    return results_chirho


def compute_bleu_chirho(predictions_chirho: list[str], references_chirho: list[str]) -> float:
    """Compute BLEU score using sacrebleu."""
    try:
        import sacrebleu

        bleu_chirho = sacrebleu.corpus_bleu(
            predictions_chirho, [references_chirho]
        )
        return bleu_chirho.score
    except ImportError:
        print("  WARNING: sacrebleu not installed, computing simple BLEU approximation")
        # Simple unigram precision as fallback
        correct_chirho = 0
        total_chirho = 0
        for pred_chirho, ref_chirho in zip(predictions_chirho, references_chirho):
            pred_tokens_chirho = pred_chirho.lower().split()
            ref_tokens_chirho = set(ref_chirho.lower().split())
            for token_chirho in pred_tokens_chirho:
                total_chirho += 1
                if token_chirho in ref_tokens_chirho:
                    correct_chirho += 1
        return (correct_chirho / max(1, total_chirho)) * 100


def evaluate_simplification_chirho(
    examples_chirho: list[dict], predictions_chirho: list[str]
) -> dict:
    """Evaluate simplification task."""
    references_chirho = [ex_chirho["target_chirho"] for ex_chirho in examples_chirho]

    bleu_score_chirho = compute_bleu_chirho(predictions_chirho, references_chirho)

    # Length ratio
    pred_lengths_chirho = [len(p_chirho.split()) for p_chirho in predictions_chirho]
    ref_lengths_chirho = [len(r_chirho.split()) for r_chirho in references_chirho]
    avg_pred_len_chirho = np.mean(pred_lengths_chirho) if pred_lengths_chirho else 0
    avg_ref_len_chirho = np.mean(ref_lengths_chirho) if ref_lengths_chirho else 0

    # Exact match
    exact_match_chirho = sum(
        1
        for p_chirho, r_chirho in zip(predictions_chirho, references_chirho)
        if p_chirho.strip().lower() == r_chirho.strip().lower()
    )

    return {
        "bleu_chirho": bleu_score_chirho,
        "exact_match_chirho": exact_match_chirho,
        "total_chirho": len(examples_chirho),
        "avg_pred_length_chirho": avg_pred_len_chirho,
        "avg_ref_length_chirho": avg_ref_len_chirho,
    }


def main_chirho():
    """Main evaluation function."""
    print("=" * 60)
    print("Passage Difficulty Scorer & Simplifier Evaluation")
    print("=" * 60)

    device_chirho = detect_device_chirho()

    # Use CPU for MPS to avoid generation issues
    inference_device_chirho = device_chirho if device_chirho != "mps" else "cpu"

    # ─── Load model ───
    print(f"\nLoading model from {MODEL_DIR_CHIRHO}...")
    if not MODEL_DIR_CHIRHO.exists():
        print(f"ERROR: Model not found at {MODEL_DIR_CHIRHO}")
        print("Run training first: python src-chirho/train-chirho/train-simplifier-chirho.py")
        sys.exit(1)

    tokenizer_chirho = AutoTokenizer.from_pretrained(str(MODEL_DIR_CHIRHO))
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(str(MODEL_DIR_CHIRHO))
    model_chirho.to(inference_device_chirho)
    model_chirho.eval()

    print("  Model loaded successfully.")

    # ─── Load test data ───
    test_path_chirho = DATA_DIR_CHIRHO / "test-simplifier-chirho.jsonl"
    print(f"\nLoading test data from {test_path_chirho}...")
    all_test_chirho = load_test_data_chirho(test_path_chirho)
    print(f"  Total test examples: {len(all_test_chirho)}")

    # Separate by task
    difficulty_examples_chirho = [
        ex_chirho for ex_chirho in all_test_chirho if ex_chirho.get("task_chirho") == "difficulty_scoring"
    ]
    simplification_examples_chirho = [
        ex_chirho for ex_chirho in all_test_chirho if ex_chirho.get("task_chirho") == "simplification"
    ]

    print(f"  Difficulty scoring: {len(difficulty_examples_chirho)} examples")
    print(f"  Simplification: {len(simplification_examples_chirho)} examples")

    # ─── Evaluate Difficulty Scoring ───
    print("\n" + "=" * 60)
    print("Task 1: Difficulty Scoring")
    print("=" * 60)

    if difficulty_examples_chirho:
        diff_inputs_chirho = [ex_chirho["input_chirho"] for ex_chirho in difficulty_examples_chirho]

        print(f"\nGenerating {len(diff_inputs_chirho)} predictions...")
        diff_preds_chirho = generate_predictions_chirho(
            model_chirho, tokenizer_chirho, diff_inputs_chirho,
            inference_device_chirho, BATCH_SIZE_CHIRHO
        )

        diff_results_chirho = evaluate_difficulty_chirho(
            difficulty_examples_chirho, diff_preds_chirho
        )

        accuracy_chirho = (
            diff_results_chirho["difficulty_correct_chirho"]
            / max(1, diff_results_chirho["total_chirho"])
        )
        vocab_acc_chirho = (
            diff_results_chirho["vocab_correct_chirho"]
            / max(1, diff_results_chirho["total_chirho"])
        )

        print(f"\nResults:")
        print(f"  Difficulty accuracy: {accuracy_chirho:.4f} ({diff_results_chirho['difficulty_correct_chirho']}/{diff_results_chirho['total_chirho']})")
        print(f"  Vocab complexity accuracy: {vocab_acc_chirho:.4f}")

        if diff_results_chirho["reading_level_errors_chirho"]:
            mae_chirho = np.mean(diff_results_chirho["reading_level_errors_chirho"])
            print(f"  Reading level MAE: {mae_chirho:.2f}")

        # Confusion matrix
        print(f"\n  Confusion Matrix (target -> pred):")
        labels_chirho = ["easy", "medium", "hard"]
        header_chirho = "         " + "  ".join(f"{l_chirho:>8}" for l_chirho in labels_chirho)
        print(f"  {header_chirho}")
        for target_label_chirho in labels_chirho:
            row_chirho = f"  {target_label_chirho:>8}"
            for pred_label_chirho in labels_chirho:
                count_chirho = diff_results_chirho["confusion_matrix_chirho"].get(
                    (target_label_chirho, pred_label_chirho), 0
                )
                row_chirho += f"  {count_chirho:>8}"
            print(row_chirho)

        # Qualitative examples
        print(f"\n  Sample Predictions:")
        for i_chirho in range(min(5, len(difficulty_examples_chirho))):
            input_text_chirho = diff_inputs_chirho[i_chirho][:80]
            if len(diff_inputs_chirho[i_chirho]) > 80:
                input_text_chirho += "..."
            print(f"\n    Input:  {input_text_chirho}")
            print(f"    Target: {difficulty_examples_chirho[i_chirho]['target_chirho']}")
            print(f"    Pred:   {diff_preds_chirho[i_chirho]}")
    else:
        print("  No difficulty scoring examples in test set.")

    # ─── Evaluate Simplification ───
    print("\n" + "=" * 60)
    print("Task 2: Simplification")
    print("=" * 60)

    if simplification_examples_chirho:
        simp_inputs_chirho = [ex_chirho["input_chirho"] for ex_chirho in simplification_examples_chirho]

        print(f"\nGenerating {len(simp_inputs_chirho)} predictions...")
        simp_preds_chirho = generate_predictions_chirho(
            model_chirho, tokenizer_chirho, simp_inputs_chirho,
            inference_device_chirho, BATCH_SIZE_CHIRHO
        )

        simp_results_chirho = evaluate_simplification_chirho(
            simplification_examples_chirho, simp_preds_chirho
        )

        print(f"\nResults:")
        print(f"  BLEU score: {simp_results_chirho['bleu_chirho']:.2f}")
        print(f"  Exact match: {simp_results_chirho['exact_match_chirho']}/{simp_results_chirho['total_chirho']} ({simp_results_chirho['exact_match_chirho'] / max(1, simp_results_chirho['total_chirho']) * 100:.1f}%)")
        print(f"  Avg prediction length: {simp_results_chirho['avg_pred_length_chirho']:.1f} words")
        print(f"  Avg reference length: {simp_results_chirho['avg_ref_length_chirho']:.1f} words")

        # Qualitative examples
        print(f"\n  Sample Predictions (KJV -> Simplified):")
        shown_chirho = 0
        for i_chirho in range(len(simplification_examples_chirho)):
            if shown_chirho >= 8:
                break

            input_text_chirho = simp_inputs_chirho[i_chirho].replace("simplify: ", "")
            target_text_chirho = simplification_examples_chirho[i_chirho]["target_chirho"]
            pred_text_chirho = simp_preds_chirho[i_chirho]

            # Show interesting examples (not too short)
            if len(input_text_chirho) < 30:
                continue

            print(f"\n    [{shown_chirho + 1}] Original:   {input_text_chirho[:120]}{'...' if len(input_text_chirho) > 120 else ''}")
            print(f"        Reference:  {target_text_chirho[:120]}{'...' if len(target_text_chirho) > 120 else ''}")
            print(f"        Predicted:  {pred_text_chirho[:120]}{'...' if len(pred_text_chirho) > 120 else ''}")
            shown_chirho += 1
    else:
        print("  No simplification examples in test set.")

    # ─── BERTScore (optional) ───
    print("\n" + "=" * 60)
    print("BERTScore (Simplification)")
    print("=" * 60)

    if simplification_examples_chirho:
        try:
            from bert_score import score as bert_score_fn_chirho

            # Use a subset for speed
            max_bert_chirho = min(500, len(simplification_examples_chirho))
            bert_preds_chirho = simp_preds_chirho[:max_bert_chirho]
            bert_refs_chirho = [
                ex_chirho["target_chirho"] for ex_chirho in simplification_examples_chirho[:max_bert_chirho]
            ]

            print(f"\nComputing BERTScore on {max_bert_chirho} examples...")
            p_chirho, r_chirho, f1_chirho = bert_score_fn_chirho(
                bert_preds_chirho, bert_refs_chirho, lang="en", verbose=False
            )

            print(f"  BERTScore Precision: {p_chirho.mean():.4f}")
            print(f"  BERTScore Recall: {r_chirho.mean():.4f}")
            print(f"  BERTScore F1: {f1_chirho.mean():.4f}")
        except ImportError:
            print("  bert-score not installed, skipping. Install with: pip install bert-score")
        except Exception as error_chirho:
            print(f"  BERTScore computation failed: {error_chirho}")

    # ─── Overall Summary ───
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    if difficulty_examples_chirho:
        print(f"  Difficulty Accuracy:   {accuracy_chirho:.4f}")
    if simplification_examples_chirho:
        print(f"  Simplification BLEU:   {simp_results_chirho['bleu_chirho']:.2f}")
        target_bleu_chirho = 30
        target_bertscore_chirho = 0.85
        bleu_status_chirho = "PASS" if simp_results_chirho["bleu_chirho"] >= target_bleu_chirho else "BELOW TARGET"
        print(f"  BLEU target ({target_bleu_chirho}):     {bleu_status_chirho}")

    print("\nEvaluation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main_chirho()
