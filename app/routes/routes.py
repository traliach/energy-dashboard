from app.services.services import EnergyDataService
from fastapi import APIRouter, Depends

router = APIRouter()

# Dependency function to get an instance of EnergyDataService
def get_energy_service():
    return EnergyDataService()

@router.post("/data/")
async def create_energy_data(service: EnergyDataService = Depends(get_energy_service)):
    return await service.fetch_data()

@router.get("/data/")
async def get_energy_data(service: EnergyDataService = Depends(get_energy_service)):
    return await service.fetch_data()