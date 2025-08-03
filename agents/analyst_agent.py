import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def analyze_stock(news_data, financial_data):
    news_text = "\n".join(
        [f"- {item['title']}: {item.get('description', '')}" for item in news_data if 'title' in item]
    )

    prompt = f"""
You are a financial analyst AI. You are given the latest news and financial data of a company.

News Headlines:
{news_text}

Financial Summary:
Company Info: {financial_data['info']}
Key Financials: {financial_data['financials'].to_string()}

Based on this information, provide the following:

1. 📈 Technical Analysis-Based Reasoning (consider P/E ratio, price trends, 52-week high/low, etc.)
2. 📰 News-Based Reasoning (based on recent events, investor sentiment, and news tone)
3. 🧾 Final Summary/Recommendation (summarize your judgment in 2–3 lines)

Format the output as:

Technical Reasoning:
...

News-Based Reasoning:
...

Summary:
...
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8080",
        "X-Title": "Stock Analyzer",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=15
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return parse_analysis_response(content)

    except requests.exceptions.RequestException as e:
        return {
            "technical_reason": "N/A",
            "news_reason": "N/A",
            "summary": f"API Error: {str(e)}"
        }
    except KeyError:
        print("Debug - Full API Response:", response.json())
        return {
            "technical_reason": "N/A",
            "news_reason": "N/A",
            "summary": "Error: Unexpected API response format"
        }
    except Exception as e:
        return {
            "technical_reason": "N/A",
            "news_reason": "N/A",
            "summary": f"Processing Error: {str(e)}"
        }

def parse_analysis_response(response_text):
    technical = re.search(r"Technical Reasoning:(.*?)(News-Based Reasoning:|Summary:)", response_text, re.DOTALL)
    news = re.search(r"News-Based Reasoning:(.*?)(Summary:)", response_text, re.DOTALL)
    summary = re.search(r"Summary:(.*)", response_text, re.DOTALL)

    return {
        "technical_reason": technical.group(1).strip() if technical else "N/A",
        "news_reason": news.group(1).strip() if news else "N/A",
        "summary": summary.group(1).strip() if summary else response_text.strip()
    }
