import streamlit as st # the library used to display all the pages
from datetime import date # the library allows dates to be used
import pandas as pd # imports the library pandas to allow for graphs to be drawn
import webbrowser # imports the library webbrowser to allow web-based documents to be displayed

import yfinance as yf # the library is used to get the prices
from fbprophet import Prophet # the library is used to produce the forecasted data
from fbprophet.plot import plot_plotly # the library is used to plot the graph
from plotly import graph_objs as go # the library is used to plot the graph

import sqlite3 # imports the library sqlite3 for communicating with the database

def stock_forecast(): # for the sake of modularity, all forecasing function is under one function

    START = "2015-01-01" # start date is set as most stocks started thereabouts
    TODAY = date.today().strftime("%Y-%m-%d") # end date is today's date

    st.title('Stock Market Prediction App') # clear title

    stocks = ('AAPL','NKE') # stocks / crypto that can be selected
    selected_stock = st.selectbox('Select dataset for predicition',stocks) # drop-down menu
    n_years = st.slider('Years of prediction:', 1,5) # slider for numbers of years to predicit
    period = n_years * 365 # sets the number of days in a year
    
    def load_data(ticker): # function to load the data
        data = yf.download(ticker, START, TODAY) # downloads/caches the prices
        data.reset_index(inplace=True)
        return data # returns the data
        
    data_load_state = st.text('Loading data...') # informs user the data is being loaded
    data = load_data(selected_stock) # loads the data
    data_load_state.text('Loading data... done!') # informs user the data is loaded

    st.subheader('Raw data') # clear sub-title
    st.write(data.tail()) # displays the last few records / prices
    
    # Plot raw data
    def plot_raw_data(): # function to plot the data
        fig = go.Figure() # sets the area for the graph
        # plots the open and close prices of the stock / crypto
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        # gives functionality to the zoom function
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig, use_container_width=True) # plots with auto adjusting to the width
    
    plot_raw_data() # calls the function to plot the graph

    # Predict forecast with Prophet.
    df_train = data[['Date','Close']] # gets the data for closed price and date respectively
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet() # calls the forecasting library
    m.fit(df_train) # trains the algorithm with previous data
    future = m.make_future_dataframe(periods=period) # forecasting the data
    forecast = m.predict(future) # forecasting using the data

    # Show and plot forecast
    st.subheader('Forecast data') # clear sub-title
    st.write(forecast.tail()) # displays last few records / prices
        
    st.write(f'Forecast plot for {n_years} years') # clear sub-title
    fig1 = plot_plotly(m, forecast) # plots the forecasted data
    st.plotly_chart(fig1, use_container_width=True) # plots with auto adjusting to the width

    st.write("Forecast components") # clear sub-title
    fig2 = m.plot_components(forecast) # plots the trends and patterns to fig2
    st.write(fig2)

# Security
import hashlib # imports the library hashlib to hash the passwords for added security

def make_hashes(password): # function to hash passwords from new user pages
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text): # function to check whether the hashed passwords match with the database
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management

conn = sqlite3.connect('data.db') # establishes a connection with the correct database
c = conn.cursor() # allows changes to be directed through the web app and its interactive features

# DB Functions
def create_usertable(): # function creates a table for database if it doesn't exist
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT NOT NULL UNIQUE,password TEXT NOT NULL UNIQUE, name TEXT NOT NULL UNIQUE)')


def add_userdata(username,password,name): # function to add new user details to database
    users = view_all_users() # gets the list of the users
    for i in range(0,len(users)): # searches through the list of users
        if username == " " or password == " " or name == " " or len(username) == 0 or len(password) == 0 or len(name) == 0: # validation
            st.warning("Not a valid input") # displays error message
        elif username == users[i][0]: # if the user already exists then do the following
            st.warning("User already exists") # displays an error to the user
        else:
            c.execute('INSERT INTO userstable(username,password,name) VALUES (?,?,?)',(username,password,make_hashes(name))) # add the user to the table if requirements are met
            st.success("You have successfully created a valid Account") # message to inform new account created successfully
            st.info("Go to Login Menu to login") # instruction to where to go next
    
    conn.commit() # executes the instructions above through connection with database

def login_user(username,password): # function to login the user to their respective account
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

