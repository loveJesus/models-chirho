# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
pipeline_chirho.py
Inference pipeline for the Biblical Language Tutor.
Combines parser + glosser models for word parsing and interlinear glossing.

Usage:
    python pipeline_chirho.py parse hebrew "בָּרָא" "GEN 1:1" "בְּרֵאשִׁית אֱלֹהִים"
    python pipeline_chirho.py gloss hebrew "בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם" "GEN 1:1"
"""

import sys
from pathlib import Path

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent

# Try local models first, fall back to HuggingFace Hub
PARSER_LOCAL_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "parser-chirho" / "best-chirho"
GLOSSER_LOCAL_CHIRHO = BASE_DIR_CHIRHO / "models-chirho" / "glosser-chirho" / "best-chirho"
PARSER_HF_CHIRHO = "LoveJesus/biblical-parser-chirho"
GLOSSER_HF_CHIRHO = "LoveJesus/biblical-glosser-chirho"


class BiblicalTutorChirho:
    """Combined parser + glosser pipeline."""

    def __init__(self):
        self.device_chirho = self._detect_device_chirho()
        self.parser_model_chirho = None
        self.parser_tokenizer_chirho = None
        self.glosser_model_chirho = None
        self.glosser_tokenizer_chirho = None

    def _detect_device_chirho(self) -> str:
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def _load_model_chirho(self, local_path_chirho: Path, hf_id_chirho: str):
        """Load model from local path or HuggingFace Hub."""
        source_chirho = str(local_path_chirho) if local_path_chirho.exists() else hf_id_chirho
        print(f"  Loading from: {source_chirho}")
        tokenizer_chirho = AutoTokenizer.from_pretrained(source_chirho)
        model_chirho = AutoModelForSeq2SeqLM.from_pretrained(source_chirho)
        model_chirho.to(self.device_chirho)
        model_chirho.eval()
        return model_chirho, tokenizer_chirho

    def load_parser_chirho(self):
        """Load parser model."""
        if self.parser_model_chirho is None:
            print("Loading parser...")
            self.parser_model_chirho, self.parser_tokenizer_chirho = self._load_model_chirho(
                PARSER_LOCAL_CHIRHO, PARSER_HF_CHIRHO
            )

    def load_glosser_chirho(self):
        """Load glosser model."""
        if self.glosser_model_chirho is None:
            print("Loading glosser...")
            self.glosser_model_chirho, self.glosser_tokenizer_chirho = self._load_model_chirho(
                GLOSSER_LOCAL_CHIRHO, GLOSSER_HF_CHIRHO
            )

    def _generate_chirho(self, model_chirho, tokenizer_chirho, input_text_chirho: str, max_len_chirho: int = 128) -> str:
        inputs_chirho = tokenizer_chirho(
            input_text_chirho, return_tensors="pt", max_length=max_len_chirho, truncation=True
        )
        inputs_chirho = {k_chirho: v_chirho.to(self.device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

        with torch.no_grad():
            output_ids_chirho = model_chirho.generate(**inputs_chirho, max_length=max_len_chirho)

        return tokenizer_chirho.decode(output_ids_chirho[0], skip_special_tokens=True)

    def parse_word_chirho(
        self, word_chirho: str, lang_chirho: str, ref_chirho: str = "?", context_chirho: str = ""
    ) -> dict:
        """Parse a single word into morphological tags."""
        self.load_parser_chirho()

        input_text_chirho = f"parse [{lang_chirho}]: {word_chirho} [{ref_chirho}]"
        if context_chirho:
            input_text_chirho += f" context: {context_chirho}"

        raw_output_chirho = self._generate_chirho(
            self.parser_model_chirho, self.parser_tokenizer_chirho, input_text_chirho
        )

        # Parse output into dict
        tags_chirho = {}
        for part_chirho in raw_output_chirho.split("|"):
            part_chirho = part_chirho.strip()
            if ":" in part_chirho:
                key_chirho, value_chirho = part_chirho.split(":", 1)
                tags_chirho[key_chirho.strip()] = value_chirho.strip()

        return {
            "input_chirho": input_text_chirho,
            "raw_output_chirho": raw_output_chirho,
            "tags_chirho": tags_chirho,
        }

    def gloss_verse_chirho(self, verse_text_chirho: str, lang_chirho: str, ref_chirho: str = "?") -> dict:
        """Generate interlinear gloss for a verse."""
        self.load_glosser_chirho()

        input_text_chirho = f"gloss [{lang_chirho}]: {verse_text_chirho} [{ref_chirho}]"
        raw_output_chirho = self._generate_chirho(
            self.glosser_model_chirho, self.glosser_tokenizer_chirho, input_text_chirho, max_len_chirho=256
        )

        original_words_chirho = verse_text_chirho.split()
        gloss_words_chirho = [g_chirho.strip() for g_chirho in raw_output_chirho.split("|")]

        interlinear_chirho = []
        for i_chirho in range(max(len(original_words_chirho), len(gloss_words_chirho))):
            orig_chirho = original_words_chirho[i_chirho] if i_chirho < len(original_words_chirho) else ""
            gloss_chirho = gloss_words_chirho[i_chirho] if i_chirho < len(gloss_words_chirho) else ""
            interlinear_chirho.append({"original_chirho": orig_chirho, "gloss_chirho": gloss_chirho})

        return {
            "input_chirho": input_text_chirho,
            "raw_output_chirho": raw_output_chirho,
            "interlinear_chirho": interlinear_chirho,
        }


def main_chirho():
    """CLI interface."""
    if len(sys.argv) < 4:
        print("Usage:")
        print('  python pipeline_chirho.py parse hebrew "בָּרָא" "GEN 1:1" "בְּרֵאשִׁית אֱלֹהִים"')
        print('  python pipeline_chirho.py gloss hebrew "בְּרֵאשִׁית בָּרָא אֱלֹהִים" "GEN 1:1"')
        sys.exit(1)

    tutor_chirho = BiblicalTutorChirho()
    mode_chirho = sys.argv[1]
    lang_chirho = sys.argv[2]

    if mode_chirho == "parse":
        word_chirho = sys.argv[3]
        ref_chirho = sys.argv[4] if len(sys.argv) > 4 else "?"
        context_chirho = sys.argv[5] if len(sys.argv) > 5 else ""

        result_chirho = tutor_chirho.parse_word_chirho(word_chirho, lang_chirho, ref_chirho, context_chirho)
        print(f"\nInput:  {result_chirho['input_chirho']}")
        print(f"Output: {result_chirho['raw_output_chirho']}")
        print("\nParsed tags:")
        for key_chirho, value_chirho in result_chirho["tags_chirho"].items():
            print(f"  {key_chirho}: {value_chirho}")

    elif mode_chirho == "gloss":
        verse_chirho = sys.argv[3]
        ref_chirho = sys.argv[4] if len(sys.argv) > 4 else "?"

        result_chirho = tutor_chirho.gloss_verse_chirho(verse_chirho, lang_chirho, ref_chirho)
        print(f"\nInput:  {result_chirho['input_chirho']}")
        print(f"Output: {result_chirho['raw_output_chirho']}")
        print("\nInterlinear:")
        for entry_chirho in result_chirho["interlinear_chirho"]:
            print(f"  {entry_chirho['original_chirho']:20s} → {entry_chirho['gloss_chirho']}")

    else:
        print(f"Unknown mode: {mode_chirho}. Use 'parse' or 'gloss'.")
        sys.exit(1)


if __name__ == "__main__":
    main_chirho()
