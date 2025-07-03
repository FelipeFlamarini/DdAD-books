from datetime import date
from beanie import PydanticObjectId

from src.api.models.Event import EventModel
from src.api.models.Subscription import SubscriptionModel
from .EventDtos import EventCreateDto
from src.core.exceptions import NotFoundException


class EventRepository:
    @staticmethod
    async def findAll() -> list[EventModel]:
        return await EventModel.find_all().to_list()

    @staticmethod
    async def findUpcoming() -> list[EventModel]:
        today = date.today()
        return await EventModel.find(EventModel.date >= today).to_list()

    @staticmethod
    async def findById(event_id: PydanticObjectId) -> EventModel:
        event = await EventModel.get(event_id)
        if not event:
            raise NotFoundException(f"Event with id {event_id} not found")
        return event

    @staticmethod
    async def create(data: EventCreateDto) -> EventModel:
        event = EventModel(
            maxParticipants=data.maxParticipants,
            registeredParticipants=0,
            date=data.date,
            title=data.title,
            description=data.description,
        )
        return await event.insert()

    @staticmethod
    async def incrementParticipants(event_id: PydanticObjectId) -> EventModel:
        event = await EventRepository.findById(event_id)
        event.registeredParticipants += 1
        await event.save()
        return event

    @staticmethod
    async def findSubscriptionsByEvent(
        event_id: PydanticObjectId,
    ) -> list[SubscriptionModel]:
        return await SubscriptionModel.find(
            SubscriptionModel.event_id == event_id
        ).to_list()

    @staticmethod
    async def findSubscriptionByEventAndEmail(
        event_id: PydanticObjectId, email: str
    ) -> SubscriptionModel:
        return await SubscriptionModel.find_one(
            SubscriptionModel.event_id == event_id,
            SubscriptionModel.participant_email == email,
        )

    @staticmethod
    async def createSubscription(
        event_id: PydanticObjectId, email: str
    ) -> SubscriptionModel:
        subscription = SubscriptionModel(event_id=event_id, participant_email=email)
        return await subscription.insert()
