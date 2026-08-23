import re

import requests

from src.bootstrap.container import DependencyContainer
from src.llm.base.llm_provider import LLMProvider
from src.utils.formatting.strings import (
    OPEN_CODE_DEFAULT_MAX_ATTEMPTS,
    OPEN_CODE_EXECUTABLE,
    OPEN_CODE_ID_KEY,
    OPEN_CODE_MESSAGE_ENDPOINT,
    OPEN_CODE_OUTPUT_LOG,
    OPEN_CODE_PARTS_KEY,
    OPEN_CODE_REQUEST_TIMEOUT,
    OPEN_CODE_SERVE_COMMAND,
    OPEN_CODE_SERVER_URL_ERROR,
    OPEN_CODE_SESSION_ENDPOINT,
    OPEN_CODE_SESSION_TIMEOUT,
    OPEN_CODE_TEXT_KEY,
    OPEN_CODE_TYPE_KEY,
    OPEN_CODE_URL_REGEX,
)


class OpenCodeProvider(LLMProvider):
    def __init__(self, dependencies: DependencyContainer):
        super().__init__(dependencies)
        open_code_path = self.environment_system.find_executable(OPEN_CODE_EXECUTABLE)
        self.open_code_process = self.environment_system.start_subprocess(
            [open_code_path, OPEN_CODE_SERVE_COMMAND]
        )
        self.base_url = self.get_server_url()
        self.session = requests.post(
            f"{self.base_url}{OPEN_CODE_SESSION_ENDPOINT}",
            json={},
            timeout=OPEN_CODE_SESSION_TIMEOUT,
        ).json()

    def close(self) -> None:
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

    def get_server_url(self, max_attempts: int = OPEN_CODE_DEFAULT_MAX_ATTEMPTS):
        for _ in range(max_attempts):
            line = self.open_code_process.stdout.readline()

            print(OPEN_CODE_OUTPUT_LOG.format(line))

            match = re.search(
                OPEN_CODE_URL_REGEX,
                line,
            )

            if match:
                return match.group()

        raise RuntimeError(OPEN_CODE_SERVER_URL_ERROR)

    async def invoke(self, messages: list[dict]) -> str:
        response = requests.post(
            f"{self.base_url}{OPEN_CODE_MESSAGE_ENDPOINT.format(self.session[OPEN_CODE_ID_KEY])}",
            json={
                OPEN_CODE_PARTS_KEY: [
                    {
                        OPEN_CODE_TYPE_KEY: OPEN_CODE_TEXT_KEY,
                        OPEN_CODE_TEXT_KEY: str(messages),
                    }
                ]
            },
            timeout=OPEN_CODE_REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        response_data = response.json()

        text_part = next(
            part
            for part in response_data[OPEN_CODE_PARTS_KEY]
            if part[OPEN_CODE_TYPE_KEY] == OPEN_CODE_TEXT_KEY
        )

        return text_part[OPEN_CODE_TEXT_KEY]
