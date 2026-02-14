# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
app.py - HuggingFace Space for the Biblical Language Tutor.
Loads parser + glosser mT5 models from HuggingFace Hub.
Tabs: Parse Word, Interlinear, Explore, About.
"""

import gradio as gr
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# HuggingFace model IDs
PARSER_ID_CHIRHO = "LoveJesus/biblical-parser-chirho"
GLOSSER_ID_CHIRHO = "LoveJesus/biblical-glosser-chirho"

# Global model holders
parser_model_chirho = None
parser_tokenizer_chirho = None
glosser_model_chirho = None
glosser_tokenizer_chirho = None
device_chirho = None

# Sample verses for the Explore tab
SAMPLE_VERSES_CHIRHO = {
    "GEN 1:1 (Hebrew)": {
        "lang_chirho": "hebrew",
        "text_chirho": "בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
        "ref_chirho": "GEN 1:1",
    },
    "PSA 23:1 (Hebrew)": {
        "lang_chirho": "hebrew",
        "text_chirho": "יְהוָה רֹעִי לֹא אֶחְסָר",
        "ref_chirho": "PSA 23:1",
    },
    "ISA 53:5 (Hebrew)": {
        "lang_chirho": "hebrew",
        "text_chirho": "וְהוּא מְחֹלָל מִפְּשָׁעֵנוּ מְדֻכָּא מֵעֲוֺנֹתֵינוּ",
        "ref_chirho": "ISA 53:5",
    },
    "MAT 1:1 (Greek)": {
        "lang_chirho": "greek",
        "text_chirho": "Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυὶδ υἱοῦ Ἀβραάμ",
        "ref_chirho": "MAT 1:1",
    },
    "JHN 1:1 (Greek)": {
        "lang_chirho": "greek",
        "text_chirho": "Ἐν ἀρχῇ ἦν ὁ λόγος καὶ ὁ λόγος ἦν πρὸς τὸν θεόν καὶ θεὸς ἦν ὁ λόγος",
        "ref_chirho": "JHN 1:1",
    },
    "JHN 3:16 (Greek)": {
        "lang_chirho": "greek",
        "text_chirho": "Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον ὥστε τὸν υἱὸν τὸν μονογενῆ ἔδωκεν",
        "ref_chirho": "JHN 3:16",
    },
    "ROM 8:28 (Greek)": {
        "lang_chirho": "greek",
        "text_chirho": "οἴδαμεν δὲ ὅτι τοῖς ἀγαπῶσιν τὸν θεὸν πάντα συνεργεῖ εἰς ἀγαθόν",
        "ref_chirho": "ROM 8:28",
    },
    "REV 21:1 (Greek)": {
        "lang_chirho": "greek",
        "text_chirho": "Καὶ εἶδον οὐρανὸν καινὸν καὶ γῆν καινήν",
        "ref_chirho": "REV 21:1",
    },
}


def load_models_chirho():
    """Load both models from HuggingFace Hub."""
    global parser_model_chirho, parser_tokenizer_chirho
    global glosser_model_chirho, glosser_tokenizer_chirho, device_chirho

    # Device
    if torch.cuda.is_available():
        device_chirho = torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = torch.device("mps")
    else:
        device_chirho = torch.device("cpu")
    print(f"Using device: {device_chirho}")

    # Parser
    print("Loading parser model...")
    parser_tokenizer_chirho = AutoTokenizer.from_pretrained(PARSER_ID_CHIRHO)
    parser_model_chirho = AutoModelForSeq2SeqLM.from_pretrained(PARSER_ID_CHIRHO)
    parser_model_chirho.to(device_chirho)
    parser_model_chirho.eval()

    # Glosser
    print("Loading glosser model...")
    glosser_tokenizer_chirho = AutoTokenizer.from_pretrained(GLOSSER_ID_CHIRHO)
    glosser_model_chirho = AutoModelForSeq2SeqLM.from_pretrained(GLOSSER_ID_CHIRHO)
    glosser_model_chirho.to(device_chirho)
    glosser_model_chirho.eval()

    print("All models loaded!")


def generate_chirho(
    model_chirho, tokenizer_chirho, input_text_chirho: str, max_length_chirho: int = 128
) -> str:
    """Generate output from a model."""
    inputs_chirho = tokenizer_chirho(
        input_text_chirho, return_tensors="pt", max_length=max_length_chirho, truncation=True
    )
    inputs_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

    with torch.no_grad():
        output_ids_chirho = model_chirho.generate(**inputs_chirho, max_length=max_length_chirho)

    return tokenizer_chirho.decode(output_ids_chirho[0], skip_special_tokens=True)


# ─── Tab Functions ───

def parse_word_tab_chirho(
    word_chirho: str, language_chirho: str, reference_chirho: str, context_chirho: str
) -> str:
    """Tab 1: Parse a single word."""
    if not word_chirho.strip():
        return "Please enter a word to parse."

    lang_label_chirho = language_chirho.lower()
    ref_chirho = reference_chirho.strip() if reference_chirho.strip() else "?"
    ctx_chirho = context_chirho.strip() if context_chirho.strip() else ""

    input_text_chirho = f"parse [{lang_label_chirho}]: {word_chirho.strip()} [{ref_chirho}]"
    if ctx_chirho:
        input_text_chirho += f" context: {ctx_chirho}"

    result_chirho = generate_chirho(parser_model_chirho, parser_tokenizer_chirho, input_text_chirho)

    # Format output as a table
    tags_chirho = [t_chirho.strip() for t_chirho in result_chirho.split("|")]
    lines_chirho = [f"**Input:** `{input_text_chirho}`\n", "| Tag | Value |", "| --- | --- |"]

    for tag_chirho in tags_chirho:
        if ":" in tag_chirho:
            key_chirho, value_chirho = tag_chirho.split(":", 1)
            lines_chirho.append(f"| **{key_chirho.strip()}** | {value_chirho.strip()} |")
        else:
            lines_chirho.append(f"| | {tag_chirho} |")

    return "\n".join(lines_chirho)


def interlinear_tab_chirho(verse_text_chirho: str, language_chirho: str, reference_chirho: str) -> str:
    """Tab 2: Generate interlinear gloss for a verse."""
    if not verse_text_chirho.strip():
        return "Please enter a verse in Hebrew or Greek."

    lang_label_chirho = language_chirho.lower()
    ref_chirho = reference_chirho.strip() if reference_chirho.strip() else "?"

    input_text_chirho = f"gloss [{lang_label_chirho}]: {verse_text_chirho.strip()} [{ref_chirho}]"
    result_chirho = generate_chirho(
        glosser_model_chirho, glosser_tokenizer_chirho, input_text_chirho, max_length_chirho=256
    )

    # Build interlinear display
    original_words_chirho = verse_text_chirho.strip().split()
    gloss_words_chirho = [g_chirho.strip() for g_chirho in result_chirho.split("|")]

    lines_chirho = [
        f"**Reference:** {ref_chirho}\n",
        "| Original | Gloss |",
        "| --- | --- |",
    ]

    for i_chirho in range(max(len(original_words_chirho), len(gloss_words_chirho))):
        orig_chirho = original_words_chirho[i_chirho] if i_chirho < len(original_words_chirho) else ""
        gloss_chirho = gloss_words_chirho[i_chirho] if i_chirho < len(gloss_words_chirho) else ""
        lines_chirho.append(f"| {orig_chirho} | {gloss_chirho} |")

    return "\n".join(lines_chirho)


def explore_tab_chirho(verse_selection_chirho: str) -> str:
    """Tab 3: Explore a pre-loaded verse with both parsing and glossing."""
    if not verse_selection_chirho or verse_selection_chirho not in SAMPLE_VERSES_CHIRHO:
        return "Please select a verse."

    verse_chirho = SAMPLE_VERSES_CHIRHO[verse_selection_chirho]
    lang_chirho = verse_chirho["lang_chirho"]
    text_chirho = verse_chirho["text_chirho"]
    ref_chirho = verse_chirho["ref_chirho"]

    # Glossing
    gloss_input_chirho = f"gloss [{lang_chirho}]: {text_chirho} [{ref_chirho}]"
    gloss_result_chirho = generate_chirho(
        glosser_model_chirho, glosser_tokenizer_chirho, gloss_input_chirho, 256
    )

    # Build output
    lines_chirho = [
        f"## {ref_chirho}",
        f"**Original:** {text_chirho}\n",
        "### Interlinear Gloss",
    ]

    original_words_chirho = text_chirho.split()
    gloss_words_chirho = [g_chirho.strip() for g_chirho in gloss_result_chirho.split("|")]

    lines_chirho.append("| # | Original | Gloss |")
    lines_chirho.append("| --- | --- | --- |")
    for i_chirho in range(max(len(original_words_chirho), len(gloss_words_chirho))):
        orig_chirho = original_words_chirho[i_chirho] if i_chirho < len(original_words_chirho) else ""
        gloss_chirho = gloss_words_chirho[i_chirho] if i_chirho < len(gloss_words_chirho) else ""
        lines_chirho.append(f"| {i_chirho + 1} | {orig_chirho} | {gloss_chirho} |")

    # Parse first 3 words
    lines_chirho.append("\n### Word Parsing (first 3 words)")

    for word_chirho in original_words_chirho[:3]:
        parse_input_chirho = f"parse [{lang_chirho}]: {word_chirho} [{ref_chirho}] context: {' '.join(original_words_chirho[:5])}"
        parse_result_chirho = generate_chirho(
            parser_model_chirho, parser_tokenizer_chirho, parse_input_chirho
        )
        lines_chirho.append(f"\n**{word_chirho}**: {parse_result_chirho}")

    return "\n".join(lines_chirho)


# ─── Build Gradio Interface ───

def build_demo_chirho() -> gr.Blocks:
    """Build the Gradio demo."""
    with gr.Blocks(
        title="Biblical Language Tutor - loveJesus/models-chirho",
        theme=gr.themes.Soft(),
    ) as demo_chirho:
        gr.Markdown("# Biblical Language Tutor")
        gr.Markdown(
            "*For God so loved the world that he gave his only begotten Son, "
            "that whoever believes in him should not perish but have eternal life. - John 3:16*"
        )
        gr.Markdown(
            "**Morphological parsing** and **interlinear glossing** for biblical Hebrew and Greek. "
            "Two mT5-small models trained on the Macula treebank (~563K annotated words)."
        )

        with gr.Tab("Parse Word"):
            gr.Markdown("Enter a Hebrew or Greek word to see its morphological breakdown.")
            with gr.Row():
                word_input_chirho = gr.Textbox(label="Word", placeholder="בָּרָא or λόγος")
                lang_input_chirho = gr.Dropdown(
                    choices=["hebrew", "greek"], value="hebrew", label="Language"
                )
            with gr.Row():
                ref_input_chirho = gr.Textbox(
                    label="Reference (optional)", placeholder="GEN 1:1"
                )
                ctx_input_chirho = gr.Textbox(
                    label="Context (optional)", placeholder="בְּרֵאשִׁית אֱלֹהִים"
                )
            parse_btn_chirho = gr.Button("Parse Word", variant="primary")
            parse_output_chirho = gr.Markdown()

            parse_btn_chirho.click(
                parse_word_tab_chirho,
                inputs=[word_input_chirho, lang_input_chirho, ref_input_chirho, ctx_input_chirho],
                outputs=[parse_output_chirho],
            )

            gr.Examples(
                examples=[
                    ["בָּרָא", "hebrew", "GEN 1:1", "בְּרֵאשִׁית אֱלֹהִים"],
                    ["אֱלֹהִים", "hebrew", "GEN 1:1", "בָּרָא אֵת הַשָּׁמַיִם"],
                    ["λόγος", "greek", "JHN 1:1", "ἐν ἀρχῇ ἦν"],
                    ["ἠγάπησεν", "greek", "JHN 3:16", "οὕτως γὰρ ὁ θεὸς"],
                ],
                inputs=[word_input_chirho, lang_input_chirho, ref_input_chirho, ctx_input_chirho],
            )

        with gr.Tab("Interlinear"):
            gr.Markdown("Enter a verse in Hebrew or Greek to see word-by-word English glosses.")
            verse_input_chirho = gr.Textbox(
                label="Verse text (original language)",
                placeholder="בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
                lines=2,
            )
            with gr.Row():
                verse_lang_chirho = gr.Dropdown(
                    choices=["hebrew", "greek"], value="hebrew", label="Language"
                )
                verse_ref_chirho = gr.Textbox(label="Reference", placeholder="GEN 1:1")

            gloss_btn_chirho = gr.Button("Generate Interlinear", variant="primary")
            gloss_output_chirho = gr.Markdown()

            gloss_btn_chirho.click(
                interlinear_tab_chirho,
                inputs=[verse_input_chirho, verse_lang_chirho, verse_ref_chirho],
                outputs=[gloss_output_chirho],
            )

            gr.Examples(
                examples=[
                    [
                        "בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
                        "hebrew",
                        "GEN 1:1",
                    ],
                    [
                        "Ἐν ἀρχῇ ἦν ὁ λόγος καὶ ὁ λόγος ἦν πρὸς τὸν θεόν",
                        "greek",
                        "JHN 1:1",
                    ],
                    [
                        "Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον",
                        "greek",
                        "JHN 3:16",
                    ],
                ],
                inputs=[verse_input_chirho, verse_lang_chirho, verse_ref_chirho],
            )

        with gr.Tab("Explore"):
            gr.Markdown("Select a famous verse to see full parsing and glossing.")
            verse_select_chirho = gr.Dropdown(
                choices=list(SAMPLE_VERSES_CHIRHO.keys()),
                label="Select Verse",
                value="GEN 1:1 (Hebrew)",
            )
            explore_btn_chirho = gr.Button("Explore", variant="primary")
            explore_output_chirho = gr.Markdown()

            explore_btn_chirho.click(
                explore_tab_chirho,
                inputs=[verse_select_chirho],
                outputs=[explore_output_chirho],
            )

        with gr.Tab("About"):
            gr.Markdown("""# Biblical Language Tutor

