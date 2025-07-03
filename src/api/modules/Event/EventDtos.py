from pydantic import BaseModel, Field, PositiveInt, EmailStr
from beanie import PydanticObjectId
from datetime import date


class EventReturnDto(BaseModel):
    id: PydanticObjectId
    maxParticipants: PositiveInt = Field(ge=1)
    registeredParticipants: int = Field(ge=0, default=0)
    date: date
    title: str
    description: str


class EventCreateDto(BaseModel):
    maxParticipants: PositiveInt = Field(ge=1)
    date: date
    title: str
    description: str


class SubscriptionCreateDto(BaseModel):
    event_id: PydanticObjectId
    participant_email: EmailStr


class SubscriptionReturnDto(BaseModel):
    id: PydanticObjectId
    event_id: PydanticObjectId
    participant_email: EmailStr


class ParticipantRegistrationRequest(BaseModel):
    participant_email: str
