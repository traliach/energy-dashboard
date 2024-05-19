from sqlalchemy import Column, Integer, String, Float, DateTime, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

DATABASE_URL = "sqlite:///energy.db"

database = Database(DATABASE_URL)
metadata = MetaData()

Base = declarative_base(metadata=metadata)

class EnergyData(Base):
    __tablename__ = 'energy_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(DateTime, nullable=False)
    respondent = Column(String, nullable=True)
    respondent_name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    type_name = Column(String, nullable=True)
    value = Column(Float, nullable=True)
    value_units = Column(String, nullable=True)

engine = create_engine(DATABASE_URL)
# Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine)
