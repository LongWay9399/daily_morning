from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
wedding_date = os.environ['WEDDING_DATE']
marriage_date = os.environ['MARRIAGE_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = ["oOQk26iVxG1MEznmGJ6Pj7IIJStI", "oOQk26nqcIpadV8XPKj5zRtL4t_w"]
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

    return "今天是"+Y+" "+get_week_day(W)


def get_week_day(date):
    week_day_dict = {
        1: '星期一',
        2: '星期二',
        3: '星期三',
        4: '星期四',
        5: '星期五',
        6: '星期六',
        0: '星期天',
    }

    return week_day_dict[date]


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, airQuality = get_weather()


data = {"weather": {"value": wea, "color": get_random_color()},
        "today": {"value": get_today(), "color": get_random_color()},
        "temperature": {"value": temperature, "color": get_random_color()},
        "airQuality": {"value": airQuality, "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "birthday_left": {"value": get_birthday(), "color": get_random_color()},
        "wedding_left": {"value": get_wedding(), "color": get_random_color()},
        "marriage_left": {"value": get_marriage(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}}
# res = wm.send_template(user_id, template_id, data)
# print(res)

for i in range(len(user_id)):
    res = wm.send_template(user_id[i], template_id, data)
    print(res)
