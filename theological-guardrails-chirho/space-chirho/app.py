# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
app.py - HuggingFace Space for the Theological Guardrails Pipeline.
Loads all 3 models from HuggingFace Hub and provides a Gradio interface.
"""

from dataclasses import dataclass, field

import gradio as gr
import numpy as np
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)
from sentence_transformers import SentenceTransformer

# HuggingFace model IDs
CLASSIFIER_ID_CHIRHO = "LoveJesus/theologian-classifier-chirho"
EMBEDDER_ID_CHIRHO = "LoveJesus/theologian-embedder-chirho"
EXPLAINER_ID_CHIRHO = "LoveJesus/theologian-explainer-chirho"

LABELS_CHIRHO = [
    "orthodox_chirho", "arianism_chirho", "pelagianism_chirho", "gnosticism_chirho",
    "modalism_chirho", "docetism_chirho", "nestorianism_chirho", "marcionism_chirho",
    "apollinarianism_chirho", "monothelitism_chirho", "semi_pelagianism_chirho",
    "adoptionism_chirho", "patripassianism_chirho",
]

MAX_LENGTH_CHIRHO = 256
MAX_INPUT_LENGTH_CHIRHO = 512
MAX_OUTPUT_LENGTH_CHIRHO = 256


@dataclass
class ClassificationResultChirho:
    """Result from the theological guardrails pipeline."""
    text_chirho: str
    overall_label_chirho: str = "unknown"
    confidence_chirho: float = 0.0
    heresy_scores_chirho: dict = field(default_factory=dict)
    top_heresies_chirho: list = field(default_factory=list)
    explanation_chirho: str = ""
    embedding_similarity_chirho: float = 0.0


# Global model holders
classifier_chirho = None
classifier_tokenizer_chirho = None
embedder_chirho = None
explainer_chirho = None
explainer_tokenizer_chirho = None
orthodox_centroid_chirho = None
device_chirho = None


def load_models_chirho():
    """Load all three models from HuggingFace Hub."""
    global classifier_chirho, classifier_tokenizer_chirho
    global embedder_chirho
    global explainer_chirho, explainer_tokenizer_chirho
    global orthodox_centroid_chirho, device_chirho

    # Device
    if torch.cuda.is_available():
        device_chirho = torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = torch.device("mps")
    else:
        device_chirho = torch.device("cpu")

    print(f"Using device: {device_chirho}")

    # Classifier
    print("Loading classifier...")
    classifier_tokenizer_chirho = AutoTokenizer.from_pretrained(CLASSIFIER_ID_CHIRHO)
    classifier_chirho = AutoModelForSequenceClassification.from_pretrained(CLASSIFIER_ID_CHIRHO)
    classifier_chirho.to(device_chirho)

    # Embedder
    print("Loading embedder...")
    embedder_chirho = SentenceTransformer(EMBEDDER_ID_CHIRHO, device=str(device_chirho))

    # Explainer
    print("Loading explainer...")
    explainer_tokenizer_chirho = AutoTokenizer.from_pretrained(EXPLAINER_ID_CHIRHO)
    explainer_chirho = AutoModelForSeq2SeqLM.from_pretrained(EXPLAINER_ID_CHIRHO)
    explainer_chirho.to(device_chirho)

    # Precompute orthodox centroid
    orthodox_statements_chirho = [
        "Jesus Christ is truly God and truly man, one person with two natures.",
        "We worship one God in Trinity and Trinity in Unity.",
        "The Son is eternally begotten of the Father, not made, of one Being with the Father.",
        "The Holy Spirit proceeds from the Father and is worshipped with the Father and Son.",
        "Christ has two wills, divine and human, the human freely submitting to the divine.",
        "In the incarnation, the Word became flesh and dwelt among us.",
        "Salvation is by grace through faith, the gift of God.",
        "God created the heavens and the earth, and all that he made was very good.",
    ]
    embeddings_chirho = embedder_chirho.encode(orthodox_statements_chirho)
    orthodox_centroid_chirho = np.mean(embeddings_chirho, axis=0)

    print("All models loaded!")


def analyze_chirho(text_chirho: str, threshold_chirho: float = 0.5) -> ClassificationResultChirho:
    """Run the full three-model pipeline."""
    result_chirho = ClassificationResultChirho(text_chirho=text_chirho)

    # Step 1: Classify
    inputs_chirho = classifier_tokenizer_chirho(
        text_chirho, return_tensors="pt", max_length=MAX_LENGTH_CHIRHO,
        truncation=True, padding="max_length",
    )
    inputs_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

    with torch.no_grad():
        outputs_chirho = classifier_chirho(**inputs_chirho)
        scores_chirho = torch.sigmoid(outputs_chirho.logits).cpu().numpy()[0]

    for i_chirho, label_chirho in enumerate(LABELS_CHIRHO):
        result_chirho.heresy_scores_chirho[label_chirho] = float(scores_chirho[i_chirho])

    orthodox_score_chirho = scores_chirho[0]
    heresy_scores_chirho = scores_chirho[1:]
    max_heresy_score_chirho = float(np.max(heresy_scores_chirho)) if len(heresy_scores_chirho) > 0 else 0.0

    if orthodox_score_chirho > threshold_chirho and max_heresy_score_chirho < threshold_chirho:
        result_chirho.overall_label_chirho = "orthodox"
        result_chirho.confidence_chirho = float(orthodox_score_chirho)
    elif max_heresy_score_chirho > threshold_chirho:
        result_chirho.overall_label_chirho = "heterodox"
        result_chirho.confidence_chirho = float(max_heresy_score_chirho)
        result_chirho.top_heresies_chirho = [
            LABELS_CHIRHO[i_chirho + 1]
            for i_chirho, s_chirho in enumerate(heresy_scores_chirho)
            if s_chirho > threshold_chirho
        ]
    else:
        result_chirho.overall_label_chirho = "uncertain"
        result_chirho.confidence_chirho = float(max(orthodox_score_chirho, max_heresy_score_chirho))

    # Step 2: Embed
    embedding_chirho = embedder_chirho.encode([text_chirho])[0]
    dot_chirho = np.dot(embedding_chirho, orthodox_centroid_chirho)
    norm_a_chirho = np.linalg.norm(embedding_chirho)
    norm_b_chirho = np.linalg.norm(orthodox_centroid_chirho)
    result_chirho.embedding_similarity_chirho = float(dot_chirho / (norm_a_chirho * norm_b_chirho))

    # Step 3: Explain
    heresy_str_chirho = ", ".join(result_chirho.top_heresies_chirho) if result_chirho.top_heresies_chirho else "none"
    input_text_chirho = (
        f"explain theological classification: {text_chirho} | "
        f"label: {result_chirho.overall_label_chirho} | "
        f"heresy types: {heresy_str_chirho}"
    )
    exp_inputs_chirho = explainer_tokenizer_chirho(
        input_text_chirho, return_tensors="pt", max_length=MAX_INPUT_LENGTH_CHIRHO, truncation=True,
    )
    exp_inputs_chirho = {k_chirho: v_chirho.to(device_chirho) for k_chirho, v_chirho in exp_inputs_chirho.items()}

    with torch.no_grad():
        exp_outputs_chirho = explainer_chirho.generate(
            **exp_inputs_chirho, max_length=MAX_OUTPUT_LENGTH_CHIRHO, num_beams=4, early_stopping=True,
        )
    result_chirho.explanation_chirho = explainer_tokenizer_chirho.decode(
        exp_outputs_chirho[0], skip_special_tokens=True
    )

    return result_chirho


# ─── Gradio Tab Functions ───

def classify_statement_chirho(text_chirho: str, threshold_chirho: float = 0.5) -> tuple:
    """Tab 1: Quick Classification."""
    if not text_chirho.strip():
        return "Please enter a statement.", "", "", ""

    result_chirho = analyze_chirho(text_chirho, threshold_chirho)

    label_map_chirho = {
        "orthodox": "Orthodox", "heterodox": "Heterodox",
        "uncertain": "Uncertain", "unknown": "Unknown",
    }
    label_display_chirho = label_map_chirho.get(result_chirho.overall_label_chirho, result_chirho.overall_label_chirho)
    label_with_conf_chirho = f"{label_display_chirho} (confidence: {result_chirho.confidence_chirho:.1%})"

    heresies_display_chirho = ""
    if result_chirho.top_heresies_chirho:
        heresies_display_chirho = "\n".join(
            f"- {h.replace('_chirho', '').replace('_', ' ').title()}: {result_chirho.heresy_scores_chirho.get(h, 0):.1%}"
            for h in result_chirho.top_heresies_chirho
        )
    else:
        heresies_display_chirho = "No heresies detected."

    similarity_chirho = f"Orthodox similarity: {result_chirho.embedding_similarity_chirho:.3f}"

    return label_with_conf_chirho, heresies_display_chirho, similarity_chirho, result_chirho.explanation_chirho


def detailed_scores_chirho(text_chirho: str) -> str:
    """Tab 2: Detailed Scores."""
    if not text_chirho.strip():
        return "Please enter a statement."

    result_chirho = analyze_chirho(text_chirho)

    lines_chirho = ["| Label | Score | Status |", "| --- | --- | --- |"]
    for label_chirho, score_chirho in sorted(
        result_chirho.heresy_scores_chirho.items(), key=lambda x: -x[1]
    ):
        display_name_chirho = label_chirho.replace("_chirho", "").replace("_", " ").title()
        bar_chirho = "=" * int(score_chirho * 20)
        status_chirho = "DETECTED" if score_chirho > 0.5 else ""
        lines_chirho.append(f"| {display_name_chirho} | {score_chirho:.3f} {bar_chirho} | {status_chirho} |")

    return "\n".join(lines_chirho)


def compare_statements_chirho(text_a_chirho: str, text_b_chirho: str) -> str:
    """Tab 3: Compare Statements."""
    if not text_a_chirho.strip() or not text_b_chirho.strip():
        return "Please enter both statements."

    result_a_chirho = analyze_chirho(text_a_chirho)
    result_b_chirho = analyze_chirho(text_b_chirho)

    emb_a_chirho = embedder_chirho.encode([text_a_chirho])[0]
    emb_b_chirho = embedder_chirho.encode([text_b_chirho])[0]
    similarity_chirho = float(
        np.dot(emb_a_chirho, emb_b_chirho) / (np.linalg.norm(emb_a_chirho) * np.linalg.norm(emb_b_chirho))
    )

    return f"""## Statement A
