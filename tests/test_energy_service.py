import pytest
import httpx
from app.services import EnergyDataClient

@pytest.mark.asyncio
async def test_fetch_data(monkeypatch):
    # Mock the response from the API
    async def mock_get(self, url):
        return httpx.Response(
            status_code=200,
            json={
                "data": [
                    {
                        "period": "2024-05-16T00:00:00Z",
                        "respondent": "MISO",
                        "respondent_name": "MISO",
                        "type": "D",
                        "type_name": "Demand",
                        "value": 1000.0,
                        "value_units": "MW"
                    }
                ]
            }
        )

    # Use monkeypatch to replace the 'get' method in httpx.AsyncClient with the mock
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    # Create an instance of the service
    async with httpx.AsyncClient() as client:
        service = EnergyDataClient(client)

        # Call the fetch_data method
        result = await service.fetch_data()

        # Assert the result
        assert result == {
            "data": [
                {
                    "period": "2024-05-16T00:00:00Z",
                    "respondent": "MISO",
                    "respondent_name": "MISO",
                    "type": "D",
                    "type_name": "Demand",
                    "value": 1000.0,
                    "value_units": "MW"
                }
            ]
        }