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
                    self.records[endpoint] = {"test_page_log": None, "production_page_log": None}
                if 'https://www.wellsfargo.com' in url:
                    self.records[endpoint]["production_page_log"] = log_data
                else:
                    self.records[endpoint]["test_page_log"] = log_data
    

