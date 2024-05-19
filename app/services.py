import os
import httpx
from fastapi import Depends
from app.utils import URLBuilder
from dotenv import load_dotenv

load_dotenv()

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

    async def fetch_data(self,) -> dict:
        params = {
            "frequency": "hourly",
            "data[0]": "value",
            "facets[respondent][]": "MISO",
            "facets[type][]": "D",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "offset": 0,
            "length": 5000,
            "start": "2024-05-16T00",
            "end": "2024-05-17T00",
        }
        
        url = self.build_url(params)
        response = await self.client.get(url)
        return response.json()
