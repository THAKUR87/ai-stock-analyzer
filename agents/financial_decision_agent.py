import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Update env variable name

def make_decision(current_price, analysis_summary):
    prompt = f"""
You are a stock advisor. A stock is currently priced at ${current_price}.
Here is a detailed analysis of its news and financials:

{analysis_summary}

Based on the above, recommend if the investor should Buy, Hold, or Sell. Give your reasoning in 2-3 sentences.
    """
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8080",  # Required by OpenRouter (can be any valid URL)
        "X-Title": "Stock Advisor",      # Required by OpenRouter (any name)
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistralai/mistral-7b-instruct",  # Free model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=20  # Add timeout to prevent hanging
        )
        response.raise_for_status()  # Raises HTTP errors
        
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
        
    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"
    except KeyError:
        return f"Unexpected response format: {response_data}"

# Example usage
#if __name__ == "__main__":
#    print(make_decision(150.50, "Strong earnings but high volatility."))