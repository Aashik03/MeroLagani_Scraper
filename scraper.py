from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

URL = "https://merolagani.com/LatestMarket.aspx"

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def get_page_source(url):
    driver = get_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody tr")))
        time.sleep(3)
        return driver.page_source
    finally:
        driver.quit()

def scrape_live_market():
    source = get_page_source(URL)
    soup = BeautifulSoup(source, "html.parser")
    tables = soup.find_all("table", class_="table")
    data = []
    if tables:
        rows = tables[0].find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 4:
                data.append({
                    "symbol":     cols[0].text.strip(),
                    "ltp":        cols[1].text.strip(),
                    "change_pct": cols[2].text.strip(),
                    "volume":     cols[3].text.strip(),
                    "scraped_at": None
                })
    print(f"Scraped {len(data)} stocks from live market")
    return data

def scrape_top_gainers():
    source = get_page_source(URL)
    soup = BeautifulSoup(source, "html.parser")
    tables = soup.find_all("table", class_="table")
    data = []
    if len(tables) >= 2:
        rows = tables[1].find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                data.append({
                    "symbol":     cols[0].text.strip(),
                    "ltp":        cols[1].text.strip(),
                    "change_pct": cols[2].text.strip(),
                    "scraped_at": None
                })
    print(f"Scraped {len(data)} top gainers")
    return data

def scrape_top_losers():
    source = get_page_source(URL)
    soup = BeautifulSoup(source, "html.parser")
    tables = soup.find_all("table", class_="table")
    data = []
    if len(tables) >= 3:
        rows = tables[2].find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                data.append({
                    "symbol":     cols[0].text.strip(),
                    "ltp":        cols[1].text.strip(),
                    "change_pct": cols[2].text.strip(),
                    "scraped_at": None
                })
    print(f"Scraped {len(data)} top losers")
    return data