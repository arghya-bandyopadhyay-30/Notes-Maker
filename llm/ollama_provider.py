from pydantic import BaseModel

from llm.llm_provider import LLMProvider
from prompt_factory.prompt import PromptTemplate


class OllamaProvider(LLMProvider):
    def __init__(self):
        pass

    async def invoke(self, prompt: list[PromptTemplate], parser: BaseModel):
        pass