**Label:** {result_a_chirho.overall_label_chirho} ({result_a_chirho.confidence_chirho:.1%})
**Heresies:** {', '.join(h.replace('_chirho', '') for h in result_a_chirho.top_heresies_chirho) or 'None'}
**Orthodox similarity:** {result_a_chirho.embedding_similarity_chirho:.3f}

## Statement B
**Label:** {result_b_chirho.overall_label_chirho} ({result_b_chirho.confidence_chirho:.1%})
**Heresies:** {', '.join(h.replace('_chirho', '') for h in result_b_chirho.top_heresies_chirho) or 'None'}
**Orthodox similarity:** {result_b_chirho.embedding_similarity_chirho:.3f}

## Comparison
**Semantic similarity:** {similarity_chirho:.3f}
**Same classification:** {'Yes' if result_a_chirho.overall_label_chirho == result_b_chirho.overall_label_chirho else 'No'}
"""


def batch_analysis_chirho(texts_chirho: str) -> str:
    """Tab 4: Batch Analysis."""
    if not texts_chirho.strip():
        return "Please enter statements (one per line)."

    lines_chirho = texts_chirho.strip().split("\n")
    results_chirho = []

    for line_chirho in lines_chirho:
        if not line_chirho.strip():
            continue
        result_chirho = analyze_chirho(line_chirho.strip())
        heresies_str_chirho = ", ".join(
            h.replace("_chirho", "") for h in result_chirho.top_heresies_chirho
        ) or "-"
        display_text_chirho = line_chirho.strip()[:60]
        if len(line_chirho.strip()) > 60:
            display_text_chirho += "..."
        results_chirho.append(
            f"| {display_text_chirho} | {result_chirho.overall_label_chirho} | "
            f"{result_chirho.confidence_chirho:.1%} | {heresies_str_chirho} |"
        )

    header_chirho = "| Statement | Label | Confidence | Heresies |\n| --- | --- | --- | --- |"
    return header_chirho + "\n" + "\n".join(results_chirho)


# ─── Build Gradio Interface ───

def build_demo_chirho() -> gr.Blocks:
    """Build the Gradio demo."""
    with gr.Blocks(
        title="Theological Guardrails - loveJesus/models-chirho",
        theme=gr.themes.Soft(),
    ) as demo_chirho:
        gr.Markdown("# Theological Guardrails Pipeline")
        gr.Markdown(
            "*For God so loved the world that he gave his only begotten Son, "
            "that whoever believes in him should not perish but have eternal life. - John 3:16*"
        )
        gr.Markdown(
            "Classify theological statements as **orthodox**, **heterodox**, or **denominational distinctive** "
            "based on the first six ecumenical councils. Three-model pipeline: "
            "RoBERTa-large classifier + MiniLM-L12 embedder + Flan-T5-base explainer."
        )

        with gr.Tab("Classify"):
            text_input_chirho = gr.Textbox(
                label="Theological Statement",
                placeholder="Enter a theological statement to classify...",
                lines=3,
            )
            threshold_input_chirho = gr.Slider(0.1, 0.9, value=0.5, step=0.05, label="Threshold")
            classify_btn_chirho = gr.Button("Analyze", variant="primary")

            label_output_chirho = gr.Textbox(label="Classification")
            heresies_output_chirho = gr.Textbox(label="Detected Heresies")
            similarity_output_chirho = gr.Textbox(label="Embedding Similarity")
            explanation_output_chirho = gr.Textbox(label="Explanation", lines=4)

            classify_btn_chirho.click(
                classify_statement_chirho,
                inputs=[text_input_chirho, threshold_input_chirho],
                outputs=[label_output_chirho, heresies_output_chirho, similarity_output_chirho, explanation_output_chirho],
            )

            gr.Examples(
                examples=[
                    ["Jesus Christ is the eternal Son of God, fully divine and fully human, two natures in one person."],
                    ["Jesus was a created being, the first and greatest of God's creations."],
                    ["God is one person who manifests in three different modes: Father, Son, and Spirit."],
                    ["We can earn salvation through our own good works without needing divine grace."],
                    ["The physical world is evil, created by a lesser deity, and salvation comes through secret knowledge."],
                    ["Christ only appeared to have a human body; his suffering was an illusion."],
                    ["Believers should be baptized by immersion as a public confession of faith."],
                ],
                inputs=[text_input_chirho],
            )

        with gr.Tab("Detailed Scores"):
            detail_input_chirho = gr.Textbox(label="Statement", lines=3)
            detail_btn_chirho = gr.Button("Show All Scores")
            detail_output_chirho = gr.Markdown()
            detail_btn_chirho.click(detailed_scores_chirho, inputs=[detail_input_chirho], outputs=[detail_output_chirho])

        with gr.Tab("Compare"):
            compare_a_chirho = gr.Textbox(label="Statement A", lines=2)
            compare_b_chirho = gr.Textbox(label="Statement B", lines=2)
            compare_btn_chirho = gr.Button("Compare")
            compare_output_chirho = gr.Markdown()
            compare_btn_chirho.click(
                compare_statements_chirho,
                inputs=[compare_a_chirho, compare_b_chirho],
                outputs=[compare_output_chirho],
            )

        with gr.Tab("Batch"):
            batch_input_chirho = gr.Textbox(label="Statements (one per line)", lines=10)
            batch_btn_chirho = gr.Button("Analyze All")
            batch_output_chirho = gr.Markdown()
            batch_btn_chirho.click(batch_analysis_chirho, inputs=[batch_input_chirho], outputs=[batch_output_chirho])

        with gr.Tab("About"):
            gr.Markdown("""# Theological Guardrails

