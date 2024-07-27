from __future__ import annotations

from .llm_hf import LLM_HF
from transformers import LlamaForCausalLM, AutoTokenizer
import torch

class LLM_CPU(LLM_HF):
    def __init__(self, model_name: str, system_prompt: str, thread_n: int) -> None:
        torch.set_num_threads(thread_n)
        model = LlamaForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map='cpu',
        )
        # model = torch.quantization.quantize_dynamic(
        #     model, {torch.nn.Linear}, dtype=torch.qint8
        # )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        super().__init__(model, tokenizer, system_prompt)

