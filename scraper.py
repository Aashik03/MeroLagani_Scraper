from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")        
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def scrape_live_market():
    driver= get_driver()
    data=[]
    try:
        driver.get("https://merolagani.com/LatestMarket.aspx")
        #wait for the table to load
        WebDriverWait(driver,15).until(
            EC.presence_of_element_located(By.CSS_SELECTOR,"table.table tbody tr"))
        time.sleep(2)
        rows=driver.find_elements(By.CSS_SELECTOR,"table.table tbody tr")
        for row in rows:
            cols=row.find_elements(By.TAG_NAME,"td")
            if len(cols)>=6:
                data.append({
                    "symbol":cols[0].text.strip(),
                    "ltp":cols[1].text.strip(),
                    "change_pct":cols[2].text.strip(),
                    "volume":cols[3].text.strip(),
                    "scraped_at":None
                })
        print(f"Scraped {len(data)} stocks from MeroLagani Live Market ")
    finally:
        driver.quit()
    return data
def scrape_top_gainers():
    driver=get_driver()
    data=[]
    try:
        driver.get("https://merolagani.com/LatestMarket.aspx")
        WebDriverWait(driver,15).until(
            EC.presence_of_element_located(By.CSS_SELECTOR,"table.table tbody tr"))
        time.sleep(2)
        table=driver.find_element(By.CSS_SELECTOR,"table.table")
        if len(table)>=2:
            rows=table[1].find_elements(By.TAG_NAME,"tr")[1:]
            for row in rows:
                cols=row.find_elements(By.TAG_NAME,"td")
                if len(cols)>=3:
                    data.append({
                        "symbol":cols[0].text.strip(),
                        "ltp":cols[1].text.strip(),
                        "change_pct":cols[2].text.strip(),
                        "scraped_at":None
                    })
        print(f"Scraped {len(data)} stocks from MeroLagani Top Gainers ")
    finally:
        driver.quit()
    return data

def scrape_top_losers():
    driver=get_driver()
    data=[]
    try:
        driver.get("https://merolagani.com/LatestMarket.aspx")
        WebDriverWait(driver,15).until(
            EC.presence_of_element_located(By.CSS_SELECTOR,"table.table tbody tr"))
        time.sleep(2)
        table=driver.find_element(By.CSS_SELECTOR,"table.table")
        if len(table)>=3:
            rows=table[2].find_elements(By.TAG_NAME,"tr")[1:]
            for row in rows:
                cols=row.find_elements(By.TAG_NAME,"td")
                if len(cols)>=3:
                    data.append({
                        "symbol":cols[0].text.strip(),
                        "ltp":cols[1].text.strip(),
                        "change_pct":cols[2].text.strip(),
                        "scraped_at":None
                    })
        print(f"Scraped {len(data)} stocks from MeroLagani Top Losers ")
    finally:        
        driver.quit()
    return data