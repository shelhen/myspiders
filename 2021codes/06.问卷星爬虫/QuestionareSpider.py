import requests
import random
import re
import time
import js2py

class QuestionareSpider(object):

    def __init__(self, id):
        self.sessions = requests.session()
        self.shortId = id
        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }

    def get_jqsign(self, ktimes:int, jqnonce:str):
        result = []
        b = ktimes % 10 if ktimes % 10 != 0 else 1
        for char in list(jqnonce):
            f = ord(char) ^ b
            result.append(chr(f))
        return ''.join(result)

    def get_jqpraram(self, rndnum, activityId, starttime):
        with open('datas/questionare_.js', 'r', encoding='utf8') as f:
            script = f.read()
        context = js2py.EvalJs(enable_require=True)
        context.execute(script)
        ts = int(time.mktime(time.strptime(starttime, "%Y/%m/%d %H:%M:%S")))
        # print(context._0x156205('988609781.60866459', 1689348352, '228882520'))
        return context._0x156205(rndnum, ts, activityId)

    def get_cookies(self):
        self.headers['X-Forwarded-For'] = f'{112}.{random.randint(64, 68)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
        response = self.sessions.get('https://www.wjx.cn/vm/'+ self.shortId +'.aspx', headers=self.headers, timeout=10)
        self.sessions.get("https://image.wjx.cn/js/plugin/jquery-viewer.js?v=3219",headers=self.headers,timeout=10)
        res2 = self.sessions.get('https://ynuf.aliapp.org/w/wu.json',headers=self.headers,timeout=10)
        self.sessions.cookies.update({
            'ssxmod_itna':'Qq0xyWK7qYqq2Dl4iwlEYGCIG8KN6Eo43D7W+zDBMhd4iNDnD8x7YDv+I5dw73O0Enxa45mRw4aeWQrcAxfi0hphaN3g+reDHxY=DU=7doDx1q0rD74irDDxD3Db4QDSDWKD9D0+kSBuqtDm4GWCqGfDDoDYR=nDitD4qDB+2dDKqGgCLhbCkrXzlUdLkGPsBxyD0UQxBdt8cuo1P9bSkrTrpiaiqGySPGuRMtVDMbDCoUVnwisC+ho+A5KYo3YQDAQYGGhi+qN/0DKt44f5GwKW0PoSE1DG4d9TrD=='
        })
        self.sessions.cookies.update({'ssxmod_itna2':'Qq0xyWK7qYqq2Dl4iwlEYGCIG8KN6Eo43D7WD8q10AnDGNI3Gaz70IoBQGx8gOFNKcWlSyjbulxQgbm3=4lBpANsWRB0Eqf9laRw/n4miHA5vRgkiG0DT9COn6LzWUWSuNNtHZhNWTAGKRoMfqtnYl0/eQjcelt9GS=KOSQlfWbyme05vAeGjEQ31BrG3BrKD1KKB+Rto=qTvEwOk19=TkF75jN0WptE/T6HoFuH0CnvWz3404u8T47F=iOG3=EmSCf8QtWXMz6EsBxHs8uxIhpfI/9jXmcbK4+5FdWv6H1jzyoSnIaup5dO68QhcA6QWeEEtqDtz1fZZej238E08n=77ExljpZ+nE=cQhv0pnxeq/2/0huZ4qC2QKf/DY3IrrImRlGQQu7lXRDhaRDa8u7nbhU2a8n++bqG4DQKFD08DijbYD=='})
        print(f'参数的含义暂时未知：{res2.content.decode()}')
        # 经过几次发送验证码抓包对比，发现data开头的106!这几个字符是固定的。106!后面随意拼接字符都可以正常取到token
        rand_str = 'GwWKhOu41p50+P3j7ad9FmtEMZ/8oVHYJicCg6fbLqAkyBxQX=Rl2erUvDInzTSsN'
        randtumple = (rand_str[random.randrange(0, len(rand_str))] for i in range(0, 570))
        string = ''.join(randtumple)
        data={'data': "107!"+ string+'==',"xa": "FFFF00000000016770EE", "xt": "", "efy": 1}
        res3 = self.sessions.post('https://ynuf.aliapp.org/service/um.json',headers=self.headers, data=data, timeout=10)
        print(f"id:{res3.json()['id']}")
        print(f'tn:{res3.json()["tn"]}')
        # print(self.sessions.cookies.items())
        return response.content.decode()

    def get_params(self, content):
        # ktimes 为鼠标移动次数
        ktimes = random.randint(57, 143) + int(random.random() * 286)
        jqnonce = re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}', content).group()
        rndnum = re.search(r'\d{9,10}\.\d{8}', content).group()
        start_time = re.search(r'\d+?/\d+?/\d+?\s\d+?:\d{2}:\d{2}', content).group()
        activityId = re.search(r'activityId =(\d+);', content).group(1)
        activityId = int(activityId) ^ 2130030173
        params = {
            'shortid': self.shortId,
            'starttime': start_time,
            'submittype': 1,
            'ktimes': ktimes,
            'hlv': 1,
            'rn': rndnum,
            'jqpram': self.get_jqpraram(rndnum, str(activityId), start_time),
            'nw': '1',
            'jwt': '4',
            'jpm': '83',
            't': int(time.time() * 1000),
            'jqnonce': jqnonce,
            'jqsign':self.get_jqsign(ktimes,jqnonce),
        }
        return activityId, params

    def submit(self, submitdata):
        content = self.get_cookies()
        params = self.get_params(content)
        self.headers.pop('X-Forwarded-For')
        url = "https://www.wjx.cn/joinnew/processjq.ashx"
        data = {'submitdata': submitdata}
        self.sessions.get('https://image.wjx.cn/images/wjxMobile/wait.gif',headers=self.headers, timeout=10)
        playload={"APIVersion": "0.6.0","a": params[0],'pd': data['submitdata']}
        self.headers['Origin']='https://www.wjx.cn'
        self.headers["Host"] = 'www.wjx.cn'
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers["Referer"] = 'https://www.wjx.cn/vm/h4IsOBH.aspx'
        self.sessions.get("https://sojump.cn-hangzhou.log.aliyuncs.com/logstores/activitypostdata/track.gif", params=playload, headers=self.headers,timeout=10)
        res = self.sessions.post(url, headers=self.headers, params=params[1],data=data, timeout=10)
        pd = res.content.decode()
        print(pd)
        params_={"APIVersion": "0.6.0", "a": params[0],'pd':pd}
        self.sessions.get('https://sojump.cn-hangzhou.log.aliyuncs.com/logstores/activitypostdata/track.gif',headers=self.headers,timeout=10,params=params_)
        finish_url = f'https://sojump.cn-hangzhou.log.aliyuncs.com/logstores/activityfinish/track.gif?APIVersion=0.6.0&activity={params[0]}&source=1&weixin=0&vip=0&qtype=1&qw=0&name=BMvL05bbhlcmCLd4yzLerQ%3D%3D'
        self.sessions.get(finish_url,headers=self.headers,timeout=10)
        # refer = pd.split('?')[1]
        # https://www.wjx.cn/wjx/join/completemobile2.aspx?
        # activityid=h4IsOBH&joinactivity=118268349309&sojumpindex=11&tvd=4w0ngE1RduU%3d&comsign=748F2A7A0DF2A11D5BAC9440C58B59E14FFB3B75&ge=1&nw=1&jpm=83
        # activityid=h4IsOBH&joinid=118268349412&sojumpindex=12&tvd=4w0ngE1RduU%3d&comsign=7D5BE7DD2F5D8D5C4C5D3E2C829651B1A70D5E25&ge=1&nw=1&jpm=83


if __name__ == '__main__':
    id = 'h4IsOBH'
    # url ='https://www.wjx.cn/vm/h4IsOBH.aspx'  #
    submitdata = "1$1}2$2}3$1|2|4}4$1|2|3}5$1}6$2"
    qs = QuestionareSpider(id)
    qs.submit(submitdata)
    # for i in range(10):
    #
    #     time.sleep(random.random()*20+10)





