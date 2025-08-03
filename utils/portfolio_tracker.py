import pandas as pd
from datetime import datetime
import os

PORTFOLIO_FILE = "portfolio.csv"

def log_decision(symbol, current_price, decision):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = pd.DataFrame([{
        "DateTime": now,
        "Stock": symbol,
        "Price": current_price,
        "Decision": decision
    }])
    
    if os.path.exists(PORTFOLIO_FILE):
        df = pd.read_csv(PORTFOLIO_FILE)
        df = pd.concat([df, entry], ignore_index=True)
    else:
        df = entry
    df.to_csv(PORTFOLIO_FILE, index=False)

def get_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        return pd.read_csv(PORTFOLIO_FILE)
    else:
        return pd.DataFrame(columns=["DateTime", "Stock", "Price", "Decision"])
