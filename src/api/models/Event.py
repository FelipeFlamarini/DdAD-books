from beanie import Document, PydanticObjectId
from pydantic import Field
from datetime import date


class EventModel(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    maxParticipants: int = Field(min=1)
    registeredParticipants: int = Field(default=0, ge=0)
    date: date
    title: str
    description: str

    class Settings:
        collection = "events"
