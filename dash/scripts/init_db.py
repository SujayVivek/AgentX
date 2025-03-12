import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import engine
from db.models import Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!")