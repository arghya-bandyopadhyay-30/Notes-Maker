import asyncio
from abc import ABC, abstractmethod

from pydantic import BaseModel

from pipeline_statistics.execution_time import execution_time
from prompt_factory.prompt import PromptTemplate


class LLMProvider(ABC):
    @abstractmethod
    async def invoke(self, prompt: list[PromptTemplate], parser: BaseModel) -> str:
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
