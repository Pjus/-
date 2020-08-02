#전처리
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
#머신러닝
import tensorflow as tf
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow.keras.backend as k 
from tensorflow.keras.callbacks import EarlyStopping
#데이터 
import pandas_datareader as pdr
df= pdr.get_data_yahoo('AAPL', '2000-01-01')

def predstock(col):
    tempdf = df[col]
    # log scaler 
    logdf = np.log(df[col]) 
    #MinMaxScaler
    global scaler_high
    global scaler_low
    global scaler_open
    global scaler_close
    if col == 'High':
        scaler_high = MinMaxScaler() 
        sc_logdf = pd.DataFrame(scaler_high.fit_transform(np.array(logdf).reshape(-1,1)), index= logdf.index, columns=[col]) 
    elif col =='Low':
        scaler_low = MinMaxScaler() 
        sc_logdf = pd.DataFrame(scaler_low.fit_transform(np.array(logdf).reshape(-1,1)), index= logdf.index, columns=[col]) 
    elif col =='Open':
        scaler_open = MinMaxScaler() 
        sc_logdf = pd.DataFrame(scaler_open.fit_transform(np.array(logdf).reshape(-1,1)), index= logdf.index, columns=[col]) 
    elif col =='Close':
        scaler_close = MinMaxScaler() 
        sc_logdf = pd.DataFrame(scaler_close.fit_transform(np.array(logdf).reshape(-1,1)), index= logdf.index, columns=[col]) 

    # Time shift
    for s in range(1,6):
        sc_logdf['shift_{}'.format(s)] = sc_logdf[col].shift(s)
    #split train/test set_ 200개씩 분리
    x_train = sc_logdf.dropna().drop(col, axis =1).iloc[:-200] 
    y_train = sc_logdf.dropna()[col].iloc[:-200]
    x_test = sc_logdf.dropna().drop(col, axis =1).iloc[-200:]
    y_test = sc_logdf.dropna()[col].iloc[:-200]

    x_train = x_train.values
    y_train = y_train.values
    x_test = x_test.values
    y_test = y_test.values

    x_train_t = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
    x_test_t = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)


    #머신러닝 모델 만들기_ col 마다 별도 모델 생성 후 저장
    global model_high
    global model_low
    global model_open
    global model_close
    if col == 'High':
        model_high = tf.keras.models.Sequential()
        model_high.add(LSTM(20, input_shape=(x_train.shape[1],1)))
        model_high.add(Dense(1))
        model_high.compile(loss='mean_squared_error', optimizer='adam')
        model_high.fit(x_train_t, y_train, epochs = 2000, batch_size = 2, verbose=1)
        pred = model_high.predict(np.array(x_test_t).reshape(x_test_t.shape[0],x_test_t.shape[1],1))
        pred = np.exp(scaler_high.inverse_transform(pred))
        result = pd.DataFrame(df[col].iloc[-200:])
        result['Pred'] = pred

    elif col == 'Low':
        model_low = tf.keras.models.Sequential()
        model_low.add(LSTM(20, input_shape=(x_train.shape[1],1)))
        model_low.add(Dense(1))
        model_low.compile(loss='mean_squared_error', optimizer='adam')
        model_low.fit(x_train_t, y_train, epochs = 2000, batch_size = 2, verbose=1)
        pred = model_low.predict(np.array(x_test_t).reshape(x_test_t.shape[0],x_test_t.shape[1],1))
        pred = np.exp(scaler_low.inverse_transform(pred))
        result = pd.DataFrame(df[col].iloc[-200:])
        result['Pred'] = pred

    elif col == 'Open':
        model_open = tf.keras.models.Sequential()
        model_open.add(LSTM(20, input_shape=(x_train.shape[1],1)))
        model_open.add(Dense(1))
        model_open.compile(loss='mean_squared_error', optimizer='adam')
        model_open.fit(x_train_t, y_train, epochs = 2000, batch_size = 2, verbose=1)
        pred = model_open.predict(np.array(x_test_t).reshape(x_test_t.shape[0],x_test_t.shape[1],1))
        pred = np.exp(scaler_open.inverse_transform(pred))
        result = pd.DataFrame(df[col].iloc[-200:])
        result['Pred'] = pred

    elif col == 'Close':
        model_close = tf.keras.models.Sequential()
        model_close.add(LSTM(20, input_shape=(x_train.shape[1],1)))
        model_close.add(Dense(1))
        model_close.compile(loss='mean_squared_error', optimizer='adam')
        model_close.fit(x_train_t, y_train, epochs = 10, batch_size = 2, verbose=1)
        pred = model_close.predict(np.array(x_test_t).reshape(x_test_t.shape[0],x_test_t.shape[1],1))
        pred = np.exp(scaler_close.inverse_transform(pred))
        result = pd.DataFrame(df[col].iloc[-200:])
        result['Pred'] = pred

    return result