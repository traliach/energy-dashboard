from datetime import datetime
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from .services import EnergyDataService
from .models import database
import asyncio
import json
import httpx

router = APIRouter()

# Dependency function to get an instance of EnergyDataService
def get_energy_service():
    return EnergyDataService(httpx.AsyncClient())

# Endpoint to seed energy data
@router.post("/seed-data/")
async def seed_energy_data(service: EnergyDataService = Depends(get_energy_service)):
    return await service.fetch_data(
        params={
            "frequency": "hourly",
            "data[0]": "value",
            "facets[type][]": "D",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "offset": 0,
            "length": 5000,
            "start": "2019-01-29T00",
            "end": "2019-02-04T23",
        }
    )

# Event generator function to generate streaming data
async def event_generator():
    last_id = 0
    while True:
        query = f"SELECT * FROM energy_data WHERE id > {last_id} ORDER BY id ASC LIMIT 1"
        row = await database.fetch_one(query)
        if row:
            last_id = row.id
            # Check if period is a datetime object
            if isinstance(row.period, datetime):
                period = row.period.isoformat()
            else:
                # Convert period to a datetime object and call isoformat on it
                period = datetime.strptime(row.period, "%Y-%m-%d %H:%M:%S.%f").isoformat()
            data = {
                "period": period,
                "respondent": row.respondent,
                "respondent_name": row.respondent_name,
                "type": row.type,
                "value": row.value
            }
            yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(1)

# Endpoint to stream data
@router.get('/stream')
async def stream():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
