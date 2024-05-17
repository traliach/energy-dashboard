from fastapi import APIRouter, Depends, HTTPException
from .services import EnergyDataService
from sqlalchemy.orm import sessionmaker
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter()

def get_energy_service(session_factory = Depends(get_session_factory)):
    return EnergyDataService(session_factory())

@router.post("/data/")
async def create_energy_data(energy_consumption: float, power_demand: float, service: EnergyDataService = Depends(get_energy_service)):
    return await service.create_energy_data(energy_consumption, power_demand)

@router.get("/stream/", response_class=StreamingResponse)
async def stream_energy_data(service: EnergyDataService = Depends(get_energy_service)):
    last_id = 0
    async def event_stream():
        nonlocal last_id
        while True:
            new_entries = await service.fetch_latest(last_id)
            if new_entries:
                last_entry = new_entries[-1]
                last_id = last_entry.id
                yield f"data: {{\"energy_consumption\": {last_entry.energy_consumption}, \"power_demand\": {last_entry.power_demand}}}\n\n"
            await asyncio.sleep(1)
    return event_stream()
