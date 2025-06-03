from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Define database path (SQLite file in the root directory)
DATABASE_URL = "sqlite:///tv_series.db"

# Create engine and bind it to the Base
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

# Create all tables
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Export for use in seed and cli
__all__ = ["engine", "Session", "session"]
