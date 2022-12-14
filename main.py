from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id_ = "oU1cX6H0njPkQao84BPmbNF5kS90"
template_id = os.environ["TEMPLATE_ID"]
remainder = """\n
#############\n
11点健身\n
好好和我谈恋爱\n
等我回国娶你\n
#############"""
"""
药宗美人图
12.3成男
12.4成女
12.7正太
12.9萝莉
"""
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {\
        "weather":{"value":wea},\
        "temperature":{"value":temperature},\
        "love_days":{"value":get_count()},\
        "birthday_left":{"value":get_birthday()},\
        "words":{"value":get_words(),\
        "color":get_random_color()},\
        "remainder":{"value":remainder}\
       }
res = wm.send_template(user_id, template_id, data), wm.send_template(user_id_, template_id, data)
print(res)
