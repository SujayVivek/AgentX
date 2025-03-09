from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from ..config.database import get_db
from ..services.monitoring import MonitoringService

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
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