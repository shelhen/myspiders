# https://www.mafengwo.cn/poi/6326847.html
import hashlib
import time
import json
import re
import js2py
import requests


class Mafeng(object):
    def __init__(self):
        self.polids=[
            '6326847',  # 汉文化景区
        ]
        self.session = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            'Host': 'www.mafengwo.cn',
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Upgrade-Insecure-Requests": "1"
        }

    def get_cookies(self):
        self.get_conect()
        res = self.session.get('https://www.mafengwo.cn/poi/6326847.html', headers=self.headers, timeout=10)
        print(res.text)

    def get_conect(self):
        url = 'https://www.mafengwo.cn/poi/6326847.html'
        res = self.session.get(url, headers=self.headers, timeout=10)
        js_clearance = re.findall('cookie=(.*?);location', res.text)[0]
        result = js2py.eval_js(js_clearance).split(';')[0].split('=')
        self.session.cookies.update({result[0]: result[1]})
        response = self.session.get(url, headers=self.headers, timeout=10)
        parameter = json.loads(re.findall(r';go\((.*?)\)', response.text)[0])
        for i in range(len(parameter['chars'])):
            for j in range(len(parameter['chars'])):
                values = parameter['bts'][0] + parameter['chars'][i] + parameter['chars'][j] + parameter['bts'][1]
                if parameter['ha'] == 'md5':
                    ha = hashlib.md5(values.encode()).hexdigest()
                elif parameter['ha'] == 'sha1':
                    ha = hashlib.sha1(values.encode()).hexdigest()
                elif parameter['ha'] == 'sha256':
                    ha = hashlib.sha256(values.encode()).hexdigest()
                if ha == parameter['ct']:
                    __jsl_clearance_s = values
        self.session.cookies.update({result[0]: __jsl_clearance_s})


    def main(self):
        self.get_cookies()


if __name__ == '__main__':
    mafeng=Mafeng()
    mafeng.main()