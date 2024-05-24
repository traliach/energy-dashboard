from pathlib import Path
from urllib.parse import urlencode

ROOT_DIR = Path(__file__).parent.parent.parent
TEMPLATES_DIR = f"{Path(__file__).parent}/templates"


class URLBuilder:
    BASE_URL = "https://api.eia.gov/v2"
    ROUTE = "/electricity/rto/region-data/data/"

    def __init__(self):
        self._url = self.BASE_URL + self.ROUTE
        self._params = {}

    def add_param(self, key: str, value: str) -> "URLBuilder":
        self._params[key] = value
        return self

    def build(self) -> str:
        query_string = urlencode(self._params)
        return f"{self._url}?{query_string}"

    def add_api_key(self, key: str) -> "URLBuilder":
        return self.add_param("api_key", key)
