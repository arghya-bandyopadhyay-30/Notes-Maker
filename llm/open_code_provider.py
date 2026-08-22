import re

import requests

from llm.llm_provider import LLMProvider
from utils.environment_system import EnvironmentSystem


class OpenCodeProvider(LLMProvider):
    def __init__(self, environment_system: EnvironmentSystem):
        open_code_path = environment_system.find_executable("opencode")
        self.open_code_process = environment_system.start_process(
            [
                open_code_path,
                "serve"
            ]
        )
        self.base_url = self.get_server_url()
        self.session = requests.post(
            f"{self.base_url}/session",
            json={},
            timeout=10
        ).json()

    def get_server_url(self, max_attempts: int = 10):
        try:
            return next(
                match.group()
                for _ in range(max_attempts)
                if (
                    match := re.search(
                        r"http://127\.0\.0\.1:\d+",
                        self.open_code_process.stdout.readline(),
                    )
                )
            )
        except StopIteration as error:
            raise RuntimeError(
                "Failed to determine the OpenCode server URL."
            ) from error


    async def generate(self, prompt: str):
        pass
