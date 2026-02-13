# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
demo-chirho.py
Gradio demo for the theological guardrails pipeline.
Interactive web interface with 6 tabs for exploring the models.
"""

import json
from pathlib import Path

import gradio as gr
import numpy as np

# Import our pipeline
from pipeline_chirho import TheologianPipelineChirho, ClassificationResultChirho

# Initialize pipeline once
pipeline_chirho = None


def get_pipeline_chirho() -> TheologianPipelineChirho:
    """Lazy-load the pipeline."""
    global pipeline_chirho
    if pipeline_chirho is None:
        pipeline_chirho = TheologianPipelineChirho()
    return pipeline_chirho


# Tab 1: Quick Classification
def classify_statement_chirho(text_chirho: str, threshold_chirho: float = 0.5) -> tuple:
    """Classify a theological statement."""
    if not text_chirho.strip():
        return "Please enter a statement.", "", ""

    p_chirho = get_pipeline_chirho()
    result_chirho = p_chirho.analyze_chirho(text_chirho, threshold_chirho)

    # Format label with emoji
    label_map_chirho = {
        "orthodox": "Orthodox",
        "heterodox": "Heterodox",
        "uncertain": "Uncertain",
        "denominational_distinctive": "Denominational Distinctive",
        "unknown": "Unknown",
    }

    label_display_chirho = label_map_chirho.get(result_chirho.overall_label_chirho, result_chirho.overall_label_chirho)
    label_with_conf_chirho = f"{label_display_chirho} (confidence: {result_chirho.confidence_chirho:.1%})"

    # Format heresies
    heresies_display_chirho = ""
    if result_chirho.top_heresies_chirho:
        heresies_display_chirho = "\n".join(
            f"- {h.replace('_chirho', '').replace('_', ' ').title()}: {result_chirho.heresy_scores_chirho.get(h, 0):.1%}"
            for h in result_chirho.top_heresies_chirho
        )
    else:
        heresies_display_chirho = "No heresies detected."

    return label_with_conf_chirho, heresies_display_chirho, result_chirho.explanation_chirho


# Tab 2: Detailed Scores
def detailed_scores_chirho(text_chirho: str) -> str:
    """Show all label scores for a statement."""
    if not text_chirho.strip():
        return "Please enter a statement."

    p_chirho = get_pipeline_chirho()
    result_chirho = p_chirho.analyze_chirho(text_chirho)

    lines_chirho = ["| Label | Score | Status |", "| --- | --- | --- |"]
    for label_chirho, score_chirho in sorted(
        result_chirho.heresy_scores_chirho.items(), key=lambda x: -x[1]
    ):
        display_name_chirho = label_chirho.replace("_chirho", "").replace("_", " ").title()
        bar_chirho = "=" * int(score_chirho * 20)
        status_chirho = "DETECTED" if score_chirho > 0.5 else ""
        lines_chirho.append(f"| {display_name_chirho} | {score_chirho:.3f} {bar_chirho} | {status_chirho} |")

    return "\n".join(lines_chirho)


# Tab 3: Compare Statements
def compare_statements_chirho(text_a_chirho: str, text_b_chirho: str) -> str:
    """Compare two theological statements."""
    if not text_a_chirho.strip() or not text_b_chirho.strip():
        return "Please enter both statements."

    p_chirho = get_pipeline_chirho()
    result_a_chirho = p_chirho.analyze_chirho(text_a_chirho)
    result_b_chirho = p_chirho.analyze_chirho(text_b_chirho)

    # Compute similarity between the two statements
    similarity_chirho = 0.0
    if p_chirho.embedder_chirho is not None:
        emb_a_chirho = p_chirho.embedder_chirho.encode([text_a_chirho])[0]
        emb_b_chirho = p_chirho.embedder_chirho.encode([text_b_chirho])[0]
        dot_chirho = np.dot(emb_a_chirho, emb_b_chirho)
        similarity_chirho = float(dot_chirho / (np.linalg.norm(emb_a_chirho) * np.linalg.norm(emb_b_chirho)))

    output_chirho = f"""## Statement A
**Label:** {result_a_chirho.overall_label_chirho} ({result_a_chirho.confidence_chirho:.1%})
**Heresies:** {', '.join(result_a_chirho.top_heresies_chirho) or 'None'}
**Orthodox similarity:** {result_a_chirho.embedding_similarity_chirho:.3f}

## Statement B
**Label:** {result_b_chirho.overall_label_chirho} ({result_b_chirho.confidence_chirho:.1%})
**Heresies:** {', '.join(result_b_chirho.top_heresies_chirho) or 'None'}
**Orthodox similarity:** {result_b_chirho.embedding_similarity_chirho:.3f}

