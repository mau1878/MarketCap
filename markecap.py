import streamlit as st
import yfinance as yf
import requests
import pandas as pd
import plotly.express as px

# Function to fetch shares outstanding from Alpha Vantage
def get_shares_outstanding(alpha_vantage_key, ticker):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={alpha_vantage_key}"
    response = requests.get(url)
    data = response.json()
    
    if "SharesOutstanding" in data:
        return int(data["SharesOutstanding"])
    else:
        st.error("Error fetching shares outstanding data from Alpha Vantage.")
        return None

# Function to calculate historical market cap
def calculate_market_cap(ticker, start_date, end_date, shares_outstanding):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data['MarketCap'] = stock_data['Adj Close'] * shares_outstanding
    return stock_data

# Streamlit app
st.title('Historical Market Cap Plot')

# Alpha Vantage API key input
alpha_vantage_key = st.text_input("Enter your Alpha Vantage API Key")

# Ticker input
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT)")

# Date range selection
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Button to fetch and plot the data
if st.button('Fetch and Plot'):
    if alpha_vantage_key and ticker:
        # Fetch shares outstanding
        shares_outstanding = get_shares_outstanding(alpha_vantage_key, ticker)
        
        if shares_outstanding:
            # Fetch and calculate market cap
            market_cap_data = calculate_market_cap(ticker, start_date, end_date, shares_outstanding)

            # Plotting the market cap data
            fig = px.line(market_cap_data, x=market_cap_data.index, y='MarketCap', title=f'Historical Market Cap for {ticker}')
            st.plotly_chart(fig)
    else:
        st.error("Please provide both a valid Alpha Vantage API key and stock ticker.")
