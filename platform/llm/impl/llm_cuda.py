from __future__ import annotations

from .llm_hf import LLM_HF
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoTokenizer, DynamicCache, StoppingCriteria, MaxLengthCriteria
import torch

class LLM_CUDA(LLM_HF):
    def __init__(self, model_name: str, system_prompt: str) -> None:
        model = LlamaForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map='auto',
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        super().__init__(model, tokenizer, system_prompt)

