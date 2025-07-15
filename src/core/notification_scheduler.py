import asyncio
from datetime import datetime
from src.api.modules.BookRental.BookRentalService import BookRentalService

class NotificationScheduler:
    def __init__(self):
        self.rental_service = BookRentalService()
        self.running = False
        
    async def start(self):
        """Start the notification scheduler"""
        self.running = True
        print("Notification scheduler started")
        
        while self.running:
            try:
                await self.rental_service.check_and_send_notifications()
                print(f"Notification check completed at {datetime.now()}")
                
                await asyncio.sleep(3600)
                
            except Exception as e:
                print(f"Error in notification scheduler: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def stop(self):
        """Stop the notification scheduler"""
        self.running = False
        print("Notification scheduler stopped")