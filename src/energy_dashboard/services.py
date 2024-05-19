from datetime import datetime
import os
import httpx
import logging
from .utils import URLBuilder
from dotenv import load_dotenv
from sqlalchemy import insert
from .models import EnergyData, database

load_dotenv()    

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnergyDataService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.api_key = os.getenv("API_KEY")

    def build_url(self, params: dict) -> str:
        url_builder = URLBuilder()
        
        for key, value in params.items():
            url_builder.add_param(key, value)
            
        url_builder.add_api_key(self.api_key)
        return url_builder.build()

    # A significant demand spike in the MISO footprint occurred during the week of January 29, 2019. 
    # This period experienced extremely cold temperatures due to the polar vortex, which led to a surge in heating demand across the Midwest. 
    # MISO reported a peak demand of around 104.8 GW on January 30, 2019, marking one of the highest winter demand levels in recent history. 
    # This spike stressed the grid, highlighting the importance of reliable energy supply during extreme weather events​ 
    async def fetch_data(self) -> dict:
        params = {
            "frequency": "hourly",
            "data[0]": "value",
            # "facets[respondent][]": "MISO",
            "facets[type][]": "D",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "offset": 0,
            "length": 5000,
            "start": "2019-01-29T00",
            "end": "2019-02-04T23",
        }
        url = self.build_url(params)
        response = await self.client.get(url)
        data = response.json()
        logger.info(f"Logged item: {data}")

        while data['response']['data']:
            for item in data['response']['data']:
                value = float(item['value']) if item['value'] is not None else 0.0
                period = datetime.strptime(item['period'], "%Y-%m-%dT%H")  # adjusted format string

                query = insert(EnergyData).values(
                    value=value,
                    period=period,
                    respondent=item['respondent'],
                    respondent_name=item['respondent-name'],
                    type=item['type'],
                    type_name=item['type-name'],
                    value_units=item['value-units']
                )
                await database.execute(query)       
                # Log the item

            params['offset'] += params['length']
            url = self.build_url(params)
            response = await self.client.get(url)
            data = response.json()
            logger.info(f"Logged item: {data}")
        
        return data
