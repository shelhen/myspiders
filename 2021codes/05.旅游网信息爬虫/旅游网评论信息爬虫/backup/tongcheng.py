import re
import time
import requests
import random


class TongSpider(object):
    def __init__(self):
        self.pliId= [
            '20256',  # 汉文化景区
        ]
        self.ak = 'bc4b3ca6ae27747981b43e9f4a6aa769'
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Referer': 'https://www.ly.com/scenery/BookSceneryTicket_20256.html',
            "Host": "www.ly.com",
        }
        self.session=requests.session()
        self.cookies={
            '_dx_captcha_cid': '99085399',   # 08871580
        }


    def get_cookies(self):
        self.get_sessionId()
        # print(self.session.cookies.keys())
        url = "https://www.ly.com/udc/api/getsurvey?callback=handler&platform=PC&page=%E5%A4%A7%E5%91%A8%E8%BE%B9%E6%99%AF%E5%8C%BA%E7%BB%88%E9%A1%B5&_=" + str(int(time.time()))
        r = self.session.get(url, headers=self.headers,timeout=10)
        print(r.content.decode()) # 测试成功，成功拿到数据
        self.get_cid()
        #             # 1677650949930Mywl9zAcc8H8nWbLTYGbix8Epjm8KmHs
        #             # 1677652685595uT7TWfMUWhxk2Snn0lHzdptTI5wsYPRQ
        #             # '_dx_uzZo5y':'',
        # '_dx_uzZo5y': '550edefcff14f5e4f56f63584b9fabc0b73538c3b08c81d7d5b39ff9185ee15e0307d46f',
        # d885978e377583eec3be2e018aec0d297d598ab64fd480d3bab1473c8a590b8264d64ed9

        # ak = 'etBRsREU2D0Zj6enHl69ZsbhS8Tqqeae'


    def get_sessionId(self):
        url = "https://www.ly.com/scenery/AjaxHelper/ValidPic.aspx?action=PRICECODE&sid=20256&itype=12&pcrefId=215909561&pctype=15"
        self.session.get(url, headers=self.headers, timeout=10)
        data = {
            'channel': 'scenery',
            'action': 'getBulletin',
            'asyncRefid': 0,
            'asyncUniqueKey': 'undefined',
            'date': time.strftime('%a %b %d %Y %H:%M:%S GMT+0800 (中国标准时间)'),
            '_dAjax': 'callback',
            'callback': 'tc' + str(random.random())[-11:]
        }
        self.session.get("https://www.ly.com/AjaxHelper/TopLoginHandler.aspx",data=data, headers=self.headers,timeout=10)
        longkey = time.time()*1e6
        ts = (longkey+6414837)/1e6
        shortkey = str(int((longkey-6414837)/1e3))
        self.session.cookies.update({
            '17uCNRefId': 'RefId=0&SEFrom=&SEKeyWords=',  # 常量
            'TicketSEInfo': 'RefId=0&SEFrom=&SEKeyWords=',  # 常量
            'CNSEInfo': 'RefId=0&tcbdkeyid=&SEFrom=&SEKeyWords=&RefUrl=',  # 常量
            'qdid': '-9999',  # 常量
            'Hm_lvt_c6a93e2a75a5b1ef9fb5d4553a2226e5': str(int(ts)),
            'Hm_lpvt_c6a93e2a75a5b1ef9fb5d4553a2226e5': str(int(ts)),
            '__tctmc': '144323752.270198135',  # 未变化
            '__tctmd': '144323752.737325',  # 未变化
            '__tctmu': '144323752.0.0',  # 未变化
            '__tctma': '144323752.' + str(int(longkey/1e3)) + '.' + shortkey + '.' + shortkey+'.' +shortkey + '.1',
            # 144323752.682227496435949.1677650942426.1677650942426.1
            '__tctmb': '144323752.682227496435949.' + shortkey + '.' + shortkey + '.1',
            '__tctmz': '144323752.' + shortkey + '.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none)',
            'longKey': str(int(longkey)),
            '__tctrack': '0',  # 常量
            'SECKEY_ABVK': 'VKGRlYevo7CwDC4DeOI7SzYH7eBGLR2DJzOm2jmAdn8%3D',
        })

    def get_cid(self):
        ts = str(int(time.time()*1000))
        data = {
            'w': 300,
            'h': 150,
            's': 50,
            'ak': self.ak,
            'c': '',
            'jsv': '1.5.31.1',
            'aid': 'dx-'+ ts +'-'+ '28888107' +'-1',
            'wp': 1,
            'de': 0,
            'uid': '',
            'lf': 0,
            'tpc': '',
            '_r': random.random()
        }
        url = 'https://cap.dingxiang-inc.com/api/a?'
        r = self.session.get(url,data=data,headers=self.headers,timeout=10)
        print(r.content.decode())


    def get_comments(self):

        data={
            'action': 'GetDianPingList',
            'sid': 20256,
            'page': 1,
            'pageSize': 10,
            'labId': 1,
            'sort': 0,
            'iid': random.random(),
        }
        # url = "https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx"
        # self.session.cookies.update(self.cookie)
        # res = self.session.get(url, data=data, headers=self.headers, timeout=10)
        # print(res.json())

        # ak: etBRsREU2D0Zj6enHl69ZsbhS8Tqqeae

    def main(self):
        self.get_cookies()
        # https://www.ly.com/scenery/BookSceneryTicket_20256.html
        #
        # self.get_comments()
        # 直接给定cookie成功获得假数据
        # data={
        #     'callback': 'handler',
        #     'platform': 'PC',
        #     'page': '大周边景区终页',
        #     '_': '1677598782443'
        # }
        # url ='https://www.ly.com/udc/api/getsurvey'
        # # 加上部分cookie
        # self.session.get(url,data=data,headers=self.headers,timeout=10)


if __name__ == '__main__':
    tong=TongSpider()
    tong.main()