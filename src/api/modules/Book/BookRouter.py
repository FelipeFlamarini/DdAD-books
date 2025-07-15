from fastapi import APIRouter, Depends, Query
from typing import List
from src.api.modules.Book.BookService import BookService
from src.api.modules.Book.BookDtos import BookCreateDto, BookResponseDto

router = APIRouter(prefix="/books", tags=["books"])

def get_book_service() -> BookService:
    return BookService()

@router.post("/", response_model=BookResponseDto)
async def create_book(
    book_data: BookCreateDto,
    service: BookService = Depends(get_book_service)
):
    """Create a new book"""
    return await service.create_book(book_data)

@router.get("/{book_id}", response_model=BookResponseDto)
async def get_book(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    """Get a book by ID"""
    return await service.get_book_by_id(book_id)

@router.get("/", response_model=List[BookResponseDto])
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: BookService = Depends(get_book_service)
):
    """Get all books with pagination"""
    return await service.get_all_books(skip, limit)

@router.get("/available/list", response_model=List[BookResponseDto])
async def get_available_books(
    service: BookService = Depends(get_book_service)
):
    """Get books that have available copies"""
    return await service.get_available_books()

@router.get("/{book_id}/availability")
async def check_book_availability(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    """Check if a book is available for rental"""
    available = await service.check_availability(book_id)
    return {"book_id": book_id, "available": available}