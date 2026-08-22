import asyncio
from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.pipeline.statistics.execution import execution_time
from src.prompts.models import PromptTemplate


class LLMProvider(ABC):
    @abstractmethod
    async def invoke(self, prompt: list[PromptTemplate], parser: BaseModel) -> str:
        pass

    @abstractmethod
    def close(self):
        pass

    @execution_time
    async def generate(self, prompt: list[PromptTemplate], parser: BaseModel) -> str:
        return await self.invoke(prompt, parser)

    @execution_time
    async def batch_generate(self, prompts: list[list[PromptTemplate]], parser: BaseModel) -> list[str]:
        return await asyncio.gather(
            *(
                self.invoke(prompt, parser)
                for prompt in prompts
            )
        )
