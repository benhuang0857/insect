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

Browser = webdriver.Chrome('./chromedriver')
LoginUrl= ('http://ez.homebook.tw/index.php')
UserName= ('Ok111')
UserPass= ('0857')

Browser.get(LoginUrl) #打開

#等到DOM生成
linkID = None
linkPS = None
linkSendJoin = None

while not (linkID and linkPS and linkSendJoin):
    try:
        linkID = WebDriverWait(Browser, 5, 0.5).until(
            EC.presence_of_element_located((By.ID, 'id'))
        )
        linkPS = WebDriverWait(Browser, 5, 0.5).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        linkSendJoin = WebDriverWait(Browser, 5, 0.5).until(
            EC.presence_of_element_located((By.ID, 'SendJoin'))
        )
    except Exception as e:
        print("問題為：找不到元素卡在登陸", format(e))
        Browser.refresh()

#登入
Browser.find_element_by_id('id').send_keys(UserName)
Browser.find_element_by_id('password').send_keys(UserPass)
Browser.find_element_by_id('SendJoin').click()

#等到alert生成
alert = None

while not alert:
    try:
        alert = WebDriverWait(Browser, 5, 0.5).until(
            EC.alert_is_present()
        )
    except Exception as e:
        print("問題為：找不到Alert卡在登陸", format(e))
        Browser.refresh()

#點擊彈出視窗的確定按鈕
alert = Browser.switch_to.alert
sleep(1)
alert.accept()
sleep(1)

#跳至網頁表單，準配開始抓取
url = '?htm=EzList'

xpath = None

while not xpath:
    try:
        xpath = WebDriverWait(Browser, 5, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="'+url+'"]'))
        )
    except Exception as e:
        print("問題為：登入後找不到指定元素", format(e))
        Browser.refresh()

Browser.find_element_by_xpath('//a[@href="'+url+'"]').click()

sl = Select(Browser.find_element_by_name('e_space'))
sl.select_by_value("C") #北北基

Browser.find_element_by_id('Btn_scan').click()
sleep(1)

phoneTmp = ""

while True:
    tab_cars = None
    td = None
    while not (tab_cars and td):
        try:
            tab_cars = WebDriverWait(Browser, 5, 0.5).until(
                EC.presence_of_element_located((By.ID, 'tab_cars'))
            )
            td = WebDriverWait(Browser, 5, 0.5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'td'))
            )
        except Exception as e:
            print("問題為：找不到元素無法抓取", format(e))
            Browser.refresh()
    
    table = Browser.find_element_by_id('tab_cars')
    tdlist = table.find_elements_by_tag_name('td')
    lst = []
    for td in tdlist[2:8]:
        lst.append(td.text)
    print(lst)
    
    #header#
    myHeader = {
         'Content-type': 'application/json',
         'X-Requested-With': 'XMLHttpRequest',
         'Accept-Encoding': 'gzip, deflate, br',
         'Connection': 'keep-alive',
         'Accept': '*/*',
         'APP_KEY' : '123',
    }
    
    if lst[0] != phoneTmp:
        print("POP")
        data = {
            'phone': lst[0],
            'line' : lst[1],
            'name' : lst[2],
            'reason' : lst[3],
            'location' : lst[4],
            'amount' : lst[5],
            'contact_time' : '任何時間皆可',
            
        }
        response = requests.post('https://lkb-bank.com/api/application/submit', headers=myHeader, data=json.dumps(data))
        print("Status code: ", response.status_code)
        phoneTmp = lst[0]
    else:
        print("NOPOP")
    sleep(200)
    Browser.refresh()