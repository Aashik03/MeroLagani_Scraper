from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://merolagani.com/LatestMarket.aspx")
time.sleep(3)
print("Page title:", driver.title)
print("Page loaded successfully")
driver.quit()