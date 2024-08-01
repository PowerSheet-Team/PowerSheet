from __future__ import annotations

from .llm_hf import LLM_HF
from transformers import AutoTokenizer


import torch

class LLM_NPU(LLM_HF):
    
    def __init__(self, model_name: str, q_name: str, system_prompt: str) -> None:
        from llm.impl.amd import LlamaAttention, LlamaForCausalLM, LlamaFlashAttention
        import qlinear
        model: LlamaForCausalLM = torch.load(q_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        for n, m in model.named_modules():
            if isinstance(m, qlinear.QLinearPerGrp):
                print(f"Preparing weights of layer : {n}")
                m.device = "aie"
                m.quantize_weights()
        super().__init__(model, tokenizer, system_prompt)

