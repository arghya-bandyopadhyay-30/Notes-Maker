import asyncio
from abc import ABC, abstractmethod

from pipeline_statistics.execution_time import execution_time


class LLMProvider(ABC):
    @abstractmethod
    async def invoke(self, prompt) -> str:
        pass

    @execution_time
    async def generate(self, prompt: str) -> str:
        return await self.invoke(prompt)

    @execution_time
    async def batch_generate(self, prompts: list[str]) -> list[str]:
        return await asyncio.gather(
            *(
                self.invoke(prompt)
                for prompt in prompts
            )
        )
