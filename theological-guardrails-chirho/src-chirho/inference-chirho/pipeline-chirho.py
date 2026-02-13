# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
pipeline-chirho.py
Unified inference pipeline that combines all three models:
1. Classifier (DeBERTa-v3-large) - multi-label classification
2. Embedder (MiniLM-L12) - theological embedding similarity
3. Explainer (Flan-T5-base) - natural language explanation
"""

import json
from pathlib import Path
from dataclasses import dataclass, field

import numpy as np
import torch
import yaml
from transformers import (
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

BASE_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH_CHIRHO = BASE_DIR_CHIRHO / "src-chirho" / "train-chirho" / "config-chirho.yaml"
MODELS_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho"


@dataclass
class ClassificationResultChirho:
    """Result from the theological guardrails pipeline."""
    text_chirho: str
    overall_label_chirho: str  # orthodox, heterodox, denominational_distinctive
    confidence_chirho: float
    heresy_scores_chirho: dict[str, float] = field(default_factory=dict)
    top_heresies_chirho: list[str] = field(default_factory=list)
    explanation_chirho: str = ""
    embedding_similarity_chirho: float = 0.0  # similarity to orthodox centroid
    raw_logits_chirho: dict[str, float] = field(default_factory=dict)


class TheologianPipelineChirho:
    """
    Three-model pipeline for theological statement analysis.

    Usage:
        pipeline = TheologianPipelineChirho()
        result = pipeline.analyze_chirho("Jesus is a created being.")
        print(result.overall_label_chirho)  # "heterodox"
        print(result.top_heresies_chirho)   # ["arianism"]
        print(result.explanation_chirho)     # "This statement..."
    """

    def __init__(
        self,
        classifier_path_chirho: str | Path | None = None,
        embedder_path_chirho: str | Path | None = None,
        explainer_path_chirho: str | Path | None = None,
        device_chirho: str | None = None,
    ):
        # Config
        with open(CONFIG_PATH_CHIRHO, "r") as f_chirho:
            self.config_chirho = yaml.safe_load(f_chirho)

        self.labels_chirho = self.config_chirho["classifier_chirho"]["labels_chirho"]

        # Device
        if device_chirho:
            self.device_chirho = torch.device(device_chirho)
        elif torch.backends.mps.is_available():
            self.device_chirho = torch.device("mps")
        elif torch.cuda.is_available():
            self.device_chirho = torch.device("cuda")
        else:
            self.device_chirho = torch.device("cpu")

        print(f"TheologianPipeline using device: {self.device_chirho}")

        # Load models
        self._load_classifier_chirho(classifier_path_chirho)
        self._load_embedder_chirho(embedder_path_chirho)
        self._load_explainer_chirho(explainer_path_chirho)

        # Precompute orthodox centroid for embedder
        self._compute_orthodox_centroid_chirho()

    def _load_classifier_chirho(self, path_chirho: str | Path | None = None):
        """Load the DeBERTa classifier."""
        model_path_chirho = Path(path_chirho) if path_chirho else MODELS_DIR_CHIRHO / "classifier-chirho" / "best-chirho"
        if not model_path_chirho.exists():
            print(f"  Classifier not found at {model_path_chirho}")
            self.classifier_chirho = None
            self.classifier_tokenizer_chirho = None
            return

        print("  Loading classifier...")
        self.classifier_tokenizer_chirho = AutoTokenizer.from_pretrained(str(model_path_chirho))
        self.classifier_chirho = AutoModelForSequenceClassification.from_pretrained(str(model_path_chirho))
        self.classifier_chirho.to(self.device_chirho)

    def _load_embedder_chirho(self, path_chirho: str | Path | None = None):
        """Load the sentence transformer embedder."""
        model_path_chirho = Path(path_chirho) if path_chirho else MODELS_DIR_CHIRHO / "embedder-chirho" / "best-chirho"
        if not model_path_chirho.exists():
            print(f"  Embedder not found at {model_path_chirho}")
            self.embedder_chirho = None
            return

        print("  Loading embedder...")
        from sentence_transformers import SentenceTransformer
        self.embedder_chirho = SentenceTransformer(str(model_path_chirho), device=str(self.device_chirho))

    def _load_explainer_chirho(self, path_chirho: str | Path | None = None):
        """Load the Flan-T5 explainer."""
        model_path_chirho = Path(path_chirho) if path_chirho else MODELS_DIR_CHIRHO / "explainer-chirho" / "best-chirho"
        if not model_path_chirho.exists():
            print(f"  Explainer not found at {model_path_chirho}")
            self.explainer_chirho = None
            self.explainer_tokenizer_chirho = None
            return

        print("  Loading explainer...")
        self.explainer_tokenizer_chirho = AutoTokenizer.from_pretrained(str(model_path_chirho))
        self.explainer_chirho = AutoModelForSeq2SeqLM.from_pretrained(str(model_path_chirho))
        self.explainer_chirho.to(self.device_chirho)

    def _compute_orthodox_centroid_chirho(self):
        """Compute average embedding of known orthodox statements."""
        if self.embedder_chirho is None:
            self.orthodox_centroid_chirho = None
            return

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

        embeddings_chirho = self.embedder_chirho.encode(orthodox_statements_chirho)
        self.orthodox_centroid_chirho = np.mean(embeddings_chirho, axis=0)

    def analyze_chirho(self, text_chirho: str, threshold_chirho: float = 0.5) -> ClassificationResultChirho:
        """
        Run the full three-model pipeline on a theological statement.

        Args:
            text_chirho: The statement to analyze
            threshold_chirho: Classification threshold (default 0.5)

        Returns:
            ClassificationResultChirho with full analysis
        """
        result_chirho = ClassificationResultChirho(text_chirho=text_chirho, overall_label_chirho="unknown", confidence_chirho=0.0)

        # Step 1: Classify
        if self.classifier_chirho is not None:
            self._classify_chirho(result_chirho, threshold_chirho)

        # Step 2: Embed and compare
        if self.embedder_chirho is not None:
            self._embed_chirho(result_chirho)

        # Step 3: Explain
        if self.explainer_chirho is not None:
            self._explain_chirho(result_chirho)

        return result_chirho

    def _classify_chirho(self, result_chirho: ClassificationResultChirho, threshold_chirho: float):
        """Run classifier on the statement."""
        inputs_chirho = self.classifier_tokenizer_chirho(
            result_chirho.text_chirho,
            return_tensors="pt",
            max_length=self.config_chirho["classifier_chirho"]["max_length_chirho"],
            truncation=True,
            padding="max_length",
        )
        inputs_chirho = {k_chirho: v_chirho.to(self.device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

        with torch.no_grad():
            outputs_chirho = self.classifier_chirho(**inputs_chirho)
            scores_chirho = torch.sigmoid(outputs_chirho.logits).cpu().numpy()[0]

        # Build scores dict
        for i_chirho, label_chirho in enumerate(self.labels_chirho):
            result_chirho.heresy_scores_chirho[label_chirho] = float(scores_chirho[i_chirho])
            result_chirho.raw_logits_chirho[label_chirho] = float(outputs_chirho.logits.cpu().numpy()[0][i_chirho])

        # Determine label
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
                self.labels_chirho[i_chirho + 1]
                for i_chirho, s_chirho in enumerate(heresy_scores_chirho)
                if s_chirho > threshold_chirho
            ]
        else:
            result_chirho.overall_label_chirho = "uncertain"
            result_chirho.confidence_chirho = float(max(orthodox_score_chirho, max_heresy_score_chirho))

    def _embed_chirho(self, result_chirho: ClassificationResultChirho):
        """Compute embedding similarity to orthodox centroid."""
        if self.orthodox_centroid_chirho is None:
            return

        embedding_chirho = self.embedder_chirho.encode([result_chirho.text_chirho])[0]

        # Cosine similarity
        dot_chirho = np.dot(embedding_chirho, self.orthodox_centroid_chirho)
        norm_a_chirho = np.linalg.norm(embedding_chirho)
        norm_b_chirho = np.linalg.norm(self.orthodox_centroid_chirho)
        similarity_chirho = float(dot_chirho / (norm_a_chirho * norm_b_chirho))

        result_chirho.embedding_similarity_chirho = similarity_chirho

    def _explain_chirho(self, result_chirho: ClassificationResultChirho):
        """Generate explanation using the explainer model."""
        heresy_str_chirho = ", ".join(result_chirho.top_heresies_chirho) if result_chirho.top_heresies_chirho else "none"
        input_text_chirho = (
            f"explain theological classification: {result_chirho.text_chirho} | "
            f"label: {result_chirho.overall_label_chirho} | "
            f"heresy types: {heresy_str_chirho}"
        )

        inputs_chirho = self.explainer_tokenizer_chirho(
            input_text_chirho,
            return_tensors="pt",
            max_length=self.config_chirho["explainer_chirho"]["max_input_length_chirho"],
            truncation=True,
        )
        inputs_chirho = {k_chirho: v_chirho.to(self.device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

        with torch.no_grad():
            outputs_chirho = self.explainer_chirho.generate(
                **inputs_chirho,
                max_length=self.config_chirho["explainer_chirho"]["max_output_length_chirho"],
                num_beams=4,
                early_stopping=True,
            )

        result_chirho.explanation_chirho = self.explainer_tokenizer_chirho.decode(
            outputs_chirho[0], skip_special_tokens=True
        )


def main_chirho():
    """Demo of the pipeline."""
    print("Theological Guardrails Pipeline Demo")
    print("=" * 60)

    pipeline_chirho = TheologianPipelineChirho()

    test_statements_chirho = [
        "Jesus Christ is the eternal Son of God, fully divine and fully human.",
        "Jesus was a created being, the first and greatest of God's creations.",
        "God is one person who manifests as Father, Son, and Spirit.",
        "We can earn salvation through our own good works without needing grace.",
        "The physical world is evil, created by a lesser deity.",
        "Christ has two wills, divine and human, in perfect harmony.",
        "Believers should be baptized by immersion as a public confession of faith.",
    ]

    for statement_chirho in test_statements_chirho:
        print(f"\n{'─' * 60}")
        result_chirho = pipeline_chirho.analyze_chirho(statement_chirho)

        print(f"Statement: {result_chirho.text_chirho}")
        print(f"Label: {result_chirho.overall_label_chirho} (confidence: {result_chirho.confidence_chirho:.3f})")
        if result_chirho.top_heresies_chirho:
            print(f"Heresies: {', '.join(result_chirho.top_heresies_chirho)}")
        print(f"Orthodox similarity: {result_chirho.embedding_similarity_chirho:.3f}")
        if result_chirho.explanation_chirho:
            print(f"Explanation: {result_chirho.explanation_chirho}")


if __name__ == "__main__":
    main_chirho()
