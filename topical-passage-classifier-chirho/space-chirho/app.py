# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
Gradio Space for Topical Bible Passage Search.
Enter a topic or question, get the most relevant Bible verses ranked by semantic similarity.
"""

import csv
import io
import os
from pathlib import Path

import gradio as gr
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

MODEL_ID_CHIRHO = "LoveJesus/biblical-topical-search-chirho"
FALLBACK_MODEL_CHIRHO = "sentence-transformers/all-MiniLM-L6-v2"

KJV_URL_CHIRHO = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/csv/KJV.csv"

model_chirho = None
bible_verses_chirho = None
bible_embeddings_chirho = None


def load_kjv_bible_chirho() -> list[dict]:
    """Download and parse KJV Bible into list of {ref, text} dicts."""
    import urllib.request

    print("Downloading KJV Bible for verse lookup...")
    response_chirho = urllib.request.urlopen(KJV_URL_CHIRHO)
    content_chirho = response_chirho.read().decode("utf-8")

    verses_chirho = []
    reader_chirho = csv.reader(io.StringIO(content_chirho))

    for row_chirho in reader_chirho:
        if len(row_chirho) < 4:
            continue
        book_chirho = row_chirho[0].strip().strip('"')
        chapter_chirho = row_chirho[1].strip()
        verse_num_chirho = row_chirho[2].strip()
        text_chirho = row_chirho[3].strip().strip('"')

        # Skip header
        if book_chirho == "Book" or not chapter_chirho.isdigit():
            continue

        if len(text_chirho) < 10:
            continue

        ref_chirho = f"{book_chirho} {chapter_chirho}:{verse_num_chirho}"
        verses_chirho.append({
            "ref_chirho": ref_chirho,
            "text_chirho": text_chirho,
        })

    print(f"  Loaded {len(verses_chirho)} verses")
    return verses_chirho


def initialize_chirho():
    """Load model and Bible data on first use."""
    global model_chirho, bible_verses_chirho, bible_embeddings_chirho

    if model_chirho is not None and bible_embeddings_chirho is not None:
        return

    # Detect device
    device_chirho = "cpu"
    if torch.cuda.is_available():
        device_chirho = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = "mps"

    # Load model (try fine-tuned first, fall back to base)
    if model_chirho is None:
        try:
            print(f"Loading model: {MODEL_ID_CHIRHO}")
            model_chirho = SentenceTransformer(MODEL_ID_CHIRHO, device=device_chirho)
        except Exception as error_chirho:
            print(f"Fine-tuned model not available ({error_chirho}), using base model")
            model_chirho = SentenceTransformer(FALLBACK_MODEL_CHIRHO, device=device_chirho)

    # Load Bible
    if bible_verses_chirho is None:
        bible_verses_chirho = load_kjv_bible_chirho()

    # Pre-compute embeddings for all Bible verses
    if bible_embeddings_chirho is None:
        print("Computing verse embeddings (this may take a minute)...")
        verse_texts_chirho = [v_chirho["text_chirho"] for v_chirho in bible_verses_chirho]
        bible_embeddings_chirho = model_chirho.encode(
            verse_texts_chirho,
            batch_size=256,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
        print(f"  Computed {len(bible_embeddings_chirho)} embeddings")


def search_bible_chirho(
    query_chirho: str,
    top_n_chirho: int = 10,
) -> str:
    """Search the Bible for verses matching the given topic/question."""
    if not query_chirho or not query_chirho.strip():
        return "Please enter a topic or question to search."

    initialize_chirho()

    # Encode query
    query_embedding_chirho = model_chirho.encode(
        [query_chirho], convert_to_numpy=True
    )

    # Compute similarities
    similarities_chirho = cos_sim(query_embedding_chirho, bible_embeddings_chirho)[0]
    similarities_np_chirho = similarities_chirho.cpu().numpy() if hasattr(similarities_chirho, "cpu") else np.array(similarities_chirho)

    # Get top-N indices
    top_indices_chirho = np.argsort(similarities_np_chirho)[::-1][:top_n_chirho]

    # Format results
    results_lines_chirho = []
    results_lines_chirho.append(f"Top {top_n_chirho} results for: \"{query_chirho}\"\n")
    results_lines_chirho.append("=" * 60)

    for rank_chirho, idx_chirho in enumerate(top_indices_chirho):
        verse_chirho = bible_verses_chirho[idx_chirho]
        score_chirho = similarities_np_chirho[idx_chirho]
        ref_chirho = verse_chirho["ref_chirho"]
        text_chirho = verse_chirho["text_chirho"]

        results_lines_chirho.append(
            f"\n#{rank_chirho + 1}  [{ref_chirho}]  (similarity: {score_chirho:.4f})"
        )
        results_lines_chirho.append(f"  {text_chirho}")

    results_lines_chirho.append("\n" + "=" * 60)
    results_lines_chirho.append(
        "Model: all-MiniLM-L6-v2 fine-tuned on Nave's Topical Bible + TSK Cross-References"
    )

    return "\n".join(results_lines_chirho)


# ============================================================
# Gradio Interface
# ============================================================

EXAMPLES_CHIRHO = [
    ["What does the Bible say about anxiety?"],
    ["verses about love"],
    ["passages about forgiveness"],
    ["creation of the world"],
    ["prayer and intercession"],
    ["salvation through faith"],
    ["suffering and endurance"],
    ["wisdom and knowledge"],
    ["the Holy Spirit"],
    ["resurrection of Jesus"],
]

with gr.Blocks(
    title="Topical Bible Search",
    theme=gr.themes.Soft(),
) as demo_chirho:
    gr.Markdown(
        """
        # Topical Bible Search
        *Find Bible verses by topic using semantic search*

        Enter a topic, question, or phrase and discover the most relevant
        Bible passages. Powered by a sentence transformer fine-tuned on
        Nave's Topical Bible and TSK cross-references.

        ---
        *For God so loved the world that he gave his only begotten Son,
        that whoever believes in him should not perish but have eternal life.* -- John 3:16
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            query_input_chirho = gr.Textbox(
                label="Search Topic or Question",
                placeholder="e.g., 'What does the Bible say about anxiety?'",
                lines=2,
            )
        with gr.Column(scale=1):
            top_n_input_chirho = gr.Slider(
                minimum=5,
                maximum=25,
                value=10,
                step=1,
                label="Number of Results",
            )

    search_btn_chirho = gr.Button("Search", variant="primary", size="lg")

    results_output_chirho = gr.Textbox(
        label="Search Results",
        lines=25,
        max_lines=50,
    )

    search_btn_chirho.click(
        search_bible_chirho,
        inputs=[query_input_chirho, top_n_input_chirho],
        outputs=results_output_chirho,
    )

    # Also trigger on Enter key
    query_input_chirho.submit(
        search_bible_chirho,
        inputs=[query_input_chirho, top_n_input_chirho],
        outputs=results_output_chirho,
    )

    gr.Examples(
        examples=EXAMPLES_CHIRHO,
        inputs=[query_input_chirho],
        label="Try these examples:",
    )

    with gr.Accordion("About this model", open=False):
        gr.Markdown(
            """
            ## Model Details

            - **Base**: sentence-transformers/all-MiniLM-L6-v2 (22M params)
            - **Training**: MultipleNegativesRankingLoss on ~170K topical pairs
            - **Data Sources**:
              - Nave's Topical Bible (public domain, 1896) -- topic-to-verse mappings
              - Treasury of Scripture Knowledge cross-references (OpenBible.info)
            - **Embedding dim**: 384
            - **Task**: Semantic topical Bible search

            ## How it works

            The model was fine-tuned on pairs of (topic/question, Bible verse) and
            (verse, related verse). Given a natural language query about a biblical
            topic, it finds the most semantically relevant passages from the entire
            KJV Bible (31,000+ verses).

            Unlike keyword search, this model understands meaning:
            - "anxiety" matches "casting all your care upon him" (1 Peter 5:7)
            - "forgiveness" matches "cleanse us from all unrighteousness" (1 John 1:9)
            - "creation" matches "In the beginning God created..." (Genesis 1:1)

            ## Bible Text

            All verse text is from the **King James Version** (public domain).

            ---
            *For God so loved the world that he gave his only begotten Son,
            that whoever believes in him should not perish but have eternal life.* -- John 3:16
            """
        )

demo_chirho.launch()
