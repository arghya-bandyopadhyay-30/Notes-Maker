from dataclasses import dataclass, field
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
        return self.validation_score > 0.85

    @classmethod
    def from_dict(cls, data: dict) -> "ProcessedScript":
        return cls(
            original_script=require_field(data, "original_script"),
            translated_script=require_field(data, "translated_script"),
            validation_score=require_field(data, "validation_score"),
            missing_information=require_field(data, "missing_information"),
            incorrect_meaning=require_field(data, "incorrect_meaning"),
            hallucinated_information=require_field(data, "hallucinated_information"),
            incorrect_terminology=require_field(data, "incorrect_terminology"),
            major_grammatical_errors=require_field(data, "major_grammatical_errors"),
        )

    def to_string(self) -> str:
        return "\n".join([
            ("Translated English Script:" if self.is_valid else "Original Script:"),
            self.translated_script if self.is_valid else self.original_script,
            f"Validation Score: {self.validation_score:.0%}",
            *(
                f"{label}: {', '.join(values)}"
                for label, values in [
                ("Missing Information", self.missing_information),
                ("Incorrect Meaning", self.incorrect_meaning),
                ("Hallucinated Information", self.hallucinated_information),
                ("Incorrect Terminology", self.incorrect_terminology),
                ("Major Grammatical Errors", self.major_grammatical_errors),
            ]
                if values
            ),
        ])
