import httpx
from fastapi import APIRouter, Depends
from app.services import EnergyDataService

router = APIRouter()

# Dependency function to get an instance of EnergyDataService
def get_energy_service():
    return EnergyDataService(httpx.AsyncClient())

@router.get("/data/")
async def get_energy_data(service: EnergyDataService = Depends(get_energy_service)):
    return await service.fetch_data()
