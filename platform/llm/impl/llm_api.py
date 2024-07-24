from abc import abstractmethod
from openai import OpenAI

from ..llm import LLM, Context


class Context_API(Context):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.messages = []

    def query(self, input: str) -> str:
        completion = self.api.client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=self.make_messages(input),
            temperature=0.3,
        )

        assistant_message = completion.choices[0].message
        self.messages.append(assistant_message)
        return assistant_message.content

    def make_messages(self, input: str, n: int = 20) -> list[dict]:

        self.messages.append({
            "role": "user",
            "content": input,
        })

        new_messages = []
        new_messages.extend(self.api.system_messages)

        if len(self.messages) > 20:
            self.messages = self.messages[-20:]

        new_messages.extend(self.messages)
        return new_messages




class LLM_API(LLM):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            api_key="sk-wGOzmydo7eSA3DnihxDksTWwllymhDyzp58q7mVQDmYCrhnN",
            base_url="https://api.moonshot.cn/v1",
        )
        self.system_messages = [
            {"role": "system",
             "content": "You are an expert in Excel formulas and macros, capable of generating accurate and precise Excel formulas through table examples and prompts."},
        ]

    def getContext(self):
        return Context_API(self)