## Comparison
**Semantic similarity:** {similarity_chirho:.3f}
**Same classification:** {'Yes' if result_a_chirho.overall_label_chirho == result_b_chirho.overall_label_chirho else 'No'}
"""
    return output_chirho


# Tab 4: Batch Analysis
def batch_analysis_chirho(texts_chirho: str) -> str:
    """Analyze multiple statements (one per line)."""
    if not texts_chirho.strip():
        return "Please enter statements (one per line)."

    p_chirho = get_pipeline_chirho()
    lines_chirho = texts_chirho.strip().split("\n")
    results_chirho = []

    for line_chirho in lines_chirho:
        if not line_chirho.strip():
            continue
        result_chirho = p_chirho.analyze_chirho(line_chirho.strip())
        heresies_str_chirho = ", ".join(
            h.replace("_chirho", "") for h in result_chirho.top_heresies_chirho
        ) or "-"
        results_chirho.append(
            f"| {line_chirho.strip()[:60]}... | {result_chirho.overall_label_chirho} | "
            f"{result_chirho.confidence_chirho:.1%} | {heresies_str_chirho} |"
        )

    header_chirho = "| Statement | Label | Confidence | Heresies |\n| --- | --- | --- | --- |"
    return header_chirho + "\n" + "\n".join(results_chirho)


# Tab 5: About
def about_text_chirho() -> str:
    return """# Theological Guardrails

## What This Does
This AI system classifies theological statements as **orthodox**, **heterodox**, or **denominational distinctive** based on the first six ecumenical councils:

1. **Nicaea I** (325 AD) - Christ is God, consubstantial with the Father
2. **Constantinople I** (381 AD) - Holy Spirit is God, full Trinity
3. **Ephesus** (431 AD) - Christ is one person, Mary is Theotokos
4. **Chalcedon** (451 AD) - Two natures, fully God and fully man
5. **Constantinople II** (553 AD) - Reinforces Chalcedon
6. **Constantinople III** (681 AD) - Two wills in Christ

## Three-Model Pipeline
1. **Classifier** (DeBERTa-v3-large) - Multi-label classification
2. **Embedder** (MiniLM-L12) - Theological embedding space
3. **Explainer** (Flan-T5-base) - Natural language explanations

## Important Disclaimer
This is an **assistive tool**, not a replacement for theological education or pastoral wisdom. It may make errors, especially on nuanced or novel statements. Always consult trained theologians for important doctrinal questions.

## Heresies Detected
Arianism, Pelagianism, Gnosticism, Modalism, Docetism, Nestorianism, Marcionism, Apollinarianism, Monothelitism, Semi-Pelagianism, Adoptionism, Patripassianism

## Denominational Handling
Intra-Christian disagreements (predestination, baptism mode, spiritual gifts, etc.) are labeled as **denominational distinctives**, NOT heresy.

---
Built with love for Jesus. Published by [loveJesus](https://huggingface.co/loveJesus).
"""


# Tab 6: Model Info
def model_info_chirho() -> str:
    """Display model information."""
    p_chirho = get_pipeline_chirho()

    classifier_status_chirho = "Loaded" if p_chirho.classifier_chirho is not None else "Not found"
    embedder_status_chirho = "Loaded" if p_chirho.embedder_chirho is not None else "Not found"
    explainer_status_chirho = "Loaded" if p_chirho.explainer_chirho is not None else "Not found"

    return f"""## Model Status
| Model | Status | Architecture |
| --- | --- | --- |
| Classifier | {classifier_status_chirho} | DeBERTa-v3-large |
| Embedder | {embedder_status_chirho} | MiniLM-L12 |
| Explainer | {explainer_status_chirho} | Flan-T5-base |

## Device
**{p_chirho.device_chirho}**

## Labels
{', '.join(p_chirho.labels_chirho)}
"""


def build_demo_chirho() -> gr.Blocks:
    """Build the Gradio demo interface."""
    with gr.Blocks(
        title="Theological Guardrails - loveJesus/models-chirho",
        theme=gr.themes.Soft(),
    ) as demo_chirho:
        gr.Markdown("# Theological Guardrails Pipeline")
        gr.Markdown("*For God so loved the world that he gave his only begotten Son, that whoever believes in him should not perish but have eternal life. - John 3:16*")

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
            explanation_output_chirho = gr.Textbox(label="Explanation")

            classify_btn_chirho.click(
                classify_statement_chirho,
                inputs=[text_input_chirho, threshold_input_chirho],
                outputs=[label_output_chirho, heresies_output_chirho, explanation_output_chirho],
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
            gr.Markdown(about_text_chirho())

        with gr.Tab("Model Info"):
            info_btn_chirho = gr.Button("Refresh Model Info")
            info_output_chirho = gr.Markdown()
            info_btn_chirho.click(model_info_chirho, outputs=[info_output_chirho])

    return demo_chirho


if __name__ == "__main__":
    demo_chirho = build_demo_chirho()
    demo_chirho.launch(share=False, server_name="0.0.0.0", server_port=7860)
