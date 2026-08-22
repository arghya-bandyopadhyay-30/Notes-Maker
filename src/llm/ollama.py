from pydantic import BaseModel

from src.llm.base import LLMProvider
from src.prompts.models import PromptTemplate


class OllamaProvider(LLMProvider):
    def __init__(self):
        pass

    async def invoke(self, prompt: list[PromptTemplate]):
        pass
