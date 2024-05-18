## Basic Setup:
### Directory Structure

```
.
├── DEMO.md
├── README.md
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── user_routes.py
│   ├── services
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── templates
│   │   └── index.html
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── docker
│   ├── Dockerfile-app
│   ├── Dockerfile-db
│   └── compose.yml
├── eia-api-swagger.yaml
├── setup.sh
└── venv
    ├── bin
    ├── include
    ├── lib
    └── pyvenv.cfg
```

### `app/__init__.py`

```python
from fastapi import FastAPI
from .routes import user_routes
from .models import database, metadata, engine

def create_app() -> FastAPI:
    app = FastAPI()
    
    metadata.create_all(engine)  # Create tables

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    # Include routers
    app.include_router(user_routes.router, prefix="/users", tags=["users"])
    
    return app

app = create_app()
```

### `app/models/__init__.py`

```python
from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "postgresql://user:password@localhost/dbname"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
```

### `app/models/user.py`

```python
from sqlalchemy import Table, Column, Integer, String
from . import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String, unique=True)
)
```

### `app/routes/__init__.py`

```python
# This file can be left empty or used to include common utilities for routes
```

### `app/routes/user_routes.py`

```python
from fastapi import APIRouter, HTTPException
from ..models import users, database
from ..services.user_service import fetch_user_data

router = APIRouter()

@router.get("/")
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

@router.post("/")
async def create_user(name: str, email: str):
    query = users.insert().values(name=name, email=email)
    await database.execute(query)
    return {"message": "User created"}

@router.get("/fetch")
async def fetch_and_store_user():
    user_data = await fetch_user_data()
    if user_data:
        query = users.insert().values(name=user_data["name"], email=user_data["email"])
        await database.execute(query)
        return {"message": "User data fetched and stored"}
    raise HTTPException(status_code=404, detail="User data not found")
```

### `app/services/__init__.py`

```python
# This file can be left empty or used to include common utilities for services
```

### `app/services/user_service.py`

```python
import httpx

async def fetch_user_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/user")
        if response.status_code == 200:
            return response.json()
        return None
```

### `app/utils/__init__.py`

```python
# This file can be left empty or used to include common utilities for utils
```

### `app/utils/helpers.py`

```python
# This file can contain utility functions if needed
```

### `app/templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI Application</title>
</head>
<body>
    <h1>Welcome to FastAPI Application</h1>
</body>
</html>
```

### `app/main.py`

```python
import uvicorn
from . import app

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

### `setup.sh`

```bash
#!/bin/bash

# Install dependencies
pip install fastapi uvicorn sqlalchemy asyncpg htmx jinja2 databases httpx

# Set up database (example for PostgreSQL)
# You can modify this script to create the database if it doesn't exist

echo "Setup complete"
```

### `docker/Dockerfile-app`

```Dockerfile
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY setup.sh .

# Install dependencies
RUN chmod +x setup.sh && ./setup.sh

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### `docker/Dockerfile-db`

```Dockerfile
FROM postgres:13

# Add custom setup if needed
```

### `docker/compose.yml`

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: docker/Dockerfile-app
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
    ports:
      - "5432:5432"
```

### Running the Application

1. **Set up the environment**:
    ```bash
    source venv/bin/activate
    ./setup.sh
    ```

2. **Run the application**:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

3. **Using Docker**:
    ```bash
    docker-compose up --build
    ```

With this setup, you have a scaffolded FastAPI application that can fetch data from an endpoint and persist it to a PostgreSQL database.



# Demo: Energy Monitoring Dashboard

- **Use Case:** Create a dynamic energy monitoring dashboard that displays real-time energy consumption data on a web page. The dashboard should update automatically, providing users with up-to-date information about energy usage without needing to manually refresh the page.

#### Environment Setup
First, ensure you have Python installed. Create a new project directory and set up a virtual environment:

```bash
mkdir energy_dashboard
cd energy_dashboard
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy asyncpg htmx jinja2
```

#### Define the Database Model with SQLAlchemy
Create a file called `models.py` to define your database schema:

```python
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
ENGINE = create_engine("postgresql+asyncpg://user:password@localhost/energydb")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base.metadata.create_all(bind=ENGINE)
```

Replace `"postgresql+asyncpg://user:password@localhost/energydb"` with your actual database credentials.

#### Create FastAPI App
Set up the FastAPI application in a file called `main.py`:

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, EnergyData
import datetime

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/data/")
async def create_energy_data(energy_consumption: float, unit: str, db: Session = Depends(get_db)):
    db_data = EnergyData(energy_consumption=energy_consumption, unit=unit)
    db.add(db_data)
    db.commit()
    return db_data

@app.get("/data/", response_model=list[EnergyData])
async def read_energy_data(db: Session = Depends(get_db)):
    return db.query(EnergyData).all()
```

#### Implement Server-Sent Events (SSE)
Add an endpoint in `main.py` for SSE:

```python
from fastapi.responses import StreamingResponse

@app.get("/stream/")
async def stream_energy_data(db: Session = Depends(get_db)):
    def event_stream():
        while True:
            # Here we would ideally add logic to fetch only new data entries
            data = db.query(EnergyData).order_by(EnergyData.timestamp.desc()).first()
            yield f"data: {data.energy_consumption} {data.unit}\n\n"
            time.sleep(1)  # Adjust the timing based on your data update frequency
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

#### Create HTMX and Jinja2 Frontend
Set up the HTML template using Jinja2 in a file `templates/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Energy Dashboard</title>
    <script src="https://unpkg.com/htmx.org"></script>
</head>
<body>
    <h1>Energy Consumption</h1>
    <div id="energy-data" hx-get="/stream/" hx-swap="outerHTML" hx-trigger="sse:open">
        Waiting for data...
    </div>
</body>
</html>
```

#### Serve the HTML Template
Modify `main.py` to serve the template:

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

#### Running the Server
Use Uvicorn to run your FastAPI application:

```bash
uvicorn main:app --reload
```

This command starts your FastAPI app with live reloading enabled.

### Final Notes
- **Ensure your database and user credentials are set correctly** in `models.py`.
- **The SSE connection is kept simple**; for a production scenario, consider handling reconnections and more complex streaming logic.
- **HTMX will update the div** whenever a new SSE message is received,

 making the dashboard dynamic and real-time.
