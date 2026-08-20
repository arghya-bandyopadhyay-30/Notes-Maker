from abc import ABC, abstractmethod


class LLMClient(ABC):
    async def batch_processing(self):
        pass

    async def async_processing(self):
        pass