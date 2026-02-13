# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
evaluate-chirho.py
Comprehensive assessment of the theological guardrails pipeline.
Tests classifier, embedder, and explainer individually and as a pipeline.
"""

import json
from pathlib import Path

import numpy as np
import torch
import yaml
from sklearn.metrics import (
    f1_score,
    precision_recall_fscore_support,
)
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Paths
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH_CHIRHO = BASE_DIR_CHIRHO / "src-chirho" / "train-chirho" / "config-chirho.yaml"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
MODELS_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho"


def load_config_chirho() -> dict:
    with open(CONFIG_PATH_CHIRHO, "r") as f_chirho:
        return yaml.safe_load(f_chirho)


def load_test_data_chirho() -> list[dict]:
    test_path_chirho = DATA_DIR_CHIRHO / "test-chirho.jsonl"
    examples_chirho = []
    with open(test_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if line_chirho.strip():
                examples_chirho.append(json.loads(line_chirho))
    return examples_chirho


def assess_classifier_chirho(config_chirho: dict, test_data_chirho: list[dict]):
    """Assess the RoBERTa-large classifier on the test set."""
    print("\n" + "=" * 60)
    print("CLASSIFIER ASSESSMENT (RoBERTa-large)")
    print("=" * 60)

    classifier_config_chirho = config_chirho["classifier_chirho"]
    labels_chirho = classifier_config_chirho["labels_chirho"]
    model_path_chirho = MODELS_DIR_CHIRHO / "classifier-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Model not found at {model_path_chirho}. Train first.")
        return

    # Load model
    tokenizer_chirho = AutoTokenizer.from_pretrained(str(model_path_chirho))
    model_chirho = AutoModelForSequenceClassification.from_pretrained(str(model_path_chirho))

    if torch.backends.mps.is_available():
        device_chirho = torch.device("mps")
    elif torch.cuda.is_available():
        device_chirho = torch.device("cuda")
    else:
        device_chirho = torch.device("cpu")

    model_chirho.to(device_chirho)

    all_predictions_chirho = []
    all_true_labels_chirho = []

    for example_chirho in test_data_chirho:
        text_chirho = example_chirho.get("text_chirho", "")

        # Build true label vector
        true_labels_chirho = [0] * len(labels_chirho)
        if example_chirho.get("label_chirho") == "orthodox":
            true_labels_chirho[0] = 1
        else:
            for ht_chirho in example_chirho.get("heresy_types_chirho", []):
                label_key_chirho = f"{ht_chirho}_chirho"
                if label_key_chirho in labels_chirho:
                    idx_chirho = labels_chirho.index(label_key_chirho)
                    true_labels_chirho[idx_chirho] = 1

        # Predict
        inputs_chirho = tokenizer_chirho(
            text_chirho,
            return_tensors="pt",
            max_length=classifier_config_chirho["max_length_chirho"],
            truncation=True,
            padding="max_length",
        )
        inputs_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

        with torch.no_grad():
            outputs_chirho = model_chirho(**inputs_chirho)
            predictions_chirho = (
                torch.sigmoid(outputs_chirho.logits).cpu().numpy()[0] > 0.5
            ).astype(int)

        all_predictions_chirho.append(predictions_chirho)
        all_true_labels_chirho.append(true_labels_chirho)

    # Metrics
    all_predictions_np_chirho = np.array(all_predictions_chirho)
    all_true_np_chirho = np.array(all_true_labels_chirho)

    f1_macro_chirho = f1_score(all_true_np_chirho, all_predictions_np_chirho, average="macro", zero_division=0)
    f1_micro_chirho = f1_score(all_true_np_chirho, all_predictions_np_chirho, average="micro", zero_division=0)

    print(f"\n  F1 (macro): {f1_macro_chirho:.4f}")
    print(f"  F1 (micro): {f1_micro_chirho:.4f}")

    # Per-label metrics
    print("\n  Per-label results:")
    for i_chirho, label_chirho in enumerate(labels_chirho):
        if all_true_np_chirho[:, i_chirho].sum() > 0:
            p_chirho, r_chirho, f_chirho, _ = precision_recall_fscore_support(
                all_true_np_chirho[:, i_chirho],
                all_predictions_np_chirho[:, i_chirho],
                average="binary",
                zero_division=0,
            )
            print(f"    {label_chirho}: P={p_chirho:.3f} R={r_chirho:.3f} F1={f_chirho:.3f}")

    # Target check
    target_f1_chirho = config_chirho["assessment_chirho"]["target_f1_chirho"] if "assessment_chirho" in config_chirho else config_chirho.get("evaluation_chirho", {}).get("target_f1_chirho", 0.85)
    status_chirho = "PASS" if f1_macro_chirho >= target_f1_chirho else "FAIL"
    print(f"\n  Target F1 >= {target_f1_chirho}: {status_chirho} ({f1_macro_chirho:.4f})")

    return f1_macro_chirho


def assess_embedder_chirho(config_chirho: dict, test_data_chirho: list[dict]):
    """Assess the sentence transformer embedder."""
    print("\n" + "=" * 60)
    print("EMBEDDER ASSESSMENT (MiniLM-L12)")
    print("=" * 60)

    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    model_path_chirho = MODELS_DIR_CHIRHO / "embedder-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Model not found at {model_path_chirho}. Train first.")
        return

    model_chirho = SentenceTransformer(str(model_path_chirho))

    orthodox_texts_chirho = [
        ex_chirho["text_chirho"] for ex_chirho in test_data_chirho
        if ex_chirho.get("label_chirho") == "orthodox"
    ][:100]
    heterodox_texts_chirho = [
        ex_chirho["text_chirho"] for ex_chirho in test_data_chirho
        if ex_chirho.get("label_chirho") == "heterodox"
    ][:100]

    if not orthodox_texts_chirho or not heterodox_texts_chirho:
        print("  Not enough test data for embedder assessment")
        return

    # Encode
    orthodox_embeddings_chirho = model_chirho.encode(orthodox_texts_chirho, show_progress_bar=False)
    heterodox_embeddings_chirho = model_chirho.encode(heterodox_texts_chirho, show_progress_bar=False)

    # Compute cosine similarities
    oo_sim_chirho = cosine_similarity(orthodox_embeddings_chirho)
    oo_avg_chirho = np.mean(oo_sim_chirho[np.triu_indices_from(oo_sim_chirho, k=1)])

    hh_sim_chirho = cosine_similarity(heterodox_embeddings_chirho)
    hh_avg_chirho = np.mean(hh_sim_chirho[np.triu_indices_from(hh_sim_chirho, k=1)])

    oh_sim_chirho = cosine_similarity(orthodox_embeddings_chirho, heterodox_embeddings_chirho)
    oh_avg_chirho = np.mean(oh_sim_chirho)

    print(f"\n  Orthodox-Orthodox avg similarity: {oo_avg_chirho:.4f}")
    print(f"  Heterodox-Heterodox avg similarity: {hh_avg_chirho:.4f}")
    print(f"  Orthodox-Heterodox avg similarity: {oh_avg_chirho:.4f}")
    print(f"  Separation gap: {oo_avg_chirho - oh_avg_chirho:.4f}")

    if oo_avg_chirho > oh_avg_chirho:
        print("  PASS: Orthodox statements cluster more tightly than with heterodox")
    else:
        print("  WARN: Embeddings need more training")


def assess_explainer_chirho(config_chirho: dict, test_data_chirho: list[dict]):
    """Assess the Flan-T5-base explainer on a sample of test examples."""
    print("\n" + "=" * 60)
    print("EXPLAINER ASSESSMENT (Flan-T5-base)")
    print("=" * 60)

    explainer_config_chirho = config_chirho["explainer_chirho"]
    model_path_chirho = MODELS_DIR_CHIRHO / "explainer-chirho" / "best-chirho"

    if not model_path_chirho.exists():
        print(f"  Model not found at {model_path_chirho}. Train first.")
        return

    from transformers import AutoModelForSeq2SeqLM

    tokenizer_chirho = AutoTokenizer.from_pretrained(str(model_path_chirho))
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(str(model_path_chirho))

    if torch.backends.mps.is_available():
        device_chirho = torch.device("mps")
    elif torch.cuda.is_available():
        device_chirho = torch.device("cuda")
    else:
        device_chirho = torch.device("cpu")

    model_chirho.to(device_chirho)

    # Sample heterodox examples that have explanations
    samples_chirho = [
        ex_chirho for ex_chirho in test_data_chirho
        if ex_chirho.get("explanation_chirho") and ex_chirho.get("label_chirho") == "heterodox"
    ][:20]

    if not samples_chirho:
        print("  No test examples with explanations found.")
        return

    print(f"  Evaluating on {len(samples_chirho)} samples with reference explanations...\n")

    generated_count_chirho = 0
    for i_chirho, example_chirho in enumerate(samples_chirho[:10]):
        text_chirho = example_chirho.get("text_chirho", "")
        label_chirho = example_chirho.get("label_chirho", "")
        heresy_types_chirho = example_chirho.get("heresy_types_chirho", [])
        ref_explanation_chirho = example_chirho.get("explanation_chirho", "")

        heresy_str_chirho = ", ".join(heresy_types_chirho) if heresy_types_chirho else "none"
        input_text_chirho = (
            f"explain theological classification: {text_chirho} | "
            f"label: {label_chirho} | "
            f"heresy types: {heresy_str_chirho}"
        )

        inputs_chirho = tokenizer_chirho(
            input_text_chirho,
            return_tensors="pt",
            max_length=explainer_config_chirho["max_input_length_chirho"],
            truncation=True,
        )
        inputs_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

        with torch.no_grad():
            outputs_chirho = model_chirho.generate(
                **inputs_chirho,
                max_length=explainer_config_chirho["max_output_length_chirho"],
                num_beams=4,
                early_stopping=True,
            )

        generated_chirho = tokenizer_chirho.decode(outputs_chirho[0], skip_special_tokens=True)
        generated_count_chirho += 1

        print(f"  [{i_chirho+1}] Text: {text_chirho[:80]}...")
        print(f"      Heresies: {heresy_str_chirho}")
        print(f"      Reference: {ref_explanation_chirho[:120]}...")
        print(f"      Generated: {generated_chirho[:120]}...")
        print()

    print(f"  Generated {generated_count_chirho} explanations for manual review.")
    print("  (Explainer quality is best assessed by human review of theological accuracy)")


def main_chirho():
    """Run full assessment pipeline."""
    print("Theological Guardrails - Full Assessment")
    print("=" * 60)

    config_chirho = load_config_chirho()
    test_data_chirho = load_test_data_chirho()
    print(f"Loaded {len(test_data_chirho)} test examples")

    assess_classifier_chirho(config_chirho, test_data_chirho)
    assess_embedder_chirho(config_chirho, test_data_chirho)
    assess_explainer_chirho(config_chirho, test_data_chirho)

    print("\n" + "=" * 60)
    print("Assessment complete!")


if __name__ == "__main__":
    main_chirho()
