import pandas as pd
import streamlit as st
from datetime import datetime
import io

def load_uploaded_portfolio(uploaded_file):
    """Load the user's uploaded CSV into a DataFrame."""
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    else:
        # Return empty template if no file uploaded
        return pd.DataFrame(columns=["DateTime", "Stock", "Price", "Decision"])

def log_decision_to_session(stock, price, decision, session_key="portfolio"):
    """Add decision to in-session portfolio DataFrame."""
    new_entry = {
        "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Stock": stock,
        "Price": price,
        "Decision": decision
    }
    if session_key not in st.session_state:
        st.session_state[session_key] = pd.DataFrame(columns=["DateTime", "Stock", "Price", "Decision"])
    df = st.session_state[session_key]
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    st.session_state[session_key] = df

def get_portfolio_from_session(session_key="portfolio"):
    """Get portfolio from session."""
    if session_key in st.session_state:
        return st.session_state[session_key]
    return pd.DataFrame(columns=["DateTime", "Stock", "Price", "Decision"])

def download_portfolio_csv(session_key="portfolio"):
    """Return downloadable CSV bytes."""
    df = get_portfolio_from_session(session_key)
    return df.to_csv(index=False).encode("utf-8")
