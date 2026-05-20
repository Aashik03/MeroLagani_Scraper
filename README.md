# Merolagani NEPSE Scraper

An automated web scraping pipeline that collects live Nepal Stock Exchange (NEPSE) data from [Merolagani](https://merolagani.com), transforms it, and loads it into a PostgreSQL database. Orchestrated with Apache Airflow to run automatically during NEPSE trading hours.

---

## Pipeline running successfully

Airflow DAG
<img width="1435" height="713" alt="Screenshot 2026-05-18 112049" src="https://github.com/user-attachments/assets/76a89df4-11e1-4e1d-9bbc-9573fd232630" />
<img width="1919" height="873" alt="Screenshot 2026-05-18 111943" src="https://github.com/user-attachments/assets/942ca66d-4f61-4cc9-b4ca-fce189326325" />
Using Logging
<img width="760" height="291" alt="Screenshot 2026-05-17 230336" src="https://github.com/user-attachments/assets/ce0e0ec7-aaba-435b-9e4b-f0aa934f2a9f" />
---

## What It Does

Every hour during NEPSE trading hours (11am–3pm, Sunday–Thursday), the pipeline:

1. **Scrapes** — uses Selenium to load Merolagani's JavaScript-rendered pages, then BeautifulSoup to parse the HTML
2. **Transforms** — cleans raw scraped text into typed numeric data using pandas
3. **Loads** — inserts clean records into three PostgreSQL tables

Each run captures:
- **338+ live stocks** — symbol, LTP, % change, volume
- **Top 10 gainers** — biggest % winners of the day
- **Top 10 losers** — biggest % losers of the day

---

## Project Structure

```
merolagani-scraper/
├── scraper.py          # Selenium + BeautifulSoup scraping logic
├── transform.py        # Cleans raw scraped data with pandas
├── load.py             # Creates tables and inserts into PostgreSQL
├── pipeline.py         # Orchestrates scrape → transform → load
├── merolagani_dag.py   # Apache Airflow DAG definition
├── .env                # Database credentials (not committed to git)
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| Selenium | Loads JavaScript-rendered pages via headless Chrome |
| BeautifulSoup4 | Parses static HTML snapshot from Selenium |
| pandas | Data cleaning and transformation |
| psycopg2 | PostgreSQL connection |
| python-dotenv | Environment variable management |
| Apache Airflow | Pipeline orchestration and scheduling |
| PostgreSQL | Data storage |

---

## Why Selenium + BeautifulSoup?

Merolagani is a **dynamic site** — live prices are rendered by JavaScript after the page loads. A simple `requests` call returns empty tables.

The solution uses two tools for two different jobs:

```
Selenium                          BeautifulSoup
--------                          -------------
Opens real Chrome (headless) →   Parses the HTML Selenium captured
Executes JavaScript               Finds tables, rows, columns
Waits for data to load            Extracts text cleanly
Grabs final page HTML        →   Done — no stale element errors
```

Selenium grabs `driver.page_source` once JavaScript has finished rendering, then quits. BeautifulSoup reads that frozen HTML snapshot — immune to the `StaleElementReferenceException` that occurs when holding live Selenium references while the page auto-updates.

---

## Airflow DAG Structure

The three scrape tasks run **in parallel**, then feed into one transform and load task:

```
scrape_live_market ──┐
scrape_top_gainers ──┼──► transform_and_load
scrape_top_losers  ──┘
```

This is faster than running sequentially — all three pages are scraped at the same time.

### Schedule

```
0 11,12,13,14 * * 0,1,2,3,4
```

Runs at 11am, 12pm, 1pm, and 2pm Nepal time, Sunday through Thursday — exactly NEPSE trading hours. Automatically skips weekends and Fridays when the market is closed.

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS nepse_LiveMarket (
    id         SERIAL PRIMARY KEY,
    symbol     VARCHAR(20),
    ltp        FLOAT,
    change_pct FLOAT,
    volume     FLOAT,
    scraped_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS nepse_top_gainers (
    id         SERIAL PRIMARY KEY,
    symbol     VARCHAR(20),
    ltp        FLOAT,
    change_pct FLOAT,
    scraped_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS nepse_top_losers (
    id         SERIAL PRIMARY KEY,
    symbol     VARCHAR(20),
    ltp        FLOAT,
    change_pct FLOAT,
    scraped_at TIMESTAMP
);
```

---

## Sample Data in PostgreSQL

**Live market data**
<img width="1217" height="937" alt="Screenshot 2026-05-18 112338" src="https://github.com/user-attachments/assets/524607b0-90d0-453a-903c-2c68739e39bf" />


**Top gainers**

<img width="847" height="686" alt="Screenshot 2026-05-18 112248" src="https://github.com/user-attachments/assets/4cdc9644-51f7-483f-bc26-b52f81705ae2" />

**Top losers**

<img width="854" height="976" alt="Screenshot 2026-05-18 112401" src="https://github.com/user-attachments/assets/c343c244-cbba-42cc-a015-bfed27d4dfdb" />

---

## Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/merolagani-scraper.git
cd merolagani-scraper
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# or
source venv/bin/activate       # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
DB_HOST=localhost
DB_NAME=nepse_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_PORT=5432
```

### 5. Create the PostgreSQL database

```sql
CREATE DATABASE nepse_db;
```

### 6. Run the pipeline once to test

```bash
python pipeline.py
```

### 7. Run with Airflow (recommended)

Copy the DAG file to your Airflow dags folder and start Airflow:

```bash
cp merolagani_dag.py ~/airflow/dags/

# Terminal 1
airflow webserver --port 8080

# Terminal 2
airflow scheduler
```

Open `http://localhost:8080`, toggle on `merolagani_nepse_scraper` and trigger a manual run.

---

## License

MIT
