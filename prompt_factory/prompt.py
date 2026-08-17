from dataclasses import field, dataclass

from utils.string_constants import (
    CONTENT,
    DESCRIPTION,
    METADATA,
    NAME,
    PARAMETERS,
    PROMPT,
    ROLE,
)
from utils.validation import require_field


@dataclass
class PromptMetadata:
    name: str
    description: str
    parameters: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            NAME: self.name,
            DESCRIPTION: self.description,
            PARAMETERS: self.parameters,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PromptMetadata":
        return cls(
            name=require_field(data, NAME),
            description=require_field(data, DESCRIPTION),
            parameters=require_field(data, PARAMETERS),
        )


@dataclass
class PromptContent:
    role: str
    prompt: str

    def to_dict(self) -> dict:
        return {
            ROLE: self.role,
            PROMPT: self.prompt,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PromptContent":
        return cls(
            role=require_field(data, ROLE),
            prompt=require_field(data, PROMPT),
        )


@dataclass
class Prompt:
    metadata: PromptMetadata
    content: list[PromptContent]

    def to_dict(self) -> dict:
        return {
            METADATA: self.metadata.to_dict(),
            CONTENT: [item.to_dict() for item in self.content],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Prompt":
        return cls(
            metadata=PromptMetadata.from_dict(
                require_field(data, METADATA)
            ),
            content=[
                PromptContent.from_dict(item)
                for item in require_field(data, CONTENT)
            ],
        )