from abc import abstractmethod

from ..llm import LLM, Context


class Context_CPU(Context):
    def __init__(self):
        super().__init__()

    def query(self, input: str) -> str:
        return ""


class LLM_CPU(LLM):
    def __init__(self):
        super().__init__()

    def getContext(self):
        super().getContext()
