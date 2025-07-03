from beanie import Document, PydanticObjectId
from pydantic import Field
from datetime import datetime


class SubscriptionModel(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    event_id: PydanticObjectId
    participant_email: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        collection = "subscriptions"