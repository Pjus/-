"""
Gerald Appel에 의해 1970대 말 고안 됨

MACD = EMA(numFast) - EMA(numSlow)

EMA(Exponential Moving Average ; 지수이동평균)

numFast: 기간

numSlow: 기간

numSignal: 기간

MACD(numFast, numSlow, numSignal)

numFast, numSlow 기간으로 MACD값을 산출하고 이를 c기간의 EMA를 시그널 선으로 활용합니다.

일반적으로 MACD(12, 26, 9)가 많이 사용됩니다.
"""

def fnMACD(m_Df, m_NumFast=12, m_NumSlow=26, m_NumSignal=9):
    m_Df['EMAFast'] = m_Df['Close'].rolling(window=m_NumFast).mean()
    m_Df['EMASlow'] = m_Df['Close'].rolling(window=m_NumSlow).mean()
    m_Df['MACD'] = m_Df['EMAFast'] - m_Df['EMASlow']
    m_Df['MACDSignal'] = m_Df['MACD'].rolling(window=m_NumSignal).mean()
    m_Df['MACDDiff'] = m_Df['MACD'] - m_Df['MACDSignal']
    return m_Df