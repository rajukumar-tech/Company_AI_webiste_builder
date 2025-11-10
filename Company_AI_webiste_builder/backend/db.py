# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

# Load .env file (contains DATABASE_URL)
load_dotenv()

# Default local PostgreSQL connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://mastersolis_user:YourStrongPassword@localhost:5432/mastersolis_db"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    """Provide a SQLAlchemy session context."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
