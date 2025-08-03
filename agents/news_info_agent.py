from utils.gnews_api import fetch_latest_news

def get_stock_news(symbol):
    return fetch_latest_news(symbol)
