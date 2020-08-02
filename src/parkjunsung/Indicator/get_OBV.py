import pandas as pd

def faster_OBV(data):
    close, volume = data['Close'], data['Volume']
    # obv 값이 저장될 리스트를 생성합니다.
    obv_value = [None] * len(close)
    obv_value[0] = volume.iloc[0]
    # 마지막에 사용할 인덱스를 저장해 둡니다.
    index = close.index

    # 연산에서 사용하기 위해 리스트 형태로 바꾸어 줍니다.
    close = list(close)
    volume = list(volume)
    
    # OBV 산출공식을 구현
    for i in range(1,len(close)):
    
        if close[i] > close[i-1] : 
            obv_value[i] = obv_value[i-1] + volume[i]
            
        elif close[i] < close[i-1] :
            obv_value[i] = obv_value[i-1] - volume[i]
            
        else:
            obv_value[i] = obv_value[i-1]
            
    # 계산된 리스트 결과물을 마지막에 Series 구조로 변환해 줍니다.
    obv = pd.Series(obv_value, index=index)
    data['OBV'] = obv
    return data