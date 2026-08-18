from pydantic import BaseModel, Field


class TranslationValidation(BaseModel):
    score: float = Field(
        ge=0.0,
        le=1.0,
        description="Translation accuracy score between 0 and 1",
    )
    issues: list[str] = Field(
        default_factory=list,
        description="Issues found in the translation."
    )
