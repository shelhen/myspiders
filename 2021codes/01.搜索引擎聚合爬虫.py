import requests
from parsel import Selector
import time
import random


class SearchSpider(object):
    def __init__(self, keyword):
        self.keyword = keyword
        self.session = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.3"
        }

    def search_by_baidu(self, keyword):
        self.session.get('https://www.baidu.com/',headers=self.headers)
        params = { 'ie': 'UTF-8', 'wd': keyword}
        response = self.session.get('https://www.baidu.com/s', headers=self.headers, timeout=10, params=params)
        sel = Selector(response.text)
        divNodes = sel.xpath('//div[@id="content_left"]').xpath('./div[contains(attribute::*,"result")]')
        results=[]
        for need in divNodes:
            result = need.xpath('.//h3//em/..//text()').getall()
            if result:
                text = ''.join(result)
                results.append('百度搜索结果：'+ text.replace('\n', '').strip(' '))
        return results

    def search_by_sogo(self, keyword):
        response = self.session.get('https://www.sogou.com/',headers=self.headers,timeout=10)
        sel = Selector(response.text)
        formNoe = sel.xpath('//form[@id="sf"]')
        ts = int(1e3 *(1e3*time.time() + random.random()))
        self.session.cookies.update({'SUV': str(ts)})
        w = formNoe.xpath('./input[@name="w"]').attrib['value']
        p = formNoe.xpath('./input[@name="p"]').attrib['value']
        params={
           'query':keyword,
            "_asf":'www.sogou.com',
            "_ast":'',
            'w':w,
            'p':p,
            'ie':'utf8',
            'from':'index-nologin',
            's_from':'index',
            "sut":'now-inputtime',
            'sst0':int(time.time()*1e3),  # now
            'lkt':f"{len(keyword)},{int(time.time()*1e3)-554-204*len(keyword)},{int(time.time()*1e3)-554}",
            'sugsuv':ts,
            'sugtime':int(time.time()*1e3)
        }
        response = self.session.get('https://www.sogou.com/web',headers=self.headers,timeout=10,params=params)
        sel = Selector(response.text)
        aNodes = sel.xpath("//div[@class='results']//h3/a")
        results = []
        for need in aNodes:
            result = need.xpath('.//em/..//text()').getall()
            if result:
                text = ''.join(result)
                results.append('搜狗搜索结果：'+ text.replace('\n', '').strip(' '))
        return results


    def search_by_360(self, keyword):
        params = {'ie': 'utf-8', 'q':keyword}
        self.session.get("https://www.so.com/",headers=self.headers,timeout=10)
        response =self.session.get("https://www.so.com/s", headers=self.headers, params=params, timeout=10)
        sel = Selector(response.text)
        h3Nodes = sel.xpath("//ul[@class='result']//h3")
        results = []
        for need in h3Nodes:
            result = need.xpath('.//em/..//text()').getall()
            if result:
                text = ''.join(result)
                # print(text.replace('\n', '').strip(' '))
                results.append('360搜索结果：' + text.replace('\n', '').strip(' '))
        return results


    def main(self):
        result = []
        baidu_res = self.search_by_baidu(self.keyword)
        sougo_res = self.search_by_sogo(self.keyword)
        s60_res = self.search_by_360(self.keyword)
        result.extend(baidu_res)
        result.extend(sougo_res)
        result.extend(s60_res)
        for res_ in set(result):
            print(res_)


if __name__ == '__main__':
    seach = SearchSpider('Python')
    seach.main()