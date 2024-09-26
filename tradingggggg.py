import alpaca_trade_api as tradeapi
import openai
import logging
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# API Info for fetching data, portfolio, etc. from Alpaca
BASE_URL = os.getenv("BASE_URL")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Initialize Alpaca API
api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY,
                    base_url=BASE_URL, api_version='v2')

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_stock_symbol():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Generate a stock symbol for a popular company. Find 10 different ones and only choose 1 of them. Only list me the symbol. Do not make it AAPL."}
        ]
    )
    stock_symbol = response.choices[0].message['content'].strip()
    return stock_symbol

def buy_stock(symbol):
    order = api.submit_order(
        symbol=symbol,
        qty=20,  # fractional shares
        side='buy',
        type='market',
        time_in_force='day',
    )
    return order

# Get account info
account = api.get_account()
print(account)

# Generate stock symbol using ChatGPT 3.5
stock_symbol = get_stock_symbol()
print(f"Generated stock symbol: {stock_symbol}")

# Buy the generated stock symbol
order = buy_stock(stock_symbol)
print(order)