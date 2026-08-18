from dataclasses import field, dataclass
from typing import Any

from utils.string_constants import (
    CONTENT,
    DESCRIPTION,
    METADATA,
    NAME,
    PARAMETERS,
    PROMPT,
    ROLE,
)
from utils.validation import require_field, validate_parameters


@dataclass
class PromptMetadata:
    name: str
    description: str
    parameters: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            NAME: self.name,
            DESCRIPTION: self.description,
            PARAMETERS: self.parameters,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], placeholders: dict[str, Any]) -> "PromptMetadata":
        parameters = require_field(data, PARAMETERS)
        validate_parameters(
            parameters=parameters,
            placeholders=placeholders
        )

        return cls(
            name=require_field(data, NAME),
            description=require_field(data, DESCRIPTION),
            parameters=parameters
        )


@dataclass
class PromptContent:
    role: str
    prompt: str

    def to_dict(self) -> dict[str, Any]:
        return {
            ROLE: self.role,
            PROMPT: self.prompt,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], placeholders: dict[str, Any]) -> "PromptContent":
        render_prompt = (
            lambda prompt: prompt.format(**placeholders)
        )

        return cls(
            role=require_field(data, ROLE),
            prompt=render_prompt(
                prompt=require_field(data, PROMPT),
            ),
        )


@dataclass
class Prompt:
    metadata: PromptMetadata
    content: list[PromptContent]

    def to_dict(self) -> dict[str, Any]:
        return {
            METADATA: self.metadata.to_dict(),
            CONTENT: [item.to_dict() for item in self.content],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], placeholders: dict[str, Any]) -> "Prompt":
        return cls(
            metadata=PromptMetadata.from_dict(
                data=require_field(data, METADATA),
                placeholders=placeholders
            ),
            content=[
                PromptContent.from_dict(
                    data=item,
                    placeholders=placeholders
                )
                for item in require_field(data, CONTENT)
            ],
        )
