# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
app.py - HuggingFace Space for Model 9: Evangelism & Apologetics Pipeline.
Demonstrates intent classification and apologetics passage retrieval.
Generator (Qwen3-14B + LoRA) requires GPU and is documented but not loaded here.
"""

import json

import gradio as gr
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# HuggingFace model IDs
INTENT_ID_CHIRHO = "LoveJesus/evangelism-intent-classifier-chirho"
RETRIEVER_ID_CHIRHO = "LoveJesus/evangelism-retriever-chirho"
GENERATOR_ID_CHIRHO = "LoveJesus/evangelism-generator-chirho"
DATASET_ID_CHIRHO = "LoveJesus/evangelism-dataset-chirho"

INTENT_LABELS_CHIRHO = [
    "evangelism_dialogue",
    "apologetics_qa",
    "creation_science",
    "historical_evidence",
    "miracle_testimony",
]

INTENT_DISPLAY_CHIRHO = {
    "evangelism_dialogue": "Evangelism Dialogue",
    "apologetics_qa": "Apologetics Q&A",
    "creation_science": "Creation Science",
    "historical_evidence": "Historical Evidence",
    "miracle_testimony": "Miracle Testimony",
}

INTENT_EMOJI_CHIRHO = {
    "evangelism_dialogue": "conversation",
    "apologetics_qa": "book",
    "creation_science": "microscope",
    "historical_evidence": "scroll",
    "miracle_testimony": "star",
}

# Global model holders
intent_model_chirho = None
intent_tokenizer_chirho = None
retriever_chirho = None
corpus_passages_chirho = []
corpus_embeddings_chirho = None
device_chirho = None


def load_models_chirho():
    """Load intent classifier and retriever from HuggingFace Hub."""
    global intent_model_chirho, intent_tokenizer_chirho
    global retriever_chirho, corpus_passages_chirho, corpus_embeddings_chirho
    global device_chirho

    if torch.cuda.is_available():
        device_chirho = torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = torch.device("mps")
    else:
        device_chirho = torch.device("cpu")
    print(f"Using device: {device_chirho}")

    # Intent Classifier
    print("Loading intent classifier...")
    intent_tokenizer_chirho = AutoTokenizer.from_pretrained(INTENT_ID_CHIRHO)
    intent_model_chirho = AutoModelForSequenceClassification.from_pretrained(INTENT_ID_CHIRHO)
    intent_model_chirho.to(device_chirho)
    intent_model_chirho.eval()
    print("  Intent classifier loaded.")

    # Retriever
    print("Loading retriever...")
    retriever_chirho = SentenceTransformer(RETRIEVER_ID_CHIRHO, device=str(device_chirho))
    print("  Retriever loaded.")

    # Load corpus from dataset repo
    print("Loading corpus...")
    try:
        from huggingface_hub import hf_hub_download
        corpus_files_chirho = [
            "raw-chirho/apologetics-chirho/gotquestions-chirho.jsonl",
            "raw-chirho/apologetics-chirho/apologetics-articles-chirho.jsonl",
            "raw-chirho/evidence-chirho/evidence-expanded-chirho.jsonl",
            "raw-chirho/evidence-chirho/creation-science-chirho.jsonl",
            "raw-chirho/evidence-chirho/historical-evidence-chirho.jsonl",
            "raw-chirho/miracles-chirho/miracle-testimony-expanded-chirho.jsonl",
            "raw-chirho/fathers-chirho/early-fathers-apologetics-chirho.jsonl",
            "raw-chirho/sermons-chirho/spurgeon-sermons-chirho.jsonl",
            "raw-chirho/dialogues-chirho/compiled-dialogues-chirho.jsonl",
            "raw-chirho/dialogues-chirho/evangelism-dialogues-seed-chirho.jsonl",
        ]
        for filename_chirho in corpus_files_chirho:
            try:
                path_chirho = hf_hub_download(
                    repo_id=DATASET_ID_CHIRHO,
                    filename=filename_chirho,
                    repo_type="dataset",
                )
                with open(path_chirho, "r", encoding="utf-8") as f_chirho:
                    for line_chirho in f_chirho:
                        line_chirho = line_chirho.strip()
                        if not line_chirho:
                            continue
                        try:
                            entry_chirho = json.loads(line_chirho)
                        except json.JSONDecodeError:
                            continue
                        text_chirho = _extract_text_chirho(entry_chirho)
                        if text_chirho and len(text_chirho) > 30:
                            corpus_passages_chirho.append({
                                "text_chirho": text_chirho.strip(),
                                "source_chirho": entry_chirho.get("source_chirho", "unknown"),
                                "scripture_chirho": entry_chirho.get("scripture_chirho", []),
                                "question_chirho": entry_chirho.get("question_chirho", ""),
                                "category_chirho": entry_chirho.get("category_chirho", ""),
                            })
            except Exception as e_chirho:
                print(f"  Warning: Could not load {filename_chirho}: {e_chirho}")

        print(f"  Loaded {len(corpus_passages_chirho)} passages.")

        if corpus_passages_chirho:
            print("  Encoding corpus (this may take a moment)...")
            texts_chirho = [p_chirho["text_chirho"][:512] for p_chirho in corpus_passages_chirho]
            corpus_embeddings_chirho = retriever_chirho.encode(
                texts_chirho,
                batch_size=128,
                show_progress_bar=True,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
            print("  Corpus index built!")
    except Exception as e_chirho:
        print(f"  Warning: Could not load corpus: {e_chirho}")

    print("All models loaded!")


def _extract_text_chirho(entry_chirho):
    """Extract searchable text from a corpus entry."""
    if "answer_chirho" in entry_chirho:
        return entry_chirho["answer_chirho"][:1000]
    elif "evidence_chirho" in entry_chirho:
        claim_chirho = entry_chirho.get("claim_chirho", "")
        evidence_chirho = entry_chirho.get("evidence_chirho", "")
        return f"{claim_chirho}\n{evidence_chirho}"[:1000]
    elif "text_chirho" in entry_chirho:
        return entry_chirho["text_chirho"][:1000]
    elif "argument_chirho" in entry_chirho:
        argument_chirho = entry_chirho.get("argument_chirho", "")
        context_chirho = entry_chirho.get("context_chirho", "")
        return f"{argument_chirho}\n{context_chirho}"[:1000]
    return ""


# Tab Functions

def classify_intent_tab_chirho(question_chirho: str) -> tuple:
    """Tab 1: Classify the intent of a question."""
    if not question_chirho.strip():
        return "Please enter a question.", ""

    inputs_chirho = intent_tokenizer_chirho(
        question_chirho,
        truncation=True,
        max_length=128,
        padding="max_length",
        return_tensors="pt",
    )
    inputs_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

    with torch.no_grad():
        outputs_chirho = intent_model_chirho(**inputs_chirho)
        probs_chirho = torch.softmax(outputs_chirho.logits, dim=-1).cpu().numpy()[0]

    pred_idx_chirho = int(np.argmax(probs_chirho))
    label_chirho = INTENT_LABELS_CHIRHO[pred_idx_chirho]
    display_chirho = INTENT_DISPLAY_CHIRHO[label_chirho]
    confidence_chirho = float(probs_chirho[pred_idx_chirho])

    main_result_chirho = f"## {display_chirho}\n**Confidence:** {confidence_chirho:.1%}"

    scores_lines_chirho = ["| Category | Score |", "| --- | --- |"]
    for i_chirho in np.argsort(probs_chirho)[::-1]:
        label_i_chirho = INTENT_LABELS_CHIRHO[i_chirho]
        display_i_chirho = INTENT_DISPLAY_CHIRHO[label_i_chirho]
        score_chirho = float(probs_chirho[i_chirho])
        bar_len_chirho = int(score_chirho * 20)
        bar_chirho = "=" * bar_len_chirho
        scores_lines_chirho.append(
            f"| {display_i_chirho} | {score_chirho:.3f} {bar_chirho} |"
        )

    return main_result_chirho, "\n".join(scores_lines_chirho)


def retrieve_passages_tab_chirho(query_chirho: str, k_chirho: int = 5) -> str:
    """Tab 2: Retrieve relevant passages for a question."""
    if not query_chirho.strip():
        return "Please enter a question."
    if corpus_embeddings_chirho is None:
        return "Corpus index not available. Please try again later."

    query_emb_chirho = retriever_chirho.encode(
        [query_chirho], normalize_embeddings=True, convert_to_numpy=True
    )[0]

    similarities_chirho = np.dot(corpus_embeddings_chirho, query_emb_chirho)
    top_indices_chirho = np.argsort(similarities_chirho)[::-1][:int(k_chirho)]

    lines_chirho = []
    for rank_chirho, idx_chirho in enumerate(top_indices_chirho, 1):
        passage_chirho = corpus_passages_chirho[idx_chirho]
        sim_chirho = float(similarities_chirho[idx_chirho])
        text_preview_chirho = passage_chirho["text_chirho"][:300]
        source_chirho = passage_chirho.get("source_chirho", "unknown")
        question_orig_chirho = passage_chirho.get("question_chirho", "")
        scripture_chirho = passage_chirho.get("scripture_chirho", [])

        lines_chirho.append(f"### #{rank_chirho} (similarity: {sim_chirho:.3f})")
        if question_orig_chirho:
            lines_chirho.append(f"**Original question:** {question_orig_chirho}")
        lines_chirho.append(f"{text_preview_chirho}...")
        if scripture_chirho:
            if isinstance(scripture_chirho, list):
                lines_chirho.append(f"**Scripture:** {', '.join(str(s_chirho) for s_chirho in scripture_chirho[:5])}")
            else:
                lines_chirho.append(f"**Scripture:** {scripture_chirho}")
        lines_chirho.append(f"*Source: {source_chirho}*")
        lines_chirho.append("---")

    return "\n\n".join(lines_chirho)


def full_pipeline_tab_chirho(question_chirho: str, k_chirho: int = 5) -> tuple:
    """Tab 3: Full pipeline - classify + retrieve."""
    if not question_chirho.strip():
        return "Please enter a question.", ""

    # Classify
    inputs_chirho = intent_tokenizer_chirho(
        question_chirho,
        truncation=True,
        max_length=128,
        padding="max_length",
        return_tensors="pt",
    )
    inputs_chirho = {k_c: v_c.to(device_chirho) for k_c, v_c in inputs_chirho.items()}

    with torch.no_grad():
        outputs_chirho = intent_model_chirho(**inputs_chirho)
        probs_chirho = torch.softmax(outputs_chirho.logits, dim=-1).cpu().numpy()[0]

    pred_idx_chirho = int(np.argmax(probs_chirho))
    label_chirho = INTENT_LABELS_CHIRHO[pred_idx_chirho]
    display_chirho = INTENT_DISPLAY_CHIRHO[label_chirho]
    confidence_chirho = float(probs_chirho[pred_idx_chirho])

    intent_result_chirho = (
        f"## Intent: {display_chirho} ({confidence_chirho:.1%})\n\n"
        "In the full pipeline, this intent determines how the question is routed:\n"
    )
    if label_chirho == "evangelism_dialogue":
        intent_result_chirho += "- Sent directly to the **Generator** for conversational response.\n"
    else:
        intent_result_chirho += "- **Retriever** fetches relevant passages, then **Generator** produces Scripture-grounded answer.\n"

    # Retrieve
    retrieval_result_chirho = ""
    if corpus_embeddings_chirho is not None:
        query_emb_chirho = retriever_chirho.encode(
            [question_chirho], normalize_embeddings=True, convert_to_numpy=True
        )[0]
        similarities_chirho = np.dot(corpus_embeddings_chirho, query_emb_chirho)
        top_indices_chirho = np.argsort(similarities_chirho)[::-1][:int(k_chirho)]

        lines_chirho = ["### Retrieved Context Passages\n"]
        for rank_chirho, idx_chirho in enumerate(top_indices_chirho, 1):
            passage_chirho = corpus_passages_chirho[idx_chirho]
            sim_chirho = float(similarities_chirho[idx_chirho])
            text_preview_chirho = passage_chirho["text_chirho"][:200]
            lines_chirho.append(
                f"**[{rank_chirho}]** (score: {sim_chirho:.3f}) {text_preview_chirho}..."
            )
        lines_chirho.append(
            "\n---\n*In production, these passages are sent to the Qwen3-14B + LoRA generator "
            "which produces a final Scripture-grounded response, then verified by theological guardrails (F1=0.997).*"
        )
        retrieval_result_chirho = "\n\n".join(lines_chirho)
    else:
        retrieval_result_chirho = "Corpus not available for retrieval demo."

    return intent_result_chirho, retrieval_result_chirho


# Build Gradio Interface

def build_demo_chirho() -> gr.Blocks:
    """Build the Gradio demo."""
    with gr.Blocks(
        title="Evangelism & Apologetics Pipeline - LoveJesus/models-chirho",
        theme=gr.themes.Soft(),
    ) as demo_chirho:
        gr.Markdown("# Evangelism & Apologetics Pipeline")
        gr.Markdown(
            "*For God so loved the world that he gave his only begotten Son, "
            "that whoever believes in him should not perish but have eternal life. - John 3:16*"
        )
        gr.Markdown(
            "A **3-model AI pipeline** for answering apologetics questions with Scripture. "
            "Classifies intent, retrieves relevant passages, and generates grounded responses. "
            "Part of [bible.systems](https://bible.systems) - Model 9."
        )

        with gr.Tab("Ask a Question"):
            gr.Markdown(
                "Enter any question about Christianity, apologetics, creation, "
                "historical evidence, or miracles. The pipeline classifies your intent "
                "and retrieves relevant passages."
            )
            question_input_chirho = gr.Textbox(
                label="Your Question",
                placeholder="What evidence is there for the resurrection of Jesus?",
                lines=2,
            )
            k_slider_chirho = gr.Slider(3, 10, value=5, step=1, label="Number of passages")
            ask_btn_chirho = gr.Button("Ask", variant="primary")
            intent_output_chirho = gr.Markdown(label="Intent Classification")
            retrieval_output_chirho = gr.Markdown(label="Retrieved Passages")

            ask_btn_chirho.click(
                full_pipeline_tab_chirho,
                inputs=[question_input_chirho, k_slider_chirho],
                outputs=[intent_output_chirho, retrieval_output_chirho],
            )

            gr.Examples(
                examples=[
                    ["What evidence is there for the resurrection of Jesus?"],
                    ["How do you explain the existence of evil if God is good?"],
                    ["What does the fossil record really show about evolution?"],
                    ["Are there any documented modern miracles?"],
                    ["How can I share the Gospel with someone who doesn't believe in God?"],
                    ["What non-biblical sources confirm that Jesus existed?"],
                    ["How do we know the Bible hasn't been changed over time?"],
                    ["What is the cosmological argument for God's existence?"],
                ],
                inputs=[question_input_chirho],
            )

        with gr.Tab("Classify Intent"):
            gr.Markdown(
                "Test the **intent classifier** (RoBERTa-base, macro F1=0.83). "
                "It routes questions to the appropriate pipeline stage."
            )
            cls_input_chirho = gr.Textbox(
                label="Question",
                placeholder="Enter a question...",
                lines=2,
            )
            cls_btn_chirho = gr.Button("Classify")
            cls_result_chirho = gr.Markdown(label="Result")
            cls_scores_chirho = gr.Markdown(label="All Scores")

            cls_btn_chirho.click(
                classify_intent_tab_chirho,
                inputs=[cls_input_chirho],
                outputs=[cls_result_chirho, cls_scores_chirho],
            )

            gr.Examples(
                examples=[
                    ["What evidence is there for the resurrection?"],
                    ["How old is the earth according to science?"],
                    ["Can you tell me about a modern miracle?"],
                    ["How would you share the Gospel with an atheist?"],
                    ["What did Josephus write about Jesus?"],
                ],
                inputs=[cls_input_chirho],
            )

        with gr.Tab("Search Corpus"):
            gr.Markdown(
                "Search the apologetics corpus using the **retriever** "
                "(MiniLM-L12, Pearson=0.90). Over 13,000 passages from "
                "GotQuestions, Spurgeon sermons, church fathers, creation science, "
                "historical evidence, and miracle testimonies."
            )
            search_input_chirho = gr.Textbox(
                label="Search Query",
                placeholder="Enter a topic or question...",
                lines=2,
            )
            search_k_chirho = gr.Slider(3, 15, value=5, step=1, label="Number of results")
            search_btn_chirho = gr.Button("Search")
            search_output_chirho = gr.Markdown()

            search_btn_chirho.click(
                retrieve_passages_tab_chirho,
                inputs=[search_input_chirho, search_k_chirho],
                outputs=[search_output_chirho],
            )

            gr.Examples(
                examples=[
                    ["soft tissue dinosaur bones young earth"],
                    ["manuscript reliability Bible"],
                    ["fine tuning universe intelligent design"],
                    ["George Muller answered prayer"],
                    ["early church fathers apologetics"],
                ],
                inputs=[search_input_chirho],
            )

        with gr.Tab("About"):
            gr.Markdown("""# Model 9: Evangelism & Apologetics Pipeline

