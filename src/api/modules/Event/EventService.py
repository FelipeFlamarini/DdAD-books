from beanie import PydanticObjectId
from .EventRepository import EventRepository
from .EventDtos import (
    EventCreateDto,
    EventReturnDto,
    SubscriptionCreateDto,
    SubscriptionReturnDto,
)
from src.core.email.email_queue_service import EmailQueueService
from src.core.exceptions import ConflictException

email_queue_service = EmailQueueService(queue_name="events_email_queue")


class EventService:
    @staticmethod
    async def getAllEvents() -> list[EventReturnDto]:
        return await EventRepository.findAll()

    @staticmethod
    async def getUpcomingEvents() -> list[EventReturnDto]:
        return await EventRepository.findUpcoming()

    @staticmethod
    async def createEvent(data: EventCreateDto) -> EventReturnDto:
        return await EventRepository.create(data)

    @staticmethod
    async def registerParticipant(
        subscription_data: SubscriptionCreateDto,
    ) -> SubscriptionReturnDto:
        # Verificar se o evento existe
        event = await EventRepository.findById(subscription_data.event_id)

        # Verificar se o evento não está lotado
        if event.registeredParticipants >= event.maxParticipants:
            raise ConflictException(
                f"Event '{event.title}' is full. Maximum participants: {event.maxParticipants}"
            )

        # Verificar se o participante já está inscrito
        existing_subscription = await EventRepository.findSubscriptionByEventAndEmail(
            subscription_data.event_id, subscription_data.participant_email
        )

        if existing_subscription:
            raise ConflictException(
                f"Participant {subscription_data.participant_email} is already registered for this event"
            )

        # Criar a subscrição
        subscription = await EventRepository.createSubscription(
            subscription_data.event_id, subscription_data.participant_email
        )

        # Incrementar o número de participantes registrados
        updated_event = await EventRepository.incrementParticipants(
            subscription_data.event_id
        )

        # Enviar email de confirmação
        await email_queue_service.queue_email(
            subscription_data.participant_email,
            f"Registration confirmed for {updated_event.title}",
            "event_registration",
            {
                "event_title": updated_event.title,
                "event_date": updated_event.date.strftime("%Y-%m-%d"),
                "event_description": updated_event.description,
                "participant_email": subscription_data.participant_email,
            },
        )

        return SubscriptionReturnDto(**subscription.dict())
