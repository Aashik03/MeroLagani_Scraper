from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.insert(0, "/root/merolagani-scraper")

from scraper import scrape_live_market, scrape_top_gainers, scrape_top_losers
from transform import transform_live, transform_gainers_losers
from load import create_table, load_data

default_args = {
    "owner": "you",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def run_scrape_market(**context):
    data = scrape_live_market()
    context["ti"].xcom_push(key="market_data", value=data)

def run_scrape_gainers(**context):
    data = scrape_top_gainers()
    context["ti"].xcom_push(key="gainers_data", value=data)

def run_scrape_losers(**context):
    data = scrape_top_losers()
    context["ti"].xcom_push(key="losers_data", value=data)

def run_transform_load(**context):
    ti = context["ti"]

    market = ti.xcom_pull(key="market_data", task_ids="scrape_live_market")
    gainers = ti.xcom_pull(key="gainers_data", task_ids="scrape_top_gainers")
    losers = ti.xcom_pull(key="losers_data", task_ids="scrape_top_losers")

    create_table()      # changed from create_tables

    df_market = transform_live(market)
    load_data(df_market, "nepse_LiveMarket")

    df_gainers = transform_gainers_losers(gainers)
    load_data(df_gainers, "nepse_top_gainers")

    df_losers = transform_gainers_losers(losers)
    load_data(df_losers, "nepse_top_losers")

with DAG(
    dag_id="merolagani_nepse_scraper",
    default_args=default_args,
    description="Scrapes live NEPSE data from Merolagani",
    schedule_interval="0 11,12,13,14 * * 0,1,2,3,4",  # every hour 11am-2pm Sun-Thu
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["nepse", "scraper"],
) as dag:

    t1 = PythonOperator(task_id="scrape_live_market", python_callable=run_scrape_market)
    t2 = PythonOperator(task_id="scrape_top_gainers", python_callable=run_scrape_gainers)
    t3 = PythonOperator(task_id="scrape_top_losers", python_callable=run_scrape_losers)
    t4 = PythonOperator(task_id="transform_and_load", python_callable=run_transform_load)

    [t1, t2, t3] >> t4