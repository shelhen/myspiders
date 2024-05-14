import requests
import random
from datetime import datetime
import re


class Xinxin(object):
    def __init__(self):
        # [微信测试号接口信息]
        self.appID = 'wx8047d06522cf1f8f'
        self.appSecret = 'd3ff27ed1449140998f02d670e037aad'
        self.templateId = 'UWrCmeIBaJ7dvot2uM3KG1AZvtpkHZ5LXQ4sYQL4PIs'
        self.toUser = [
            'oAPf45wzhAz7zn6m5WWfihEqRCj8',  # 恒恒
            # 欣欣
        ]
        self.city_name = '徐州'
        self.appid = 'bae296d045c144aea387a15464196a3a'

    def get_access_token(self):
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appID,
            "secret": self.appSecret,
        }
        accessToken = requests.get(url, params=params, timeout=30).json()["access_token"]
        return accessToken

    def send_msg(self, data):
        accessToken = self.get_access_token()
        if accessToken:
            url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + accessToken
            for user in self.toUser:
                payload = {
                    "touser": user,
                    "template_id": self.templateId,
                    "url": "http://weixin.qq.com/download",
                    "color": "#FF0000",
                    "data": data
                }
                requests.post(url, json=payload, timeout=30)

    def get_word(self):
        # 整点土味情话
        content = requests.get('https://api.1314.cool/words/api.php?return=json').json()['word']
        text = requests.get("http://open.iciba.com/dsapi/", timeout=10).json()
        note_en = text["content"]
        note_cn = text["note"]
        return content, note_en, note_cn

    def get_weather(self):
        # 天气接口
        res = requests.get(
            str('https://geoapi.qweather.com/v2/city/lookup?location=' + self.city_name + '&key=' + self.appid)
        ).json()['location'][0]
        city_name = res['adm1'].rstrip('市').rstrip('省') + ' ' + res['name']
        locationid = res['id']
        url = [
            'https://devapi.qweather.com/v7/weather/now?location=' + locationid + '&key=' + self.appid,
            'https://devapi.qweather.com/v7/indices/1d?type=3&location=' + locationid + '&key=' + self.appid
        ]
        weather = requests.get(url[0]).json()['now']
        text = requests.get(url[1]).json()['daily'][0]['text']
        weather_list = [weather['text'], str(int(weather['temp']) - 3) + '~' + str(int(weather['feelsLike'])) + '℃', ]
        return city_name, weather_list, text

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
        date = now.strftime(f"%Y年%m月%d日 {week_dict[str(now.strftime('%A'))]}")
        commemoration = datetime(2022, 11, 20)  # 恋爱纪念日
        girl_birthday = datetime(1998, 11, 10)  # 女孩生日
        boy_birthday = datetime(1997, 4, 5)
        # 计算在一起总时常
        day_long = re.search(r'(\d+) days',str(now - commemoration)).group(1)  #   3 days, 19:15:02.032365
        # 计算距离恋爱纪念日还有多少天
        dst1 = str(commemoration.replace(year=datetime.now().year + 1) - now)[:3]
        # 计算距离女孩生日还有多少天
        dst2 = str(girl_birthday.replace(year=datetime.now().year + 1) - now)[:3]
        # 计算距离男孩生日还有多少天
        dst3 = str(boy_birthday.replace(year=datetime.now().year + 1) - now)[:3]
        # 计算距离下次见面还有多少天
        # dst4 = str(meet_day - now)[:2]
        return [date, day_long, dst1, dst2, dst3]  # day_long,

    def generate_color(self):
        randomColor = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
        color_list = randomColor(100)
        return random.choice(color_list)

    def main(self):
        print("当前执行微信公众测试号推送")
        datelist = self.get_times() # ['今日日期', '在一起纪念日', "女孩生日计时", "男孩生日计时"]
        city_name, weather_list, text = self.get_weather()  # city_name, weather_list, text
        content = self.get_word()
        # 自定义消息模板的变量必须是全部小写
        msg = {
            "date": {"value": datelist[0], "color": self.generate_color()},
            "city": {"value": city_name, "color": self.generate_color()},
            "weather": {"value": weather_list[0], "color": self.generate_color()},
            "temp": {"value": weather_list[1], "color": self.generate_color()},
            "loveDays": {"value": datelist[1], "color": self.generate_color()},
            # "loveDay": {"value": datelist[2], "color": self.generate_color()},  # 周年纪念日
            "girlBirthday": {"value": datelist[2], "color": self.generate_color()},
            # "boyBirthday": {"value": datelist[3], "color": self.generate_color()},
            # "meetDay": {"value": datelist[5], "color": self.generate_color()},
            "noteEn": {"value": content[1], "color": self.generate_color()},
            "noteCh": {"value": content[2], "color": self.generate_color()},
            # "loveWord": {"value": content[0], "color": self.generate_color()},
            "health": {"value": text, "color": self.generate_color()}
        }
        self.send_msg(msg)
        print('执行完毕！')


if __name__ == '__main__':
    xin=Xinxin()
    xin.main()


