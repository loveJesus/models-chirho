# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
app.py - HuggingFace Space for the Passage Difficulty Scorer & Simplifier.
Loads the fine-tuned Flan-T5-base (248M params) from HuggingFace Hub and provides
a Gradio interface with two tabs: Simplify and Difficulty.
"""

import gradio as gr
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# HuggingFace model ID
MODEL_ID_CHIRHO = "LoveJesus/passage-difficulty-simplifier-chirho"

MAX_INPUT_LENGTH_CHIRHO = 256
MAX_TARGET_LENGTH_CHIRHO = 256

# Global model holders
model_chirho = None
tokenizer_chirho = None
device_chirho = None


def load_model_chirho():
    """Load the Flan-T5-base dual-task model from HuggingFace Hub."""
    global model_chirho, tokenizer_chirho, device_chirho

    # Device detection
    if torch.cuda.is_available():
        device_chirho = torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = torch.device("cpu")  # Use CPU for Gradio to avoid MPS issues
    else:
        device_chirho = torch.device("cpu")

    print(f"Using device: {device_chirho}")

    print("Loading model...")
    tokenizer_chirho = AutoTokenizer.from_pretrained(MODEL_ID_CHIRHO)
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID_CHIRHO)
    model_chirho.to(device_chirho)
    model_chirho.eval()

    param_count_chirho = sum(p_chirho.numel() for p_chirho in model_chirho.parameters())
    print(f"Model loaded: {param_count_chirho:,} parameters")


def generate_chirho(input_text_chirho: str) -> str:
    """Generate output from the model."""
    inputs_chirho = tokenizer_chirho(
        input_text_chirho,
        return_tensors="pt",
        max_length=MAX_INPUT_LENGTH_CHIRHO,
        truncation=True,
    )
    inputs_chirho = {
        k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in inputs_chirho.items()
    }

    with torch.no_grad():
        outputs_chirho = model_chirho.generate(
            **inputs_chirho,
            max_length=MAX_TARGET_LENGTH_CHIRHO,
            num_beams=4,
            early_stopping=True,
        )

    result_chirho = tokenizer_chirho.decode(outputs_chirho[0], skip_special_tokens=True)
    return result_chirho


# ─── Tab 1: Simplify ───

def simplify_verse_chirho(text_chirho: str) -> str:
    """Simplify a Bible verse into plain language."""
    if not text_chirho.strip():
        return "Please enter a verse to simplify."

    input_text_chirho = f"simplify: {text_chirho.strip()}"
    result_chirho = generate_chirho(input_text_chirho)
    return result_chirho


# ─── Tab 2: Difficulty ───

def rate_difficulty_chirho(text_chirho: str) -> tuple:
    """Rate the reading difficulty of a Bible passage."""
    if not text_chirho.strip():
        return "Please enter a verse to analyze.", "", "", ""

    input_text_chirho = f"rate difficulty: {text_chirho.strip()}"
    raw_result_chirho = generate_chirho(input_text_chirho)

    # Parse structured output
    reading_level_chirho = "N/A"
    vocab_complexity_chirho = "N/A"
    archaic_forms_chirho = "N/A"
    difficulty_chirho = "N/A"

    import re

    rl_match_chirho = re.search(r"reading_level:\s*(\d+)", raw_result_chirho)
    if rl_match_chirho:
        level_chirho = int(rl_match_chirho.group(1))
        grade_labels_chirho = {
            1: "Grade 1 (Age 6-7)",
            2: "Grade 2 (Age 7-8)",
            3: "Grade 3 (Age 8-9)",
            4: "Grade 4 (Age 9-10)",
            5: "Grade 5 (Age 10-11)",
            6: "Grade 6 (Age 11-12)",
            7: "Grade 7 (Age 12-13)",
            8: "Grade 8 (Age 13-14)",
            9: "Grade 9 (Age 14-15)",
            10: "Grade 10 (Age 15-16)",
            11: "Grade 11 (Age 16-17)",
            12: "Grade 12+ (Age 17+)",
        }
        reading_level_chirho = grade_labels_chirho.get(level_chirho, f"Grade {level_chirho}")

    vc_match_chirho = re.search(r"vocab_complexity:\s*(\w+)", raw_result_chirho)
    if vc_match_chirho:
        vc_val_chirho = vc_match_chirho.group(1)
        vc_labels_chirho = {
            "low": "Low - Common everyday words",
            "medium": "Medium - Some specialized vocabulary",
            "high": "High - Many uncommon or archaic terms",
        }
        vocab_complexity_chirho = vc_labels_chirho.get(vc_val_chirho, vc_val_chirho)

    af_match_chirho = re.search(r"archaic_forms:\s*(\d+)", raw_result_chirho)
    if af_match_chirho:
        af_count_chirho = int(af_match_chirho.group(1))
        if af_count_chirho == 0:
            archaic_forms_chirho = "None detected"
        elif af_count_chirho <= 2:
            archaic_forms_chirho = f"{af_count_chirho} (few)"
        else:
            archaic_forms_chirho = f"{af_count_chirho} (many)"

    df_match_chirho = re.search(r"difficulty:\s*(\w+)", raw_result_chirho)
    if df_match_chirho:
        df_val_chirho = df_match_chirho.group(1)
        df_labels_chirho = {
            "easy": "Easy - Accessible to most readers",
            "medium": "Medium - May require some familiarity with biblical language",
            "hard": "Hard - Contains archaic or complex language",
        }
        difficulty_chirho = df_labels_chirho.get(df_val_chirho, df_val_chirho)

    return reading_level_chirho, vocab_complexity_chirho, archaic_forms_chirho, difficulty_chirho


# ─── Build Gradio Interface ───

def build_demo_chirho() -> gr.Blocks:
    """Build the Gradio demo with two tabs."""
    with gr.Blocks(
        title="Passage Difficulty Scorer & Simplifier - loveJesus/models-chirho",
        theme=gr.themes.Soft(),
    ) as demo_chirho:
        gr.Markdown("# Passage Difficulty Scorer & Plain-Language Simplifier")
        gr.Markdown(
            "*For God so loved the world that he gave his only begotten Son, "
            "that whoever believes in him should not perish but have eternal life. - John 3:16*"
        )
        gr.Markdown(
            "A fine-tuned **Flan-T5-base** (248M params) model for two tasks: "
            "(1) assessing Bible passage reading difficulty, and "
            "(2) simplifying archaic or complex passages into plain modern English. "
            "Trained on KJV, BBE, OEB, ASV, YLT, and Darby translations."
        )

        with gr.Tab("Simplify"):
            gr.Markdown("### Simplify Bible Passages")
            gr.Markdown(
                "Enter a Bible verse (especially from KJV, ASV, YLT, or Darby) "
                "and receive a plain-language version."
            )

            simplify_input_chirho = gr.Textbox(
                label="Original Verse",
                placeholder="Enter a Bible verse to simplify...",
                lines=3,
            )
            simplify_btn_chirho = gr.Button("Simplify", variant="primary")
            simplify_output_chirho = gr.Textbox(
                label="Simplified Version",
                lines=3,
                interactive=False,
            )

            simplify_btn_chirho.click(
                simplify_verse_chirho,
                inputs=[simplify_input_chirho],
                outputs=[simplify_output_chirho],
            )

            gr.Examples(
                examples=[
                    [
                        "For God so loved the world, that he gave his only begotten Son, "
                        "that whosoever believeth in him should not perish, but have everlasting life."
                    ],
                    [
                        "And the LORD God formed man of the dust of the ground, and breathed "
                        "into his nostrils the breath of life; and man became a living soul."
                    ],
                    [
                        "Wherefore, as by one man sin entered into the world, and death by sin; "
                        "and so death passed upon all men, for that all have sinned:"
                    ],
                    [
                        "Blessed are the poor in spirit: for theirs is the kingdom of heaven."
                    ],
                    [
                        "But the fruit of the Spirit is love, joy, peace, longsuffering, "
                        "gentleness, goodness, faith, Meekness, temperance: against such there is no law."
                    ],
                    [
                        "In the beginning was the Word, and the Word was with God, "
                        "and the Word was God."
                    ],
                    [
                        "Verily, verily, I say unto thee, Except a man be born again, "
                        "he cannot see the kingdom of God."
                    ],
                    [
                        "For all have sinned, and come short of the glory of God;"
                    ],
                ],
                inputs=[simplify_input_chirho],
            )

        with gr.Tab("Difficulty"):
            gr.Markdown("### Assess Passage Difficulty")
            gr.Markdown(
                "Enter a Bible verse to get its reading level, vocabulary complexity, "
                "archaic form count, and overall difficulty rating."
            )

            difficulty_input_chirho = gr.Textbox(
                label="Verse Text",
                placeholder="Enter a Bible verse to assess difficulty...",
                lines=3,
            )
            difficulty_btn_chirho = gr.Button("Assess Difficulty", variant="primary")

            with gr.Row():
                reading_level_output_chirho = gr.Textbox(
                    label="Reading Level", interactive=False
                )
                difficulty_output_chirho = gr.Textbox(
                    label="Overall Difficulty", interactive=False
                )

            with gr.Row():
                vocab_output_chirho = gr.Textbox(
                    label="Vocabulary Complexity", interactive=False
                )
                archaic_output_chirho = gr.Textbox(
                    label="Archaic Forms", interactive=False
                )

            difficulty_btn_chirho.click(
                rate_difficulty_chirho,
                inputs=[difficulty_input_chirho],
                outputs=[
                    reading_level_output_chirho,
                    vocab_output_chirho,
                    archaic_output_chirho,
                    difficulty_output_chirho,
                ],
            )

            gr.Examples(
                examples=[
                    [
                        "In the beginning God created the heaven and the earth."
                    ],
                    [
                        "For God so loved the world, that he gave his only begotten Son, "
                        "that whosoever believeth in him should not perish, but have everlasting life."
                    ],
                    [
                        "God is love."
                    ],
                    [
                        "And the LORD God formed man of the dust of the ground, "
                        "and breathed into his nostrils the breath of life; "
                        "and man became a living soul."
                    ],
                    [
                        "Wherefore seeing we also are compassed about with so great a cloud "
                        "of witnesses, let us lay aside every weight, and the sin which doth "
                        "so easily beset us, and let us run with patience the race that is set before us,"
                    ],
                    [
                        "Jesus wept."
                    ],
                ],
                inputs=[difficulty_input_chirho],
            )

        with gr.Tab("About"):
            gr.Markdown("""# Passage Difficulty Scorer & Plain-Language Simplifier

