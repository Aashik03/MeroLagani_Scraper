import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def create_table():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""
                create table if not exists nepse_LiveMarket(
                id serial primary key,
                symbol varchar(20),
                ltp float,
                change_pct float,
                volume float,
                scraped_at timestamp
                );

                create table if not exists nepse_top_gainers(
                id serial primary key,
                symbol varchar(20),
                ltp float,
                change_pct float,
                scraped_at timestamp
                );

                create table if not exists nepse_top_losers(
                id serial primary key,
                symbol varchar(20),
                ltp float,
                change_pct float,
                scraped_at timestamp    
                );
                """)
    conn.commit()
    cur.close()
    conn.close()    

def load_data(df,table):
    conn=get_connection()
    cur=conn.cursor()
    inserted=0

    for _,row in df.iterrows():
        if table=="nepse_LiveMarket":
            cur.execute("""
                        insert into nepse_LiveMarket(symbol,ltp,change_pct,volume,scraped_at)
                        values(%s,%s,%s,%s,%s)
                        """,(row['symbol'],row['ltp'],row['change_pct'],row['volume'],row['scraped_at'])    
                        )
        else:
            cur.execute(f"""
                        insert into {table} (symbol,ltp,change_pct,scraped_at)
                        values(%s,%s,%s,%s)
                        """,(row['symbol'],row['ltp'],row['change_pct'],row['scraped_at']))
            
        inserted+=1
    conn.commit()
    cur.close()
    conn.close()    
    print(f"{table}:Inserted {inserted} rows")
    
