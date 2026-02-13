# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
train-explainer-chirho.py
Fine-tunes Flan-T5-base to generate human-readable explanations
of why a statement is heterodox, citing relevant creeds and scripture.
"""

import json
from pathlib import Path

import torch
import yaml
from datasets import Dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

# Paths
BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH_CHIRHO = BASE_DIR_CHIRHO / "src-chirho" / "train-chirho" / "config-chirho.yaml"
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho"
OUTPUT_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "explainer-chirho"


def load_config_chirho() -> dict:
    """Load training configuration."""
    with open(CONFIG_PATH_CHIRHO, "r") as f_chirho:
        return yaml.safe_load(f_chirho)


def load_explanation_pairs_chirho(split_name_chirho: str) -> list[dict]:
    """Load dataset and build input/output pairs for explanation generation."""
    file_path_chirho = DATA_DIR_CHIRHO / f"{split_name_chirho}-chirho.jsonl"
    pairs_chirho = []

    with open(file_path_chirho, "r") as f_chirho:
        for line_chirho in f_chirho:
            if not line_chirho.strip():
                continue
            item_chirho = json.loads(line_chirho)

            text_chirho = item_chirho.get("text_chirho", "")
            label_chirho = item_chirho.get("label_chirho", "")
            heresy_types_chirho = item_chirho.get("heresy_types_chirho", [])
            explanation_chirho = item_chirho.get("explanation_chirho", "")
            scripture_refs_chirho = item_chirho.get("scripture_refs_chirho", [])
            creed_refs_chirho = item_chirho.get("creed_refs_chirho", [])

            if not explanation_chirho:
                continue

            # Build input format
            heresy_str_chirho = ", ".join(heresy_types_chirho) if heresy_types_chirho else "none"
            input_text_chirho = (
                f"explain theological classification: {text_chirho} | "
                f"label: {label_chirho} | "
                f"heresy types: {heresy_str_chirho}"
            )

            # Build target: explanation with references
            refs_str_chirho = ""
            if scripture_refs_chirho:
                refs_str_chirho += f" Scripture: {', '.join(scripture_refs_chirho)}."
            if creed_refs_chirho:
                refs_str_chirho += f" Creeds: {', '.join(creed_refs_chirho)}."

            output_text_chirho = f"{explanation_chirho}{refs_str_chirho}"

            pairs_chirho.append({
                "input_text_chirho": input_text_chirho,
                "target_text_chirho": output_text_chirho,
            })

    return pairs_chirho


def main_chirho():
    """Main training loop for the theological explainer."""
    print("=" * 60)
    print("Theological Explainer Training (Flan-T5-base)")
    print("=" * 60)

    config_chirho = load_config_chirho()
    explainer_config_chirho = config_chirho["explainer_chirho"]

    model_name_chirho = explainer_config_chirho["model_name_chirho"]
    print(f"Model: {model_name_chirho}")

    # Device
    if torch.backends.mps.is_available():
        device_chirho = "mps"
        print("Using Apple MPS")
    elif torch.cuda.is_available():
        device_chirho = "cuda"
        print("Using CUDA")
    else:
        device_chirho = "cpu"
        print("Using CPU")

    # Load tokenizer and model
    print("\nLoading tokenizer and model...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(model_name_chirho)
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(model_name_chirho)

    # Load data
    print("Loading datasets...")
    train_pairs_chirho = load_explanation_pairs_chirho("train")
    val_pairs_chirho = load_explanation_pairs_chirho("val")

    print(f"  Train pairs: {len(train_pairs_chirho)}")
    print(f"  Val pairs: {len(val_pairs_chirho)}")

    # Convert to HuggingFace datasets
    train_dataset_chirho = Dataset.from_dict({
        "input_text_chirho": [p_chirho["input_text_chirho"] for p_chirho in train_pairs_chirho],
        "target_text_chirho": [p_chirho["target_text_chirho"] for p_chirho in train_pairs_chirho],
    })
    val_dataset_chirho = Dataset.from_dict({
        "input_text_chirho": [p_chirho["input_text_chirho"] for p_chirho in val_pairs_chirho],
        "target_text_chirho": [p_chirho["target_text_chirho"] for p_chirho in val_pairs_chirho],
    })

    max_input_len_chirho = explainer_config_chirho["max_input_length_chirho"]
    max_output_len_chirho = explainer_config_chirho["max_output_length_chirho"]

    def preprocess_function_chirho(examples_chirho):
        model_inputs_chirho = tokenizer_chirho(
            examples_chirho["input_text_chirho"],
            max_length=max_input_len_chirho,
            truncation=True,
        )
        labels_chirho = tokenizer_chirho(
            text_target=examples_chirho["target_text_chirho"],
            max_length=max_output_len_chirho,
            truncation=True,
        )
        model_inputs_chirho["labels"] = labels_chirho["input_ids"]
        return model_inputs_chirho

    print("Tokenizing datasets...")
    train_dataset_chirho = train_dataset_chirho.map(
        preprocess_function_chirho,
        batched=True,
        remove_columns=["input_text_chirho", "target_text_chirho"],
    )
    val_dataset_chirho = val_dataset_chirho.map(
        preprocess_function_chirho,
        batched=True,
        remove_columns=["input_text_chirho", "target_text_chirho"],
    )

    # Data collator
    data_collator_chirho = DataCollatorForSeq2Seq(
        tokenizer_chirho, model=model_chirho, label_pad_token_id=-100
    )

    # Training arguments
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    training_args_chirho = Seq2SeqTrainingArguments(
        output_dir=str(OUTPUT_DIR_CHIRHO),
        num_train_epochs=explainer_config_chirho["num_epochs_chirho"],
        per_device_train_batch_size=explainer_config_chirho["batch_size_chirho"],
        per_device_eval_batch_size=explainer_config_chirho["batch_size_chirho"],
        learning_rate=explainer_config_chirho["learning_rate_chirho"],
        warmup_steps=100,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="loss",
        greater_is_better=False,
        predict_with_generate=True,
        generation_max_length=max_output_len_chirho,
        logging_steps=50,
        save_total_limit=3,
        fp16=False,  # MPS compatibility
        dataloader_pin_memory=False if device_chirho == "mps" else True,
        report_to="none",
        seed=42,
    )

    # Trainer
    trainer_chirho = Seq2SeqTrainer(
        model=model_chirho,
        args=training_args_chirho,
        train_dataset=train_dataset_chirho,
        eval_dataset=val_dataset_chirho,
        data_collator=data_collator_chirho,
        tokenizer=tokenizer_chirho,
    )

    # Train
    print(f"\nStarting training for {explainer_config_chirho['num_epochs_chirho']} epochs...")
    train_result_chirho = trainer_chirho.train()

    print("\nTraining complete!")
    print(f"  Training loss: {train_result_chirho.training_loss:.4f}")

    # Save best model
    best_model_dir_chirho = OUTPUT_DIR_CHIRHO / "best-chirho"
    trainer_chirho.save_model(str(best_model_dir_chirho))
    tokenizer_chirho.save_pretrained(str(best_model_dir_chirho))

    print(f"\nModel saved to: {best_model_dir_chirho}")

    # Demo: generate a few explanations
    print("\n--- Demo Explanations ---")
    demo_inputs_chirho = [
        "explain theological classification: Jesus is a created being, the first of God's creations. | label: heterodox | heresy types: arianism",
        "explain theological classification: Christ is fully God and fully man, two natures in one person. | label: orthodox | heresy types: none",
        "explain theological classification: The Father himself suffered on the cross. | label: heterodox | heresy types: patripassianism",
    ]

    model_chirho.to(device_chirho)
    for input_chirho in demo_inputs_chirho:
        inputs_chirho = tokenizer_chirho(
            input_chirho, return_tensors="pt", max_length=max_input_len_chirho, truncation=True
        )
        inputs_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

        with torch.no_grad():
            outputs_chirho = model_chirho.generate(
                **inputs_chirho,
                max_length=max_output_len_chirho,
                num_beams=4,
                early_stopping=True,
            )
        decoded_chirho = tokenizer_chirho.decode(outputs_chirho[0], skip_special_tokens=True)
        print(f"\n  Input: {input_chirho[:80]}...")
        print(f"  Output: {decoded_chirho}")


if __name__ == "__main__":
    main_chirho()
