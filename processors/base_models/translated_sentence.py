from pydantic import BaseModel, Field


class TranslatedSentence(BaseModel):
    text: str = Field(
        ...,
        description="The natural English translation of the source sentence."
    )