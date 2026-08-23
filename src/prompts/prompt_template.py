from dataclasses import dataclass
from typing import Any

from src.utils.formatting.strings import (
    CONTENT,
    ROLE,
)
from src.utils.validation.validators import require_field


@dataclass
class PromptTemplate:
    role: str
    content: str

    def to_dict(self) -> dict[str, Any]:
        return {
            ROLE: self.role,
            CONTENT: self.content,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], placeholders: dict[str, Any]) -> "PromptTemplate":
        def render_prompt(prompt: str) -> str:
            return prompt.format(**placeholders)

        return cls(
            role=require_field(data, ROLE),
            content=render_prompt(
                prompt=require_field(data, CONTENT),
            ),
        )
