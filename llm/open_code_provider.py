from llm.llm_provider import LLMProvider
from utils.environment_system import EnvironmentSystem


class OpenCodeProvider(LLMProvider):
    def __init__(self, environment_system: EnvironmentSystem):
        open_code_path = environment_system.find_executable("opencode")


    async def generate(self, prompt: str):
        pass
