# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
app.py - HuggingFace Space for the Intertextual Reference Network.
Loads embedder + classifier from HuggingFace Hub for cross-reference discovery.
"""

import json

import gradio as gr
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# HuggingFace model IDs
EMBEDDER_ID_CHIRHO = "LoveJesus/intertextual-embedder-chirho"
CLASSIFIER_ID_CHIRHO = "LoveJesus/intertextual-classifier-chirho"
DATASET_ID_CHIRHO = "LoveJesus/intertextual-dataset-chirho"

LABELS_CHIRHO = [
    "direct_quote", "allusion", "thematic_parallel", "typological",
    "prophecy_fulfillment", "parallel_narrative", "contrast",
]

LABEL_DISPLAY_CHIRHO = {
    "direct_quote": "Direct Quote",
    "allusion": "Allusion",
    "thematic_parallel": "Thematic Parallel",
    "typological": "Typological",
    "prophecy_fulfillment": "Prophecy Fulfillment",
    "parallel_narrative": "Parallel Narrative",
    "contrast": "Contrast",
}

# Global model holders
embedder_chirho = None
classifier_chirho = None
classifier_tokenizer_chirho = None
verse_ids_chirho = []
verse_texts_chirho = []
verse_embeddings_chirho = None
device_chirho = None


def load_models_chirho():
    """Load both models from HuggingFace Hub."""
    global embedder_chirho, classifier_chirho, classifier_tokenizer_chirho
    global verse_ids_chirho, verse_texts_chirho, verse_embeddings_chirho, device_chirho

    # Device
    if torch.cuda.is_available():
        device_chirho = torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = torch.device("mps")
    else:
        device_chirho = torch.device("cpu")
    print(f"Using device: {device_chirho}")

    # Embedder
    print("Loading embedder...")
    embedder_chirho = SentenceTransformer(EMBEDDER_ID_CHIRHO, device=str(device_chirho))

    # Classifier
    print("Loading classifier...")
    classifier_tokenizer_chirho = AutoTokenizer.from_pretrained(CLASSIFIER_ID_CHIRHO)
    classifier_chirho = AutoModelForSequenceClassification.from_pretrained(CLASSIFIER_ID_CHIRHO)
    classifier_chirho.to(device_chirho)
    classifier_chirho.eval()

    # Load verse map from dataset repo
    print("Loading verse map...")
    try:
        from huggingface_hub import hf_hub_download
        verse_map_path_chirho = hf_hub_download(
            repo_id=DATASET_ID_CHIRHO,
            filename="verse-map-chirho.json",
            repo_type="dataset",
        )
        with open(verse_map_path_chirho, "r") as f_chirho:
            verse_map_chirho = json.load(f_chirho)
        verse_ids_chirho = list(verse_map_chirho.keys())
        verse_texts_chirho = list(verse_map_chirho.values())
        print(f"  Loaded {len(verse_ids_chirho)} verses")

        # Pre-encode all verses
        print("Encoding all verses (this takes a moment)...")
        verse_embeddings_chirho = embedder_chirho.encode(
            verse_texts_chirho,
            batch_size=256,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        print("  Index built!")
    except Exception as e_chirho:
        print(f"  Warning: Could not load verse map: {e_chirho}")
        print("  Find References tab will be unavailable.")

    print("All models loaded!")


def classify_pair_chirho(text_a_chirho: str, text_b_chirho: str) -> dict:
    """Classify connection type between two texts."""
    inputs_chirho = classifier_tokenizer_chirho(
        text_a_chirho, text_b_chirho,
        return_tensors="pt", truncation=True, max_length=256, padding=True,
    )
    inputs_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

    with torch.no_grad():
        outputs_chirho = classifier_chirho(**inputs_chirho)
        probs_chirho = torch.softmax(outputs_chirho.logits, dim=-1).cpu().numpy()[0]

    pred_idx_chirho = int(np.argmax(probs_chirho))
    return {
        "type_chirho": LABELS_CHIRHO[pred_idx_chirho],
        "confidence_chirho": float(probs_chirho[pred_idx_chirho]),
        "scores_chirho": {LABELS_CHIRHO[i_chirho]: float(probs_chirho[i_chirho]) for i_chirho in range(len(LABELS_CHIRHO))},
    }


# ─── Tab Functions ───

def find_references_tab_chirho(query_text_chirho: str, k_chirho: int = 10) -> str:
    """Tab 1: Find cross-references for a verse."""
    if not query_text_chirho.strip():
        return "Please enter a verse text."
    if verse_embeddings_chirho is None:
        return "Verse index not available. Please try again later."

    query_emb_chirho = embedder_chirho.encode(
        [query_text_chirho], normalize_embeddings=True, convert_to_numpy=True
    )[0]

    similarities_chirho = np.dot(verse_embeddings_chirho, query_emb_chirho)
    top_indices_chirho = np.argsort(similarities_chirho)[::-1][:int(k_chirho)]

    lines_chirho = ["| # | Verse | Similarity | Connection Type | Confidence |", "| --- | --- | --- | --- | --- |"]

    for rank_chirho, idx_chirho in enumerate(top_indices_chirho, 1):
        verse_id_chirho = verse_ids_chirho[idx_chirho]
        verse_text_chirho = verse_texts_chirho[idx_chirho][:80]
        sim_chirho = float(similarities_chirho[idx_chirho])

        cls_chirho = classify_pair_chirho(query_text_chirho, verse_texts_chirho[idx_chirho])
        type_display_chirho = LABEL_DISPLAY_CHIRHO.get(cls_chirho["type_chirho"], cls_chirho["type_chirho"])

        lines_chirho.append(
            f"| {rank_chirho} | **{verse_id_chirho}** {verse_text_chirho}... | {sim_chirho:.3f} | {type_display_chirho} | {cls_chirho['confidence_chirho']:.1%} |"
        )

    return "\n".join(lines_chirho)


def classify_pair_tab_chirho(text_a_chirho: str, text_b_chirho: str) -> tuple:
    """Tab 2: Classify connection between two verses."""
    if not text_a_chirho.strip() or not text_b_chirho.strip():
        return "Please enter both verses.", ""

    result_chirho = classify_pair_chirho(text_a_chirho, text_b_chirho)
    type_display_chirho = LABEL_DISPLAY_CHIRHO.get(result_chirho["type_chirho"], result_chirho["type_chirho"])
    main_result_chirho = f"**{type_display_chirho}** (confidence: {result_chirho['confidence_chirho']:.1%})"

    scores_lines_chirho = ["| Connection Type | Score |", "| --- | --- |"]
    for type_chirho, score_chirho in sorted(result_chirho["scores_chirho"].items(), key=lambda x: -x[1]):
        display_chirho = LABEL_DISPLAY_CHIRHO.get(type_chirho, type_chirho)
        bar_chirho = "=" * int(score_chirho * 20)
        scores_lines_chirho.append(f"| {display_chirho} | {score_chirho:.3f} {bar_chirho} |")

    return main_result_chirho, "\n".join(scores_lines_chirho)


def explore_tab_chirho(verse_id_chirho: str, k_chirho: int = 10) -> str:
    """Tab 3: Explore references for a specific verse ID."""
    if not verse_id_chirho.strip():
        return "Please enter a verse ID (e.g., Gen.1.1, John.3.16)."
    if verse_embeddings_chirho is None:
        return "Verse index not available."

    verse_id_chirho = verse_id_chirho.strip()
    if verse_id_chirho in verse_ids_chirho:
        idx_chirho = verse_ids_chirho.index(verse_id_chirho)
        query_text_chirho = verse_texts_chirho[idx_chirho]
        return f"**{verse_id_chirho}**: _{query_text_chirho}_\n\n" + find_references_tab_chirho(query_text_chirho, k_chirho)
    else:
        return f"Verse ID '{verse_id_chirho}' not found. Use OSIS format: Gen.1.1, Matt.5.3, Rev.21.1"


# ─── Build Gradio Interface ───

def build_demo_chirho() -> gr.Blocks:
    """Build the Gradio demo."""
    with gr.Blocks(
        title="Intertextual Reference Network - loveJesus/models-chirho",
        theme=gr.themes.Soft(),
    ) as demo_chirho:
        gr.Markdown("# Intertextual Reference Network")
        gr.Markdown(
            "*For God so loved the world that he gave his only begotten Son, "
            "that whoever believes in him should not perish but have eternal life. - John 3:16*"
        )
        gr.Markdown(
            "Discover **biblical cross-references** and classify their **connection types** "
            "using a two-model ML pipeline: MiniLM-L12 embedder + RoBERTa-base classifier. "
            "Trained on 344,799 cross-reference pairs from the Treasury of Scripture Knowledge."
        )

        with gr.Tab("Find References"):
            query_input_chirho = gr.Textbox(
                label="Enter verse text",
                placeholder="In the beginning God created the heaven and the earth.",
                lines=2,
            )
            k_input_chirho = gr.Slider(5, 25, value=10, step=1, label="Number of results")
            find_btn_chirho = gr.Button("Find Cross-References", variant="primary")
            find_output_chirho = gr.Markdown()

            find_btn_chirho.click(
                find_references_tab_chirho,
                inputs=[query_input_chirho, k_input_chirho],
                outputs=[find_output_chirho],
            )

            gr.Examples(
                examples=[
                    ["In the beginning God created the heaven and the earth."],
                    ["For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."],
                    ["The LORD is my shepherd; I shall not want."],
                    ["But thou, Bethlehem Ephratah, though thou be little among the thousands of Judah, yet out of thee shall he come forth unto me that is to be ruler in Israel."],
                ],
                inputs=[query_input_chirho],
            )

        with gr.Tab("Classify Pair"):
            pair_a_chirho = gr.Textbox(label="Verse A", lines=2, placeholder="Enter first verse...")
            pair_b_chirho = gr.Textbox(label="Verse B", lines=2, placeholder="Enter second verse...")
            classify_btn_chirho = gr.Button("Classify Connection")

            cls_result_chirho = gr.Markdown(label="Result")
            cls_scores_chirho = gr.Markdown(label="All Scores")

            classify_btn_chirho.click(
                classify_pair_tab_chirho,
                inputs=[pair_a_chirho, pair_b_chirho],
                outputs=[cls_result_chirho, cls_scores_chirho],
            )

            gr.Examples(
                examples=[
                    [
                        "Therefore the Lord himself shall give you a sign; Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel.",
                        "Now all this was done, that it might be fulfilled which was spoken of the Lord by the prophet, saying, Behold, a virgin shall be with child.",
                    ],
                    [
                        "The LORD is my shepherd; I shall not want.",
                        "I am the good shepherd: the good shepherd giveth his life for the sheep.",
                    ],
                    [
                        "For as in Adam all die, even so in Christ shall all be made alive.",
                        "Wherefore, as by one man sin entered into the world, and death by sin; and so death passed upon all men, for that all have sinned.",
                    ],
                ],
                inputs=[pair_a_chirho, pair_b_chirho],
            )

        with gr.Tab("Explore"):
            explore_input_chirho = gr.Textbox(
                label="Verse ID (OSIS format)",
                placeholder="Gen.1.1, John.3.16, Ps.23.1, Rev.21.1",
            )
            explore_k_chirho = gr.Slider(5, 25, value=10, step=1, label="Results")
            explore_btn_chirho = gr.Button("Explore")
            explore_output_chirho = gr.Markdown()
            explore_btn_chirho.click(
                explore_tab_chirho,
                inputs=[explore_input_chirho, explore_k_chirho],
                outputs=[explore_output_chirho],
            )

        with gr.Tab("About"):
            gr.Markdown("""# Intertextual Reference Network

