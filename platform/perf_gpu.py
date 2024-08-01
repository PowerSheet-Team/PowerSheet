import os
from llm import LLM_CUDA, PerfStreamer
import torch
import psutil
from llm_models import HF_LLAMA_3_8B_INSTRUCT, Q_LLAMA_3_8B_INSTRUCT


SYSTEM_PROMPT = "You will be working with Excel Sheets. You should output the content of each cell, in column-major order, one line for a single cell. WRAP THE CELL CONTENT in <CELL></CELL> and only wrap them ONCE. You are expected to output at least 1 lines. You are encouraged to use formula if it is appliable. You should only generate one possible solution, and only output ONCE for each cell in <CELL></CELL>. Don't output the additional evaluated result of formulas."
USER_PROMPT1 = "I have an Excel sheet, and a section from A4 to A9. Now I want you to fill A10 with data or formula. I want to fill in the way that \"sum them up\"."
def main():
    llm = LLM_CUDA(HF_LLAMA_3_8B_INSTRUCT, SYSTEM_PROMPT)
    for k in range(3):
        ctx = llm.getContext()
        ctx.query(USER_PROMPT1, perf=k >= 1)
    PerfStreamer.report_counter()

if __name__ == '__main__':
    main()