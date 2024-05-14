import requests
import random
import re
import time
import js2py


class QuestionareSpider(object):

    def __init__(self, id):
        self.sessions = requests.session()
        self.shortId = id
        self.sessions.headers={
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309080f) XWEB/8461 Flue'
        }

    def get_jqsign(self, ktimes:int, jqnonce:str):
        result = []
        b = ktimes % 10 if ktimes % 10 != 0 else 1
        for char in list(jqnonce):
            f = ord(char) ^ b
            result.append(chr(f))
        return ''.join(result)

    def get_jqpraram(self, rndnum, activityId, starttime):
        with open('questionare_.js', 'r', encoding='utf8') as f:
            script = f.read()
        context = js2py.EvalJs(enable_require=True)
        context.execute(script)
        ts = int(time.mktime(time.strptime(starttime, "%Y/%m/%d %H:%M:%S")))
        return context._0x156205(rndnum, ts, activityId)

    def get_token(self, num, flag=False):
        """
        :return: 获取随机token.
        """
        rand_str = '_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'[flag:]
        randtumple = (rand_str[random.randrange(0, len(rand_str))] for i in range(0, num))
        return ''.join(randtumple)

    def get_params(self, content):
        # ktimes 为鼠标移动次数
        ktimes = random.randint(57, 143) + int(random.random() * 286)
        jqnonce = re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}', content).group()
        username='BMvL05bbhlcmCLd4yzLerQ=='
        rndnum = re.search(r'\d{9,10}\.\d{8}', content).group()
        start_time = re.search(r'\d+?/\d+?/\d+?\s\d+?:\d{2}:\d{2}', content).group()
        activityId = re.search(r'activityId =(\d+);', content).group(1)
        activityId = int(activityId) ^ 2130030173
        params = {
            'shortid': self.shortId,
            'starttime': start_time,
            'cst':int(time.time() * 1e3)-int(random.random()*10),
            'submittype': 1,
            'ktimes': ktimes,
            'hlv': 1,
            'rn': rndnum,
            'access_token': f'75_{self.get_token(107)}',
            'openid': f'o_{self.get_token(26)}',
            'union': f'o{self.get_token(27, flag=True)}',
            'jqpram': self.get_jqpraram(rndnum, str(activityId), start_time),
            'nw': 1,
            'jwt': 2,
            'jpm': 68,
            'iwx': 1,
            't': int(time.time() * 1e3),
            'jqnonce': jqnonce,
            'jqsign': self.get_jqsign(ktimes, jqnonce),
        }
        return activityId, params

    def submit(self, submitdata, proxy=None):
        # https://www.wjx.cn/vm/mBrk8fi.aspx
        referer = 'https://www.wjx.cn/vm/' + self.shortId + '.aspx'
        content = self.sessions.get(referer, verify=False, timeout=10,proxies=proxy).content.decode()
        print(content)



        target = "https://www.wjx.cn/joinnew/processjq.ashx"
        activityId, params = self.get_params(content)
        self.sessions.headers.update({
            'Origin': referer[:18],
            'Host': referer[8:18],
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': referer
        })
        data={'submitdata': submitdata}

        res = self.sessions.post(target, params=params, data=data, timeout=10, proxies=proxy,verify=False)
        # print(res.content.decode())


if __name__ == '__main__':

    id = 'mBrk8fi'


    submitdata='1$1}2$1}3$1|2}4$-3}5$嘿嘿嘿'
    data={'submitdata': submitdata}

    # 1$1}
    # 2$1}
    # 3$1|2}
    # 4$1}
    # 5$嘿嘿嘿
    


    qs = QuestionareSpider(id)
    # 传入proxy参数，切换代理ip
    qs.submit(submitdata, proxy=None)





