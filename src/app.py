from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from src.core.db import init_db
from src.api.modules.Event.EventRouter import event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()

    yield

    print("Shutting down gracefully...")
    if hasattr(app.state, "email_task"):
        app.state.email_task.cancel()
        try:
            await app.state.email_task
        except asyncio.CancelledError:
            print("Email worker stopped.")


app = FastAPI(lifespan=lifespan)
app.include_router(event_router)
