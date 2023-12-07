import streamlit as st
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import time

# Function calling local CSS sheet
def local_css(file_name):
    with open(file_name) as f:
        st.sidebar.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Local CSS sheet
local_css("style.css")

# Create an opening screen
# Display the GIF
st.image("bday.gif", use_column_width=True)
st.markdown("<h4 style='text-align: center; color: #FF5733;'>Explore the last 50 years of stocks...</h4>", unsafe_allow_html=True)
st.write("using Yahoo Finance")

# Sleep for 5 seconds to display the opening screen
time.sleep(3)

# Clear the opening screen
st.text("")

# Ticker search feature in sidebar
st.sidebar.subheader("Stock Search Web App")
selected_stock = st.sidebar.text_input("Enter a valid stock ticker...", "^IXIC")

# Date range selector with default start and end dates
default_start_date = datetime(1973, 12, 6)
default_end_date = datetime.today()
start_date = st.sidebar.date_input("Select a start date:", default_start_date)
end_date = st.sidebar.date_input("Select an end date:", default_end_date)

# Main function
def main(selected_stock):
    st.subheader(f"Daily **closing price** for {selected_stock} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    # Get data on searched ticker
    stock_data = yf.Ticker(selected_stock)
    # Get historical data for searched ticker within the selected date range
    stock_df = stock_data.history(period='1d', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    # Print line chart with daily closing prices for searched ticker
    st.line_chart(stock_df.Close)

    # Get daily volume for searched ticker
    st.subheader(f"Daily **volume** for {selected_stock} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    st.line_chart(stock_df.Volume)

    # Additional information feature in sidebar
    st.sidebar.subheader("Display Additional Information")
    
    # Checkbox to display stock actions for the searched ticker
    actions = st.sidebar.checkbox("Stock Actions")
    if actions:
        st.subheader(f"Stock **actions** for {selected_stock}")
        display_action = stock_data.actions
        if display_action.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_action)

    # Checkbox to display quarterly financials for the searched ticker
    financials = st.sidebar.checkbox("Quarterly Financials")
    if financials:
        st.subheader(f"**Quarterly financials** for {selected_stock}")
        display_financials = stock_data.quarterly_financials
        if display_financials.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_financials)

    # Checkbox to display list of institutional shareholders for searched ticker
    major_shareholders = st.sidebar.checkbox("Institutional Shareholders")
    if major_shareholders:
        st.subheader(f"**Institutional investors** for {selected_stock}")
        display_shareholders = stock_data.institutional_holders
        if display_shareholders.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_shareholders)

    # Checkbox to display quarterly balance sheet for searched ticker
    balance_sheet = st.sidebar.checkbox("Quarterly Balance Sheet")
    if balance_sheet:
        st.subheader(f"**Quarterly balance sheet** for {selected_stock}")
        display_balancesheet = stock_data.quarterly_balance_sheet
        if display_balancesheet.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_balancesheet)

    # Checkbox to display quarterly cashflow for searched ticker
    cashflow = st.sidebar.checkbox("Quarterly Cashflow")
    if cashflow:
        st.subheader(f"**Quarterly cashflow** for {selected_stock}")
        display_cashflow = stock_data.quarterly_cashflow
        if display_cashflow.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_cashflow)

    # Compare Multiple Stocks
    st.sidebar.subheader("Compare Multiple Stocks")
    selected_stocks = st.sidebar.text_input("Enter stock tickers separated by commas (e.g., AAPL, MSFT):")
    selected_stocks_list = [stock.strip() for stock in selected_stocks.split(",")]

    if selected_stocks_list:
        st.subheader("Comparison of Selected Stocks")
        comparison_df = yf.download(selected_stocks_list, start=start_date, end=None)['Adj Close']
        st.line_chart(comparison_df)

if __name__ == "__main__":
    main(selected_stock)
