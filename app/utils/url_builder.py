class URLBuilder:
    BASE_URL = "https://api.eia.gov/v2"
    ROUTE = "/electricity/rto/region-data/data/"
    FREQUENCY = "?frequency="
    DATA = "&data%5B0%5D="
    RESPONDENT = "&facets%5Brespondent%5D%5B%5D="
    TYPE = "&facets%5Btype%5D%5B%5D="
    SORT_COLUMN = "&sort%5B0%5D%5Bcolumn%5D="
    SORT_DIRECTION = "&sort%5B0%5D%5Bdirection%5D="
    OFFSET = "&offset="
    LENGTH = "&length="

    def __init__(self):
        self._url = self.BASE_URL

    def add_frequency(self, frequency):
        self._url += self.FREQUENCY + frequency
        return self

    def add_data(self, data):
        self._url += self.DATA + data
        return self

    def add_respondent(self, respondent):
        self._url += self.RESPONDENT + respondent
        return self

    def add_type(self, type):
        self._url += self.TYPE + type
        return self

    def add_sort_column(self, column):
        self._url += self.SORT_COLUMN + column
        return self

    def add_sort_direction(self, direction):
        self._url += self.SORT_DIRECTION + direction
        return self

    def add_offset(self, offset):
        self._url += self.OFFSET + str(offset)
        return self

    def add_length(self, length):
        self._url += self.LENGTH + str(length)
        return self
    
    def add_start(self, start):
        self._url += self.START + str(start)
        return self
    
    def add_end(self, end):
        self._url += self.END + str(end)
        return self

    def build(self):
        return self._url
    
    