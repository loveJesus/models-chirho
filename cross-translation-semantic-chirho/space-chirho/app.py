# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
Gradio Space for Cross-Translation Semantic Model
Compare Bible verses across translations using embedding similarity.
"""

import gradio as gr
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

MODEL_ID_CHIRHO = "LoveJesus/biblical-cross-translation-chirho"

model_chirho = None


def load_model_chirho():
    """Load model on first use."""
    global model_chirho
    if model_chirho is not None:
        return

    device_chirho = "cpu"
    if torch.cuda.is_available():
        device_chirho = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = "mps"

    model_chirho = SentenceTransformer(MODEL_ID_CHIRHO, device=device_chirho)


def compare_verses_chirho(verse1_chirho: str, verse2_chirho: str) -> str:
    """Compare two verse texts and return similarity score."""
    load_model_chirho()

    embeddings_chirho = model_chirho.encode([verse1_chirho, verse2_chirho])
    similarity_chirho = cos_sim(embeddings_chirho[0], embeddings_chirho[1]).item()

    interpretation_chirho = ""
    if similarity_chirho > 0.9:
        interpretation_chirho = "Very high similarity — likely same verse, different translation"
    elif similarity_chirho > 0.7:
        interpretation_chirho = "High similarity — related content or close paraphrase"
    elif similarity_chirho > 0.5:
        interpretation_chirho = "Moderate similarity — some shared themes"
    else:
        interpretation_chirho = "Low similarity — likely different content"

    return (
        f"Cosine Similarity: {similarity_chirho:.4f}\n\n"
        f"Interpretation: {interpretation_chirho}\n\n"
        f"Verse 1: {verse1_chirho}\n"
        f"Verse 2: {verse2_chirho}"
    )


def compare_multi_chirho(
    verse_text_chirho: str,
    kjv_chirho: str,
    asv_chirho: str,
    ylt_chirho: str,
    bbe_chirho: str,
) -> str:
    """Compare one verse across multiple translations."""
    load_model_chirho()

    translations_chirho = {
        "Input": verse_text_chirho,
        "KJV": kjv_chirho,
        "ASV": asv_chirho,
        "YLT": ylt_chirho,
        "BBE": bbe_chirho,
    }

    # Filter out empty entries
    active_chirho = {k: v for k, v in translations_chirho.items() if v.strip()}
    if len(active_chirho) < 2:
        return "Please enter at least 2 verses to compare."

    labels_chirho = list(active_chirho.keys())
    texts_chirho = list(active_chirho.values())

    embeddings_chirho = model_chirho.encode(texts_chirho)
    sim_matrix_chirho = cos_sim(embeddings_chirho, embeddings_chirho)

    # Format as table
    header_chirho = "       " + "  ".join(f"{l:>7}" for l in labels_chirho)
    rows_chirho = [header_chirho]
    for i_chirho, label_i_chirho in enumerate(labels_chirho):
        row_chirho = f"{label_i_chirho:>7}"
        for j_chirho in range(len(labels_chirho)):
            val_chirho = sim_matrix_chirho[i_chirho][j_chirho].item()
            row_chirho += f"  {val_chirho:>7.3f}"
        rows_chirho.append(row_chirho)

    return "Similarity Matrix:\n" + "\n".join(rows_chirho)


with gr.Blocks(title="Cross-Translation Bible Embeddings") as demo_chirho:
    gr.Markdown(
        """
        # Cross-Translation Bible Embeddings
        *Compare Bible verses across translations using semantic similarity*

        This model creates a shared embedding space where semantically equivalent
        verses map to nearby vectors, regardless of translation style
        (formal vs. dynamic equivalence).
        """
    )

    with gr.Tab("Compare Two Verses"):
        with gr.Row():
            verse1_input_chirho = gr.Textbox(
                label="Verse 1",
                value="[KJV] In the beginning God created the heaven and the earth.",
                lines=2,
            )
            verse2_input_chirho = gr.Textbox(
                label="Verse 2",
                value="[BBE] At the first God made the heaven and the earth.",
                lines=2,
            )
        compare_btn_chirho = gr.Button("Compare", variant="primary")
        compare_output_chirho = gr.Textbox(label="Result", lines=6)
        compare_btn_chirho.click(
            compare_verses_chirho,
            inputs=[verse1_input_chirho, verse2_input_chirho],
            outputs=compare_output_chirho,
        )

    with gr.Tab("Multi-Translation Comparison"):
        gr.Markdown("Enter the same verse in different translations:")
        input_verse_chirho = gr.Textbox(label="Reference Verse", value="For God so loved the world")
        kjv_input_chirho = gr.Textbox(label="KJV", value="For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.")
        asv_input_chirho = gr.Textbox(label="ASV", value="For God so loved the world, that he gave his only begotten Son, that whosoever believeth on him should not perish, but have eternal life.")
        ylt_input_chirho = gr.Textbox(label="YLT", value="for God did so love the world, that His Son -- the only begotten -- He gave, that every one who is believing in him may not perish, but may have life age-during.")
        bbe_input_chirho = gr.Textbox(label="BBE", value="For God had such love for the world that he gave his only Son, so that whoever has faith in him may not come to destruction but have eternal life.")
        multi_btn_chirho = gr.Button("Compare All", variant="primary")
        multi_output_chirho = gr.Textbox(label="Similarity Matrix", lines=8)
        multi_btn_chirho.click(
            compare_multi_chirho,
            inputs=[input_verse_chirho, kjv_input_chirho, asv_input_chirho, ylt_input_chirho, bbe_input_chirho],
            outputs=multi_output_chirho,
        )

    with gr.Tab("About"):
        gr.Markdown(
            """
            ## Model Details

            - **Base**: paraphrase-multilingual-MiniLM-L12-v2 (118M params)
            - **Training**: Contrastive learning on ~300K verse pairs
            - **Translations**: KJV, ASV, YLT, BBE, WEB (all public domain)
            - **Embedding dim**: 384
            - **Task**: Cross-translation semantic similarity

            ## How it works

            The model was fine-tuned on pairs of the same Bible verse in different
            translations (positive pairs) and different verses (negative pairs).
            This teaches it that "God created the heaven" (KJV) and "God made the
            heaven" (BBE) mean the same thing, while "In the beginning" and
            "And God said" are different concepts.

            ---
            *For God so loved the world that he gave his only begotten Son,
            that whoever believes in him should not perish but have eternal life.* — John 3:16
            """
        )

demo_chirho.launch()
