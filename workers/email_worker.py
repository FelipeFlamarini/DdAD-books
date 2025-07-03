import asyncio
import signal
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.config import get_settings
from src.core.email.email_queue_service import EmailQueueService



class EmailWorker:
    def __init__(self):
        self.settings = get_settings()
        self.email_service = EmailQueueService(
            queue_name="events_email_queue")
        self._shutdown = False
        self._consuming_task = None

    async def start(self):
        print("Starting email worker...")
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self._signal_handler)

        try:
            self._consuming_task = asyncio.create_task(
                self.email_service.start_consuming()
            )
            await self._consuming_task
        except asyncio.CancelledError:
            print("Email worker consumption cancelled")
        except Exception as e:
            print(f"Error in email worker: {e}")
            raise

    def _signal_handler(self):
        print("Received shutdown signal, stopping email worker...")
        self._shutdown = True
        if self._consuming_task and not self._consuming_task.done():
            self._consuming_task.cancel()

    async def stop(self):
        print("Stopping email worker...")
        if self._consuming_task and not self._consuming_task.done():
            self._consuming_task.cancel()
            try:
                await self._consuming_task
            except asyncio.CancelledError:
                pass

        if hasattr(self.email_service, "queue") and hasattr(
            self.email_service.queue, "close"
        ):
            self.email_service.queue.close()


async def main():
    worker = EmailWorker()

    try:
        await worker.start()
    except KeyboardInterrupt:
        print("\nReceived interrupt signal")
    finally:
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
