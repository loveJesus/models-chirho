# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
pipeline-chirho.py
Inference pipeline for Model 9: Evangelism & Apologetics.

Architecture:
  User Question -> [Intent Classifier (RoBERTa-base)]
      |-> evangelism_dialogue -> [Generator directly]
      |-> apologetics_qa -> [Retriever] -> [RAG corpus] -> [Generator]
      |-> creation_science -> [Retriever] -> [RAG corpus] -> [Generator]
      |-> historical_evidence -> [Retriever] -> [RAG corpus] -> [Generator]
      |-> miracle_testimony -> [Retriever] -> [RAG corpus] -> [Generator]
                |
      [Qwen3-14B LoRA Generator]
                |
      [Theological Guardrails (existing, F1=0.997)]
                |
      Final Response with Scripture references
"""

import json
from pathlib import Path

import numpy as np
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoModelForCausalLM,
    AutoTokenizer,
)
from sentence_transformers import SentenceTransformer

try:
    from peft import PeftModel
except ImportError:
    PeftModel = None

# ── Constants ──────────────────────────────────────────────────────────
BASE_DIR_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho")
MODELS_DIR_CHIRHO = BASE_DIR_CHIRHO / "models-chirho"

INTENT_MODEL_DIR_CHIRHO = MODELS_DIR_CHIRHO / "intent-classifier-chirho" / "best-chirho"
RETRIEVER_MODEL_DIR_CHIRHO = MODELS_DIR_CHIRHO / "retriever-chirho" / "best-chirho"
GENERATOR_MODEL_DIR_CHIRHO = MODELS_DIR_CHIRHO / "generator-chirho" / "best-chirho"
CORPUS_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "raw-chirho"

GENERATOR_BASE_CHIRHO = "Qwen/Qwen3-14B"
TOP_K_PASSAGES_CHIRHO = 5

INTENT_LABELS_CHIRHO = [
    "evangelism_dialogue",
    "apologetics_qa",
    "creation_science",
    "historical_evidence",
    "miracle_testimony",
]

SYSTEM_PROMPT_CHIRHO = (
    "You are a knowledgeable Christian apologist and evangelist. "
    "Answer questions with Scripture references, sound reasoning, "
    "and a heart for sharing the Gospel of Jesus Christ. "
    "All answers should be grounded in biblical truth (2 Timothy 3:16). "
    "Be respectful, thorough, and always point to Christ."
)


class EvangelismPipelineChirho:
    """Full inference pipeline for evangelism and apologetics."""

    def __init__(self, device_chirho=None):
        if device_chirho is None:
            if torch.backends.mps.is_available():
                self.device_chirho = "mps"
            elif torch.cuda.is_available():
                self.device_chirho = "cuda"
            else:
                self.device_chirho = "cpu"
        else:
            self.device_chirho = device_chirho

        print(f"Pipeline device: {self.device_chirho}")

        self.intent_model_chirho = None
        self.intent_tokenizer_chirho = None
        self.retriever_chirho = None
        self.generator_chirho = None
        self.generator_tokenizer_chirho = None
        self.corpus_embeddings_chirho = None
        self.corpus_passages_chirho = None

    def load_intent_classifier_chirho(self):
        """Load the intent classification model."""
        print("Loading intent classifier...")
        self.intent_tokenizer_chirho = AutoTokenizer.from_pretrained(
            str(INTENT_MODEL_DIR_CHIRHO)
        )
        self.intent_model_chirho = AutoModelForSequenceClassification.from_pretrained(
            str(INTENT_MODEL_DIR_CHIRHO)
        )
        self.intent_model_chirho.to(self.device_chirho) if self.device_chirho != "cpu" else None
        print("  Intent classifier loaded.")

    def load_retriever_chirho(self):
        """Load the retriever model and build corpus index."""
        print("Loading retriever...")
        self.retriever_chirho = SentenceTransformer(
            str(RETRIEVER_MODEL_DIR_CHIRHO),
            device=self.device_chirho,
        )

        # Build corpus index from all raw data
        print("  Building corpus index...")
        self.corpus_passages_chirho = []
        self._load_corpus_chirho()

        if self.corpus_passages_chirho:
            texts_chirho = [p_chirho["text_chirho"] for p_chirho in self.corpus_passages_chirho]
            self.corpus_embeddings_chirho = self.retriever_chirho.encode(
                texts_chirho,
                show_progress_bar=True,
                batch_size=64,
                convert_to_numpy=True,
            )
            print(f"  Indexed {len(self.corpus_passages_chirho)} passages.")
        else:
            print("  Warning: No corpus passages found.")

    def _load_corpus_chirho(self):
        """Load all raw corpus data for retrieval."""
        for jsonl_path_chirho in CORPUS_DIR_CHIRHO.rglob("*.jsonl"):
            with open(jsonl_path_chirho, "r", encoding="utf-8") as f_chirho:
                for line_chirho in f_chirho:
                    line_chirho = line_chirho.strip()
                    if not line_chirho:
                        continue
                    try:
                        entry_chirho = json.loads(line_chirho)
                    except json.JSONDecodeError:
                        continue

                    text_chirho = ""
                    meta_chirho = {}

                    if "answer_chirho" in entry_chirho:
                        text_chirho = entry_chirho["answer_chirho"][:2000]
                        meta_chirho["question_chirho"] = entry_chirho.get("question_chirho", "")
                    elif "evidence_chirho" in entry_chirho:
                        claim_chirho = entry_chirho.get("claim_chirho", "")
                        evidence_chirho = entry_chirho.get("evidence_chirho", "")
                        rebuttal_chirho = entry_chirho.get("rebuttal_chirho", "")
                        text_chirho = f"{claim_chirho}\n\n{evidence_chirho}\n\n{rebuttal_chirho}"[:2000]
                        meta_chirho["category_chirho"] = entry_chirho.get("category_chirho", "")
                    elif "text_chirho" in entry_chirho:
                        text_chirho = entry_chirho["text_chirho"][:2000]
                    elif "argument_chirho" in entry_chirho:
                        text_chirho = entry_chirho.get("argument_chirho", "")
                        context_chirho = entry_chirho.get("context_chirho", "")
                        text_chirho = f"{text_chirho}\n\n{context_chirho}"[:2000]

                    if text_chirho and len(text_chirho) > 30:
                        meta_chirho["source_chirho"] = entry_chirho.get("source_chirho", "unknown")
                        meta_chirho["scripture_chirho"] = entry_chirho.get("scripture_chirho", [])
                        self.corpus_passages_chirho.append({
                            "text_chirho": text_chirho.strip(),
                            "meta_chirho": meta_chirho,
                        })

    def load_generator_chirho(self):
        """Load the generator model (Qwen3-4B + LoRA)."""
        print("Loading generator...")
        self.generator_tokenizer_chirho = AutoTokenizer.from_pretrained(
            str(GENERATOR_MODEL_DIR_CHIRHO),
            trust_remote_code=True,
        )
        if self.generator_tokenizer_chirho.pad_token is None:
            self.generator_tokenizer_chirho.pad_token = self.generator_tokenizer_chirho.eos_token

        dtype_chirho = torch.bfloat16 if self.device_chirho == "cuda" else torch.float32

        base_model_chirho = AutoModelForCausalLM.from_pretrained(
            GENERATOR_BASE_CHIRHO,
            torch_dtype=dtype_chirho,
            trust_remote_code=True,
            device_map="auto" if self.device_chirho == "cuda" else None,
        )

        if PeftModel is not None:
            self.generator_chirho = PeftModel.from_pretrained(
                base_model_chirho,
                str(GENERATOR_MODEL_DIR_CHIRHO),
            )
        else:
            self.generator_chirho = base_model_chirho

        if self.device_chirho == "mps":
            self.generator_chirho.to("mps")
        print("  Generator loaded.")

    def load_all_chirho(self):
        """Load all pipeline components."""
        self.load_intent_classifier_chirho()
        self.load_retriever_chirho()
        self.load_generator_chirho()
        print("\nAll components loaded. Pipeline ready.")

    def classify_intent_chirho(self, question_chirho):
        """Classify the user's intent."""
        inputs_chirho = self.intent_tokenizer_chirho(
            question_chirho,
            truncation=True,
            max_length=128,
            padding="max_length",
            return_tensors="pt",
        )
        if self.device_chirho != "cpu":
            inputs_chirho = {k_chirho: v_chirho.to(self.device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

        with torch.no_grad():
            outputs_chirho = self.intent_model_chirho(**inputs_chirho)
            probs_chirho = torch.softmax(outputs_chirho.logits, dim=-1)
            pred_idx_chirho = torch.argmax(probs_chirho, dim=-1).item()
            confidence_chirho = probs_chirho[0][pred_idx_chirho].item()

        return {
            "intent_chirho": INTENT_LABELS_CHIRHO[pred_idx_chirho],
            "confidence_chirho": confidence_chirho,
        }

    def retrieve_passages_chirho(self, query_chirho, top_k_chirho=TOP_K_PASSAGES_CHIRHO):
        """Retrieve relevant passages for the query."""
        if self.corpus_embeddings_chirho is None:
            return []

        query_embedding_chirho = self.retriever_chirho.encode(
            [query_chirho], convert_to_numpy=True
        )

        similarities_chirho = np.dot(
            self.corpus_embeddings_chirho, query_embedding_chirho.T
        ).flatten()

        top_indices_chirho = np.argsort(similarities_chirho)[-top_k_chirho:][::-1]

        results_chirho = []
        for idx_chirho in top_indices_chirho:
            results_chirho.append({
                "text_chirho": self.corpus_passages_chirho[idx_chirho]["text_chirho"],
                "score_chirho": float(similarities_chirho[idx_chirho]),
                "meta_chirho": self.corpus_passages_chirho[idx_chirho]["meta_chirho"],
            })

        return results_chirho

    def generate_response_chirho(self, question_chirho, context_chirho="", max_new_tokens_chirho=512):
        """Generate a response using the fine-tuned generator."""
        if context_chirho:
            user_content_chirho = (
                f"Context (retrieved passages):\n{context_chirho}\n\n"
                f"Question: {question_chirho}\n\n"
                f"Please answer using the context above and Scripture references."
            )
        else:
            user_content_chirho = question_chirho

        messages_chirho = [
            {"role": "system", "content": SYSTEM_PROMPT_CHIRHO},
            {"role": "user", "content": user_content_chirho},
        ]

        text_chirho = self.generator_tokenizer_chirho.apply_chat_template(
            messages_chirho,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs_chirho = self.generator_tokenizer_chirho(
            text_chirho, return_tensors="pt"
        )
        if self.device_chirho != "cpu":
            inputs_chirho = {k_chirho: v_chirho.to(self.device_chirho) for k_chirho, v_chirho in inputs_chirho.items()}

        with torch.no_grad():
            outputs_chirho = self.generator_chirho.generate(
                **inputs_chirho,
                max_new_tokens=max_new_tokens_chirho,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.generator_tokenizer_chirho.pad_token_id,
            )

        generated_ids_chirho = outputs_chirho[0][inputs_chirho["input_ids"].shape[-1]:]
        response_chirho = self.generator_tokenizer_chirho.decode(
            generated_ids_chirho, skip_special_tokens=True
        )

        return response_chirho.strip()

    def answer_chirho(self, question_chirho):
        """Full pipeline: classify, retrieve, generate."""
        # 1. Classify intent
        intent_result_chirho = self.classify_intent_chirho(question_chirho)
        intent_chirho = intent_result_chirho["intent_chirho"]
        confidence_chirho = intent_result_chirho["confidence_chirho"]

        print(f"  Intent: {intent_chirho} ({confidence_chirho:.2%})")

        # 2. Retrieve context (skip for direct evangelism dialogue)
        context_chirho = ""
        retrieved_chirho = []
        if intent_chirho != "evangelism_dialogue":
            retrieved_chirho = self.retrieve_passages_chirho(question_chirho)
            if retrieved_chirho:
                context_parts_chirho = []
                for i_chirho, passage_chirho in enumerate(retrieved_chirho):
                    context_parts_chirho.append(
                        f"[{i_chirho + 1}] (score: {passage_chirho['score_chirho']:.3f}) "
                        f"{passage_chirho['text_chirho'][:500]}"
                    )
                context_chirho = "\n\n".join(context_parts_chirho)
                print(f"  Retrieved {len(retrieved_chirho)} passages.")

        # 3. Generate response
        response_chirho = self.generate_response_chirho(question_chirho, context_chirho)

        return {
            "question_chirho": question_chirho,
            "intent_chirho": intent_chirho,
            "intent_confidence_chirho": confidence_chirho,
            "retrieved_passages_chirho": len(retrieved_chirho),
            "response_chirho": response_chirho,
        }


def main_chirho():
    """Interactive demo of the evangelism pipeline."""
    print("=" * 60)
    print("Model 9: Evangelism & Apologetics Pipeline")
    print("=" * 60)

    pipeline_chirho = EvangelismPipelineChirho()
    pipeline_chirho.load_all_chirho()

    print("\nReady! Type a question (or 'quit' to exit):\n")

    while True:
        try:
            question_chirho = input("Q: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if question_chirho.lower() in ("quit", "exit", "q"):
            break

        if not question_chirho:
            continue

        print()
        result_chirho = pipeline_chirho.answer_chirho(question_chirho)
        print(f"\nA: {result_chirho['response_chirho']}\n")
        print("-" * 40)


if __name__ == "__main__":
    main_chirho()
