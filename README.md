# Stock Forecasting App

## Overview

This is a stock forecasting web application built using Python. It allows users to predict stock prices using historical data and machine learning algorithms. The application is implemented using Streamlit for the user interface, Facebook's Prophet library for forecasting, and SQLite for user authentication and data management.

## Features

- **Stock Prediction**: Users can select stocks and predict future prices using the Prophet forecasting model.
- **Data Visualization**: Displays historical stock prices and forecasted data using interactive plots.
- **User Authentication**: Users can sign up, log in, and view their profiles.
- **Analytics**: Compare historical data of two selected stocks or cryptocurrencies.

## Requirements

- Python 3.x
- Streamlit
- Pandas
- Plotly
- yFinance
- fbprophet
- SQLite3

You can install the required libraries using pip:

```bash
pip install streamlit pandas plotly yfinance fbprophet
```

## Usage

1. **Run the Application**:
   To start the application, execute the following command in your terminal:

   ```bash
   streamlit run main.py
   ```

2. **Navigating the App**:
   - **Home**: Provides a brief introduction to the stock market and displays an introductory image.
   - **Login**: Allows users to log in to their accounts. Users must enter a username and password to access the prediction and analytics features.
   - **Sign Up**: Users can create a new account by entering their name, username, and password.
   - **Stock Prediction App**: After logging in, users can select a stock or cryptocurrency, choose a prediction period, and view the historical and forecasted data.
   - **Analytics**: Compare the historical data of two different stocks or cryptocurrencies.
   - **Profiles**: Displays all user profiles stored in the database.

## Code Explanation

- **`main.py`**: Contains the core logic for the app, including:
  - **Stock Forecasting**: `stock_forecast()` function uses Prophet to forecast stock prices.
  - **User Authentication**: Functions for user sign-up, login, and profile management.
  - **Analytics**: `analytics()` function compares historical data of selected stocks.
  - **Database Management**: Functions to interact with the SQLite database.

### Important Functions:

- `stock_forecast()`: Handles the stock prediction logic and displays historical and forecasted stock data.
- `analytics()`: Displays comparative historical data for selected stocks or cryptocurrencies.
- `create_usertable()`, `add_userdata()`, `login_user()`, `view_all_users()`: Functions for managing user data in the SQLite database.

## File Structure

- **`main.py`**: Main application script containing the logic for forecasting, user authentication, and analytics.
- **`data.db`**: SQLite database file for storing user credentials and profiles.
- **`stock_image.jpeg`**: An image file displayed on the home page (optional).

## Notes

- Ensure you have the necessary libraries installed.
- Modify the stock symbols and date ranges in the `stock_forecast()` function as needed.
- The `data.db` file will be created automatically if it doesn't exist.

## Acknowledgements

- **Streamlit**: For creating the web interface.
- **yFinance**: For fetching stock data.
- **Prophet**: For time series forecasting.
- **Plotly**: For interactive data visualization.
