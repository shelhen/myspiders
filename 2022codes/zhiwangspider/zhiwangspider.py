import requests
import execjs
import os
from parsel import Selector
os.environ["EXECJS_RUNTIME"] = "Node"

class ZhiWangSpider(object):
    def __init__(self):
        self.url = 'https://www.zhiwang.com/'
        self.headers = {}
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        self.base_url = "https://libvpn.zuel.edu.cn/{0}"

    def login(self, username="202021040545", password="Xxy20021206"):
        """
        :param username:
        :param password:
        :return:
        """
        url = 'https://ids.zuel.edu.cn/authserver/login'
        login_api = 'api/acl_user/financeLogins'
        params={'service': self.base_url.format(login_api) }
        response = self.session.get(url, params=params)
        html = Selector(response.text)
        lt = html.xpath('//input[@id="lt"]/@value').get()
        data = {
            'rsa': self.encryptAES(username+password+lt),  # strEnc(u+p+lt , '1' , '2' , '3')
            'ul': len(username),  # u.length
            'pl': len(password),  # p.lenth
            'lt': lt,  # 网页中需要手动获取
            'execution':'e1s1',
            '_eventId':'submit',
        }
        self.session.post(url, params=params,data=data)

    def encryptAES(self, data, firstKey='1', secondKey='2', thirdKey='3'):
        # 创建引擎对象
        node = execjs.get()
        # 编译js获取上下文对象
        with open("./encrypt.js", 'r', encoding='utf8') as f:
            script = f.read()
        # 使用 execjs 类的compile()方法编译加载上面的 JS 字符串，返回一个上下文对象
        context = node.compile(script)
        # 调用eval()方法直接执行js代码
        rsa = context.call("strEnc", data, firstKey, secondKey, thirdKey)
        # rsa = context.eval("strEnc(data,'1','2','3')")
        return rsa

    def get_city_list(self):
        """
        51个城市需要按照省份分开，
        :return:
        """
        cities = ['天津', '唐山', '秦皇岛', '沧州', '大连', '丹东', '盘锦', '葫芦岛', '锦州', '营口', '上海', '南通', '连云港', '盐城', '杭州', '宁波', '嘉兴', '绍兴', '舟山', '台州', '温州', '福州', '厦门', '泉州', '漳州', '莆田', '宁德', '青岛', '东营', '烟台', '威海', '日照', '滨州', '潍坊', '广州', '深圳', '珠海', '汕头', '江门', '湛江', '惠州', '汕尾', '阳江', '东莞', '中山', '潮州', '揭阳', '茂名', '防城港', '钦州', '北海']

        pass

    def get_zw_tjnj(self):
        url='https://libvpn.zuel.edu.cn/pisdata.cnki.net/yearBook?type=type&code=A'
        response = self.session.get(url)

if __name__ == '__main__':

    zw = ZhiWangSpider()
    zw.login()

