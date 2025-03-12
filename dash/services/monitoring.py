from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from db.models import TweetInteractionDB, ActivityLogDB, BotMetricsDB
from models.analytics import TweetInteraction, BotMetrics, ActivityLog

class MonitoringService:
    def __init__(self, db: Session):
        self.db = db

    async def log_interaction(self, interaction: TweetInteraction):
        db_interaction = TweetInteractionDB(
            tweet_id=interaction.tweet_id,
            timestamp=interaction.timestamp,
            response_time=interaction.response_time,
            status=interaction.status,
            error=interaction.error,
            ai_model_used=interaction.ai_model_used,
            confidence_score=interaction.confidence_score
        )
        self.db.add(db_interaction)
        self.db.commit()
        self.db.refresh(db_interaction)
        return db_interaction

    async def get_metrics(self, time_range: Optional[str] = "24h") -> BotMetrics:
        # Get timestamp for the specified time range
        if time_range == "24h":
            since = datetime.utcnow() - timedelta(days=1)
        elif time_range == "7d":
            since = datetime.utcnow() - timedelta(days=7)
        else:
            since = datetime.utcnow() - timedelta(hours=1)

        interactions = self.db.query(TweetInteractionDB)\
            .filter(TweetInteractionDB.timestamp >= since)\
            .all()

        total = len(interactions)
        successful = len([i for i in interactions if i.status == "success"])
        
        metrics = BotMetricsDB(
            total_interactions=total,
            successful_replies=successful,
            failed_replies=total - successful,
            average_response_time=self._calculate_avg_response_time(interactions),
            uptime=self._calculate_uptime(),
            rate_limit_status=self._get_rate_limit_status()
        )
        
        self.db.add(metrics)
        self.db.commit()
        
        return BotMetrics.from_orm(metrics)

    def _calculate_avg_response_time(self, interactions: List[TweetInteractionDB]) -> float:
        if not interactions:
            return 0.0
        return sum(i.response_time for i in interactions) / len(interactions)

    async def get_recent_activities(self, limit: int = 10):
        return self.db.query(ActivityLogDB)\
            .order_by(ActivityLogDB.timestamp.desc())\
            .limit(limit)\
            .all() 