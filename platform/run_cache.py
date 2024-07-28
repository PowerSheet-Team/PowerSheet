from llm.impl.amd import LlamaForCausalLM
from transformers import AutoTokenizer, TextStreamer, AutoConfig, GenerationConfig
from transformers.modeling_outputs import CausalLMOutputWithPast
import torch
import qlinear
from utils import Utils
import json
torch.set_num_threads(8)
from llm_models import HF_LLAMA_3_8B_INSTRUCT, Q_LLAMA_3_8B_INSTRUCT


model_name = HF_LLAMA_3_8B_INSTRUCT
model: LlamaForCausalLM = torch.load(Q_LLAMA_3_8B_INSTRUCT)
model.generation_config = GenerationConfig.from_model_config(AutoConfig.from_pretrained(model_name))
model.generation_config.return_dict_in_generate = True
tokenizer = AutoTokenizer.from_pretrained(model_name)
print(model.generate)
for n, m in model.named_modules():
    if isinstance(m, qlinear.QLinearPerGrp):
        print(f"Preparing weights of layer : {n}")
        m.device = "aie"
        m.quantize_weights()


messages = [
    {"role": "system", "content": "You will be working with Excel Sheets. You should output the content of each cell, in column-major order, one line for a single cell. WRAP THE CELL CONTENT in <CELL></CELL> and only wrap them ONCE. You are expected to output at least 1 lines. You are encouraged to use formula if it is appliable. You should only generate one possible solution, and only output ONCE for each cell in <CELL></CELL>. Don't output the additional evaluated result of formulas."},
    {"role": "user", "content": "I have an Excel sheet, and a section from A4 to A9. Now I want you to fill A10 with data or formula. I want to fill in the way that \"sum them up\"."},
]

input_ids = tokenizer.apply_chat_template(
    messages,
)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = model.generate(
    torch.tensor([input_ids], device=model.device),
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=False,
    temperature=0.6,
    top_p=0.9,
    use_cache=True,
    return_dict=True,
)
print('outputs:', outputs)
cache = outputs.past_key_values

input_ids = outputs.sequences[0].tolist()

input_ids += tokenizer.apply_chat_template(
    messages,
)



outputs = model.generate(
    torch.tensor([input_ids], device=model.device),
    max_new_tokens=256,
    eos_token_id=terminators,
    return_dict_in_generate=True,
    do_sample=False,
    temperature=0.6,
    top_p=0.9,
    use_cache=True,
    return_dict=True,
    past_key_values = cache,
)

response = outputs.sequences[0]
print('Output')
print(tokenizer.decode(response, skip_special_tokens=True))