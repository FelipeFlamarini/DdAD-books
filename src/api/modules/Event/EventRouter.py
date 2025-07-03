from fastapi import APIRouter, HTTPException, Path
from beanie import PydanticObjectId

from .EventService import EventService
from .EventDtos import (
    EventCreateDto,
    EventReturnDto,
    SubscriptionCreateDto,
    SubscriptionReturnDto,
    ParticipantRegistrationRequest,
)
from src.core.exceptions import NotFoundException, ConflictException

event_router = APIRouter(prefix="/events", tags=["events"])


@event_router.get("/", response_model=list[EventReturnDto])
async def getAllEvents():
    """Retorna uma lista de todos os eventos cadastrados"""
    return await EventService.getAllEvents()


@event_router.get("/upcoming", response_model=list[EventReturnDto])
async def getUpcomingEvents():
    """Retorna uma lista apenas dos eventos futuros (que irão ocorrer ainda)"""
    return await EventService.getUpcomingEvents()


@event_router.post("/", response_model=EventReturnDto)
async def createEvent(event: EventCreateDto):
    """Cria um evento a partir dos dados informados"""
    return await EventService.createEvent(event)


@event_router.post("/{event_id}/register", response_model=SubscriptionReturnDto)
async def registerParticipant(
    request: ParticipantRegistrationRequest,
    event_id: PydanticObjectId = Path(..., description="ID do evento para inscrição"),
):
    """Registra a subscrição do participante em um evento"""
    try:
        subscription = SubscriptionCreateDto(
            event_id=event_id, participant_email=request.participant_email
        )

        return await EventService.registerParticipant(subscription)
    except ConflictException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
