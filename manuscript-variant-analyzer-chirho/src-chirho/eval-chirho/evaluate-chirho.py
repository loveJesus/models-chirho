# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""Evaluate manuscript variant classifier on test set."""

import json
import os
import numpy as np
import torch
from collections import Counter
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def main_chirho():
    """Run evaluation."""
    print("=" * 60)
    print("Manuscript Variant Classifier Evaluation")
    print("=" * 60)

    # Paths
    model_dir_chirho = os.path.join(os.path.dirname(__file__), "../../models-chirho/classifier-chirho/best-chirho")
    test_path_chirho = os.path.join(os.path.dirname(__file__), "../../data-chirho/processed-chirho/test-variant-chirho.jsonl")

    # Load model
    device_chirho = "cuda" if torch.cuda.is_available() else "mps" if hasattr(torch.backends, "mps") and torch.backends.mps.is_available() else "cpu"
    print(f"Device: {device_chirho}")

    tokenizer_chirho = AutoTokenizer.from_pretrained(model_dir_chirho)
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(model_dir_chirho).to(device_chirho)
    model_chirho.eval()

    # Load test data
    examples_chirho = []
    with open(test_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if line_chirho.strip():
                examples_chirho.append(json.loads(line_chirho))

    print(f"Test examples: {len(examples_chirho)}")

    # Predict in batches
    batch_size_chirho = 32
    predictions_chirho = []
    labels_chirho = []

    for i_chirho in range(0, len(examples_chirho), batch_size_chirho):
        batch_chirho = examples_chirho[i_chirho:i_chirho + batch_size_chirho]
        inputs_chirho = [ex_chirho["input_chirho"] for ex_chirho in batch_chirho]
        targets_chirho = [ex_chirho["target_chirho"] for ex_chirho in batch_chirho]

        encoded_chirho = tokenizer_chirho(inputs_chirho, return_tensors="pt", padding=True, truncation=True, max_length=256).to(device_chirho)

        with torch.no_grad():
            output_ids_chirho = model_chirho.generate(**encoded_chirho, max_length=128)

        decoded_chirho = tokenizer_chirho.batch_decode(output_ids_chirho, skip_special_tokens=True)
        predictions_chirho.extend(decoded_chirho)
        labels_chirho.extend(targets_chirho)

        if (i_chirho // batch_size_chirho) % 10 == 0:
            print(f"  Batch {i_chirho // batch_size_chirho + 1}/{(len(examples_chirho) + batch_size_chirho - 1) // batch_size_chirho}")

    # Compute metrics
    def extract_type_chirho(text_chirho):
        for part_chirho in text_chirho.split("|"):
            if "type:" in part_chirho:
                return part_chirho.strip().replace("type:", "").strip()
        return "unknown"

    exact_match_chirho = sum(1 for p, l in zip(predictions_chirho, labels_chirho) if p.strip() == l.strip()) / len(predictions_chirho)

    pred_types_chirho = [extract_type_chirho(p) for p in predictions_chirho]
    label_types_chirho = [extract_type_chirho(l) for l in labels_chirho]

    type_accuracy_chirho = sum(1 for p, l in zip(pred_types_chirho, label_types_chirho) if p == l) / len(pred_types_chirho)

    # Per-type breakdown
    type_results_chirho = {}
    for pred_chirho, label_chirho in zip(pred_types_chirho, label_types_chirho):
        if label_chirho not in type_results_chirho:
            type_results_chirho[label_chirho] = {"correct_chirho": 0, "total_chirho": 0}
        type_results_chirho[label_chirho]["total_chirho"] += 1
        if pred_chirho == label_chirho:
            type_results_chirho[label_chirho]["correct_chirho"] += 1

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Exact match: {exact_match_chirho:.4f}")
    print(f"  Type accuracy: {type_accuracy_chirho:.4f}")
    print(f"\nPer-type accuracy:")
    for type_chirho, counts_chirho in sorted(type_results_chirho.items()):
        acc_chirho = counts_chirho["correct_chirho"] / max(counts_chirho["total_chirho"], 1)
        print(f"  {type_chirho}: {acc_chirho:.4f} ({counts_chirho['correct_chirho']}/{counts_chirho['total_chirho']})")

    # Show sample predictions
    print(f"\nSample predictions:")
    for i_chirho in range(min(5, len(predictions_chirho))):
        print(f"  Input: {examples_chirho[i_chirho]['input_chirho'][:100]}...")
        print(f"  Pred:  {predictions_chirho[i_chirho][:80]}")
        print(f"  Label: {labels_chirho[i_chirho][:80]}")
        print()


if __name__ == "__main__":
    main_chirho()
