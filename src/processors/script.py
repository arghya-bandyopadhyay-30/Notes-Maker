from dataclasses import dataclass, field
from src.utils.formatting.strings import (
    TRANSLATED_ENGLISH_SCRIPT_LABEL,
    ORIGINAL_SCRIPT_LABEL,
    VALIDATION_SCORE_LABEL,
    MISSING_INFORMATION_LABEL,
    INCORRECT_MEANING_LABEL,
    HALLUCINATED_INFORMATION_LABEL,
    INCORRECT_TERMINOLOGY_LABEL,
    MAJOR_GRAMMATICAL_ERRORS_LABEL,
    ORIGINAL_SCRIPT_FIELD,
    TRANSLATED_SCRIPT_FIELD,
    ACCURACY_SCORE_FIELD,
    MISSING_INFORMATION_FIELD,
    INCORRECT_MEANING_FIELD,
    HALLUCINATED_INFORMATION_FIELD,
    INCORRECT_TERMINOLOGY_FIELD,
    MAJOR_GRAMMATICAL_ERRORS_FIELD,
    VALIDATION_THRESHOLD,
)
from src.utils.validation.validation import require_field


@dataclass
class ProcessedScript:
    original_script: str
    translated_script: str
    validation_score: float
    missing_information: list[str] = field(default_factory=list)
    incorrect_meaning: list[str] = field(default_factory=list)
    hallucinated_information: list[str] = field(default_factory=list)
    incorrect_terminology: list[str] = field(default_factory=list)
    major_grammatical_errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.validation_score > VALIDATION_THRESHOLD

    @classmethod
    def from_dict(cls, data: dict) -> "ProcessedScript":
        return cls(
            original_script=require_field(data, ORIGINAL_SCRIPT_FIELD),
            translated_script=require_field(data, TRANSLATED_SCRIPT_FIELD),
            validation_score=require_field(data, ACCURACY_SCORE_FIELD),
            missing_information=require_field(data, MISSING_INFORMATION_FIELD),
            incorrect_meaning=require_field(data, INCORRECT_MEANING_FIELD),
            hallucinated_information=require_field(data, HALLUCINATED_INFORMATION_FIELD),
            incorrect_terminology=require_field(data, INCORRECT_TERMINOLOGY_FIELD),
            major_grammatical_errors=require_field(data, MAJOR_GRAMMATICAL_ERRORS_FIELD),
        )

    def to_string(self) -> str:
        return "\n".join([
            (TRANSLATED_ENGLISH_SCRIPT_LABEL if self.is_valid else ORIGINAL_SCRIPT_LABEL),
            self.translated_script if self.is_valid else self.original_script,
            f"{VALIDATION_SCORE_LABEL} {self.validation_score:.0%}",
            *(
                f"{label}: {', '.join(values)}"
                for label, values in [
                (MISSING_INFORMATION_LABEL, self.missing_information),
                (INCORRECT_MEANING_LABEL, self.incorrect_meaning),
                (HALLUCINATED_INFORMATION_LABEL, self.hallucinated_information),
                (INCORRECT_TERMINOLOGY_LABEL, self.incorrect_terminology),
                (MAJOR_GRAMMATICAL_ERRORS_LABEL, self.major_grammatical_errors),
            ]
                if values
            ),
        ])
