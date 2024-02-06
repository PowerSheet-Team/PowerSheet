from abc import abstractmethod

class Context:
    def __init__(self):
        pass

    @abstractmethod
    def query(self, input: str) -> str:
        return ""


class LLM:
    def __init__(self):
        self.context = []
        pass

    def getContext(self):
        context = Context()
        self.context.append(context)
        return context
