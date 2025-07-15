from fastapi import APIRouter, Depends, Query
from typing import List
from src.api.modules.Person.PersonService import PersonService
from src.api.modules.Person.PersonDtos import PersonCreateDto, PersonResponseDto

router = APIRouter(prefix="/persons", tags=["persons"])


def get_person_service() -> PersonService:
    return PersonService()


@router.post("/", response_model=PersonResponseDto)
async def create_person(
    person_data: PersonCreateDto, service: PersonService = Depends(get_person_service)
):
    """Create a new person"""
    return await service.create_person(person_data)


@router.get("/{person_id}", response_model=PersonResponseDto)
async def get_person(
    person_id: str, service: PersonService = Depends(get_person_service)
):
    """Get a person by ID"""
    return await service.get_person_by_id(person_id)


@router.get("/", response_model=List[PersonResponseDto])
async def get_people(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: PersonService = Depends(get_person_service),
):
    """Get all people with pagination"""
    return await service.get_all_people(skip, limit)
