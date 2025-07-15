import asyncio
import signal
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.config import get_settings
from src.core.message_brokers.rabbitmq import RabbitMQQueue
from src.core.email.email_queue_service import EmailQueueService


class BookRentalNotificationWorker:
    def __init__(self):
        self.settings = get_settings()
        self.notification_queue = RabbitMQQueue("book_rental_notifications")
        self.email_service = EmailQueueService("events_email_queue")
        self._shutdown = False
        self._consuming_task = None

    async def start(self):
        print("Starting book rental notification worker...")
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self._signal_handler)

        try:
            self._consuming_task = asyncio.create_task(self._start_consuming())
            await self._consuming_task
        except asyncio.CancelledError:
            print("Book rental notification worker consumption cancelled")
        except Exception as e:
            print(f"Error in book rental notification worker: {e}")
            raise

    async def _start_consuming(self):
        """Start consuming notification messages"""

        async def process_notification(message):
            try:
                print(f"Processing notification: {message}")

                person_email = message.get("person_email")
                person_name = message.get("person_name")
                book_title = message.get("book_title")
                due_date = message.get("due_date")

                if not person_email:
                    print("No email address provided, skipping notification")
                    return

                await self._send_overdue_email(
                    person_email, person_name, book_title, due_date
                )

            except Exception as e:
                print(f"Error processing notification: {str(e)}")
                raise

        self.notification_queue.setup_consumer(process_notification)
        await self.notification_queue.start_consuming()

    async def _send_overdue_email(
        self, email: str, name: str, book_title: str, due_date: str
    ):
        """Send email for overdue books"""
        await self.email_service.queue_email(
            to_email=email,
            subject=f"Book '{book_title}' is overdue",
            template_name="book_overdue",
            template_data={
                "name": name,
                "book_title": book_title,
                "due_date": due_date,
            },
        )

    def _signal_handler(self):
        print("Received shutdown signal, stopping book rental notification worker...")
        self._shutdown = True
        if self._consuming_task and not self._consuming_task.done():
            self._consuming_task.cancel()

    async def stop(self):
        print("Stopping book rental notification worker...")
        if self._consuming_task and not self._consuming_task.done():
            self._consuming_task.cancel()
            try:
                await self._consuming_task
            except asyncio.CancelledError:
                pass

        if hasattr(self.notification_queue, "close"):
            self.notification_queue.close()


async def main():
    worker = BookRentalNotificationWorker()

    try:
        await worker.start()
    except KeyboardInterrupt:
        print("\nReceived interrupt signal")
    finally:
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
