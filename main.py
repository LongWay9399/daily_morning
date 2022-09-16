from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
wedding_date = "2022-10-05"
marriage_date = "09-25"
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]

    return weather['weather'], math.floor(weather['temp']), weather["airQuality"]


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) +
                             "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_marriage():
    next = datetime.strptime(str(date.today().year) +
                             "-" + marriage_date, "%Y-%m-%d")
    if next > datetime.now():
        return "距离领证还有"+str((next-today).days)+"天"
    return "距离结婚纪念日还有"+str((next.replace(year=next.year + 1)-today).days)+"天"


def get_wedding():
    delta = datetime.strptime(wedding_date, "%Y-%m-%d")
    if delta < datetime.now():
        return ""
    return "距离举行婚礼还有"+str((delta - today).days)+"天"


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def get_today():
    Y = today.strftime('%Y-%m-%d')

    W = int(today.strftime('%w'))

    return "今天是"+Y+" "+"星期"+get_week_day(W)


def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }

    return week_day_dict[date]


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, airQuality = get_weather()
Y, M, D, W = today.strftime('%Y, %m %d %w')

data = {"weather": {"value": wea, "color": get_random_color()},
        "today": {"value": get_today(), "color": get_random_color()},
        "temperature": {"value": temperature, "color": get_random_color()},
        "airQuality": {"value": airQuality, "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "birthday_left": {"value": get_birthday(), "color": get_random_color()},
        "wedding_left": {"value": get_wedding(), "color": get_random_color()},
        "marriage_left": {"value": get_marriage(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
