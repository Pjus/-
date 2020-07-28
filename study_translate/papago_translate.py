import os
import re
import sys
import urllib.request

client_id = "iX96MmkGE4zhbfqIY9AA" # 개발자센터에서 발급받은 Client ID 값
client_secret = "SVvzzojrL5" # 개발자센터에서 발급받은 Client Secret 값
encText = urllib.parse.quote("Nice to meet you")
data = "source=en&target=ko&text=" + encText
url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    # print(response_body.decode('utf-8'))
    text = response_body.decode('utf-8').split(',')
    # print(text[5])
    target = text[5]
    print(target)
    print(re.compile('[가-힣]+').findall(str(target)))
else:
    print("Error Code:" + rescode)