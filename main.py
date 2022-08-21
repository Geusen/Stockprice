import time
import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#--------------------------------------------------------------------------------------------------------------------------------------
# 準備
webhook_url = os.environ.get("WEBHOOK")
d = {'任天堂':{'yahoo':'7974.T', 'google':'7974:TYO', 'currency':'円'}, 'SONY':{'yahoo':'6758.T', 'google':'6758:TYO', 'currency':'円'}}
with open('main.json', mode='r') as f:
    l = json.load(l)

def format(cl):
  rs = soup.find(class_=cl)
  rs = [i.strip() for i in rs.text.splitlines()]
  rs = [i for i in rs if i != ""]
  return rs[0]
#--------------------------------------------------------------------------------------------------------------------------------------
# 辞書の長さ分繰り返す
for x, y in l.items():
  if y['currency'] == '円':
    # 株価取得
    url = "https://finance.yahoo.co.jp/quote/" + y['yahoo']
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    today = format('_3rXWJKZF')
    ratio = format('_1-yujUee Y_utZE_b')
  
#--------------------------------------------------------------------------------------------------------------------------------------
  # Chromeヘッドレスモード起動
  options = webdriver.ChromeOptions()
  options.headless = True
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome('chromedriver',options=options)
  driver.implicitly_wait(10)

  # サイトURL取得,ウインドウ幅・高さ指定
  driver.get("https://www.google.com/finance/quote/" + y['google'] + "?hl=ja&gl=JP&window=1M")
  WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
  driver.set_window_size(800, 600)

  # 処理後一時待機,スクリーンショット格納,ブラウザ稼働終了
  time.sleep(2)
  driver.save_screenshot('before.png')
  time.sleep(1)
  driver.quit()
  
  # 画像トリミング
  im = Image.open('before.png')
  im.crop((0, 115, 770, 550)).save('image.png', quality=95)

#--------------------------------------------------------------------------------------------------------------------------------------
  text = '今日の' + x + 'の株価は' + str(today) + y['currency'] + 'で、前日比は' + str(ratio) + 'でした。'
  content = {'content': text}
  headers = {'Content-Type': 'application/json'}
  with open('image.png', 'rb') as f:
      file_bin = f.read()
  image = {'upload' : ('image.png', file_bin)}
  response = requests.post(webhook_url, json.dumps(content), headers=headers)
  response = requests.post(webhook_url, files = image)
