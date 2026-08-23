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
