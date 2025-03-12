from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TweetInteraction(BaseModel):
    tweet_id: str
    timestamp: datetime
    response_time: float
    status: str
    error: Optional[str] = None
    ai_model_used: str
    confidence_score: float

class ActivityLog(BaseModel):
    timestamp: datetime
    activity_type: str
    description: str

class BotMetrics(BaseModel):
    total_interactions: int
    successful_replies: int
    failed_replies: int
    average_response_time: float
    uptime: float
    rate_limit_status: str

    class Config:
        from_attributes = True