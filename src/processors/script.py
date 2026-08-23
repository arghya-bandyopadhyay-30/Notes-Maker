from dataclasses import dataclass, field


@dataclass
class ProcessedScript:
    script: str
    validation_score: float
    missing_information: list[str] = field(default_factory=list)
    incorrect_meaning: list[str] = field(default_factory=list)
    hallucinated_information: list[str] = field(default_factory=list)
    incorrect_terminology: list[str] = field(default_factory=list)
    major_grammatical_errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.validation_score > 0.85

    def to_string(self) -> str:
        return "\n".join([
            ("Translated English Script:" if self.is_valid else "Original Script:"),
            self.script,
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
