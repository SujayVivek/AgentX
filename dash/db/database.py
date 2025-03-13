from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DATABASE_URL from environment or use default SQLite URL
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', "sqlite:///./sql_app.db")

# Create engine - note the additional arguments needed for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith('sqlite') else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Import models so they can be created
from db.models import TweetInteractionDB, ActivityLogDB, BotMetricsDB, BotStatus

def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()