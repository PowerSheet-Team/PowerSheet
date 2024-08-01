from __future__ import annotations
import time
import timeit
from typing import Optional
from transformers.generation.streamers import BaseStreamer
from transformers import AutoTokenizer
import statistics
import torch
from transformers import LlamaTokenizer
import sys

class Timer:
    def __enter__(self):
        self.start_time = timeit.default_timer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = timeit.default_timer()
        self.elapsed_time = self.end_time - self.start_time
        print(f"Elapsed time: {self.elapsed_time:.4f} seconds")

import statistics
import time
from transformers.generation.streamers import BaseStreamer

class PerfStreamer(BaseStreamer):
    """
    Streamer that measures the performance of the generation.
    """
    first_latency_list = []
    total_latency_list = []
    token_len_list = []
    begin_t = sys.float_info.max
    end_t = 0.0


    def __init__(self, tokenizer: LlamaTokenizer, print_output: bool = True):
        self.tokenizer = tokenizer
        self.start_time = time.time()
        PerfStreamer.begin_t = min(PerfStreamer.begin_t, self.start_time)
        self.first_time = None
        self.skip_prompt_token = True
        self.end_time = None
        self.total_tokens = 0
        self.token_cache: list[list[int]] = []
        self.prompt_tokens = 0
        self.batch_size: Optional[None] = None
        self.print_output = False

    def put(self, value: torch.Tensor):
        # print(value)
        if self.skip_prompt_token:
            # prompt tokens are list[list[int]]
            if value.dim() == 2:
                self.batch_size = value.size(0)
                self.prompt_tokens = value.size(1)
            else:
                self.prompt_tokens = value.size(0)
            self.token_cache = [ [] for _ in range(self.batch_size)]
            self.skip_prompt_token = False
            return
        if self.batch_size is None:
            assert value.shape == torch.Size([1])
        else:
            assert value.shape == torch.Size([self.batch_size])
        if self.first_time is None:
            self.first_time = time.time()
        for i, v in enumerate(value):
            # print(f'i = {i}, v = {v}.')
            self.token_cache[i].append(v.item())
        

    def end(self):
        self.end_time = time.time()
        PerfStreamer.end_t = max(PerfStreamer.end_t, self.end_time)
        first_latency = self.first_time - self.start_time
        token_len = len(self.token_cache) * len(self.token_cache[0])
        if self.print_output:
            print(f"Batch Generated sentence:")
            for tokens in self.token_cache:
                # print(tokens)
                print(self.tokenizer.decode(tokens, skip_special_tokens=True))
        total_latency = self.end_time - self.first_time
        if self.print_output:
            print(f"Generated {token_len} tokens in {self.end_time - self.start_time:.2f}s. \
                Latency: {(first_latency * 1000):.2f} ms \
                Throughout: {(token_len / (self.end_time - self.first_time))} tokens/s.")
        PerfStreamer.first_latency_list.append(first_latency)
        PerfStreamer.token_len_list.append(token_len)
        PerfStreamer.total_latency_list.append(total_latency)
    
    @classmethod
    def reset_counter(cls):
        cls.first_latency_list.clear()
        cls.total_latency_list.clear()
        cls.token_len_list.clear()
        cls.begin_t = sys.float_info.max
        cls.end_t = 0.0
    
    @classmethod
    def report_counter(cls):
        print(f"Average tokens: {statistics.fmean(cls.token_len_list):.2f}")
        print(f"Average latency: {statistics.fmean(cls.first_latency_list) * 1000:.2f} ms")
        print(f"Average throughput: {(sum(cls.token_len_list) / sum(cls.total_latency_list)):.2f} tokens/s")
        print(f"Overlap throughput: {(sum(cls.token_len_list) / (cls.end_t - cls.begin_t)):.2f} tokens/s")
