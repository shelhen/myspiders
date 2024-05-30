import datetime
import time
import re
import random
import hashlib
import requests
import json

class Search360(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'Referer': 'https://www.sou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
        # self.session.verify = "./data/FiddlerRoot.pem"
        self.host = 'www.sou.com'
        self.sid = self.get_sid()
        self.auth_token = None

    def md5_hash(self, text_string):
        # 使用hashlib库来创建一个md5对象并基于字符串的utf-8编码更新散列值
        md5 = hashlib.md5()
        # 使用update方法进行散列
        md5.update(text_string.encode('utf-8'))
        return md5.hexdigest().lower()

    def get_sid(self):
        """js逆向的sid的纯python实现"""
        def get_guid():
            components = [
                'Netscape', None, 'zh-CN', 'Win32', self.session.headers['User-Agent'],
                1920, "x", 1080, 24, ''
            ]
            # 确保 list 中的元素是字符串格式，并且过滤掉 None 值。
            us = [str(item) for item in components if item!=None]
            o = ''.join(us)
            s = len(o)
            for i in range(2, 0, -1):
                o += str(i ^ s)
                s += 1
            return 2147483647 * round(2147483647 * random.random()) ^ hash(o)

        def hash(text):
            s = 0
            for l in range(len(text) - 1, -1, -1):
                A = ord(text[l])
                s = (s << 6 & 268435455) + A + (A << 14)
                a = s & 266338304
                if a != 0:
                    s = s ^ a >> 21
            return s
        sids = [str(hash(self.host)),str(get_guid()),str(int(time.time()*1000)+random.random()*2)]
        return ''.join(sids).replace('.', 'e')[:32]

    def get_auth_token(self):
        timestamp = int(datetime.datetime.now().timestamp())
        shanghai_tz = datetime.timezone(datetime.timedelta(hours=8))
        timestamp = datetime.datetime.fromtimestamp(timestamp, tz=shanghai_tz)
        e = ("Web", timestamp.isoformat(), "1.2", self.sid, self.md5_hash(self.session.headers['User-Agent']))
        # 更新headers
        self.session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Token": e[3],
            "Auth-Token": self.auth_token if self.auth_token else '',
            "Device-Platform": e[0],
            "Mid": "",
            "Func-Ver": "1",
            "Sid": e[3],
            "Timestamp": e[1],
            "Zm-Token": self.md5_hash(''.join(e)),
            "Zm-Ua": e[4],
            "Zm-Ver": e[2],
            'Host': 'www.sou.com',
            'Origin': 'https://www.sou.com'
        })
        self.session.get('https://www.sou.com/api/user/info?version=20')
        self.auth_token = self.session.cookies['Auth-Token']

    def get_cid(self, keyword):
        url = 'https://www.sou.com/api/common/conversation/v2'
        response = self.session.post(url, data={'title': keyword, 'kwargs': {}}).json()["data"]
        return response["conversation_id"], response["msg_id"]

    def parse(self, results):
        xx = [item.get('data', '') for item in results if not item.get('data', '').startswith('{')]
        return ''.join(xx)

    def search(self, keyword):
        self.get_auth_token()
        cid, mid = self.get_cid(keyword)
        time.sleep(1+random.random())
        data = {
            "conversation_id": cid,
            "message_id": mid,
            "re_answer_msg_id": "",
            "prompt": keyword,
            "is_so": True,
            "is_copilot_enabled": False,
            "indepth_answer": 0,
            "source_type": "prophet_web",
            "retry": False,
            "re_answer": 0,
            "last_id": 0,
            "search_method": "1",
            "search_args": {},
            "kwargs": {}
        }
        print('获取响应成功，解析结果中...')
        with self.session.post('https://www.sou.com/api/common/chat/v2', json=data, stream=True) as response:
            results = []
            parsed_dict = {}
            i = 0
            for stream_line in response.iter_lines():
                # 将字节解码为字符串
                decoded_line = stream_line.decode('utf-8').strip()
                if not bool(decoded_line) or decoded_line=='ping':
                    continue
                if i%4==0:
                    status = parsed_dict.get('event', '200')
                    if parsed_dict and status=='200':
                        results.append(parsed_dict)
                    parsed_dict = {}
                result = re.search(r'([a-z]+):\s*(.*)', decoded_line)
                current_key = result.group(1)
                parsed_dict[current_key] = result.group(2)
                i += 1
        text = self.parse(results)
        return cid, mid, text

    def get_extend_info(self, cid, mid):
        data = {
            'msg_id': mid,
            'conversation_id': cid,
            'type': 1,
            'kwargs': {}
        }
        data = self.session.post('https://www.sou.com/api/chat/extended_reading', data=data).json()['data']
        print('搜索扩展'+'*'*20)
        for item in data:
            print(item['type'])
            print(f"{item['title']}：{item['content']}")

    def get_related_info(self, cid, mid):
        data = {
            'msg_id': mid,
            'conversation_id': cid,
            'kwargs': {}
        }
        data = self.session.post('https://www.sou.com/api/chat/related_infos', data=data).json()['data']
        print('相关信息'+'*'*20)
        for item in data:
            print(f"{item['type']}:{item['abstract']}")

    def get_further_info(self, cid, mid):
        data = {
            'msg_id': mid,
            'conversation_id': cid,
            'refresh': 0,
            'kwargs': {}
        }
        response = self.session.post('https://www.sou.com/api/chat/ask_further/v2', data=data)
        print('\n进一步了解'+'*'*20)
        for item in response.json()['data']:
            print(item['content'])


if __name__ == '__main__':
    s360 = Search360()
    cid, mid, text = s360.search('Pyth0n')
    print(text)
    # s360.get_related_info(cid, mid)
    # s360.get_extend_info(cid, mid)
    # s360.get_further_info(cid, mid)