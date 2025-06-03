from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Set up engine
engine = create_engine('sqlite:///tv_series.db', echo=True)

# Declarative base class
Base = declarative_base()

#Configured session class
Session = sessionmaker(bind=engine)
session = Session()
