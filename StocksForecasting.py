# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 22:13:33 2023

@author: POURNIMA
"""

import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
import yfinance as yf
import pickle
import talib

model=pickle.load(open(r'C:/Users/POURNIMA/Project 2/Deployment/Sarimax.pkl','rb'))

start_date = datetime(2015,1,1)
end_date = datetime.today()

#Project title
st.markdown(f'<h1 style="color: SkyBlue; font-family:Georgia, serif; font-weight: 800; font-size:50px;">{"Reliance Stock Forecasting"}</h1>', unsafe_allow_html=True)

#Import the data
data = yf.download('RELIANCE.NS',start=start_date,end=end_date)



#Button to show the data
if st.button("Prices & Volumes"):
    st.write(data)
if st.button ("Close"):
    st.write("")

    
    
option = st.selectbox('What are you looking for?',('Market Trends', 'Prediction'))


def Page1(Trends): 
    st.markdown(f'<h1 style="color: SkyBlue; font-family:Georgia, serif; font-weight: 800; font-size:40px;">{"Advanced Charts"}</h1>', unsafe_allow_html=True)
    #Tabs to show different graphs
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Line chart","Candlestick Chart","Moving Averages","RSI","Bollinger Bands"])
    
    
    with tab1:
        st.markdown(f'<h1 style="color: White; font-family:Georgia, serif; font-weight: 800; font-size:20px;">{"Price variation over the years"}</h1>', unsafe_allow_html=True)
        fig_line=px.line(data["Close"])
        st.plotly_chart(fig_line, use_container_width=False)
    
    
    with tab2:    
        st.markdown(f'<h1 style="color: White; font-family:Georgia, serif; font-weight: 800; font-size:20px;">{"Candlestick Chart"}</h1>', unsafe_allow_html=True)
        #candel-stick Chart
        import plotly.graph_objs as plot
        #declare figure
        fig = plot.Figure()
        plt.figure(figsize=(15,10))
        #Candlestick
        fig.add_trace(plot.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'], name = 'market data'))
        # Add titles
        fig.update_layout(yaxis_title='Stock Price (Indian Rupees per Shares)')
        # X-Axes
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(step="all")
                ])
            )
        )
        st.plotly_chart(fig,theme=None, use_container_width=False)
        
    with tab3:
        st.markdown(f'<h1 style="color: White; font-family:Georgia, serif; font-weight: 800; font-size:20px;">{"Moving Averages"}</h1>', unsafe_allow_html=True)
        data['SMA100'] = talib.SMA(data['Close'], timeperiod=100)
        data['EMA100'] = talib.EMA(data['Close'], timeperiod=100)
        fig_MA = plt.figure(figsize=(10,8))
        plt.plot(data['Close'], color='lightblue', label='Daily Close Price')
        plt.plot(data['SMA100'], color='green', label='SMA 100')
        plt.plot(data['EMA100'], color='red', label='EMA 100')
        plt.legend()
        st.plotly_chart(fig_MA,theme=None,use_container_width=False)
        

#Relative Strength Index
    with tab4:
        st.markdown(f'<h1 style="color: White; font-family:Georgia, serif; font-weight: 800; font-size:20px;">{"Relative Strength Index"}</h1>', unsafe_allow_html=True)
        data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
        fig_RSI, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(10,8))
        ax1.set_ylabel('Price')
        ax1.plot(data['Close'],color = 'lightblue')
        ax2.set_ylabel('RSI')
        ax2.plot(data['RSI'], color='green')
        ax2.axhline(y = 70, color = 'r', linestyle = '-')
        ax2.axhline(y = 30, color = 'r', linestyle = '-')
        ax1.set_title('Daily Close Price and RSI')
        st.pyplot(fig_RSI)
        
        
    with tab5:
        st.markdown(f'<h1 style="color: White; font-family:Georgia, serif; font-weight: 800; font-size:30px;">{"Bollinger Bands"}</h1>', unsafe_allow_html=True)
        upper, mid, lower = talib.BBANDS(data['Close'], nbdevup=2, nbdevdn=2, timeperiod=20)
        fig_BB = plt.figure(figsize=(10,8))
        plt.plot(upper, label="Upper band")
        plt.plot(mid, label='Middle band')
        plt.plot(lower, label='Lower band')
        plt.title('Bollinger Bands')
        plt.legend()
        st.plotly_chart(fig_BB,theme=None, use_container_width=False)
              
#Fit the model on the dataset

from pandas.tseries.offsets import DateOffset
future_dates=[data.index[-1]+ DateOffset(days=x)for x in range(0,21)]
future_datest_df=pd.DataFrame(index=future_dates[1:],columns=data.columns)
future_df=pd.concat([data['Close'],future_datest_df])
future_df['forecast'] = model.predict(start = 1620, end = 1985, typ='levels') 

data.index = data.index.tz_localize(None)



#Predictions
def Page2(Predictions):
    
    predictions=model.predict(start=1988,end=2018,typ='levels')
    predictions
    
    from datetime import timedelta, date
    Date_req = date.today() + timedelta(days=31)
    
    index_future_dates=pd.date_range(start=datetime.today(),end=Date_req)
    predictions.index=index_future_dates
    print(predictions)
    new_pred = pd.concat([data['Close'],predictions], axis=1)
    d = new_pred.index
    new_pred.index = d.strftime('%Y-%m-%d')
    fig_pred=plt.figure(figsize=(10,8))
    plt.plot(new_pred)
    plt.plot(new_pred[1958:2018])
    st.plotly_chart(fig_pred,theme=None, use_container_width=False)




if option == 'Market Trends':
    Page1(data['Close']) 
elif option == 'Prediction':
    Page2(future_df['forecast']) 





















  