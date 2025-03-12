import os
import sys

# Get the absolute path to the src directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
src_dir = os.path.join(root_dir, 'src')
print(f"Debug: root_dir = {root_dir}")
print(f"Debug: src_dir = {src_dir}")
print(f"Debug: src_dir exists = {os.path.exists(src_dir)}")
print(f"Debug: flare_ai_social dir exists = {os.path.exists(os.path.join(src_dir, 'flare_ai_social'))}")
sys.path.insert(0, src_dir)
print(f"Debug: Updated sys.path = {sys.path}")

try:
    from flare_ai_social.bot_manager import BotManager
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Looking for: {os.path.join(src_dir, 'flare_ai_social', 'bot_manager.py')}")
    print(f"File exists: {os.path.exists(os.path.join(src_dir, 'flare_ai_social', 'bot_manager.py'))}")

from db.models import BotStatus
from sqlalchemy.orm import Session
import asyncio
from datetime import datetime
from typing import List, Dict

class DashboardBotManager:
    def __init__(self):
        self.bot_manager = BotManager()
        self._bot_task = None
        self.pending_mentions = []
        self.generated_replies = {}

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
            self._bot_task = asyncio.create_task(self.monitor_mentions())
        
        return success

    async def monitor_mentions(self):
        while True:
            mentions = await self.bot_manager.get_new_mentions()
            for mention in mentions:
                if mention.id not in self.pending_mentions:
                    self.pending_mentions.append(mention)
            await asyncio.sleep(60)  # Check every minute

    async def get_pending_mentions(self) -> List[Dict]:
        return [
            {
                'id': mention.id,
                'text': mention.text,
                'author': mention.author,
                'created_at': mention.created_at
            }
            for mention in self.pending_mentions
        ]

    async def generate_reply(self, mention_id: str, custom_prompt: str = None) -> str:
        mention = next((m for m in self.pending_mentions if m.id == mention_id), None)
        if not mention:
            raise ValueError("Mention not found")
        
        reply = await self.bot_manager.generate_reply(
            mention.text,
            custom_instructions=custom_prompt
        )
        self.generated_replies[mention_id] = reply
        return reply

    async def post_reply(self, mention_id: str) -> bool:
        if mention_id not in self.generated_replies:
            raise ValueError("No generated reply found for this mention")
        
        success = await self.bot_manager.post_reply(
            mention_id,
            self.generated_replies[mention_id]
        )
        
        if success:
            # Remove from pending mentions and generated replies
            self.pending_mentions = [m for m in self.pending_mentions if m.id != mention_id]
            del self.generated_replies[mention_id]
        
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

    async def generate_post(self, prompt: str) -> str:
        """Generate a post based on the user's prompt"""
        return await self.bot_manager.generate_post(prompt)

    async def create_post(self, content: str) -> bool:
        """Create a new post with the given content"""
        return await self.bot_manager.create_post(content)