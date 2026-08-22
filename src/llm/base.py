import asyncio
from abc import ABC, abstractmethod

from pydantic import BaseModel, ValidationError

from src.pipeline.statistics.execution import execution_time
from src.prompts.models import PromptTemplate


class LLMProvider(ABC):
    @abstractmethod
    async def invoke(self, messages: list[dict]) -> str:
        pass

    @abstractmethod
    def close(self):
        pass

    async def response_with_retries(
            self,
            prompt: list[PromptTemplate],
            parser: type[BaseModel],
            max_attempts: int = 3,
    ) -> BaseModel:
        messages = [
            item.to_dict()
            for item in prompt
        ]

        validation_error = ""

        for attempt in range(1, max_attempts + 1):
            request_messages = self.request_messages(
                messages,
                validation_error,
            )

            response_text = await self.invoke(request_messages)

            try:
                return parser.model_validate_json(response_text)

            except ValidationError as exception:
                validation_error = str(exception)

                print(
                    f"LLM response validation failed "
                    f"(attempt {attempt}/{max_attempts}): "
                    f"{validation_error}"
                )

                if attempt == max_attempts:
                    raise RuntimeError(
                        f"LLM response validation failed after "
                        f"{max_attempts} attempts: "
                        f"{validation_error}"
                    ) from exception

        raise RuntimeError("LLM invocation failed.")


    def request_messages(self, messages: list[dict], validation_error: str) -> list[dict]:
        if not validation_error:
            return messages

        return [
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


    @execution_time
    async def generate(self, prompt: list[PromptTemplate], parser: type[BaseModel]) -> type[BaseModel]:
        return await self.response_with_reties(prompt, parser)

    @execution_time
    async def batch_generate(self, prompts: list[list[PromptTemplate]], parser: type[BaseModel]) -> list[type[BaseModel]]:
        return await asyncio.gather(
            *(
                self.response_with_reties(prompt, parser)
                for prompt in prompts
            )
        )
