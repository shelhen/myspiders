import time,json
from datetime import datetime
import random, requests
from apscheduler.schedulers.blocking import BlockingScheduler


class WeChat(object):

    def __init__(self):
        # [微信测试号接口]
        self.appID = 'wx8047d06522cf1f8f'
        self.appSecret = 'd3ff27ed1449140998f02d670e037aad'
        self.templateId = 'q9XH6FNfqbWN5gC10eHnI5aCsLUUhV0TmRLa7raItC4'
        self.toUser = [
            'oAPf45wzhAz7zn6m5WWfihEqRCj8',
            # 'oAPf45xuDJSCpes05m2OcATWTyY8'
        ]
        # [微信企业号接口数据]
        self.WECOM_CID = 'ww7ebbb648ff2c793a'  # 企业微信公司ID
        self.WECOM_SECRET = 'mDexwcc3rSzNsgTTN-lUiKcEbjC2TJ5QmAik2qtnbog'   # 企业微信应用Secret
        self.WECOM_AID = '1000002'  # # 企业微信应用ID
        self.WECOM_TOUID = '@all'  # 推送用户
        # [个人信息信息]  *   日期需填写公历
        self.commemoration = datetime(2019, 4, 6)  # 恋爱纪念日
        self.girl_birthday = datetime(2000, 8, 19)  # 女孩生日
        self.boy_birthday = datetime(1997, 4, 5)  # 男孩生日
        self.meet_day = datetime(2022, 10, 1)  # 下次见面日期
        # [城市信息]
        self.girl_cityName = '松江'
        self.boy_cityName = '徐州'
        # [api账号与密码]
        self.appid = 'bae296d045c144aea387a15464196a3a'

    def get_access_token(self):
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appID,
            "secret": self.appSecret,
        }
        accessToken =requests.get(url, params=params, timeout=30).json()["access_token"]
        return accessToken

    def sen_msg(self, data):
        accessToken = self.get_access_token()
        if accessToken:
            url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + accessToken
            for user in self.toUser:
                payload = {
                    "touser": user,
                    "template_id": self.templateId,
                    "url": "http://weixin.qq.com/download",
                    "color": "#FF0000",
                    # "data": json.dumps(data, ensure_ascii=False),
                    "data": data
                }
                requests.post(url, json=payload, timeout=30)

    def get_wework_astoken(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.WECOM_CID,
            "corpsecret": self.WECOM_SECRET
        }
        access_token = requests.get(url, params=params).json()['access_token']

        if access_token and len(access_token) > 0:
            return access_token

    def sendMsg(self, text):
        access_token = self.get_wework_astoken()
        print(access_token)
        if access_token:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
            payload = {
                "touser": self.WECOM_TOUID,
                "agentid": self.WECOM_AID,
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "duplicate_check_interval": 1800
            }
            requests.post(url, data=json.dumps(payload))

    def send_Mdmsg(self, text):
        # 仅支持企业微信查看
        access_token = self.get_wework_astoken()
        if access_token:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
            payload = {
                "touser": self.WECOM_TOUID,
                "agentid": self.WECOM_AID,
                "msgtype": "markdown",
                "markdown": {
                    "content": text
                },
                "duplicate_check_interval": 1800
            }
            requests.post(url, data=json.dumps(payload))

    def get_loveword(self):
        # 整点土味情话
        contents = requests.get('https://api.1314.cool/words/api.php?return=json').json()['word']
        return contents

    def iciba(self):
        # 整点金山警句
        text = requests.get("http://open.iciba.com/dsapi/",timeout=10).json()
        note_en = text["content"]
        note_cn = text["note"]
        return note_cn, note_en

    def get_cityid(self, location, appid):
        # 获取城市id
        url = str('https://geoapi.qweather.com/v2/city/lookup?location='+location+'&key=' + appid)
        res = requests.get(url).json()['location'][0]
        id = res['id']
        city_name = res['adm1'].rstrip('市').rstrip('省')+' '+res['name']
        return id, city_name

    def get_weather(self, locationid, appid):
        # 天气接口
        url = [
            'https://devapi.qweather.com/v7/weather/now?location='+ locationid +'&key='+ appid,
            'https://devapi.qweather.com/v7/indices/1d?type=1,3,8&location='+ locationid +'&key='+ appid
        ]
        weather = requests.get(url[0] ).json()['now']
        texts = requests.get(url[1] ).json()['daily']
        weather_list = [weather['text'], str(int(weather['temp'])-1) + '~' + weather['feelsLike'] + '℃', ]
        suggestions_list = [random.choice(texts)['name'], random.choice(texts)['text']]
        return weather_list, suggestions_list

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
        commemoration = self.commemoration
        girl_birthday = self.girl_birthday
        boy_birthday = self.boy_birthday
        meet_day = self.meet_day
        # 计算在一起总时常
        day_long = str(now - commemoration)[:4]
        # 计算距离恋爱纪念日还有多少天
        dst1 = str(commemoration.replace(year=datetime.now().year + 1) - now)[:3]
        # 计算距离女孩生日还有多少天
        dst2 = str(girl_birthday.replace(year=datetime.now().year + 1) - now)[:3]
        # 计算距离男孩生日还有多少天
        dst3 = str(boy_birthday.replace(year=datetime.now().year + 1) - now)[:3]
        # 计算距离下次见面还有多少天
        dst4 = str(meet_day - now)[:2]
        return [date, day_long, dst1, dst2, dst3, dst4]

    def generate_color(self):
        randomColor = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
        color_list = randomColor(100)
        return random.choice(color_list)

    def wechat_daliy_pull(self):
        print("当前执行微信公众测试号推送")
        datelist = self.get_times()
        # boy_cityCode, boy_city_name = self.api.get_cityid(config.boy_cityName, self.appid)
        girl_cityCode, girl_city_name = self.get_cityid(self.girl_cityName, self.appid)
        werther_list_g, su_list_g = self.get_weather(girl_cityCode, self.appid)
        # werther_list_b, su_list_b = self.api.get_weather(boy_cityCode, self.appid)
        content = self.get_loveword()
        note_cn, note_en = self.iciba()
        # 自定义消息模板的变量必须是全部小写
        msg = {
            "date": {"value": datelist[0], "color": self.generate_color()},
            "city": {"value": girl_city_name, "color": self.generate_color()},
            "weather": {"value": werther_list_g[0], "color": self.generate_color()},
            "temp": {"value": werther_list_g[1], "color": self.generate_color()},
            "loveDays": {"value": datelist[1], "color": self.generate_color()},
            "loveDay": {"value": datelist[2], "color": self.generate_color()},
            "girlBirthday": {"value": datelist[3], "color": self.generate_color()},
            "boyBirthday": {"value": datelist[4], "color": self.generate_color()},
            "meetDay": {"value": datelist[5], "color": self.generate_color()},
            "noteEn": {"value": note_en, "color": self.generate_color()},
            "noteCh": {"value": note_cn, "color": self.generate_color()},
            "loveWord": {"value": content, "color": self.generate_color()},
            "health": {"value": su_list_g[1], "color": self.generate_color()}
        }
        self.sen_msg(msg)
        print('执行完毕！')

    def wework_daliy_pull(self):
        print('当前执行微信企业号小程序推送')
        datelist = self.get_times()
        # boy_cityCode, boy_city_name = self.api.get_cityid(config.boy_cityName, self.appid)
        girl_cityCode, girl_city_name = self.get_cityid(self.girl_cityName, self.appid)
        werther_list_g, su_list_g = self.get_weather(girl_cityCode, self.appid)
        # werther_list_b, su_list_b = self.api.get_weather(boy_cityCode, self.appid)
        content = self.get_loveword()
        note_cn, note_en = self.iciba()
        text = []
        text.append("玥宝，早上好呀！")
        text.append(f"{datelist[0]}")
        text.append(f"城市:  {girl_city_name}")
        text.append(f"天气:  {werther_list_g[0]}")
        text.append(f"气温:  {werther_list_g[1]}")
        text.append(su_list_g[1])
        text.append("\n")
        text.append(f"今天是我们恋爱的第  [{datelist[1]}] 天")
        text.append(f"今天距离 恋爱四周年 还有 [{datelist[2]}] 天")
        text.append(f"距离 小玥生日 还有 [{datelist[3]}] 天")
        text.append(f"距离 小恒生日 还有 [{datelist[4]}] 天")
        text.append(f"距离 我们下次见面 还有 [{datelist[5]}] 天")
        text.append("\n")
        text.append(content)
        text.append("\n")
        text.append(note_cn)
        text.append(note_en)
        self.sendMsg(text="\n".join(text))
        print('执行完毕！')

    def wework_daliy_mdpull(self):
        print('当前执行微信企业号小程序md格式推送')
        time.sleep(3)
        print('执行完毕！')


if __name__ == '__main__':
    wx = WeChat()
    scheduler = BlockingScheduler()
    # scheduler = BlockingScheduler(executors=executors, timezone='Asia/Shanghai')

    # 5秒执行一次
    # scheduler.add_job(wx.wechat_daliy_pull, 'interval', seconds=5)
    # 每天9.30分执行
    scheduler.add_job(wx.wechat_daliy_pull, 'cron', hour=9, minute=30)
    # scheduler.add_job(wx.wework_daliy_pull, trigger="cron", hour=17, minute=34)
    scheduler.start()




