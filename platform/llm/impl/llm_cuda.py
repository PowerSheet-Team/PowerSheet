from __future__ import annotations
from abc import abstractmethod
from typing import Optional

from ..llm import LLM, Context
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoTokenizer, DynamicCache, StoppingCriteria, MaxLengthCriteria
from transformers.modeling_outputs import CausalLMOutputWithPast


class Context_CUDA(Context):
    def __init__(self, model: LlamaForCausalLM, tokenizer: LlamaTokenizer, cache: DynamicCache, tokens: list[int]) -> None:
        super().__init__()
        self.model = model
        self.tokenizer = tokenizer
        self.cache = cache
        self.tokens = tokens

    def query(self, input: str, prefix='', max_new_tokens=50, early_stopping: Optional[function[str, bool]] = None) -> str:
        messages = [{"role": "user", "content": input}]
        input_ids: torch.Tensor = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            use_cache = True,
        )
        self.tokens += input_ids

        # prefix
        prefix_ids = self.tokenizer.apply_chat_template(
            [{"role": "assistant", "content": prefix}],
            add_generation_prompt=False,
        )
        assert prefix_ids[-1] == self.tokenizer.convert_tokens_to_ids("<|eot_id|>"), f"!= {prefix_ids[-1]}"
        self.tokens += prefix_ids[:-1]

        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        if early_stopping is not None:
            ctx = self
            class EarlyStopping(StoppingCriteria):
                def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
                    # assume batch size is 1
                    generate_message = ctx.tokenizer.decode(input_ids[0][len(ctx.tokens):-1], skip_special_tokens=True)
                    stop =  early_stopping(generate_message)
                    # print('generate_message: ', f'"generate_message"', ' stop: ', stop)
                    return torch.tensor(stop, dtype=torch.bool, device=input_ids.device).reshape(1)
            stopping_criteria = EarlyStopping()
            # stopping_criteria = None
        else:
            stopping_criteria = None
        
        outputs = self.model.generate(
            torch.tensor([self.tokens], dtype=torch.long, device=self.model.device), 
            eos_token_id=terminators,
            use_cache=True,
            return_dict_in_generate=True, 
            past_key_values=self.cache,
            max_new_tokens=max_new_tokens,
            stopping_criteria=[stopping_criteria] if stopping_criteria is not None else None,
        )
        self.cache = outputs.past_key_values
        response = outputs.sequences[0][len(self.tokens):]
        # print(outputs)
        return prefix + self.tokenizer.decode(response, skip_special_tokens=True)


class LLM_CUDA(LLM):
    def __init__(self, model_name: str, system_prompt: str) -> None:
        super().__init__()
        self.model_name = model_name
        self.model = LlamaForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map='auto',
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.eval()
        self.cache = DynamicCache()
        self.tokens = []
        # build initial kv cache
        # https://llama.meta.com/docs/model-cards-and-prompt-formats/llama3_1/ Supported Roles
        messages = [
            {"role": "system", "content": system_prompt},
            # {"role": "user", "content": ""}, # user prompt will append here
        ]
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=False,
        )
        self.tokens += input_ids
        
        outputs: CausalLMOutputWithPast = self.model(
            torch.tensor([self.tokens], dtype=torch.long, device=self.model.device),
            past_key_values = self.cache,
            use_cache=True,
            return_dict=True,
        )
        self.cache = outputs.past_key_values

    def getContext(self):
        cache_copy = DynamicCache()
        cache_copy.key_cache = self.cache.key_cache.copy()
        cache_copy.value_cache = self.cache.value_cache.copy()
        return Context_CUDA(self.model, self.tokenizer, cache_copy, self.tokens.copy())