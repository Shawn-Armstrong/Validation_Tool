# test_selenium_basic.py

from selenium import webdriver
from src.utilities.config_utils import load_config

def test_google_search():
    """
    Opens a Chrome browser, navigates to Google, and searches for the phrase "Hello, Selenium!".

    Expected Outcome:
    - A new Chrome browser window should open.
    - The browser should navigate to the Google homepage (https://www.google.com).
    - "Hello, Selenium!" should be entered into the Google search box programmatically.
    - After submission, the search results page should have "Hello, Selenium!" in its title.

    Notes:
    - Ensure that the appropriate ChromeDriver version is set up and matches the browser version.
    """
    # Setup driver
    config = load_config()
    driver_path = config['chromedriver_path']
    driver = webdriver.Chrome(executable_path=driver_path)

    # Execute test
    driver.get("https://www.google.com")
    search_box = driver.find_element("name", "q")
    search_box.send_keys("Hello, Selenium!")
    search_box.submit()

    # Verify results
    assert "Hello, Selenium!" in driver.title
    driver.quit()