## What This Does

This AI system answers questions about Christianity, apologetics, creation science,
historical evidence, and miracles - all grounded in Scripture.

## Three-Model Architecture

```
User Question -> [Intent Classifier (RoBERTa-base)]
    |-> evangelism_dialogue -> [Generator directly]
    |-> apologetics_qa -> [Retriever] -> [Generator]
    |-> creation_science -> [Retriever] -> [Generator]
    |-> historical_evidence -> [Retriever] -> [Generator]
    |-> miracle_testimony -> [Retriever] -> [Generator]
              |
    [Qwen3-14B + LoRA Generator]
              |
    [Theological Guardrails (existing, F1=0.997)]
              |
    Final Response with Scripture references
```

| Component | Model | Metric |
| --- | --- | --- |
| **Intent Classifier** | RoBERTa-base (125M) | Macro F1 = 0.83, Weighted F1 = 0.98 |
| **Retriever** | MiniLM-L12-v2 (33M) | Pearson = 0.90, Spearman = 0.86 |
| **Generator** | Qwen3-14B + LoRA (64M trainable) | Fine-tuned on 10,622 instruction pairs |

## Training Corpus (13,278 source passages)

| Source | Count | Description |
| --- | --- | --- |
| GotQuestions.org | 9,523 | Apologetics Q&A pairs |
| Spurgeon Sermons | 3,464 | 63 volumes of sermon excerpts |
| Apologetics Articles | 85 | Structured apologetics arguments |
| Evidence Expanded | 55 | Creation science + historical evidence |
| Early Church Fathers | 50 | Justin Martyr, Irenaeus, Tertullian, Origen, Athanasius, Augustine |
| Miracle Testimonies | 31 | Documented modern miracles |
| Evangelism Dialogues | 50 | Seeker-evangelist conversation pairs |
| Creation Science | 12 | Detailed scientific evidence entries |
| Historical Evidence | 5 | Non-biblical sources for Jesus |

