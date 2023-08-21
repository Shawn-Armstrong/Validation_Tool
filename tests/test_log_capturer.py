import unittest
from unittest.mock import patch, Mock
from src import log_capturer
from unittest.mock import patch, MagicMock
import pandas as pd
from selenium.webdriver import ChromeOptions

class TestLogCapturer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        if hasattr(self, 'capturer'):
            del self.capturer

    @patch('src.log_capturer.load_config')
    @patch('pandas.read_csv')
    def test_extract_and_add_wellsfargo_urls(self, mock_read_csv, mock_load_config):
        
        # Mock the return value of load_config to return a fake CSV path
        mock_load_config.return_value = {'urls_csv_path': 'fake_path.csv'}
        
        # Mock the return value of read_csv to return a DataFrame-like object with fake data
        mock_df = MagicMock()
        mock_df.iloc[:, 0].tolist.return_value = ['http://example.com/path', 'http://test.com/testpath']
        mock_read_csv.return_value = mock_df

        capturer = log_capturer.LogCapturer()
        expected_urls = [
            'http://example.com/path',
            'http://test.com/testpath',
            'https://www.wellsfargo.com/path',
            'https://www.wellsfargo.com/testpath'
        ]
        self.assertEqual(sorted(capturer.urls), sorted(expected_urls))


    @patch('src.log_capturer.load_config')
    @patch('src.log_capturer.pd.read_csv')
    def test_empty_file_case(self, mock_read_csv, mock_load_config):

        # Mock the return value of load_config to return a fake CSV path
        mock_load_config.return_value = {'urls_csv_path': 'fake_path.csv'}

        # Mock the behavior of pd.read_csv to raise an EmptyDataError
        mock_read_csv.side_effect = pd.errors.EmptyDataError

        # Initialize LogCapturer
        capturer = log_capturer.LogCapturer()

        # Verify the urls attribute is an empty list
        self.assertEqual(capturer.urls, [])


    @patch('src.log_capturer.load_config')
    @patch('pandas.read_csv')
    def test_extract_endpoints_from_various_url_formats(self, mock_read_csv, mock_load_config):
       
        urls = [
            "https://www.google.com/helpus/",
            "http://www.example.com:8080/dashboard/user/",
            "www.yahoo.com/search/",
            "http://localhost:3000/dev/api/",
            "https://www.microsoft.com/en-us/store/b/home",
            "www.mywebsite.org:4567/articles/read/",
            "https://api.github.com/users/octocat",
            "http://192.168.1.1:8000/settings/",
            "www.localtest.me:9000/tests/run/",
            "https://subdomain.example.com:4000/profile/edit/",
            "www.bankofamerica.com:2048/accounts/overview/",
            "http://ftp.server.com:21/files/upload/",
            "www.mysite.net:2222/forum/posts/",
            "https://www.amazon.com/gp/cart/view.html",
            "http://sports.yahoo.com:80/nba/teams/lal",
        ]

       # Mock the return value of load_config to return a fake CSV path
        mock_load_config.return_value = {'urls_csv_path': 'fake_path.csv'}
        
        # Mock the return value of read_csv to return a DataFrame-like object with fake data
        mock_df = MagicMock()
        mock_df.iloc[:, 0].tolist.return_value = urls
        mock_read_csv.return_value = mock_df

        capturer = log_capturer.LogCapturer()
        expected_result = [
            "https://www.google.com/helpus/",
            "http://www.example.com:8080/dashboard/user/",
            "www.yahoo.com/search/",
            "http://localhost:3000/dev/api/",
            "https://www.microsoft.com/en-us/store/b/home",
            "www.mywebsite.org:4567/articles/read/",
            "https://api.github.com/users/octocat",
            "http://192.168.1.1:8000/settings/",
            "www.localtest.me:9000/tests/run/",
            "https://subdomain.example.com:4000/profile/edit/",
            "www.bankofamerica.com:2048/accounts/overview/",
            "http://ftp.server.com:21/files/upload/",
            "www.mysite.net:2222/forum/posts/",
            "https://www.amazon.com/gp/cart/view.html",
            "http://sports.yahoo.com:80/nba/teams/lal",
            "https://www.wellsfargo.com/helpus/",
            "https://www.wellsfargo.com/dashboard/user/",
            "https://www.wellsfargo.com/search/",
            "https://www.wellsfargo.com/dev/api/",
            "https://www.wellsfargo.com/en-us/store/b/home",
            "https://www.wellsfargo.com/articles/read/",
            "https://www.wellsfargo.com/users/octocat",
            "https://www.wellsfargo.com/settings/",
            "https://www.wellsfargo.com/tests/run/",
            "https://www.wellsfargo.com/profile/edit/",
            "https://www.wellsfargo.com/accounts/overview/",
            "https://www.wellsfargo.com/files/upload/",
            "https://www.wellsfargo.com/forum/posts/",
            "https://www.wellsfargo.com/gp/cart/view.html",
            "https://www.wellsfargo.com/nba/teams/lal"
        ]
        self.assertEqual(capturer.urls, sorted(expected_result))

    def test_setup_driver_config(self):

        capturer = log_capturer.LogCapturer()

        options, capabilities = capturer.setup_driver_config()

        # Verify that the capabilities and options are set correctly
        self.assertIsInstance(options, ChromeOptions)
        self.assertIn('goog:loggingPrefs', capabilities)
        self.assertEqual(capabilities['goog:loggingPrefs'], {'browser': 'ALL', 'performance': 'ALL'})

    def test_launch_driver(self):
        capturer = log_capturer.LogCapturer()
        
        # Execute test
        capturer.launch_driver()
        capturer.driver.get("https://www.google.com")
        search_box =  capturer.driver.find_element("name", "q")
        search_box.send_keys("Hello, Selenium!")
        search_box.submit()

        # Verify results
        assert "Hello, Selenium!" in  capturer.driver.title
        capturer.driver.quit()