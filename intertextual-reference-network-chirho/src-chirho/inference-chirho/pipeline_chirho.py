# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
pipeline_chirho.py
Two-model inference pipeline for intertextual reference discovery:
  1. Embedder: encode verses → find similar verses via cosine similarity
  2. Classifier: classify the connection type between verse pairs
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer

LABELS_CHIRHO = [
    "direct_quote", "allusion", "thematic_parallel", "typological",
    "prophecy_fulfillment", "parallel_narrative", "contrast",
]


@dataclass
class ReferenceResultChirho:
    """A single cross-reference result."""
    verse_id_chirho: str = ""
    verse_text_chirho: str = ""
    similarity_chirho: float = 0.0
    connection_type_chirho: str = ""
    connection_confidence_chirho: float = 0.0


@dataclass
class PipelineResultChirho:
    """Result from the full pipeline."""
    query_text_chirho: str = ""
    references_chirho: list = field(default_factory=list)


class IntertextualPipelineChirho:
    """Two-model pipeline for biblical cross-reference discovery."""

    def __init__(
        self,
        embedder_path_chirho: str,
        classifier_path_chirho: str,
        verse_map_path_chirho: str | None = None,
        device_chirho: str | None = None,
    ):
        # Device
        if device_chirho:
            self.device_chirho = device_chirho
        elif torch.cuda.is_available():
            self.device_chirho = "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            self.device_chirho = "mps"
        else:
            self.device_chirho = "cpu"

        # Load embedder
        self.embedder_chirho = SentenceTransformer(
            embedder_path_chirho, device=self.device_chirho
        )

        # Load classifier
        self.classifier_tokenizer_chirho = AutoTokenizer.from_pretrained(classifier_path_chirho)
        self.classifier_chirho = AutoModelForSequenceClassification.from_pretrained(
            classifier_path_chirho
        )
        self.classifier_chirho.to(self.device_chirho)
        self.classifier_chirho.eval()

        # Verse index
        self.verse_ids_chirho: list[str] = []
        self.verse_texts_chirho: list[str] = []
        self.verse_embeddings_chirho: np.ndarray | None = None

        # Load verse map if provided
        if verse_map_path_chirho:
            self.load_verse_map_chirho(verse_map_path_chirho)

    def load_verse_map_chirho(self, path_chirho: str):
        """Load verse map and pre-encode all verses."""
        with open(path_chirho, "r") as f_chirho:
            verse_map_chirho = json.load(f_chirho)

        self.verse_ids_chirho = list(verse_map_chirho.keys())
        self.verse_texts_chirho = list(verse_map_chirho.values())

    def build_index_chirho(self, batch_size_chirho: int = 256):
        """Pre-encode all verses for fast retrieval."""
        if not self.verse_texts_chirho:
            raise ValueError("No verse texts loaded. Call load_verse_map_chirho first.")

        print(f"Encoding {len(self.verse_texts_chirho)} verses...")
        self.verse_embeddings_chirho = self.embedder_chirho.encode(
            self.verse_texts_chirho,
            batch_size=batch_size_chirho,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        print("Index built.")

    def find_references_chirho(
        self,
        query_text_chirho: str,
        k_chirho: int = 10,
        classify_chirho: bool = True,
    ) -> PipelineResultChirho:
        """Find the top-k most related verses and classify connection types."""
        if self.verse_embeddings_chirho is None:
            raise ValueError("Index not built. Call build_index_chirho first.")

        # Encode query
        query_emb_chirho = self.embedder_chirho.encode(
            [query_text_chirho], normalize_embeddings=True, convert_to_numpy=True
        )[0]

        # Cosine similarity (embeddings already normalized)
        similarities_chirho = np.dot(self.verse_embeddings_chirho, query_emb_chirho)

        # Top-k
        top_indices_chirho = np.argsort(similarities_chirho)[::-1][:k_chirho]

        result_chirho = PipelineResultChirho(query_text_chirho=query_text_chirho)

        for idx_chirho in top_indices_chirho:
            ref_chirho = ReferenceResultChirho(
                verse_id_chirho=self.verse_ids_chirho[idx_chirho],
                verse_text_chirho=self.verse_texts_chirho[idx_chirho],
                similarity_chirho=float(similarities_chirho[idx_chirho]),
            )

            if classify_chirho:
                cls_result_chirho = self.classify_pair_chirho(
                    query_text_chirho, self.verse_texts_chirho[idx_chirho]
                )
                ref_chirho.connection_type_chirho = cls_result_chirho["type_chirho"]
                ref_chirho.connection_confidence_chirho = cls_result_chirho["confidence_chirho"]

            result_chirho.references_chirho.append(ref_chirho)

        return result_chirho

    def classify_pair_chirho(
        self,
        text_a_chirho: str,
        text_b_chirho: str,
    ) -> dict:
        """Classify the connection type between two verses."""
        inputs_chirho = self.classifier_tokenizer_chirho(
            text_a_chirho, text_b_chirho,
            return_tensors="pt", truncation=True, max_length=256, padding=True,
        )
        inputs_chirho = {
            k_chirho: v_chirho.to(self.device_chirho)
            for k_chirho, v_chirho in inputs_chirho.items()
        }

        with torch.no_grad():
            outputs_chirho = self.classifier_chirho(**inputs_chirho)
            probs_chirho = torch.softmax(outputs_chirho.logits, dim=-1).cpu().numpy()[0]

        pred_idx_chirho = int(np.argmax(probs_chirho))
        return {
            "type_chirho": LABELS_CHIRHO[pred_idx_chirho],
            "confidence_chirho": float(probs_chirho[pred_idx_chirho]),
            "all_scores_chirho": {
                LABELS_CHIRHO[i_chirho]: float(probs_chirho[i_chirho])
                for i_chirho in range(len(LABELS_CHIRHO))
            },
        }
