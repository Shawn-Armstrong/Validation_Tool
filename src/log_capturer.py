from selenium import webdriver
import pandas as pd
from src.utilities.config_utils import load_config
import re
import time

class LogCapturer:

    def __init__(self):
        self.urls = set(self._extract_urls_from_csv())
        self._extract_unique_endpoints_and_add_wellsfargo()
        self.urls = sorted(self.urls)
        self.options, self.capabilities = self.setup_driver_config()
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            self._driver = webdriver.Chrome(desired_capabilities=self.capabilities)
        return self._driver

    def _extract_urls_from_csv(self):
        config = load_config()
        urls_csv_path = config['urls_csv_path']
        try:
            df = pd.read_csv(urls_csv_path, header=None)
            return df.iloc[:, 0].tolist()
        except pd.errors.EmptyDataError:
            print(f"Error: The file '{urls_csv_path}' is empty or doesn't contain valid data.")
            return []

    def _extract_unique_endpoints_and_add_wellsfargo(self):
        pattern = r'^(?:https?://)?[^/]+(?::\d+)?(?P<endpoint>/.*)'
        compiled_pattern = re.compile(pattern)
        
        endpoints_set = {compiled_pattern.match(url).group('endpoint') for url in self.urls if compiled_pattern.match(url)}
        
        self.urls.update([f"https://www.wellsfargo.com{endpoint}" for endpoint in endpoints_set])

    def setup_driver_config(self):
        options = webdriver.ChromeOptions()
        capabilities = options.to_capabilities()
        capabilities['goog:loggingPrefs'] = {'browser': 'ALL', 'performance': 'ALL'}
        return options, capabilities

    def capture_logs(self):
        logs_by_url = {url: self.capture_logs_for_url(url) for url in self.urls}
        if self._driver:
            self._driver.quit()
        return logs_by_url

    def capture_logs_for_url(self, url):
        self.driver.get(url)
        time.sleep(5)
        console_logs = self.driver.get_log('browser')
        network_logs = self.driver.get_log('performance')
        return {
            'url': url,
            'console_logs': console_logs,
            'network_logs': network_logs
        }