## What This Does

This AI system provides **morphological parsing** and **interlinear glossing** for biblical Hebrew and Greek:

| Feature | Description |
| --- | --- |
| **Parse Word** | Analyze any Hebrew/Greek word: part of speech, stem, lemma, tense, person, gender, number |
| **Interlinear** | Generate word-by-word English glosses for full verses |
| **Explore** | Pre-loaded famous verses with full analysis |

## Two-Model Pipeline

1. **Parser** (mT5-small) — Morphological analysis of individual words
2. **Glosser** (mT5-small) — Word-by-word interlinear translation

Both models are based on Google's mT5-small (300M params), pre-trained on 101 languages including Hebrew and Greek.

## Training Data

- **Macula Hebrew** (Clear-Bible): ~425K OT words with morphology and glosses
- **Macula Greek SBLGNT** (Clear-Bible): ~138K NT words with morphology and glosses
- Total: ~563K annotated words from the complete Hebrew Bible and Greek New Testament

## Important Note

This is a **study tool** for exploring biblical languages. Always consult scholarly grammars, lexicons, and original language experts for serious exegetical work.

---

Built with love for Jesus. Published by [LoveJesus](https://huggingface.co/LoveJesus).
Part of the [bible.systems](https://bible.systems) project.

*Model 3 of 7 in the bible.systems ML pipeline.*
""")

    return demo_chirho


# Load models at startup
load_models_chirho()

# Launch
demo_chirho = build_demo_chirho()
demo_chirho.launch()
