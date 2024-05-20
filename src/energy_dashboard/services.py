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
        # Create an instance of URLBuilder
        url_builder = URLBuilder()

        # Add parameters to the URLBuilder
        for key, value in params.items():
            url_builder.add_param(key, value)

        # Add API key to the URLBuilder
        url_builder.add_api_key(self.api_key)
        return url_builder.build()

    async def fetch_data(self, params) -> dict:
        while True:
            # Build the URL using the parameters
            url = self.build_url(params)

            # Send a GET request to the API
            response = await self.client.get(url)

            # Parse the response as JSON
            data = response.json()

            # Break the loop if there is no data in the response
            if not data['response']['data']:
                break

            # Process each item in the data
            for item in data['response']['data']:
                # Convert the value to float, or 0.0 if it is None
                value = float(item['value']) if item['value'] is not None else 0.0

                # Parse the period string into a datetime object
                period = datetime.strptime(item['period'], "%Y-%m-%dT%H")

                # Create an insert query for the EnergyData table
                query = insert(EnergyData).values(
                    value=value,
                    period=period,
                    respondent=item['respondent'],
                    respondent_name=item['respondent-name'],
                    type=item['type'],
                    type_name=item['type-name'],
                    value_units=item['value-units']
                )

                # Execute the query
                await database.execute(query)

            # Increment the offset parameter for the next iteration
            params['offset'] += params['length']

        return data
