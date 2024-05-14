import requests
from parsel import Selector
import re

class NodeSpider(object):
    def __init__(self):
        self.session= requests.session()
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.base_url = 'https://www.shicimingju.com/'
        self.partten = re.compile(r'[^\w，。！？,.、:；℃“”"’\']')

    def get_pages(self, url):
        response = self.session.get(url, headers=self.headers, timeout=10)
        return response.content.decode()

    def parse_list(self, content):
        sel = Selector(content)
        aNodes = sel.xpath('//div[@class="book-mulu"]/ul/li/a')
        lists = [{
            'name':anode.xpath('./text()').getall()[0],
            'url':self.base_url[:-1] + anode.attrib['href']
             }for anode in aNodes]
        return lists

    def parse_chapter(self, page):

        sel = Selector(page)
        content = sel.xpath('//div[@class="chapter_content"]/text()|//div[@class="chapter_content"]/p/text()').getall()
        text = ''
        for con in content:
            # 去除多余的空格
            con = con.replace(' ','').replace('\n', '')
            # 去除特殊符号
            con = self.partten.sub("", con.lower())
            # 补充段落标记
            text += '   ' + con + '\n\n'

        return text

    def main(self):
        list_url = self.base_url + 'book/sanguoyanyi.html'
        list_content = self.get_pages(list_url)
        lists = self.parse_list(list_content)
        for chapter in lists:
            title = chapter['name']
            page = self.get_pages(chapter['url'])
            content = self.parse_chapter(page)
            data = f"\n\n{title}\n\n" + content
            print(data)
            self.save('./datas/三国演义.txt',data)

    def save(self, path, data):
        with open(path,'a',encoding='utf8') as f:
            f.write(data)


if __name__ == '__main__':
    ns = NodeSpider()
    ns.main()





