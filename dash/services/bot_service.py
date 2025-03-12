from AgentX.src.flare_ai_social.bot_manager import BotManager
from db.models import BotStatus
from sqlalchemy.orm import Session
import asyncio
from datetime import datetime

class DashboardBotManager:
    def __init__(self):
        self.bot_manager = BotManager()
        self._bot_task = None

    async def start_bot(self, db: Session):
        # Initialize AI and start Twitter bot
        self.bot_manager.initialize_ai_provider()
        success = self.bot_manager.start_twitter_bot()
        
        # Update database status
        status = BotStatus(
            is_active=success,
            last_check=datetime.utcnow(),
            error_message=None if success else "Failed to start bot"
        )
        db.add(status)
        db.commit()
        
        if success:
            self._bot_task = asyncio.create_task(self.bot_manager.monitor_bots())
        
        return success

    async def stop_bot(self, db: Session):
        if self._bot_task:
            self._bot_task.cancel()
        await self.bot_manager.shutdown()
        
        # Update database status
        status = BotStatus(
            is_active=False,
            last_check=datetime.utcnow(),
            error_message=None
        )
        db.add(status)
        db.commit()