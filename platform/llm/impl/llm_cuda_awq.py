from __future__ import annotations
import pickle

from .llm_hf import LLM_HF
from transformers import LlamaForCausalLM, AutoTokenizer
from transformers import AutoTokenizer
import torch

class LLM_CUDA_AWQ(LLM_HF):
    def __init__(self, model_name: str, quant_path: str, system_prompt: str) -> None:
        from awq import AutoAWQForCausalLM
        quant_config = { "zero_point": True, "q_group_size": 128, "w_bit": 4, "version": "GEMM" }
        with open(quant_path, "rb") as f:
            scales = pickle.load(f)
        model = AutoAWQForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map='auto',
            low_cpu_mem_usage=True,
            precomputed_scales=scales
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model.quantize(tokenizer, quant_config=quant_config)
        super().__init__(model, tokenizer, system_prompt)