## What This Does
This AI system discovers **cross-references** between Bible verses and classifies the **type of connection**:

| Type | Description | Example |
| --- | --- | --- |
| **Direct Quote** | NT directly quotes OT | Mt 1:23 quotes Is 7:14 |
| **Allusion** | Clear reference without direct quotation | Rev 5:5 alludes to Gen 49:9 |
| **Thematic Parallel** | Shared theme or motif | Ps 23 parallels Jn 10 |
| **Typological** | OT type foreshadows NT antitype | Isaac sacrifice prefigures Christ |
| **Prophecy Fulfillment** | OT prophecy fulfilled in NT | Is 53 fulfilled in Passion |
| **Parallel Narrative** | Same event in parallel accounts | Synoptic gospels |
| **Contrast** | Deliberate theological contrast | Adam vs Christ (Rom 5) |

## Two-Model Pipeline
1. **Embedder** (MiniLM-L12) — Encodes verses into semantic space for similarity search
2. **Classifier** (RoBERTa-base) — Classifies the connection type between verse pairs

## Training Data
- **344,799** cross-reference pairs from the Treasury of Scripture Knowledge (OpenBible.info)
- **31,102** KJV verses indexed for retrieval
- **28,612** Grok-labeled pairs for connection type classification

## Important Note
This is a **research tool** for exploring biblical intertextuality. Always consult scholarly commentaries and original languages for serious study.

---
Built with love for Jesus. Published by [loveJesus](https://huggingface.co/LoveJesus).
""")

    return demo_chirho


# Load models at startup
load_models_chirho()

# Launch
demo_chirho = build_demo_chirho()
demo_chirho.launch()