## What This Does
This AI system classifies theological statements as **orthodox**, **heterodox**, or **denominational distinctive** based on the first six ecumenical councils:

1. **Nicaea I** (325 AD) - Christ is God, consubstantial with the Father
2. **Constantinople I** (381 AD) - Holy Spirit is God, full Trinity
3. **Ephesus** (431 AD) - Christ is one person, Mary is Theotokos
4. **Chalcedon** (451 AD) - Two natures, fully God and fully man
5. **Constantinople II** (553 AD) - Reinforces Chalcedon
6. **Constantinople III** (681 AD) - Two wills in Christ

## Three-Model Pipeline
1. **Classifier** (RoBERTa-large, F1=0.9971) - Multi-label classification
2. **Embedder** (MiniLM-L12, Pearson=0.970) - Theological embedding space
3. **Explainer** (Flan-T5-base, eval_loss=0.0567) - Natural language explanations

## Heresies Detected
Arianism, Pelagianism, Gnosticism, Modalism, Docetism, Nestorianism, Marcionism, Apollinarianism, Monothelitism, Semi-Pelagianism, Adoptionism, Patripassianism

## Denominational Handling
Intra-Christian disagreements (predestination, baptism mode, spiritual gifts, etc.) are labeled as **denominational distinctives**, NOT heresy.

## Important Disclaimer
This is an **assistive tool**, not a replacement for theological education or pastoral wisdom. Always consult trained theologians for important doctrinal questions.

---
Built with love for Jesus. Published by [loveJesus](https://huggingface.co/LoveJesus).
""")

    return demo_chirho


# Load models at startup
load_models_chirho()

# Launch
demo_chirho = build_demo_chirho()
demo_chirho.launch()
