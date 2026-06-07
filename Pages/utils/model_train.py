from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score,mean_squared_error
from datetime import datetime,timedelta

import tensorflow
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,LSTM,Dropout

def get_data(ticker):
    stock_price = yf.download(ticker , start  = '2017-01-09')
    return stock_price[['Close']]

def stationary_check(close_price):
    adf_test = adfuller(close_price)
    p_value = round(adf_test[1],3)
    return p_value

def get_rolling_mean(close_price):
    rolling_price = close_price.rolling(window = 7).mean().dropna()
    return rolling_price

def differencing_order(close_price):
    p_value = stationary_check(close_price)
    d=0
    while True:
        if(p_value>0.05):
            d+=1
            close_price = close_price.diff().dropna()
            p_value = stationary_check(close_price)
            
        else:
            break
    return d

def fit_model(data,differencing_order,days):
    model = ARIMA(data,order=(2,differencing_order,2))
    model_fit = model.fit()
    forcast_value = days
    forecast = model_fit.get_forecast(steps = forcast_value)
    predictions = forecast.predicted_mean
    return predictions

def evaluate_model(orginal_price,differencing_order,days):
    train , test = orginal_price[:-days],orginal_price[-days:]
    predictions = fit_model(train,differencing_order,days)
    rmse = np.sqrt(mean_squared_error(test ,predictions))
    return round(rmse,2)

def scaling(close_price):
    scaler = StandardScaler()
    scaled_data  = scaler.fit_transform(np.array(close_price).reshape(-1,1))
    return scaler,scaled_data




from datetime import datetime, timedelta
import pandas as pd



def get_forecast(original_price, differencing_order,days):
    predictions = fit_model(original_price, differencing_order,days)

    # Wrap the addition in parentheses
    start_date = datetime.today().strftime("%Y-%m-%d")
    end_date = (datetime.today() + timedelta(days=days-1)).strftime("%Y-%m-%d")

    forecast_index = pd.date_range(start=start_date, end=end_date, freq="D")
    forecast_df = pd.DataFrame(
        predictions, index=forecast_index, columns=["close"]
    )

    return forecast_df

def inverse_scaling(scaler,scaled_data):
    close_price = scaler.inverse_transform(np.array(scaled_data).reshape(-1,1))
    return close_price


## SPECIFIC LSTM VERSIONS FUNCTION

#get data
#stationary check
#rolling mean
#differencing order
#fit model
#evaluate model
#scaling
#get forcast


def create_sequence(data,window_size):
    X= []
    y = []

    for i in range(window_size,len(data)):
        X.append(data[i-window_size:i])
        y.append(data[i])
    return np.array(X) , np.array(y)


def LSTM_func(X,y):
    split = int(len(X)*0.8)
    X_train ,y_train = X[:split],y[:split]
    X_test ,y_test = X[split:],y[split:]

    model = Sequential([
    LSTM(50,return_sequences=True,input_shape = (X_train.shape[1], 1)),

    LSTM(50,return_sequences=True),
    LSTM(50,return_sequences=False),
    Dense(1),
])
    model.compile(loss = 'mean_squared_error',optimizer='adam',)
    model.compile(loss = 'mean_squared_error',optimizer='adam')

    history =model.fit(X_train,y_train,epochs=20,validation_data=(X_test,y_test),batch_size=32,verbose=1)

    return model , X_test , y_test

def LSTM_model_evaluation(model,X_test,y_test,scaler):
    predictions = model.predict(X_test)

    rmse1 = np.sqrt(mean_squared_error(y_test ,predictions))

    y_pred = scaler.inverse_transform(predictions)

    y_actual = scaler.inverse_transform(y_test)

    rmse = np.sqrt(mean_squared_error(y_actual ,y_pred))

    return rmse,rmse1

def LSTM_30_day_forecast(model,scaler,scaled_data,window_size,close_price,days):
    last_window = scaled_data[-window_size:]
    future_prediction = []
    current_window = last_window.copy()

    for _ in range(days):
        current_window_reshaped = current_window.reshape(1,window_size,1)
        next_price = model.predict(current_window_reshaped,verbose=1)
        future_prediction.append(next_price[0,0])

        current_window = np.vstack([current_window[1:],next_price])

    future_value = scaler.inverse_transform(np.array(future_prediction).reshape(-1,1))

    future_dates = pd.date_range(
        start=close_price.index[-1] + pd.Timedelta(days=1),
        periods=days,
        freq='B'
    )

    forecast_df = pd.DataFrame(future_value.round(2),index=future_dates,columns  =['close'])

    return forecast_df



