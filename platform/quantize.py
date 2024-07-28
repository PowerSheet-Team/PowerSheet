import gc
from llm.impl.amd import LlamaAttention, LlamaForCausalLM, LlamaFlashAttention
from utils import Utils
from transformers import AutoTokenizer
from pre_quant import apply_awq
from quantizer import real_quantize_model_weight
from qmodule import WQLinear
import qlinear
from llm_models import HF_LLAMA_3_8B_INSTRUCT, Q_LLAMA_3_8B_INSTRUCT, AWQ_LLAMA_3_8B_INSTRUCT

import torch
import os
torch.set_num_threads(8)


w_bit = 4

# load hf model
model = LlamaForCausalLM.from_pretrained(HF_LLAMA_3_8B_INSTRUCT, torch_dtype=torch.bfloat16)
print(model)
Utils.print_model_size(model)


# real quantize
q_config = {
        "zero_point": True,
        "q_group_size": 128,  } # whether to use group quantization
awq_results = torch.load(AWQ_LLAMA_3_8B_INSTRUCT, map_location="cpu")
apply_awq(model, awq_results)
print("Quantization config:", q_config)
real_quantize_model_weight(model, w_bit=w_bit, q_config=q_config)


# flash attention
node_args = ()
node_kwargs = {
        'config': model.config,
        'device': "cpu", # args.target
        'max_new_tokens': 11,
        'quant_mode': "awq"
}
Utils.replace_node( model,
                        LlamaAttention,
                        LlamaFlashAttention,
                        node_args, node_kwargs)

Utils.print_model_size(model)
print(model)
gc.collect()


# continue real quantize, since LlamaFlashAttention has WQLinear
Utils.replace_node( model, 
                WQLinear, 
                qlinear.QLinearPerGrp, 
                (), {'device':'cpu', 'w_bit': w_bit, 'group_size':128} )

Utils.print_model_size(model)
print(model)
gc.collect()

    
# Quantize lm_head
Utils.replace_node( model, 
                    torch.nn.Linear, 
                    qlinear.QLinearPerGrp, 
                    (), {'device':'cpu', 'w_bit': 4, 'group_size':32} )
Utils.print_model_size(model)
print(model)
gc.collect()



# save model
torch.save(model, Q_LLAMA_3_8B_INSTRUCT)


print(f"Quantized and saved model: {Q_LLAMA_3_8B_INSTRUCT}")