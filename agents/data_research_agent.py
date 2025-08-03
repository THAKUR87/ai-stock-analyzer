import yfinance as yf
from nsetools import Nse

nse = Nse()
stockNse = nse.get_stock_codes()  # {'symbol': 'Company Name'}

def resolve_yf_symbol(symbol):
    symbol = symbol.upper()
    if symbol in stockNse:
        return f"{symbol}.NS"
    else:
        print(f"Warning: '{symbol}' not found in NSE codes. Assuming Yahoo Finance symbol.")
        return f"{symbol}.NS"

def get_stock_data(symbol):
    yf_symbol = resolve_yf_symbol(symbol)
    ticker = yf.Ticker(yf_symbol)
    info = ticker.info
    financials = ticker.financials

    return {
        "info": info,
        "financials": financials,
        "current_price": info.get("currentPrice", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        "market_cap": info.get("marketCap", "N/A")
    }

def symbol_to_company_name(symbol):
    yf_symbol = resolve_yf_symbol(symbol)
    stock = yf.Ticker(yf_symbol)
    return stock.info.get("longName", yf_symbol)
