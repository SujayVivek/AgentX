from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from ..config.database import get_db
from ..services.monitoring import MonitoringService
from db.database import get_db as db_get_db
from db.models import TwitterInteraction, BotStatus
from datetime import datetime, timedelta
from services.bot_service import DashboardBotManager

app = FastAPI()
bot_manager = DashboardBotManager()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stats")
async def get_stats(db: Session = Depends(db_get_db)):
    total = db.query(TwitterInteraction).count()
    successful = db.query(TwitterInteraction).filter(TwitterInteraction.success == True).count()
    
    # Calculate average response time for last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_interactions = db.query(TwitterInteraction)\
        .filter(TwitterInteraction.created_at >= yesterday)\
        .all()
    
    avg_response_time = sum(i.response_time for i in recent_interactions) / len(recent_interactions) if recent_interactions else 0
    
    return {
        "total_interactions": total,
        "successful_replies": successful,
        "average_response_time": f"{avg_response_time:.2f}s"
    }

@app.get("/api/recent-activities")
async def get_recent_activities(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.get_recent_activities(limit)

@app.get("/api/bot-status")
async def get_bot_status(db: Session = Depends(get_db)):
    monitoring_service = MonitoringService(db)
    metrics = await monitoring_service.get_metrics("1h")
    return {
        "is_active": metrics.total_interactions > 0,
        "rate_limit_status": metrics.rate_limit_status,
        "recent_metrics": metrics
    }

@app.post("/api/bot/start")
async def start_bot(db: Session = Depends(get_db)):
    success = await bot_manager.start_bot(db)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to start bot")
    return {"status": "Bot started successfully"}

@app.post("/api/bot/stop")
async def stop_bot(db: Session = Depends(get_db)):
    await bot_manager.stop_bot(db)
    return {"status": "Bot stopped successfully"}

@app.get("/api/bot/status")
async def get_bot_status(db: Session = Depends(get_db)):
    status = db.query(BotStatus).order_by(BotStatus.last_check.desc()).first()
    return {
        "is_active": status.is_active if status else False,
        "last_check": status.last_check if status else None,
        "error_message": status.error_message if status else None
    } 