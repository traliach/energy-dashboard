from sqlalchemy import Column, Integer, String, Float, DateTime, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

# Define the URL for the SQLite database
DATABASE_URL = "sqlite:///energy.db"

# Create a Database instance using the DATABASE_URL
database = Database(DATABASE_URL)

# Create a MetaData instance
metadata = MetaData()

# Create a declarative base class
Base = declarative_base(metadata=metadata)

# Define the EnergyData table
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

# Create an engine instance using the DATABASE_URL
engine = create_engine(DATABASE_URL)

# Create the tables defined in the metadata
Base.metadata.create_all(engine)
