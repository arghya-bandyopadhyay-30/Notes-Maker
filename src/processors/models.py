from pydantic import BaseModel, Field


class TranslatedSegment(BaseModel):
    text: str = Field(
        ...,
        description=(
            "The complete natural English translation of the corresponding "
            "source transcript segment, preserving its original meaning, "
            "intent, and conversational tone."
        ),
    )


class TranslationValidation(BaseModel):
    accuracy_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Overall accuracy of the English translation compared to the original transcript.",
    )
    missing_information: list[str] = Field(
        default_factory=list,
        description="Information present in the original transcript but missing from the translation.",
    )
    incorrect_meaning: list[str] = Field(
        default_factory=list,
        description="Parts of the translation that incorrectly represent the original meaning.",
    )
    hallucinated_information: list[str] = Field(
        default_factory=list,
        description="Information present in the translation that is not supported by the original transcript.",
    )
    incorrect_terminology: list[str] = Field(
        default_factory=list,
        description="Technical terms that are translated or used incorrectly.",
    )
    major_grammatical_errors: list[str] = Field(
        default_factory=list,
        description="Major grammatical errors that change the meaning of the translation.",
    )