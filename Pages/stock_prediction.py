import streamlit as st
import pandas as pd
from Pages.utils.model_train import *
from Pages.utils.plotly_figure import plotly_table,moving_average_forecast,plotly_tab,dynamic_plotly_table
from Pages.utils.model_train import differencing_order



st.set_page_config(
    page_title='Stock prediction',
    page_icon='',
    layout='wide'
)

st.title('Stock Prediction page')
st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)

ticker = st.text_input('****Select the Ticker****','AAPL')

st.subheader(f"Select the followings for : {ticker}")

st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)

close_price = get_data(ticker)



col1,col2  = st.columns([1,1])

with col1:
    model_choice = st.selectbox(
        'Select Prediction Model',
        ['ARIMA (Statistical)', 'LSTM (Deep Learning)'])
    
with col2:
    days_select = st.selectbox(
        'Select number of days you want to predict',
        [1,3,7,15,30])


if st.button('Predict Future Prices'):
    st.subheader(f'Predicting next {days_select} days for {ticker}')
    if model_choice == 'ARIMA (Statistical)':
        rolling_price = get_rolling_mean(close_price)

        diffrencing_order = differencing_order(rolling_price)
        scaler , scaled_data = scaling(rolling_price)


        forecast = get_forecast(scaled_data,diffrencing_order,days_select)

        forecast['close'] = inverse_scaling(scaler,forecast['close'])



        fig_tail = dynamic_plotly_table(forecast.sort_index(ascending=True).round(3))
        fig_tail.update_layout(height =500)
        st.plotly_chart(fig_tail,use_container_width=True)

        rmse = evaluate_model(scaled_data,diffrencing_order,days_select)
        st.write("#### The RMSE score is : ",rmse)

        rolling_price.columns = rolling_price.columns.droplevel(0)


        rolling_price.columns = ['close']

        forecast = pd.concat([rolling_price,forecast])


        st.write(f'### Line chart for {days_select} days for {ticker}')

        st.plotly_chart(moving_average_forecast(forecast.iloc[150:],days_select),use_container_width=True)



    else:
        scaler,scaled_data = scaling(close_price)
        window_size = 30
        X,y = create_sequence(scaled_data,window_size)


        model,X_test,y_test = LSTM_func(X,y)


        forecast_df = LSTM_30_day_forecast(model,scaler,scaled_data,window_size,close_price,days_select)

        st.write('#### Next 30 day Prediction ')
        fig_tail = plotly_table(forecast_df.sort_index(ascending=True).round(3))
        fig_tail.update_layout(height =500)
        st.plotly_chart(fig_tail,use_container_width=True)

        rmse,rmse1 = LSTM_model_evaluation(model,X_test,y_test,scaler)

        # st.write('#### The RMSE score with scaling is: ',rmse)
        st.write('##### The RMSE score without scaling is: ',rmse1)

        close_price.columns = close_price.columns.droplevel(0)
        close_price.columns = ['close']

        forecast_df = pd.concat([close_price,forecast_df])

        st.plotly_chart(moving_average_forecast(forecast_df,days_select),use_container_width=True)























