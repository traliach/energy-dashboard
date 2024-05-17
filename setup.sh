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

# Install required Python packages
pip install fastapi uvicorn sqlalchemy asyncpg htmx jinja2

# Running the server
echo "Starting the server..."
uvicorn main:app --reload