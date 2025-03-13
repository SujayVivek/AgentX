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

# Import the AI provider
from flare_ai_social.ai import GeminiProvider
from services.twitter_bot import TwitterBot  # Import the new TwitterBot
from generate_post import generate_tweet  # Import the generate_tweet function

class DashboardBotManager:
    def __init__(self):
        self.twitter_bot = TwitterBot()
        self._bot_task = None
        self.pending_mentions = []
        self.generated_replies = {}

    async def start_bot(self, db: Session):
        # Initialize Twitter bot
        self.twitter_bot.initialize_api()
        success = True  # Assume success for now
        
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
            mentions = self.twitter_bot.get_mentions()
            for mention in mentions:
                if mention['id'] not in self.pending_mentions:
                    self.pending_mentions.append(mention)
            await asyncio.sleep(60)  # Check every minute

    async def get_pending_mentions(self) -> List[Dict]:
        return self.pending_mentions

    async def generate_reply(self, mention_id: str, custom_prompt: str = None) -> str:
        mention = next((m for m in self.pending_mentions if m['id'] == mention_id), None)
        if not mention:
            raise ValueError("Mention not found")
        
        # Placeholder for AI generation logic
        reply = f"Generated reply to: {mention['text']}"
        self.generated_replies[mention_id] = reply
        return reply

    async def post_reply(self, mention_id: str) -> bool:
        if mention_id not in self.generated_replies:
            raise ValueError("No generated reply found for this mention")
        
        success = self.twitter_bot.reply_to_tweet(
            mention_id,
            self.generated_replies[mention_id]
        )
        
        if success:
            # Remove from pending mentions and generated replies
            self.pending_mentions = [m for m in self.pending_mentions if m['id'] != mention_id]
            del self.generated_replies[mention_id]
        
        return success

    async def generate_post(self, prompt: str) -> str:
        """Generate a post based on the user's prompt"""
        try:
            # Use the generate_tweet function from generate_post.py
            response = generate_tweet(
                f"Generate a tweet about: {prompt}\n"
                "Make it engaging and concise, suitable for Twitter/X platform."
            )
            return response
        except Exception as e:
            print(f"Error generating post: {e}")
            raise

    async def create_post(self, content: str) -> bool:
        """Create a new post with the given content"""
        return self.twitter_bot.post_tweet(content)