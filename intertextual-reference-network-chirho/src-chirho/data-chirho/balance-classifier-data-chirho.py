# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
balance-classifier-data-chirho.py
Creates a balanced training set for the intertextual classifier.
Strategy:
  1. Load all available data (train + augmented).
  2. Deduplicate by (from_id, to_id) pair.
  3. Oversample minority classes to reach a target minimum (default 2000 per class).
  4. Cap majority class (thematic_parallel) to prevent domination.
  5. Output: balanced-train-classifier-chirho.jsonl
"""

import json
import random
from collections import defaultdict
from pathlib import Path

# Paths
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"

# Target: at least this many examples per minority class
MIN_PER_CLASS_CHIRHO = 2000
# Cap majority class to this ratio of the next largest class
MAX_MAJORITY_RATIO_CHIRHO = 3.0
# Random seed for reproducibility
SEED_CHIRHO = 42


def load_jsonl_chirho(path_chirho: Path) -> list[dict]:
    """Load JSONL file."""
    items_chirho = []
    with open(path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if line_chirho.strip():
                items_chirho.append(json.loads(line_chirho))
    return items_chirho


def main_chirho():
    """Create balanced training dataset."""
    random.seed(SEED_CHIRHO)
    print("=" * 60)
    print("Balancing Intertextual Classifier Training Data")
    print("=" * 60)

    # Load all available data
    train_data_chirho = load_jsonl_chirho(DATA_DIR_CHIRHO / "train-classifier-chirho.jsonl")
    augmented_data_chirho = load_jsonl_chirho(DATA_DIR_CHIRHO / "augmented-classifier-chirho.jsonl")

    print(f"Train data: {len(train_data_chirho)} examples")
    print(f"Augmented data: {len(augmented_data_chirho)} examples")

    # Combine and deduplicate by (from_id, to_id)
    seen_pairs_chirho = set()
    all_data_chirho = []
    for item_chirho in train_data_chirho + augmented_data_chirho:
        pair_key_chirho = (
            item_chirho.get("from_id_chirho", ""),
            item_chirho.get("to_id_chirho", ""),
        )
        if pair_key_chirho not in seen_pairs_chirho:
            seen_pairs_chirho.add(pair_key_chirho)
            all_data_chirho.append(item_chirho)

    print(f"After deduplication: {len(all_data_chirho)} unique examples")

    # Group by class
    by_class_chirho = defaultdict(list)
    for item_chirho in all_data_chirho:
        conn_type_chirho = item_chirho.get("connection_type_chirho", "thematic_parallel")
        by_class_chirho[conn_type_chirho].append(item_chirho)

    print("\nOriginal class distribution:")
    for class_name_chirho, items_chirho in sorted(
        by_class_chirho.items(), key=lambda x: -len(x[1])
    ):
        print(f"  {class_name_chirho}: {len(items_chirho)}")

    # Determine target sizes
    # Minority classes: oversample to MIN_PER_CLASS_CHIRHO
    # Majority class (thematic_parallel): cap to MAX_MAJORITY_RATIO_CHIRHO * second_largest
    class_sizes_chirho = {k_chirho: len(v_chirho) for k_chirho, v_chirho in by_class_chirho.items()}
    sorted_sizes_chirho = sorted(class_sizes_chirho.values(), reverse=True)
    second_largest_chirho = sorted_sizes_chirho[1] if len(sorted_sizes_chirho) > 1 else sorted_sizes_chirho[0]

    # After oversampling minority classes, the second largest will be at least MIN_PER_CLASS_CHIRHO
    effective_second_chirho = max(second_largest_chirho, MIN_PER_CLASS_CHIRHO)
    majority_cap_chirho = int(effective_second_chirho * MAX_MAJORITY_RATIO_CHIRHO)

    print(f"\nTarget: min {MIN_PER_CLASS_CHIRHO} per class, majority cap {majority_cap_chirho}")

    # Build balanced dataset
    balanced_data_chirho = []
    for class_name_chirho, items_chirho in by_class_chirho.items():
        current_count_chirho = len(items_chirho)

        if class_name_chirho == "thematic_parallel":
            # Cap majority class
            target_chirho = min(current_count_chirho, majority_cap_chirho)
            sampled_chirho = random.sample(items_chirho, target_chirho)
            action_chirho = f"downsampled {current_count_chirho} → {target_chirho}"
        elif current_count_chirho < MIN_PER_CLASS_CHIRHO:
            # Oversample minority class
            target_chirho = MIN_PER_CLASS_CHIRHO
            # Take all originals, then repeat-sample to fill
            sampled_chirho = list(items_chirho)
            remaining_chirho = target_chirho - current_count_chirho
            sampled_chirho.extend(random.choices(items_chirho, k=remaining_chirho))
            action_chirho = f"oversampled {current_count_chirho} → {target_chirho}"
        else:
            # Keep as-is
            sampled_chirho = list(items_chirho)
            action_chirho = f"kept {current_count_chirho}"

        balanced_data_chirho.extend(sampled_chirho)
        print(f"  {class_name_chirho}: {action_chirho}")

    # Shuffle
    random.shuffle(balanced_data_chirho)

    # Write output
    output_path_chirho = DATA_DIR_CHIRHO / "balanced-train-classifier-chirho.jsonl"
    with open(output_path_chirho, "w") as f_chirho:
        for item_chirho in balanced_data_chirho:
            f_chirho.write(json.dumps(item_chirho, ensure_ascii=False) + "\n")

    print(f"\nBalanced dataset: {len(balanced_data_chirho)} examples")
    print(f"Written to: {output_path_chirho}")

    # Verify final distribution
    final_counts_chirho = defaultdict(int)
    for item_chirho in balanced_data_chirho:
        final_counts_chirho[item_chirho.get("connection_type_chirho", "unknown")] += 1

    print("\nFinal class distribution:")
    total_chirho = len(balanced_data_chirho)
    for class_name_chirho, count_chirho in sorted(
        final_counts_chirho.items(), key=lambda x: -x[1]
    ):
        pct_chirho = 100 * count_chirho / total_chirho
        print(f"  {class_name_chirho}: {count_chirho} ({pct_chirho:.1f}%)")


if __name__ == "__main__":
    main_chirho()
