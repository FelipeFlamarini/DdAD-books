from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from src.core.db import init_db
from src.core.notification_scheduler import NotificationScheduler
from src.api.modules.Book.BookRouter import router as book_router
from src.api.modules.Person.PersonRouter import router as person_router
from src.api.modules.BookRental.BookRentalRouter import router as rental_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    
    scheduler = NotificationScheduler()
    scheduler_task = asyncio.create_task(scheduler.start())
    app.state.scheduler = scheduler
    app.state.scheduler_task = scheduler_task

    yield

    print("Shutting down gracefully...")
    
    if hasattr(app.state, "scheduler"):
        await app.state.scheduler.stop()
    
    if hasattr(app.state, "scheduler_task"):
        app.state.scheduler_task.cancel()
        try:
            await app.state.scheduler_task
        except asyncio.CancelledError:
            print("Notification scheduler stopped.")
    
    if hasattr(app.state, "email_task"):
        app.state.email_task.cancel()
        try:
            await app.state.email_task
        except asyncio.CancelledError:
            print("Email worker stopped.")


app = FastAPI(
    title="Book Rental API",
    description="A FastAPI backend for book rental management with notifications",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(book_router)
app.include_router(person_router)
app.include_router(rental_router)

@app.get("/")
async def root():
    return {"message": "Book Rental API is running"}
