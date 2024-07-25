import os
from llm.impl.llm_cuda import LLM_CUDA, Context_CUDA

SYSTEM_PROMPT = "You will be working with Excel Sheets. You should output the content of each cell, in column-major order, one line for a single cell. WRAP THE CELL CONTENT in <CELL></CELL> and only wrap them ONCE. You are expected to output at least 1 lines. You are encouraged to use formula if it is appliable. You should only generate one possible solution, and only output ONCE for each cell in <CELL></CELL>. Don't output the additional evaluated result of formulas."
USER_PROMPT1 = "I have an Excel sheet, and a section from A4 to A9. Now I want you to fill A10 with data or formula. I want to fill in the way that \"sum them up\"."
USER_PROMPT2 = "Now I don't want to use formula, I want to fill with data."
USER_PROMPT3 = "Now I still want to use prompt, but I want average."
def main():
    model_name = os.environ['LLAMA3']
    llm = LLM_CUDA(model_name, SYSTEM_PROMPT)
    ctx = llm.getContext()
    print('USER_PROMPT1:', USER_PROMPT1)
    rep = ctx.query(USER_PROMPT1, prefix='<CELL>', early_stopping=lambda s: '</CELL>' in s)
    print('Respond:\n' + rep)
    print()
    print('USER_PROMPT2:', USER_PROMPT2)
    rep = ctx.query(USER_PROMPT2, prefix='<CELL>', early_stopping=lambda s: '</CELL>' in s)
    print('Respond:\n' + rep)
    print()
    print('USER_PROMPT3:', USER_PROMPT3)
    rep = ctx.query(USER_PROMPT3, prefix='<CELL>', early_stopping=lambda s: '</CELL>' in s)
    print('Respond:\n' + rep)

if __name__ == '__main__':
    main()