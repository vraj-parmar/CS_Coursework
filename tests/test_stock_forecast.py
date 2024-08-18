import pandas as pd
from stock_forecasting import load_data


def test_load_data():
    # Test loading data for a specific stock
    ticker = "AAPL"
    data = load_data(ticker)

    # Ensure data is not empty
    assert not data.empty

    # Check if the data contains expected columns
    assert all(col in data.columns for col in ["Date", "Open", "Close", "High", "Low", "Volume"])


def test_forecast_output():
    # Assuming you have a separate function for the forecasting, you can test it here
    pass  # Replace with actual forecast test
