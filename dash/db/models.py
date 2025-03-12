from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON
from .database import Base
from datetime import datetime

class TwitterInteraction(Base):
    __tablename__ = "twitter_interactions"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)
    content = Column(String)
    response = Column(String)
    success = Column(Boolean, default=True)
    response_time = Column(Float)  # in seconds
    created_at = Column(DateTime, default=datetime.utcnow)

class BotStatus(Base):
    __tablename__ = "bot_status"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    last_check = Column(DateTime, default=datetime.utcnow)
    error_message = Column(String, nullable=True)
    config = Column(JSON)  # Stores bot configuration 