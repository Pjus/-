"""
중심선: n기간 동안의 이동평균(SMA)

상단선: 중심선 + Kσ(일반적으로 K는 2배를 많이 사용함)

하단선: 중심선 - Kσ(일반적으로 K는 2배를 많이 사용함)

"""
import pandas as pd

def fnBolingerBand(m_DF, n=20, k=2):
    m_DF['20d_ma'] = m_DF['Close'].rolling(window=n).mean()
    m_DF['Bol_upper'] = m_DF['Close'].rolling(window=n).mean() + k * m_DF['Close'].rolling(window=n).std()
    m_DF['Bol_lower'] = m_DF['Close'].rolling(window=n).mean() - k * m_DF['Close'].rolling(window=n).std()
    return m_DF