import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def strawberry_data(re_data):

    final_data = []
    for data in re_data[0:24]:
        data = data / 10
        final_data.append(data)  # 濕度
    data1 = final_data[0:24]

    for data in re_data[24:48]:
        data = data / 10
        final_data.append(data)  # 溫度
    data2 = final_data[24:48]

    for data in re_data[48:51]:
        data = data * 100
        final_data.append(data)  # 日照度
    data3 = final_data[48:51]

    data = re_data[51]
    final_data.append(data)  # 電導率
    data4 = final_data[51]

    for data in re_data[52:54]:
        data = data / 10
        final_data.append(data)  # 酸鹼值
    data5 = final_data[52:54]

    data = re_data[54] / 10
    final_data.append(data)  # 環境溫度
    data6 = final_data[54]

    total_data = {'humidity': str(data1), 'temperature': str(data2), 'sunshine': str(data3), 'conductance': str(data4), 'acid': str(data5),
                  'environment': str(data6)}

    api_url = r'http://140.130.89.171/api/postBerry'
    re_data = requests.post(api_url, data=total_data)
    print('re_data status:', re_data.status_code)
    print('re_data reason:', re_data.reason)

    print('濕度:', final_data[0:24])
    print('溫度:', final_data[24:48])
    print('日照度:', final_data[48:51])
    print('電導率:', final_data[51])
    print('酸鹼:', final_data[52:54])
    print('環境溫度:', final_data[54])
    
strawberry_data([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,11,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