## Intent Categories

| Category | Description | Example Question |
| --- | --- | --- |
| **Evangelism Dialogue** | Sharing the Gospel, witnessing | "How do I tell my friend about Jesus?" |
| **Apologetics Q&A** | Defending the faith, theological questions | "Why does God allow suffering?" |
| **Creation Science** | Origins, evolution, age of earth | "What about dinosaurs and the Bible?" |
| **Historical Evidence** | Manuscript reliability, extra-biblical sources | "What did Josephus say about Jesus?" |
| **Miracle Testimony** | Documented miracles, answered prayer | "Are there proven modern miracles?" |

## Note on Generator

The **Qwen3-14B + LoRA generator** requires a GPU with 30+ GB VRAM and is not loaded
in this Space demo. The intent classifier and retriever run on CPU. For the full
pipeline experience, see the usage instructions in the
[generator model card](https://huggingface.co/LoveJesus/evangelism-generator-chirho).

## Related Models

- [LoveJesus/evangelism-intent-classifier-chirho](https://huggingface.co/LoveJesus/evangelism-intent-classifier-chirho)
- [LoveJesus/evangelism-retriever-chirho](https://huggingface.co/LoveJesus/evangelism-retriever-chirho)
- [LoveJesus/evangelism-generator-chirho](https://huggingface.co/LoveJesus/evangelism-generator-chirho)
- [LoveJesus/evangelism-dataset-chirho](https://huggingface.co/datasets/LoveJesus/evangelism-dataset-chirho)

---
Built with love for Jesus. Part of [bible.systems](https://bible.systems).
Published by [LoveJesus](https://huggingface.co/LoveJesus).
""")

    return demo_chirho


# Load models at startup
load_models_chirho()

# Launch
demo_chirho = build_demo_chirho()
demo_chirho.launch()
