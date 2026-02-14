# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
app.py - HuggingFace Space for the Biblical Entity Recognizer.
Loads the DistilBERT NER model and provides a Gradio interface for
recognizing biblical entities in text with highlighted output.

Entity types: PERSON, DIVINE, PEOPLE_GROUP, PLACE, EVENT, ARTIFACT
"""

import json
from dataclasses import dataclass, field

import gradio as gr
import torch
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    pipeline,
)

# HuggingFace model ID
MODEL_ID_CHIRHO = "LoveJesus/biblical-entity-recognizer-chirho"

# Entity type colors for display
ENTITY_COLORS_CHIRHO = {
    "PERSON": "#4CAF50",      # Green
    "DIVINE": "#FFD700",      # Gold
    "PEOPLE_GROUP": "#2196F3", # Blue
    "PLACE": "#FF9800",       # Orange
    "EVENT": "#9C27B0",       # Purple
    "ARTIFACT": "#F44336",    # Red
}

ENTITY_DESCRIPTIONS_CHIRHO = {
    "PERSON": "Biblical persons (e.g., Moses, David, Paul)",
    "DIVINE": "Names and titles of God (e.g., God, LORD, Jesus Christ, Holy Spirit)",
    "PEOPLE_GROUP": "Nations and ethnic groups (e.g., Israelites, Philistines, Pharisees)",
    "PLACE": "Geographical locations (e.g., Jerusalem, Egypt, Bethlehem)",
    "EVENT": "Biblical events and feasts (e.g., Passover, Pentecost, Sabbath)",
    "ARTIFACT": "Sacred objects (e.g., Urim, Thummim)",
}

# Example verses pre-loaded
EXAMPLE_VERSES_CHIRHO = [
    "In the beginning God created the heaven and the earth.",
    "And the LORD said unto Moses, Come up to me into the mount, and be there.",
    "Then Jesus went with his disciples unto a place called Gethsemane, and saith unto the disciples, Sit ye here, while I go and pray yonder.",
    "And the Philistines gathered together their armies to battle, and were gathered together at Shochoh, which belongeth to Judah.",
    "Now when Jesus was born in Bethlehem of Judaea in the days of Herod the king, behold, there came wise men from the east to Jerusalem.",
    "And Solomon built the house of the LORD, and his own house, in Jerusalem, the city of David.",
    "And Paul said, I would to God, that not only thou, but also all that hear me this day, were both almost, and altogether such as I am.",
    "And the LORD spake unto Moses in the wilderness of Sinai, in the tabernacle of the congregation, on the first day of the second month.",
    "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
    "And the children of Israel did evil in the sight of the LORD, and served Baalim.",
]

# Global pipeline holder
ner_pipeline_chirho = None


@dataclass
class EntityResultChirho:
    """Result for a single recognized entity."""
    text_chirho: str = ""
    entity_type_chirho: str = ""
    confidence_chirho: float = 0.0
    start_chirho: int = 0
    end_chirho: int = 0


def load_model_chirho():
    """Load the NER model and create a pipeline."""
    global ner_pipeline_chirho

    if ner_pipeline_chirho is not None:
        return

    print(f"Loading model: {MODEL_ID_CHIRHO}...")

    try:
        ner_pipeline_chirho = pipeline(
            "token-classification",
            model=MODEL_ID_CHIRHO,
            aggregation_strategy="simple",
        )
        print("Model loaded successfully!")
    except Exception as error_chirho:
        print(f"Failed to load from HF Hub ({error_chirho}), trying local model...")

        # Fallback to local model
        import os
        local_model_path_chirho = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models-chirho", "ner-chirho", "best-chirho"
        )

        if os.path.exists(local_model_path_chirho):
            ner_pipeline_chirho = pipeline(
                "token-classification",
                model=local_model_path_chirho,
                aggregation_strategy="simple",
            )
            print(f"Loaded local model from {local_model_path_chirho}")
        else:
            raise RuntimeError(
                f"Model not found at {MODEL_ID_CHIRHO} or {local_model_path_chirho}. "
                "Please train the model first or check the HuggingFace Hub."
            )


def recognize_entities_chirho(text_chirho: str) -> tuple[dict, str]:
    """
    Run NER on the input text and return highlighted text and entity table.

    Returns:
        tuple of (highlighted_entities, entity_summary_html)
    """
    if not text_chirho or not text_chirho.strip():
        return {"text": "", "entities": []}, "<p>Please enter some text.</p>"

    load_model_chirho()

    # Run pipeline
    raw_results_chirho = ner_pipeline_chirho(text_chirho)

    # Build entity results
    entities_chirho: list[EntityResultChirho] = []

    for result_chirho in raw_results_chirho:
        entity_group_chirho = result_chirho.get("entity_group", "")
        score_chirho = result_chirho.get("score", 0.0)
        word_chirho = result_chirho.get("word", "")
        start_chirho = result_chirho.get("start", 0)
        end_chirho = result_chirho.get("end", 0)

        # Clean up entity group name (remove B-/I- prefix if present)
        clean_type_chirho = entity_group_chirho
        if clean_type_chirho.startswith("B-") or clean_type_chirho.startswith("I-"):
            clean_type_chirho = clean_type_chirho[2:]

        entities_chirho.append(EntityResultChirho(
            text_chirho=word_chirho,
            entity_type_chirho=clean_type_chirho,
            confidence_chirho=score_chirho,
            start_chirho=start_chirho,
            end_chirho=end_chirho,
        ))

    # Build highlighted text for Gradio HighlightedText component
    highlighted_entities_chirho = []
    for entity_chirho in entities_chirho:
        highlighted_entities_chirho.append({
            "entity": entity_chirho.entity_type_chirho,
            "start": entity_chirho.start_chirho,
            "end": entity_chirho.end_chirho,
            "score": entity_chirho.confidence_chirho,
        })

    highlighted_output_chirho = {
        "text": text_chirho,
        "entities": highlighted_entities_chirho,
    }

    # Build summary HTML table
    if entities_chirho:
        summary_html_chirho = build_summary_html_chirho(entities_chirho)
    else:
        summary_html_chirho = "<p><em>No biblical entities detected in the input text.</em></p>"

    return highlighted_output_chirho, summary_html_chirho


def build_summary_html_chirho(entities_chirho: list[EntityResultChirho]) -> str:
    """Build an HTML summary table of detected entities."""
    rows_chirho = []

    for entity_chirho in entities_chirho:
        color_chirho = ENTITY_COLORS_CHIRHO.get(entity_chirho.entity_type_chirho, "#888888")
        confidence_pct_chirho = f"{entity_chirho.confidence_chirho * 100:.1f}%"

        # Confidence bar
        bar_width_chirho = int(entity_chirho.confidence_chirho * 100)
        bar_html_chirho = (
            f'<div style="background:#e0e0e0;border-radius:4px;height:16px;width:100px;display:inline-block;">'
            f'<div style="background:{color_chirho};border-radius:4px;height:16px;width:{bar_width_chirho}px;"></div>'
            f'</div>'
        )

        rows_chirho.append(
            f"<tr>"
            f'<td style="padding:4px 8px;"><strong>{entity_chirho.text_chirho}</strong></td>'
            f'<td style="padding:4px 8px;"><span style="background:{color_chirho};color:white;'
            f'padding:2px 8px;border-radius:4px;font-size:0.85em;">{entity_chirho.entity_type_chirho}</span></td>'
            f'<td style="padding:4px 8px;">{confidence_pct_chirho} {bar_html_chirho}</td>'
            f"</tr>"
        )

    table_html_chirho = (
        '<table style="width:100%;border-collapse:collapse;margin-top:8px;">'
        '<thead><tr>'
        '<th style="text-align:left;padding:4px 8px;border-bottom:2px solid #ddd;">Entity</th>'
        '<th style="text-align:left;padding:4px 8px;border-bottom:2px solid #ddd;">Type</th>'
        '<th style="text-align:left;padding:4px 8px;border-bottom:2px solid #ddd;">Confidence</th>'
        '</tr></thead>'
        f'<tbody>{"".join(rows_chirho)}</tbody>'
        '</table>'
    )

    # Entity type counts
    type_counts_chirho: dict[str, int] = {}
    for entity_chirho in entities_chirho:
        type_counts_chirho[entity_chirho.entity_type_chirho] = (
            type_counts_chirho.get(entity_chirho.entity_type_chirho, 0) + 1
        )

    count_parts_chirho = []
    for type_name_chirho, count_chirho in sorted(
        type_counts_chirho.items(), key=lambda x_chirho: x_chirho[1], reverse=True
    ):
        color_chirho = ENTITY_COLORS_CHIRHO.get(type_name_chirho, "#888888")
        count_parts_chirho.append(
            f'<span style="background:{color_chirho};color:white;padding:2px 8px;'
            f'border-radius:4px;margin:2px;font-size:0.85em;">'
            f'{type_name_chirho}: {count_chirho}</span>'
        )

    summary_chirho = (
        f'<div style="margin-bottom:8px;">{"  ".join(count_parts_chirho)}</div>'
        f'{table_html_chirho}'
    )

    return summary_chirho


def build_legend_html_chirho() -> str:
    """Build an HTML legend for entity types."""
    parts_chirho = []
    for type_name_chirho, description_chirho in ENTITY_DESCRIPTIONS_CHIRHO.items():
        color_chirho = ENTITY_COLORS_CHIRHO[type_name_chirho]
        parts_chirho.append(
            f'<div style="margin:4px 0;">'
            f'<span style="background:{color_chirho};color:white;padding:2px 8px;'
            f'border-radius:4px;font-size:0.85em;display:inline-block;width:120px;'
            f'text-align:center;">{type_name_chirho}</span> '
            f'<span style="color:#666;">{description_chirho}</span>'
            f'</div>'
        )
    return "<div>" + "".join(parts_chirho) + "</div>"


def create_demo_chirho() -> gr.Blocks:
    """Create the Gradio demo interface."""
    with gr.Blocks(
        title="Biblical Entity Recognizer",
        theme=gr.themes.Soft(),
    ) as demo_chirho:

        gr.HTML(
            """
            <div style="text-align:center; margin-bottom:16px;">
                <h1>Biblical Entity Recognizer</h1>
                <p style="color:#666; font-style:italic;">
                    "For God so loved the world, that he gave his only begotten Son,
                    that whosoever believeth in him should not perish,
                    but have everlasting life." - John 3:16
                </p>
                <p>
                    A DistilBERT-based NER model that recognizes persons, divine names,
                    people groups, places, events, and artifacts in biblical text.
                </p>
            </div>
            """
        )

        with gr.Row():
            with gr.Column(scale=2):
                input_text_chirho = gr.Textbox(
                    label="Enter Biblical Text",
                    placeholder="Type or paste a Bible verse here...",
                    lines=4,
                    max_lines=10,
                )

                with gr.Row():
                    submit_btn_chirho = gr.Button("Recognize Entities", variant="primary")
                    clear_btn_chirho = gr.Button("Clear")

                gr.Examples(
                    examples=[[v_chirho] for v_chirho in EXAMPLE_VERSES_CHIRHO],
                    inputs=[input_text_chirho],
                    label="Example Verses (click to try)",
                )

            with gr.Column(scale=3):
                highlighted_output_chirho = gr.HighlightedText(
                    label="Recognized Entities",
                    combine_adjacent=True,
                    show_legend=True,
                    color_map=ENTITY_COLORS_CHIRHO,
                )

                entity_summary_chirho = gr.HTML(
                    label="Entity Details",
                )

        # Entity type legend
        with gr.Accordion("Entity Type Legend", open=False):
            gr.HTML(build_legend_html_chirho())

        # Wire up events
        submit_btn_chirho.click(
            fn=recognize_entities_chirho,
            inputs=[input_text_chirho],
            outputs=[highlighted_output_chirho, entity_summary_chirho],
        )

        input_text_chirho.submit(
            fn=recognize_entities_chirho,
            inputs=[input_text_chirho],
            outputs=[highlighted_output_chirho, entity_summary_chirho],
        )

        clear_btn_chirho.click(
            fn=lambda: ("", {"text": "", "entities": []}, ""),
            inputs=[],
            outputs=[input_text_chirho, highlighted_output_chirho, entity_summary_chirho],
        )

        gr.HTML(
            """
            <div style="text-align:center; margin-top:16px; color:#999; font-size:0.85em;">
                <p>Model: DistilBERT fine-tuned on KJV Bible with STEPBible TIPNR entities</p>
                <p>Entity types: PERSON | DIVINE | PEOPLE_GROUP | PLACE | EVENT | ARTIFACT</p>
            </div>
            """
        )

    return demo_chirho


if __name__ == "__main__":
    demo_chirho = create_demo_chirho()
    demo_chirho.launch()
