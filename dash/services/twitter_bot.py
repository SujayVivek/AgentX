import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

class TwitterBot:
    def __init__(self):
        self.api = None
        self.initialize_api()

    def initialize_api(self):
        """Authenticate and initialize the Twitter API client."""
        try:
            auth = tweepy.OAuth1UserHandler(
                os.getenv("TWITTER_API_KEY"),
                os.getenv("TWITTER_API_SECRET"),
                os.getenv("TWITTER_ACCESS_TOKEN"),
                os.getenv("TWITTER_ACCESS_SECRET")
            )
            self.api = tweepy.API(auth)
        except Exception as e:
            print(f"Error initializing Twitter API: {e}")
            raise

    def post_tweet(self, content: str) -> bool:
        """Post a tweet with the given content."""
        try:
            self.api.update_status(status=content)
            return True
        except tweepy.TweepError as e:
            print(f"Error posting tweet: {e}")
            return False

    def get_mentions(self):
        """Get the latest mentions."""
        try:
            mentions = self.api.mentions_timeline()
            return [
                {
                    'id': mention.id_str,
                    'text': mention.text,
                    'author': mention.user.screen_name,
                    'created_at': mention.created_at.isoformat()
                }
                for mention in mentions
            ]
        except Exception as e:
            print(f"Error fetching mentions: {e}")
            return []

    def reply_to_tweet(self, mention_id: str, reply: str) -> bool:
        """Reply to a tweet with the given ID."""
        try:
            self.api.update_status(status=reply, in_reply_to_status_id=mention_id)
            return True
        except Exception as e:
            print(f"Error posting reply: {e}")
            return False 