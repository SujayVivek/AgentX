from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TweetInteractionDB(Base):
    __tablename__ = "tweet_interactions"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String)
    timestamp = Column(DateTime)
    response_time = Column(Float)
    status = Column(String)
    error = Column(String, nullable=True)
    ai_model_used = Column(String)
    confidence_score = Column(Float)

class ActivityLogDB(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    activity_type = Column(String)
    description = Column(String)

class BotMetricsDB(Base):
    __tablename__ = "bot_metrics"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    total_interactions = Column(Integer)
    successful_replies = Column(Integer)
    failed_replies = Column(Integer)
    average_response_time = Column(Float)
    uptime = Column(Float)
    rate_limit_status = Column(String)

class BotStatus(Base):
    __tablename__ = "bot_status"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=False)
    last_check = Column(DateTime)
    error_message = Column(String, nullable=True) 