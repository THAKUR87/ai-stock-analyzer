import streamlit as st
import pandas as pd
from agents.news_info_agent import get_stock_news
from agents.data_research_agent import get_stock_data
from agents.analyst_agent import analyze_stock
from agents.financial_decision_agent import make_decision
from utils.portfolio_tracker import get_portfolio_from_session, download_portfolio_csv, load_uploaded_portfolio, log_decision_to_session



# Custom Header (replace existing title line)
header_html = """
    <div style="background-color: #0b5394; padding: 20px; border-radius: 8px; text-align: center;">
        <h1 style="color: white; margin: 0;">📊 AI Powered – AI Stock Analyzer</h1>
        <p style="color: #d9d9d9; font-size: 16px; margin: 5px 0 0;">
            Analyze. Interpret. Decide. Empowering your investment decisions with AI.
        </p>
    </div>
"""
st.markdown(header_html, unsafe_allow_html=True)
st.set_page_config(page_title="📊 AI Powered Stock Analyzer", layout="wide")

# Allow user to upload their own portfolio file
uploaded_file = st.sidebar.file_uploader("📂 Upload your portfolio.csv", type="csv")

if uploaded_file and "portfolio" not in st.session_state:
    st.session_state["portfolio"] = load_uploaded_portfolio(uploaded_file)

# Show current portfolio from session
portfolio_df = get_portfolio_from_session()

st.sidebar.title("📋 Portfolio Tracker")
if portfolio_df.empty:
    st.sidebar.info("No portfolio data uploaded or logged yet.")
else:
    st.sidebar.dataframe(portfolio_df.sort_values("DateTime", ascending=False), use_container_width=True)

# Add download button
csv_data = download_portfolio_csv()
st.sidebar.download_button(
    label="⬇️ Download Your Portfolio",
    data=csv_data,
    file_name="portfolio.csv",
    mime="text/csv"
)

# User input
#exchange = st.selectbox("Choose Exchange", ["NSE", "BSE"])
stock_symbol_input = st.text_input("Enter Stock Symbol (e.g., RELIANCE, TCS):").upper()

if not stock_symbol_input:
    st.info("🔍 Enter a stock symbol above to analyze a company using AI.")

#suffix = ".NS" if exchange == "NSE" else ".BO"
if stock_symbol_input :
    stock_symbol = stock_symbol_input # + suffix

    # Proceed only if stock_symbol is defined
    with st.spinner("⏳ Analyzing stock data..."):
        news_data = get_stock_news(stock_symbol)
        financial_data = get_stock_data(stock_symbol)
        analysis_result = analyze_stock(news_data, financial_data)
        decision = make_decision(financial_data['current_price'], analysis_result["summary"])
        log_decision_to_session(stock_symbol, financial_data['current_price'], decision.split()[0])

    # Display recommendation with color and emoji
    if "BUY" in decision.upper():
        st.markdown("<h2 style='color: green;'>👍 Buy Recommendation</h2>", unsafe_allow_html=True)
    elif "SELL" in decision.upper():
        st.markdown("<h2 style='color: red;'>👎 Sell Recommendation</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color: orange;'>🤝 Hold Recommendation</h2>", unsafe_allow_html=True)

    # Reason for recommendation
    st.markdown("### 🧾 Reason for Recommendation")
    st.info("Split reasoning based on technical indicators and news sentiment.")

    with st.expander("📈 Technical Analysis-Based Reason"):
        st.write(analysis_result["technical_reason"])

    with st.expander("📰 News-Based Reason"):
        st.write(analysis_result["news_reason"])

    # Key financial stats
    st.subheader("📌 Key Financial Statistics")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Current Price", f"₹{financial_data['current_price']}")
    col2.metric("P/E Ratio", financial_data.get("pe_ratio", "N/A"))
    col3.metric("52W High", f"₹{financial_data.get('52_week_high', 'N/A')}")
    col4.metric("52W Low", f"₹{financial_data.get('52_week_low', 'N/A')}")
    col5.metric("Market Cap", financial_data.get("market_cap", "N/A"))

    from utils.portfolio_tracker import (
        load_uploaded_portfolio,
        log_decision_to_session,
        get_portfolio_from_session,
        download_portfolio_csv
    )


    def sanitize(value):
        if isinstance(value, (dict, list)):
            return str(value)
        elif value is None:
            return "N/A"
        elif isinstance(value, (float, int)):
            return f"{value:,.2f}"
        return str(value)

    def sanitize_financials_df_preserve_numeric(financials_df):
        df = financials_df.copy()

        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")  # Coerce strings like "N/A" to NaN

        return df




    def render_financial_overview(financial_data):
        info = financial_data.get("info", {})
    
        fields = {
            "Symbol": sanitize(info.get("symbol")),
            "Company Name": sanitize(info.get("longName")),
            "Sector": sanitize(info.get("sector")),
            "Industry": sanitize(info.get("industry")),
            "Current Price (₹)": f"₹ {sanitize(info.get('currentPrice'))}",
            "P/E Ratio": sanitize(info.get("trailingPE")),
            "52-Week Low (₹)": f"₹ {sanitize(info.get('fiftyTwoWeekLow'))}",
            "52-Week High (₹)": f"₹ {sanitize(info.get('fiftyTwoWeekHigh'))}",
            "Market Cap": f"{sanitize(round(info.get('marketCap', 0)/1e9, 2))} B",
            "Dividend Yield": sanitize(info.get("dividendYield")),
            "Beta": sanitize(info.get("beta"))
        }

        df = pd.DataFrame(list(fields.items()), columns=["Metric", "Value"])
        st.markdown("### 📊 Financial Overview")
        st.dataframe(df, use_container_width=True)



    st.markdown("### 🧾 Company Financial Statements")
    clean_financials_df = sanitize_financials_df_preserve_numeric(financial_data["financials"])
    st.dataframe(clean_financials_df.fillna("N/A"), use_container_width=True)


    with st.expander("📦 Raw Company Data (for dev/debug)"):
        st.json(financial_data["info"])

    # AI model Analysis
    st.markdown("### 🧠 AI Powered - Based Analysis")
    st.text_area("Summary", analysis_result["summary"], height=250)

    # News articles
    st.markdown("### 📰 Latest News")
    if not news_data:
        st.warning("No recent news articles found for this stock.")
    for i, article in enumerate(news_data[:5], 1):
        st.markdown(f"**{i}. {article['title']}**")
        st.write(article.get("description", "No summary available."))
        st.markdown(f"[🔗 Read more]({article.get('url', '#')})", unsafe_allow_html=True)
        st.markdown("---")


footer = """
    <style>
        .footer {
            position: relative;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            margin-top: 50px;
            color: #999999;
            font-size: 0.9em;
        }
        .footer a {
            color: #4a90e2;
            text-decoration: none;
        }
    </style>
    <div class="footer">
        © 2025 Pawan Parihar | Contact: <a href="mailto:pawanju87@gmail.com">pawanju87@gmail.com</a>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
