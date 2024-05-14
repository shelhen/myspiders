#!python3
# -*- coding: UTF-8 -*-
import requests
import time, random
from datetime import datetime
import uiautomation as uia


class WeChat(object):

    def __init__(self):
        # 获取微信程序的进程
        self.UiaAPI = uia.WindowControl(ClassName='WeChatMainWndForPC')
        self.SearchBox = self.UiaAPI.EditControl(Name='搜索')
        self.EditMsg = self.UiaAPI.EditControl(Name='输入')

    def search(self, name):
        '''
        查找微信好友或关键词
        name: 要查找的关键词，str   * 最好完整匹配，不完全匹配只会选取搜索框第一个
        '''
        self.UiaAPI.SetFocus()
        time.sleep(0.2)
        self.UiaAPI.SendKeys('{Ctrl}f', waitTime=1)
        self.SearchBox.SendKeys(name, waitTime=1.5)
        self.SearchBox.SendKeys('{Enter}')

    def send_msg(self, name='文件传输助手', msg='你好', clear=True):
        '''向当前窗口发送消息
        name: 接受信息的人
        msg : 要发送的消息
        clear : 是否清除当前已编辑内容
        '''
        self.UiaAPI.SwitchToThisWindow()
        self.search(name)
        if clear:
            self.EditMsg.SendKeys('{Ctrl}a', waitTime=0)
        self.EditMsg.SendKeys(msg, waitTime=0)
        self.EditMsg.SendKeys('{Enter}', waitTime=0)

    def get_times(self):
        now = datetime.now()
        week_dict = {
            'Monday': '星期一',
            'Tuesday': '星期二',
            'Wednesday': '星期三',
            'Thursday': '星期四',
            'Friday': '星期五',
            'Saturday': '星期六',
            'Sunday': '星期日'
        }
        weekday = week_dict[now.strftime('%A')]
        date = now.strftime(f'%Y年%m月%d日 {weekday}')
        # print(date)
        commemoration = datetime(2019, 4, 6)
        girl_birthday = datetime(2000, 8, 19)
        boy_birthday = datetime(1997, 4, 5)
        meet_day = datetime(2022, 10, 1)
        day_long = str(now - commemoration)[:4]
        # print(f"我们在一起已经{day_long}天了")
        dst1 = str(commemoration.replace(year=datetime.now().year+1)-now)[:3]
        dst2 = str(girl_birthday.replace(year=datetime.now().year+1)-now)[:3]
        dst3 = str(boy_birthday.replace(year=datetime.now().year + 1) - now)[:3]
        dst4 = str(meet_day- now)[:2]
        # print(f"距离在一起纪念日还有{dst1}天,距离她生日还有{dst2}天;距离他生日还有{dst3}天")
        return [day_long, dst1, dst2, dst3, dst4, date]

    def get_weather(self):
        locationid = '101020900'
        url = [
            'https://geoapi.qweather.com/v2/city/lookup?',
            'https://devapi.qweather.com/v7/weather/now?location='+ locationid +'&key=',
            'https://devapi.qweather.com/v7/indices/1d?type=1,3,8&location='+ locationid +'&key='
        ]
        appid = 'bae296d045c144aea387a15464196a3a'
        # r = requests.get(url[0]+'location=shanghai&key='+ appid)
        weather = requests.get(url[1] + appid).json()['now']
        texts = requests.get(url[2] + appid).json()['daily']
        # {weather['pressure'] + 'hPa'}
        text1 = f"上海松江 {weather['text']}, {str(int(weather['temp'])-1) + '~' + weather['feelsLike'] + '℃'}"
        random_suggestion = random.choice(texts)
        text2 = f"[跳跳]{random_suggestion['name']}[跳跳]\n{random_suggestion['text']}"
        return text1,text2

    def get_love_words(self):
        # 获取金山词霸每日一句
        # url = "http://open.iciba.com/dsapi"
        contents = requests.get('https://api.1314.cool/words/api.php?return=json').json()['word']
        return contents
