import yfinance as yf
from nsepython import nse_eq


# Helper function to verify if symbol is valid via nsepython
def is_valid_nse_symbol(symbol):
    try:
        data = nse_eq(symbol.upper())
        return isinstance(data, dict) and "info" in data
    except:
        return False

def resolve_yf_symbol(symbol):
    symbol = symbol.upper()
    if is_valid_nse_symbol(symbol):
        return f"{symbol}.NS"
    else:
        print(f"Warning: '{symbol}' not found via nsepython. Assuming Yahoo Finance NSE symbol.")
        return f"{symbol}.NS"  # fallback always .NS for Indian equities

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
