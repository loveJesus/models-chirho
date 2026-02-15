---
language:
- en
license: mit
tags:
- text-generation
- qwen3
- lora
- peft
- evangelism
- apologetics
- bible
- chirho
datasets:
- LoveJesus/evangelism-dataset-chirho
base_model: Qwen/Qwen3-14B
model-index:
- name: evangelism-generator-chirho
  results:
  - task:
      type: text-generation
      name: Text Generation
    metrics:
    - name: Eval Loss
      type: eval_loss
      value: 1.4060
    - name: Perplexity
      type: perplexity
      value: 4.08
---

<!-- For God so loved the world that he gave his only begotten Son,
that whoever believes in him should not perish but have eternal life. - John 3:16 -->

# Evangelism Generator (Qwen3-14B + LoRA)

Part of Model 9: Evangelism & Apologetics Pipeline for [bible.systems](https://bible.systems).

## Model Description

A Qwen3-14B-Instruct model fine-tuned with LoRA for generating apologetics and evangelism responses. Takes user questions (optionally with RAG-retrieved context passages) and generates Scripture-grounded answers.

## Architecture

- **Base model**: Qwen/Qwen3-14B
- **Fine-tuning**: LoRA (r=16, alpha=32, dropout=0.05)
- **Target modules**: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- **Trainable parameters**: 64M / 14.8B total (0.43%)
- **Training**: 3 epochs, bf16, H200 GPU
- **Eval loss**: 1.4060 (best at step 1200/1992)
- **Perplexity**: 4.08

## Pipeline Architecture

```
User Question -> [Intent Classifier] -> [Retriever] -> [Generator]
                                                         |
                                              Qwen3-14B + LoRA
                                                         |
                                              [Theological Guardrails]
                                                         |
                                              Final Response + Scripture
```

## Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model + LoRA adapter
base_model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-14B",
    torch_dtype="auto",
    trust_remote_code=True,
    device_map="auto",
)
model = PeftModel.from_pretrained(base_model, "LoveJesus/evangelism-generator-chirho")
tokenizer = AutoTokenizer.from_pretrained("LoveJesus/evangelism-generator-chirho")

messages = [
    {"role": "system", "content": "You are a knowledgeable Christian apologist and evangelist."},
    {"role": "user", "content": "What evidence is there for the resurrection of Jesus?"},
]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.7, top_p=0.9)
response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
print(response)
```

## Training Data

10,622 instruction-response pairs from diverse apologetics sources including GotQuestions.org Q&A, Spurgeon sermons, early church fathers, creation science evidence, historical evidence, and miracle testimonies.

## System Prompt

> You are a knowledgeable Christian apologist and evangelist. Answer questions with Scripture references, sound reasoning, and a heart for sharing the Gospel of Jesus Christ. All answers should be grounded in biblical truth (2 Timothy 3:16). Be respectful, thorough, and always point to Christ.

## Related Models

- [LoveJesus/evangelism-intent-classifier-chirho](https://huggingface.co/LoveJesus/evangelism-intent-classifier-chirho) - Intent classifier (RoBERTa-base, macro F1=0.83)
- [LoveJesus/evangelism-retriever-chirho](https://huggingface.co/LoveJesus/evangelism-retriever-chirho) - Passage retriever (MiniLM-L12, Pearson=0.90)
- [LoveJesus/evangelism-dataset-chirho](https://huggingface.co/datasets/LoveJesus/evangelism-dataset-chirho) - Training dataset
