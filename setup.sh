#!/bin/bash

# Define the directory and database connection details
PROJECT_DIR="energy_dashboard"
DB_HOST="localhost"
DB_NAME="energydb"

# Create project directory and initialize Python environment
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize Alembic
alembic init alembic

# Replace the sqlalchemy.url in alembic.ini
sed -i 's|sqlalchemy.url = .*|sqlalchemy.url = postgresql://user:password@db/energydb|' alembic/alembic.ini

# Generate a migration script
alembic revision --autogenerate -m "Initial migration"

# Apply the migration
alembic upgrade head

# Running the server
echo "Starting the server..."
uvicorn main:app --reload