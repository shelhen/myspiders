import requests
from parsel import Selector
import json
import re


class MoviesSpiders(object):

    def __init__(self):
        self.session = requests.session()
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.url="https://ssr1.scrape.center/"

    def get_list(self, num):
        url = f"https://ssr1.scrape.center/page/{num + 1}"
        lists = self.session.get(url,headers=self.headers,timeout=10)
        listsel = Selector(lists.text)
        anodes = listsel.xpath('//a[@class="name"]')
        hrefs = (node.attrib['href'] for node in anodes)
        return hrefs

    def get_pages(self, href):
        movie = {}
        details = self.session.get(self.url + href[1:], headers=self.headers, timeout=10)
        detailsel =  Selector(details.text)
        divNode = detailsel.xpath('//div[@class="el-card__body"]/div/div')
        movie['cover'] = divNode.xpath('//img[@class="cover"]').attrib['src']
        movie['score'] = divNode.css('p[class*="score"]::text').getall()[0].replace('\n','').replace(' ','')
        movie['name'] = divNode.xpath('./a/h2/text()').get()
        movie['categories'] = divNode.xpath('./div[@class="categories"]/button/span/text()').getall()
        infos = ''.join(divNode.xpath('./div/span/text()').getall()).replace('/n','').replace(' ','')
        publish = re.search('(\d{4}-\d{2}-\d{2})',infos)
        movie['time'] = publish.group() if publish else '未知'
        movie['describe'] = divNode.xpath('./div[@class="drama"]/p/text()').get().replace('\n','').replace(' ','')
        print(movie)
        return movie

    def save(self,path, data):

        json.dump(data, open(path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

    def main(self):
        path = './datas/doubanmovie.json'
        # 首先发起访问获取总页数
        pre_response = self.session.get(self.url,headers=self.headers)
        presel = Selector(pre_response.text)
        pageNum = presel.xpath('//span[@class="el-pagination__total"]/text()').getall()[0]
        pageNum = re.search(r'\d+', pageNum).group()
        num = int(pageNum)//10
        result=[]
        for i in range(num):
            hrefs = self.get_list(i)
            movies = [self.get_pages(href) for href in hrefs]
            result.extend(movies)
        self.save(path, result)


if __name__ == '__main__':
    ms = MoviesSpiders()
    ms.main()