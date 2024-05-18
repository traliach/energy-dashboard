from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine

class EnergyData():
    __tablename__ = 'energy_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(DateTime, nullable=False)
    respondent = Column(String, nullable=False)
    respondent_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    type_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    value_units = Column(String, nullable=False)
