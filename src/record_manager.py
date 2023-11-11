from record import Record
import re

class RecordManager:

    def __init__(self, logs):
        self.logs = logs
        self.records = {}
        self._extract_unique_endpoints_and_organize()
    
    def _extract_unique_endpoints_and_organize(self):
        pattern = r'^(?:https?://)?[^/]+(?::\d+)?(?P<endpoint>/.*)'
        compiled_pattern = re.compile(pattern)
        
        for url, log_data in self.logs.items():
            match = compiled_pattern.match(url)
            if match:
                endpoint = match.group('endpoint')
                if endpoint not in self.records:
                    self.records[endpoint] = Record(endpoint, None, None) # Create a new Record instance
                if 'https://www.wellsfargo.com' in url:
                    self.records[endpoint].prod_logs = log_data
                else:
                    self.records[endpoint].test_logs = log_data
            