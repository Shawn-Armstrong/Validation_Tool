from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from src.utilities.config_utils import load_config
import re

class LogCapturer:

    def __init__(self):
        self.urls = self._extract_urls_from_csv()
        self._extract_unique_endpoints_and_add_wellsfargo()
        self.urls = sorted(self.urls)
        self.options, self.capabilities = self.setup_driver_config()
        self.driver = None  # Driver will be initialized later when launch_driver() is called

    def _extract_urls_from_csv(self):
        
        # Load the URLs CSV path from the config file
        config = load_config()
        urls_csv_path = config['urls_csv_path']
        
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(urls_csv_path, header=None)

            # Extract the first column which contains the URLs
            return df.iloc[:, 0].tolist()
        
        except pd.errors.EmptyDataError:
            print(f"Error: The file '{urls_csv_path}' is empty or doesn't contain valid data.")
            return []

    def _extract_unique_endpoints_and_add_wellsfargo(self):
        pattern = r'^(?:https?://)?[^/]+(?::\d+)?(?P<endpoint>/.*)'
        endpoints_set = set()

        for url in self.urls:
            match = re.match(pattern, url)
            if match:
                endpoints_set.add(match.group('endpoint'))

        for endpoint in endpoints_set:
            wells_fargo_url = f"https://www.wellsfargo.com{endpoint}"
            if wells_fargo_url not in self.urls:
                self.urls.append(wells_fargo_url)

    def setup_driver_config(self):
        options = webdriver.ChromeOptions()
        capabilities = options.to_capabilities()
        capabilities['goog:loggingPrefs'] = {'browser': 'ALL', 'performance': 'ALL'}
        return options, capabilities

    def launch_driver(self):
        self.driver = webdriver.Chrome(desired_capabilities=self.capabilities)

    def capture_logs(self):
        self.launch_driver()
        logs_by_url = {url: self.capture_logs_for_url(url) for url in self.urls}
        return logs_by_url

    def capture_logs_for_url(self, url):
        self.driver.get(url)
        console_logs = self.driver.get_log('browser')
        network_logs = self.driver.get_log('performance')
        return {
            'url': url,
            'console_logs': console_logs,
            'network_logs': network_logs
        }

