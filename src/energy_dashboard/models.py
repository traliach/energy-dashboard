from databases import Database
from sqlalchemy import Column, Integer, String, Float, DateTime, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import UniqueConstraint

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
    __tablename__ = "energy_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(DateTime, nullable=False)
    respondent = Column(String, nullable=True)
    respondent_name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    type_name = Column(String, nullable=True)
    value = Column(Float, nullable=True)
    value_units = Column(String, nullable=True)

    __table_args__ = (
        # UniqueConstraint(
        #     "period", "respondent", "type", name="uix_period_respondent_type"
        # ),
    )

    def __repr__(self):
        return f"<EnergyData(id={self.id}, period={self.period}, respondent={self.respondent}, respondent_name={self.respondent_name}, type={self.type}, type_name={self.type_name}, value={self.value}, value_units={self.value_units})>"


# Create an engine instance using the DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables defined in the metadata
Base.metadata.create_all(engine)
