import re
import requests
import js2py
import random
import time
from util import remark_save


class QuSpider(object):
    def __init__(self):
        self.poioId = [
            '1468',  # 龟山汉墓
            "5158",  # 汉文化景区
            "5483",  # 徐州博物馆
            "4760",  # 狮子山楚王陵
            "7253",  # 户部山——戏马台
            "39007",  # 云龙湖
            '142546',  # 窑湾古镇
        ]
        self.session = requests.session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        self.p = re.compile(r'[^\w，。！？,.、:；℃]')
    def get_csrf(self):
        b = "123456789poiuytrewqasdfghjklmnbvcxzQWERTYUIPLKJHGFDSAZXCVBNM"
        csft = ""
        for r in range(32):
            csft += b[int(random.random() * 1e8) % len(b)]
        return csft
    def get_cpid(self, QN, QG):
        context = js2py.EvalJs(enable_require=True)
        with open("./data/qunaer.js", 'r', encoding='utf8') as f:
            result = f.read()
        context.execute(result)
        return context._initUserKey(QN, QG) + context.generateUUID()
    def get_uid(self):
        headers={
            "referer": "https://www.qunar.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        res = self.session.get("https://s.c-ctrip.com/universal-id.js?callback=_qheader_ctrip_callcallback", headers=headers, timeout=10)
        return re.search(r'"u_vid":"([A-Z0-9]+)"', res.content.decode()).group(1)
    def get_index_cookies(self):
        # 访问首页绑定cookie信息
        ts = round(time.time())
        self.session.get("https://www.qunar.com/", headers=self.headers, timeout=10)
        # 获得前三个cookie信息:QN1;QN300;QN99
        self.session.get("https://www.qunar.com/twell/cookie/allocateCookie.jsp", headers=self.headers, timeout=10)
        # 获取 QunarGlobal
        # 从cookie中拿到QN1和QunarGlobal,计算cpid构造新的cookies
        QN = self.session.cookies['QN1']
        QG = self.session.cookies['QunarGlobal']
        cpid = self.get_cpid(QN, QG)
        csrf = self.get_csrf()
        self.session.cookies.update({
            "unar-assist": '{%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}	',
            "QN205": "organic",
            "QN277": "organic",
            "QN267": cpid,
            "csrfToken": csrf,
        })
        self.session.get(f"https://qreport.qunar.com/s2/log/pv?rf=&sr=1536x864&cpid={cpid}&url=https%3A%2F%2Fwww.qunar.com%2F", headers=self.headers, timeout=10)  # 这个并无任何相应数据；或许可以忽略
        self.session.get("https://user.qunar.com/passport/addICK.jsp?ssl", headers=self.headers, timeout=10)
        # 获取了_i 和 _vi的cookie
        self.session.get(f"https://log.flight.qunar.com/l?r=pageview&rf=-1&sc=1536*864*1.25&et={ts}&at={ts}&p=home_index",
            headers=self.headers, timeout=10)  # 这里配置许多需要的cookie{QN601;QN602;QN603;QN611;QN612}
        u_vid = self.get_uid()
        self.session.get(f"https://touch.train.qunar.com/api/train/trainHotConf?jsonpCallback=jQuery17203532750888491565_{ts}&conf_type=4&confKey=json.trainCalendarConfig&_={ts}",
            headers=self.headers, timeout=10)  # 出现未知cookie{QN269} 获取了有用的cookie : QN48
        # 接下来绑定并获取session_id
        res = self.session.get("https://rmcsdf.qunar.com/js/df.js?org_id=ucenter.login&js_type=0", headers=self.headers,
        timeout=10).content.decode()
        sessionId = re.search(r'sessionId=([\w\-]+)', res).group(1)
        self.session.get(f"https://rmcsdf.qunar.com/api/device/challenge.json?callback=callback_{ts}&sessionId={sessionId}&domain=qunar.com&orgId=ucenter.login")  # 获取fid
        self.session.cookies.update({'QN271': sessionId, 'QN269':u_vid, 'QN163':'0'})
        # print(self.session.cookies.keys())
    def get_comments(self, i, id):
        '''
        网站随机返回错误字段；随机休眠0-10秒仍然无法访问拿到数据说明不是。在固定的页码处返回错误字段：我尝试遇到报错后跳过该页，发现将连续跳过多页，甚至下一次总页数也无法取得，说明不是。
        得出结论：触发了爬取太快或者因为什么反扒手段导致的返回错误字段；
        '''
        url = f"https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId={id}&index={i}&page={i}&pageSize=10&tagType=0"
        # 当来到此处时，先判断获取的数据格式是json还是{error:404}格式
        res = self.session.get(url, headers=self.headers, timeout=10).json()['data']
        return res
    def parse(self, comments):
        remarks = [{
            "publishTime": time.mktime(time.strptime(data["date"], "%Y-%m-%d")),
            "score": data["score"],
            "content": self.p.sub("", data["content"].lower()),
            "Locate": data["cityName"],
            "usefulCount": 0}
            for data in comments if data["content"] != "用户未点评，系统默认好评。"]
        return remarks
    def main(self):
        self.get_index_cookies()
        for id in self.poioId:
            res = self.get_comments(1, id)
            # 首先访问第一页获取总评论数以计算总页数
            commentCount = int(res["commentCount"])
            tatolNum = commentCount // 10 if commentCount % 10 == 0 else (commentCount // 10) + 1
            if tatolNum == 0:
                continue
            else:
                for i in range(tatolNum):
                    # 控制下爬取速率
                    time.sleep(random.random()*3)
                    comments = self.get_comments(i + 1, id)  # 访问每一页，拿回响应数据
                    remarks = self.parse(comments['commentList'])
                    for remark in remarks:
                        print(remark)
                    remark_save('qunaer', remarks)
            print(f'已完成爬取id为{id}的景区的评论数据')


if __name__ == '__main__':
    qu = QuSpider()
    qu.main()