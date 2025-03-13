from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from db.database import get_db, init_db
from services.monitoring import MonitoringService
from services.bot_service import DashboardBotManager
from db.models import TweetInteractionDB, ActivityLogDB, BotMetricsDB, BotStatus
from datetime import datetime, timedelta
from generate_post import generate_tweet  # Import the generate_tweet function

app = FastAPI()
bot_manager = DashboardBotManager()

# Initialize database tables
init_db()

# Update CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.get_metrics()

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

@app.get("/api/mentions")
async def get_mentions():
    return await bot_manager.get_pending_mentions()

@app.post("/api/generate-reply")
async def generate_reply(request: dict):
    return {
        "reply": await bot_manager.generate_reply(
            request["mention_id"],
            request.get("custom_prompt")
        )
    }

@app.post("/api/post-reply")
async def post_reply(request: dict):
    return {
        "success": await bot_manager.post_reply(request["mention_id"])
    }

@app.post("/api/generate-post")
async def generate_post(request: dict):
    try:
        generated_post = await bot_manager.generate_post(request["prompt"])
        return {"post": generated_post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/post")
async def create_post(request: dict):
    try:
        success = await bot_manager.create_post(request["content"])
        if success:
            return {"status": "success"}
        raise HTTPException(status_code=500, detail="Failed to create post")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-tweet")
async def generate_tweet_endpoint(request: dict):
    try:
        prompt = request.get("prompt")
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        generated_post = await bot_manager.generate_post(prompt)
        return {"post": generated_post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 