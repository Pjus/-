import numpy as np
import pandas as pd

# 30이하면 과매도, 70 이상이면 과매수
def fnRSI(df, m_N=7):
    delta = df['Close'].diff()

    dUp, dDown = delta.copy(), delta.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0

    RolUp = pd.DataFrame(dUp).rolling(window=14).mean()
    RolDown = pd.DataFrame(dDown).rolling(window=14).mean().abs()

    RS = RolUp / RolDown
    RSI = RS / (1+RS)
    RSI_MACD = pd.DataFrame(RSI).rolling(window=6).mean()
    df['RSI_MACD'] = RSI_MACD

    return df

if __name__ == "__main__":
    pass
