import re

import requests
from pydantic import BaseModel, ValidationError

from src.llm.base import LLMProvider
from src.prompts.models import PromptTemplate
from src.utils.io.environment import EnvironmentSystem


class OpenCodeProvider(LLMProvider):
    def __init__(self, environment_system: EnvironmentSystem):
        open_code_path = environment_system.find_executable("opencode")
        self.open_code_process = environment_system.start_subprocess(
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
        self.environment_system = environment_system

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


    async def invoke(self, prompt: list[PromptTemplate], parser: BaseModel, max_attempts: int = 3) -> str:
        messages = [
            item.to_dict()
            for item in prompt
        ]

        validation_error = None

        for attempt in range(1, max_attempts + 1):
            request_messages = messages

            if validation_error:
                request_messages = [
                    *messages,
                    {
                        "role": "user",
                        "content": (
                            "Your previous response failed schema validation.\n\n"
                            "Regenerate the complete response and strictly "
                            "follow the required JSON schema.\n\n"
                            "Requirements:\n"
                            "- Return ONLY valid JSON.\n"
                            "- Do not use Markdown code fences.\n"
                            "- Do not include explanations, comments, or "
                            "additional text.\n"
                            "- Include all required fields.\n"
                            "- Use the correct data type for every field.\n"
                            "- Correct the validation errors identified below.\n\n"
                            f"Validation error:\n{validation_error}\n\n"
                            "Regenerate the complete response now."
                        ),
                    },
                ]

            response = requests.post(
                f"{self.base_url}/session/{self.session['id']}/message",
                json={
                    "parts": [
                        {
                            "type": "text",
                            "text": str(request_messages),
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

            try:
                parsed_response = parser.model_validate_json(
                    text_part["text"]
                )

                return parsed_response.text

            except ValidationError as exception:
                validation_error = str(exception)

                if attempt == max_attempts:
                    raise

                print(
                    f"LLM response validation failed "
                    f"(attempt {attempt}/{max_attempts}): "
                    f"{validation_error}"
                )

        raise RuntimeError("LLM invocation failed.")