import pandas as pd

def clean_number(value):
    if not value or value=="-":
        return None
    return float(value.replace(",","").replace("%","").strip())

def transform_live(data):
    df=pd.DataFrame(data)
    df["scraped_at"]=pd.Timestamp.now()
    df["ltp"]=df["ltp"].apply(clean_number)
    df["change_pct"]=df["change_pct"].apply(clean_number)
    df["volume"]=df["volume"].apply(clean_number)
    df=df.dropna(subset=["symbol","ltp"])
    df=df[df["symbol"]!="-"]
    return df
def transform_gainers_losers(data):
    df=pd.DataFrame(data)
    df["scraped_at"]=pd.Timestamp.now()
    df["ltp"]=df["ltp"].apply(clean_number)
    df["change_pct"]=df["change_pct"].apply(clean_number)
    df=df.dropna(subset=["symbol","ltp"])
    df=df[df["symbol"]!="-"]
    return df