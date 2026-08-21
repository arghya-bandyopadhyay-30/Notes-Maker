import asyncio
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str):
        pass

    async def batch_generate(self, prompts: list[str]):
        return await asyncio.gather(
            *(
                self.generate(prompt)
                for prompt in prompts
            )
        )
