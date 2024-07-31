from __future__ import annotations

from transformers import PreTrainedTokenizerFast
from pre_quant import apply_awq
from quantizer import real_quantize_model_weight
from .llm_hf import LLM_HF
from llm_models import HF_LLAMA_3_8B_INSTRUCT, Q_LLAMA_3_8B_INSTRUCT, AWQ_LLAMA_3_8B_INSTRUCT, HF_LLAMA_3_8B_INSTRUCT_SHORT_NAME
from llm_eval import (
    LlamaModelEval,
)
from ryzenai_llm_engine import RyzenAILLMEngine, TransformConfig
from transformers import PreTrainedTokenizerFast
from ryzenai_llm_quantizer import QuantConfig, RyzenAILLMQuantizer

import torch

class LLM_NPU(LLM_HF):
    def __init__(self, model_name: str, q_name: str, system_prompt: str) -> None:
        model: LlamaModelEval = torch.load(q_name)
        print(model)
        tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
        
        transform_config = TransformConfig(
            flash_attention_plus=True,
            fast_mlp=True,
            fast_attention=False,
            precision="w4abf16",
            model_name=HF_LLAMA_3_8B_INSTRUCT_SHORT_NAME,
            target="aie",
            w_bit=4,
            group_size=128,
            profilegemm=False,
            profile_layer=False,
            mhaops="all",
        )

        model = RyzenAILLMEngine.transform(model, transform_config)
        model = model.to(torch.bfloat16)
        print(model)
        model.eval()
        super().__init__(model, tokenizer, system_prompt)

