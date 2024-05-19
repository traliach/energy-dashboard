from sqlalchemy import Column, Integer, Float, String, DateTime, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

DATABASE_URL = "sqlite:///energy.db"

database = Database(DATABASE_URL)
metadata = MetaData()

Base = declarative_base()

class EnergyData(Base):
    __tablename__ = 'energy_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(DateTime, nullable=False)
    respondent = Column(String, nullable=False)
    respondent_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    type_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    value_units = Column(String, nullable=False)
