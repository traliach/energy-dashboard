from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class EnergyData(Base):
    __tablename__ = 'energy_data'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    energy_consumption = Column(Float)
    unit = Column(String)

# Database connection
ENGINE = create_engine("postgresql+asyncpg://dtaylorus:dashpass@localhost/energydb")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base.metadata.create_all(bind=ENGINE)
