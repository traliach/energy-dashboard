from .models import get_session_factory, EnergyData
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

class EnergyDataService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def create_energy_data(self, energy_consumption, power_demand):
        async with self.session_factory() as session:
            new_data = EnergyData(energy_consumption=energy_consumption, power_demand=power_demand)
            session.add(new_data)
            await session.commit()
            return new_data

    async def fetch_latest(self, last_id):
        async with self.session_factory() as session:
            result = await session.execute(
                select(EnergyData)
                .where(EnergyData.id > last_id)
                .order_by(EnergyData.timestamp)
            )
            return result.scalars().all()
