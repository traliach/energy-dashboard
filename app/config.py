from databases import Database
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///energy.db")

database = Database(DATABASE_URL)
