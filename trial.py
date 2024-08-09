import streamlit as st # imports the library streamlit which allows to display the web app
import pandas as pd # imports the library pandas to allow for graphs to be drawn
import webbrowser # imports the library webbrowser to allow web-based documents to be displayed

# Security
import hashlib # imports the library hashlib to hash the passwords for added security

def make_hashes(password): # function to hash passwords from new user pages
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text): # function to check whether the hashed passwords match with the database
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
import sqlite3 # imports the library sqlite3 for communicating with the database

conn = sqlite3.connect('data.db') # establishes a connection with the correct database
c = conn.cursor() # allows changes to be directed through the web app and its interactive features

# DB Functions
def create_usertable(): # function creates a table for database if it doesn't exist
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT NOT NULL UNIQUE,password TEXT NOT NULL UNIQUE, name TEXT NOT NULL UNIQUE)')


def add_userdata(username,password,name): # function to add new user details to database
	c.execute('INSERT OR IGNORE INTO userstable(username,password,name) VALUES (?,?,?)',(username,password,name))
	conn.commit()

def login_user(username,password): # function to login the user to their respective account
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users(): # function used to get all records in the database
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


def main():

	st.title("STOCK FORECASTING") # sub-title given to the page when selected from drop-down menu

	menu = ["Home","Login","Sign Up"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		st.markdown("**♟ Welcome ♟**")
		st.markdown("The role of the stock market is to provide a venue for investors to buy and"
                            " sell individual company shares, funds or other financial products. The stock"
                            "market enables those interactions using the mechanism of price discovery based"
                            " on fundamental and technical analysis. Changes in share prices allow investors"
                            " to buy or sell financial products they are interested in owning.")
		st.image("stock_image.jpeg")
                
	elif choice == "Login":
		st.subheader("Login Section")
                
		username = st.sidebar.text_input("Username")
		password = st.sidebar.text_input("Password",type='password')

		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Stock Prediction App","Analytics","Profiles"])
				if task == "Stock Prediction App":
					stock_forecast()

				elif task == "Analytics":
					st.subheader("Analytics")
					analytics()

				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password","Name"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")

	elif choice == "Sign Up":
		st.subheader("Create New Account")
		name = st.text_input("Name")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
		
		if st.button("Sign Up"):
                        create_usertable()
                        add_userdata(new_user,make_hashes(new_password),name)

                        st.success("You have successfully created a valid Account")
                        st.info("Go to Login Menu to login")
                        
def stock_forecast():

    import streamlit as st
    from datetime import date

    import yfinance as yf
    from fbprophet import Prophet
    from fbprophet.plot import plot_plotly
    from plotly import graph_objs as go

    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    st.title('Stock Market Prediction App')

    st.image('Stock.jpg')

    stocks = ('AAPL','GOOG', 'MSFT', 'GME', 'BTC-GBP', '^FTSE', '^FTMC', 'WMT')
    selected_stock = st.selectbox('Select dataset for prediction', stocks)

    n_years = st.slider('Years of prediction:', 1, 5)
    period = n_years * 365

    def load_data(ticker):
            data = yf.download(ticker, START, TODAY)
            data.reset_index(inplace=True)
            return data
            
    data_load_state = st.text('Loading data...')
    data = load_data(selected_stock)
    data_load_state.text('Loading data... done!')

    st.subheader('Raw data')
    st.write(data.tail())

    # Plot raw data
    def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
            fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig, use_container_width=True)
            
    plot_raw_data()

    # Predict forecast with Prophet.
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())
        
    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1, use_container_width=True)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)

def analytics():

    import streamlit as st
    from datetime import date

    import yfinance as yf
    from fbprophet import Prophet
    from fbprophet.plot import plot_plotly
    from plotly import graph_objs as go

    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    stocks = ('GOOG', 'AAPL', 'MSFT', 'GME', 'BTC-GBP', '^FTSE', '^FTMC', 'WMT')
    selected_stock1 = st.selectbox('Select dataset 1', stocks)
    selected_stock2 = st.selectbox('Select dataset 2', stocks)

    def load_data(ticker):
            data = yf.download(ticker, START, TODAY)
            data.reset_index(inplace=True)
            return data
            
    data_load_state = st.text('Loading data...')
    data1 = load_data(selected_stock1)
    data2 = load_data(selected_stock2)
    data_load_state.text('Loading data... done!')

    # Plot raw data
    def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data1['Date'], y=data1['Open'], name=selected_stock1))
            fig.add_trace(go.Scatter(x=data2['Date'], y=data2['Open'], name=selected_stock2))
            fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig, use_container_width=True)
            
    plot_raw_data()


if __name__ == '__main__':
    main()
