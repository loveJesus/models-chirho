# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
Gradio Space for Manuscript Variant Analyzer
Classifies NT Greek manuscript variants by type and shows edition support.
"""

import gradio as gr
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_ID_CHIRHO = "LoveJesus/biblical-variant-classifier-chirho"

tokenizer_chirho = None
model_chirho = None
device_chirho = "cpu"


def load_model_chirho():
    """Load model on first use."""
    global tokenizer_chirho, model_chirho, device_chirho
    if model_chirho is not None:
        return

    if torch.cuda.is_available():
        device_chirho = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device_chirho = "mps"

    tokenizer_chirho = AutoTokenizer.from_pretrained(MODEL_ID_CHIRHO)
    model_chirho = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID_CHIRHO).to(device_chirho)
    model_chirho.eval()


def classify_variant_chirho(
    greek_word_chirho: str,
    verse_ref_chirho: str,
    context_chirho: str,
    editions_chirho: str,
) -> str:
    """Classify a manuscript variant."""
    load_model_chirho()

    input_text_chirho = (
        f"classify variant [greek]: {greek_word_chirho} "
        f"[{verse_ref_chirho}] editions: {editions_chirho} "
        f"context: {context_chirho}"
    )

    input_ids_chirho = tokenizer_chirho(
        input_text_chirho, return_tensors="pt", max_length=256, truncation=True
    ).input_ids.to(device_chirho)

    with torch.no_grad():
        output_ids_chirho = model_chirho.generate(input_ids_chirho, max_length=128)

    result_chirho = tokenizer_chirho.decode(output_ids_chirho[0], skip_special_tokens=True)

    # Format output nicely
    parts_chirho = [p.strip() for p in result_chirho.split("|")]
    formatted_chirho = "\n".join(f"  {p}" for p in parts_chirho)

    return f"Input: {input_text_chirho}\n\nClassification:\n{formatted_chirho}"


# Gradio interface
with gr.Blocks(title="Manuscript Variant Analyzer") as demo_chirho:
    gr.Markdown(
        """
        # Manuscript Variant Analyzer
        *Classifies New Testament Greek manuscript variants by type*

        Enter a Greek word, verse reference, surrounding context, and which critical
        editions include this reading. The model will classify the variant type
        (substitution, omission, addition, spelling, harmonization, word_order).
        """
    )

    with gr.Row():
        with gr.Column():
            greek_input_chirho = gr.Textbox(
                label="Greek Word/Phrase",
                placeholder="βαπτίζω",
                value="βαπτίζω",
            )
            ref_input_chirho = gr.Textbox(
                label="Verse Reference",
                placeholder="MAT.3.11",
                value="MAT.3.11",
            )
            context_input_chirho = gr.Textbox(
                label="Surrounding Context (Greek)",
                placeholder="ἐγὼ μὲν ὑμᾶς βαπτίζω ἐν ὕδατι",
                value="ἐγὼ μὲν ὑμᾶς βαπτίζω ἐν ὕδατι",
            )
            editions_input_chirho = gr.Textbox(
                label="Editions (N=NA28, T=TR, S=SBLGNT, B=Byz, W=WH, H=THGNT)",
                placeholder="NTS",
                value="NTS",
            )
            classify_btn_chirho = gr.Button("Classify Variant", variant="primary")

        with gr.Column():
            output_chirho = gr.Textbox(label="Classification Result", lines=10)

    classify_btn_chirho.click(
        classify_variant_chirho,
        inputs=[greek_input_chirho, ref_input_chirho, context_input_chirho, editions_input_chirho],
        outputs=output_chirho,
    )

    gr.Markdown(
        """
        ---
        *For God so loved the world that he gave his only begotten Son,
        that whoever believes in him should not perish but have eternal life.* — John 3:16

        Model: `LoveJesus/biblical-variant-classifier-chirho` | Data: STEPBible TAGNT (CC BY 4.0)
        """
    )

demo_chirho.launch()
