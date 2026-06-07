import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import plotly.graph_objects as go 
from Pages.utils.plotly_figure import plotly_table,candlestick,close_chart,RSI,MACD,moving_average

st.set_page_config(
    page_title='Stock Analysis',
    page_icon='A',
    layout='wide'
)
st.title('Stock Analysis')

col1 , col2 , col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input('Show Ticker','AAPL')

with col2:
    start_date = st.date_input("Choose Start Date",datetime.date(today.year-1,today.month,today.day))

with col3:
    end_date = st.date_input("Choose End Date",datetime.date(today.year,today.month,today.day))


st.subheader(ticker)

stocks = yf.Ticker(ticker)
st.write(stocks.info['longBusinessSummary'])
st.write('**Sector:**',stocks.info['sector'])
st.write('**Employees:**',stocks.info['fullTimeEmployees'])
st.write('**Website**:',stocks.info['website'])


col1,col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=['MarketCap','Beta','EPS','PE Ratio'])
    df[''] = [stocks.info.get('marketCap'),stocks.info.get('beta'),stocks.info.get('trailingEps'),stocks.info.get('trailingPE')]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df,use_container_width=True)

with col2:
    df = pd.DataFrame(index=['Quick Ratio','Revenue per Share','Profit Margin','Debt to Equity','Return on Equity'])
    df[''] = [stocks.info.get('quickRatio'),stocks.info.get('revenuePerShare'),stocks.info.get('profitMargin'),stocks.info.get('debtToEquity'),stocks.info.get('returnOnEquity')]

    fig_df = plotly_table(df)
    st.plotly_chart(fig_df,use_container_width=True)

data = yf.download(ticker,start=start_date,end=end_date)

col1,col2,col3 = st.columns(3)

current_price = data['Close'].values[-1]
previous_price = data['Close'].values[-2]

daily_change = current_price-previous_price

col1.metric(
    label='Daily Change',
    value=(current_price),
    delta=(daily_change)
)

last_10_df = data.tail(10).sort_index(ascending=False).round(3)
last_10_df.columns = [col[0] for col in last_10_df.columns]

fig_df = plotly_table(last_10_df)


st.write('#### Historical Data(10 days data)')
st.plotly_chart(fig_df,use_container_width=True)
    
col1,col2,col3,col4,col5,col6,col7 = st.columns(7)

num_peroid = ''
with col1:
    if(st.button('5D')):
        num_peroid='5d'

with col2:
    if(st.button('1M')):
        num_peroid='1mo'

with col3:
    if(st.button('6M')):
        num_peroid='6mo'

with col4:
    if(st.button('YTD')):
        num_peroid='ytd'

with col5:
    if(st.button('1Y')):
        num_peroid='1y'

with col6:
    if(st.button('6Y')):
        num_peroid='6y'

with col7:
    if(st.button('MAX')):
        num_peroid='max'

col1,col2,col3  = st.columns([1,1,4])
with col1:
    chart_type = st.selectbox('',('Candle','Line'))

with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('',('RSI','MACD'))
    else:
        indicators =  st.selectbox('',('RSI','Moving Average','MACD'))

ticker = yf.Ticker(ticker)
new_df1 = ticker.history(period = 'max')
data1 = ticker.history(period = 'max')


if num_peroid == '':
    if(chart_type =='Candle' and indicators=='RSI'):
        st.plotly_chart(candlestick(data1,'1y'),use_container_width=True)
        st.plotly_chart(RSI(data1,'1y'),use_container_width=True)

    if(chart_type =='Candle' and indicators=='MACD'):
        st.plotly_chart(candlestick(data1,'1y'),use_container_width=True)
        st.plotly_chart(MACD(data1,'1y'),use_container_width=True)

    if(chart_type =='Line' and indicators=='RSI'):
        st.plotly_chart(close_chart(data1,'1y'),use_container_width=True)
        st.plotly_chart(RSI(data1,'1y'),use_container_width=True)

    if(chart_type =='Line' and indicators=='Moving Average'):
        # st.plotly_chart(close_chart(data1,'1y'),use_container_width=True)
        st.plotly_chart(moving_average(data1,'1y'),use_container_width=True)

    if(chart_type =='Line' and indicators=='MACD'):
        st.plotly_chart(close_chart(data1,'1y'),use_container_width=True)
        st.plotly_chart(MACD(data1,'1y'),use_container_width=True)

else:
    if(chart_type =='Candle' and indicators=='RSI'):
        st.plotly_chart(candlestick(new_df1,num_peroid),use_container_width=True)
        st.plotly_chart(RSI(new_df1,num_peroid),use_container_width=True)

    if(chart_type =='Candle' and indicators=='MACD'):
        st.plotly_chart(candlestick(new_df1,num_peroid),use_container_width=True)
        st.plotly_chart(MACD(new_df1,num_peroid),use_container_width=True)

    if(chart_type =='Line' and indicators=='RSI'):
        st.plotly_chart(close_chart(new_df1,num_peroid),use_container_width=True)
        st.plotly_chart(RSI(new_df1,num_peroid),use_container_width=True)

    if(chart_type =='Line' and indicators=='Moving Average'):
        # st.plotly_chart(close_chart(data1,'1y'),use_container_width=True)
        st.plotly_chart(moving_average(new_df1,num_peroid),use_container_width=True)

    if(chart_type =='Line' and indicators=='MACD'):
        st.plotly_chart(close_chart(new_df1,num_peroid),use_container_width=True)
        st.plotly_chart(MACD(new_df1,num_peroid),use_container_width=True)
