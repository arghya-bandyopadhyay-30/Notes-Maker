import re

import requests
from pydantic import BaseModel, ValidationError

from src.llm.base import LLMProvider
from src.prompts.models import PromptTemplate
from src.utils.config.container import DependencyContainer
from src.utils.io.environment import EnvironmentSystem


class OpenCodeProvider(LLMProvider):
    def __init__(self, dependencies: DependencyContainer):
        super().__init__(dependencies)
        open_code_path = self.environment_system.find_executable("opencode")
        self.open_code_process = self.environment_system.start_subprocess(
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

    def close(self):
        if self.open_code_process is None:
            return

        if self.open_code_process.poll() is not None:
            self.open_code_process = None
            return

        self.open_code_process.terminate()

        try:
            self.open_code_process.wait(timeout=5)
        except self.environment_system.timeout_subprocess():
            self.open_code_process.kill()
            self.open_code_process.wait()

        self.open_code_process = None


    def get_server_url(self, max_attempts: int = 10):
        for _ in range(max_attempts):
            line = self.open_code_process.stdout.readline()

            print(f"OpenCode output: {line!r}")

            match = re.search(
                r"http://(?:127\.0\.0\.1|localhost):\d+",
                line,
            )

            if match:
                return match.group()

        raise RuntimeError(
            "Failed to determine the OpenCode server URL."
        )


    async def invoke(self, messages: list[dict]) -> str:
        response = requests.post(
            f"{self.base_url}/session/{self.session['id']}/message",
            json={
                "parts": [
                    {
                        "type": "text",
                        "text": str(messages),
                    }
                ]
            },
            timeout=300,
        )

        response.raise_for_status()

        response_data = response.json()

        text_part = next(
            part
            for part in response_data["parts"]
            if part["type"] == "text"
        )

        return text_part["text"]
