import requests
import os
from urllib.parse import urlencode
from dotenv import load_dotenv
from agents.data_research_agent import symbol_to_company_name 

load_dotenv()
API_KEY = os.getenv("GNEWS_API_KEY")

def fetch_latest_news(symbol):
    if not API_KEY:
        print("API Key not found. Set GNEWS_API_KEY in your .env file.")
        return []
    

    company_name = symbol_to_company_name(symbol)

    print("company_name: ", company_name)

    query_params = {
        "q": f'"{company_name}" stock',  # quoted for better matching
        "lang": "en",
        "country": "in",
        "max": 10,
        "token": API_KEY
    }

    url = f"https://gnews.io/api/v4/search?{urlencode(query_params)}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        articles = data.get("articles", [])

        return articles

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error {e.response.status_code}: {e.response.text}")
        return []
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return []
