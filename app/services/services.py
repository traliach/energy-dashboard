import requests

from app.utils.url_builder import URLBuilder

class EnergyDataService:
    def __init__(self):
        self._request = None

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        self._request = value

    def fetch_data(self):
        url = (URLBuilder()
            .add_frequency('hourly')
            .add_data('value')
            .add_respondent('MISO')
            .add_type('D')
            .add_sort_column('period')
            .add_sort_direction('desc')
            .add_offset(0)
            .add_length(5000)
            .add_start('2024-05-16T00')
            .add_end('2024-05-17T00')
            .build())        
        
        self.request = requests.get(url)
        return self.request.json()