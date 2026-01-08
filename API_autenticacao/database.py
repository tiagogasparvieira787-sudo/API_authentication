from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///authentic.db")

Base = declarative_base()
