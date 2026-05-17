import logging
from scraper import scrape_live_market, scrape_top_gainers, scrape_top_losers
from transform import transform_live, transform_gainers_losers
from load import create_table, load_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_pipeline():
    logging.info("Starting MeroLagani Scraper Pipeline")
    try:
        create_table()

        logging.info("Scraping live market...")
        raw_data=scrape_live_market()
        df_market=transform_live(raw_data)
        load_data(df_market,"nepse_LiveMarket")

        logging.info("Scraping top gainers...")
        raw_gainers=scrape_top_gainers()
        df_gainers=transform_gainers_losers(raw_gainers)
        load_data(df_gainers,"nepse_top_gainers")

        logging.info("Scraping top losers...")
        raw_losers=scrape_top_losers()
        df_losers=transform_gainers_losers(raw_losers)
        load_data(df_losers,"nepse_top_losers")

        logging.info("MeroLagani Scraper Pipeline completed successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise

if __name__=="__main__":
    run_pipeline()