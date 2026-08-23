from dataclasses import dataclass, field
from typing import Any

from src.utils.formatting.strings import (
    DESCRIPTION,
    NAME,
    PARAMETERS,
)
from src.utils.validation.validators import require_field, validate_parameters


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
        validate_parameters(parameters=parameters, placeholders=placeholders)

        return cls(
            name=require_field(data, NAME),
            description=require_field(data, DESCRIPTION),
            parameters=parameters,
        )
