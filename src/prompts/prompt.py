from dataclasses import dataclass
from typing import Any

from src.prompts.prompt_metadata import PromptMetadata
from src.prompts.prompt_template import PromptTemplate
from src.utils.formatting.strings import (
    METADATA,
    TEMPLATE,
)
from src.utils.validation.validators import require_field


@dataclass
class Prompt:
    metadata: PromptMetadata
    template: list[PromptTemplate]

    def to_dict(self) -> dict[str, Any]:
        return {
            METADATA: self.metadata.to_dict(),
            TEMPLATE: [item.to_dict() for item in self.template],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], placeholders: dict[str, Any]) -> "Prompt":
        return cls(
            metadata=PromptMetadata.from_dict(
                data=require_field(data, METADATA), placeholders=placeholders
            ),
            template=[
                PromptTemplate.from_dict(data=item, placeholders=placeholders)
                for item in require_field(data, TEMPLATE)
            ],
        )
