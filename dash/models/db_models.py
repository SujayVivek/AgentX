from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from config.database import Base

class TweetInteractionDB(Base):
    __tablename__ = "tweet_interactions"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    response_time = Column(Float)
    status = Column(String)
    error = Column(String, nullable=True)
    ai_model_used = Column(String)
    confidence_score = Column(Float)
    metadata = Column(JSON, nullable=True)

class ActivityLogDB(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    action = Column(String)
    details = Column(JSON)
    status = Column(String)

class BotMetricsDB(Base):
    __tablename__ = "bot_metrics"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    total_interactions = Column(Integer)
    successful_replies = Column(Integer)
    failed_replies = Column(Integer)
    average_response_time = Column(Float)
    uptime = Column(Float)
    rate_limit_status = Column(JSON)
