from dataclasses import dataclass

from src.utils.formatting.strings import (
    TRANSLATOR,
    VALIDATOR,
)
from src.utils.validation.validators import require_field


@dataclass
class ModelsConfig:
    translator: str
    validator: str

    def to_dict(self) -> dict:
        return {
            TRANSLATOR: self.translator,
            VALIDATOR: self.validator,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModelsConfig":
        return cls(
            translator=require_field(data, TRANSLATOR),
            validator=require_field(data, VALIDATOR),
        )
