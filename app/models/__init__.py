from sqlalchemy import MetaData
from databases import Database

DATABASE_URL = "postgresql+asyncpg://user:password@db/energydb"

database = Database(DATABASE_URL)
metadata = MetaData()