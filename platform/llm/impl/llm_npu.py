from abc import abstractmethod

from ..llm import LLM, Context


class Context_NPU(Context):
    def __init__(self):
        super().__init__()

    def query(self, input: str) -> str:
        return ""


class LLM_NPU(LLM):
    def __init__(self):
        super().__init__()

    def getContext(self):
        return Context_NPU()