## What This Does
This model performs two tasks on Bible passages:

### 1. Difficulty Scoring
Analyzes a passage and outputs:
- **Reading Level** (Grade 1-12): Approximate grade level needed to understand the text
- **Vocabulary Complexity** (Low/Medium/High): How many uncommon or specialized words
- **Archaic Forms**: Count of archaic English words (thee, thou, hath, etc.)
- **Overall Difficulty** (Easy/Medium/Hard): Combined difficulty assessment

### 2. Simplification
Converts archaic or complex Bible passages into plain modern English, trained on:
- **KJV -> BBE**: King James Version to Bible in Basic English (850-word vocabulary)
- **KJV -> WEB**: King James Version to World English Bible (modern)
- **ASV -> BBE**: American Standard Version to Basic English
- **YLT -> WEB**: Young's Literal Translation to modern English

## Model Details
- **Base Model**: google/flan-t5-base (248M parameters)
- **Training**: Multi-task learning with both tasks, 5 epochs on NVIDIA H200
- **Data**: ~160K examples from 6 public-domain Bible translations
- **Eval Loss**: 2.228 | **Difficulty Accuracy**: 93.8%
- **Source**: ScrollMapper Bible Databases (GitHub)

## Translations Used
| Translation | Style | Role |
|---|---|---|
| KJV (King James Version) | Formal, archaic | Complex source |
| ASV (American Standard Version) | Formal, dated | Complex source |
| YLT (Young's Literal Translation) | Ultra-literal | Complex source |
| Darby Bible | Literal, dated | Complex source |
| BBE (Bible in Basic English) | 850-word vocabulary, Grade 4 | Simple target |
| OEB (Open English Bible) | Modern, public domain | Simple target |

## Limitations
- Trained only on Bible text; may not generalize well to other domains
- Simplification quality varies by verse length and complexity
- Difficulty scoring is based on algorithmic features, not human annotation
- Simplification may occasionally alter theological nuance; always verify against original text

---
Built with love for Jesus. Published by [loveJesus](https://huggingface.co/LoveJesus).
""")

    return demo_chirho


# Load model at startup
load_model_chirho()

# Launch
demo_chirho = build_demo_chirho()
demo_chirho.launch()