def view_all_users(): # function used to get all records in the database
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def analytics(): # function to display analysis section
    
    START = "2015-01-01" # start data is set
    TODAY = date.today().strftime("%Y-%m-%d") # today's date is set

    stocks = ('GOOG', 'AAPL', 'MSFT', 'GME', 'BTC-GBP', '^FTSE', '^FTMC', 'WMT') # stock / crypto to choose
    selected_stock1 = st.selectbox('Select dataset 1', stocks) # first stock / crypto is chosen
    selected_stock2 = st.selectbox('Select dataset 2', stocks) # second stock / crypto is chosen

    def load_data(ticker): # function to load the data
        data = yf.download(ticker, START, TODAY) # downloads/caches the prices
        data.reset_index(inplace=True)
        return data # returns the data
    
    data_load_state = st.text('Loading data...') # informs user the data is being loaded
    data1 = load_data(selected_stock1) # data for first stock / crypto is loaded
    data2 = load_data(selected_stock2) # data for second stock / crypto is loaded
    data_load_state.text('Loading data... done!') # informs user the data is loaded

    # Plot raw data
    def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data1['Date'], y=data1['Open'], name=selected_stock1))
            fig.add_trace(go.Scatter(x=data2['Date'], y=data2['Open'], name=selected_stock2))
            fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig, use_container_width=True)
            
    plot_raw_data()

def main():

    st.set_page_config(layout="wide") # automatically adjusts to the width of the screen
    st.title("STOCK FORECASTING") # sub-title given to the page when selected from drop-down menu

    menu = ["Home","Login","Sign Up"] # options that will be available in drop-down menu
    choice = st.sidebar.selectbox("Menu", menu) # drop-down menu in the sidebar
    
    if choice == "Home": # if 'Home' is selected from the drop-down menu, do the following
        st.subheader("Home") # sub-title to let user know what page they are on
        st.markdown("**♟ Welcome ♟**") # greeting user and small intro below
        st.markdown("The role of the stock market is to provide a venue for investors to buy and"
                            " sell individual company shares, funds or other financial products. The stock"
                            "market enables those interactions using the mechanism of price discovery based"
                            " on fundamental and technical analysis. Changes in share prices allow investors"
                            " to buy or sell financial products they are interested in owning.")
        st.image("stock_image.jpeg") # displays image which is pre-downloaded
    
    elif  choice == "Login": # if 'Login' is selected from the drop-down menu, do the following
        st.subheader("Login") # sub-title to let user know what page they are on
        
        username = st.sidebar.text_input("Username") # username is entered here
        password = st.sidebar.text_input("Password",type='password') # password is entered here
        
        if st.sidebar.checkbox("Login"): # if the login button is pressed
            create_usertable() # calls the module to create a table
            hashed_pswd = make_hashes(password) # hashes the password

            result = login_user(username,check_hashes(password,hashed_pswd)) # gets all inputs under one variable name
            if result: # if login details match, then do the following
                users = view_all_users()
                for i in range(0,len(users)):
                    if users[i][0] == username:
                        st.success("Logged In as {}".format(users[i][2])) # displays personalised message to inform they have successfully logged in
                task = st.selectbox("Task",["Stock Prediction App","Analytics","Profiles"]) # the tasks drop-down menu displays after logging in
                if task == "Stock Prediction App": # if 'Stock Predicition App' is selected, do the following
                    stock_forecast() # run the module to display the stock forecasting app

                elif task == "Analytics": # if 'Analytics' is chosen, do the follwoing
                    st.subheader("Analytics") # clear sub-title
                    analytics()
                    
                elif task == "Profiles": # if 'Profiles' is chosen, do the follwoing
                    st.subheader("User Profiles") # clear sub-title
                    user_result = view_all_users() # get all the users' username, hashed passwords and names
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password","Name"]) # creating table
                    st.dataframe(clean_db) # inserting the details into the table
            else:
                st.warning("Incorrect Username/Password") # if username and password don't match/exist, an error message is displayed

    elif choice == "Sign Up": # if 'Sign Up' is selected from the drop-down menu
        st.subheader("Create New Account") # cler sub-title
        name = st.text_input("Name") # input area from username
        new_user = st.text_input("Username") # input area for username
        new_password = st.text_input("Password",type='password') # input area for password
        
        if st.button("Sign Up"): # if the button is pressed then do the following
                        create_usertable() # create a user table module is run
                        add_userdata(new_user,new_password,name) # adding a new user to the table is run

main() # running the program
