import asyncio
from abc import ABC, abstractmethod

from pydantic import BaseModel, ValidationError

from src.pipeline.statistics.execution import execution_time
from src.prompts.factory import PromptFactory
from src.prompts.models import PromptTemplate
from src.utils.config.container import DependencyContainer


class LLMProvider(ABC):
    def __init__(self, dependencies: DependencyContainer):
        self.prompt_factory = dependencies.prompt_factory
        self.environment_system = dependencies.environment_system

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

        async def attempt(
            attempt_number: int,
            validation_error: str,
        ) -> BaseModel:
            response_text = await self.invoke(
                self.request_messages(
                    messages=messages,
                    validation_error=validation_error,
                )
            )

            try:
                return parser.model_validate_json(response_text)

            except ValidationError as exception:
                error = str(exception)

                print(
                    f"LLM response validation failed "
                    f"(attempt {attempt_number}/{max_attempts}): "
                    f"{error}"
                )

                if attempt_number == max_attempts:
                    raise RuntimeError(
                        f"LLM response validation failed after "
                        f"{max_attempts} attempts: "
                        f"{error}"
                    ) from exception

                return await attempt(
                    attempt_number + 1,
                    error,
                )

        return await attempt(1, "")

    def request_messages(
        self,
        messages: list[dict],
        validation_error: str,
    ) -> list[dict]:
        if not validation_error:
            return messages

        validation_prompt = self.prompt_factory.pydantic_validation_prompt(
            placeholders={
                "validation_error": validation_error,
            }
        )

        return [
            *messages,
            *[
                item.to_dict()
                for item in validation_prompt.template
            ],
        ]

    @execution_time
    async def generate(
        self,
        prompt: list[PromptTemplate],
        parser: type[BaseModel],
    ) -> BaseModel:
        return await self.response_with_retries(prompt, parser)

    @execution_time
    async def batch_generate(
        self,
        prompts: list[list[PromptTemplate]],
        parser: type[BaseModel],
    ) -> list[BaseModel]:
        return await asyncio.gather(
            *(
                self.response_with_retries(prompt, parser)
                for prompt in prompts
            )
        )
