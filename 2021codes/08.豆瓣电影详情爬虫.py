import requests
from parsel import Selector
import json
import re


class DoubanSpider(object):
    def __init__(self):
        self.headers ={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Host": "movie.douban.com"
        }
        self.session = requests.Session()
        self.type = {}
        self.base_url = "https://movie.douban.com/"

    def get_pages(self, api, params=None):
        response = self.session.get(self.base_url + api, headers=self.headers, params=params, timeout=10)
        return response

    def get_movie_type(self):
        api = 'typerank'
        params={'type_name':'爱情', "type":13, "interval_id":"100:90", "action":''}
        type_response = self.get_pages(api,params)
        sel = Selector(type_response.text)
        aNodes = sel.xpath('//div[@class="types"]/span/a')
        for node in aNodes:
            typeid_match = re.search('type=(\d+)', node.attrib['href'])
            try:
                typeid =typeid_match.group(1)
                self.type[typeid] = node.xpath('./text()').getall()[0]
            except Exception as e:
                print(node.xpath('./text()').getall()[0])
                print('获取类型失败')
                print(e)

    def get_movie_list(self, type, start,limit):
        api = 'j/chart/top_list'
        params={
            "type": type,
            "interval_id": "100:90",
            "action": '',
            'start': start,
            'limit': limit
        }
        response = self.get_pages(api, params).json()
        movies =[]
        for movie in response:
            id = movie['id']
            # detail_url = movie['url']
            attr, desc = self.get_dec(id)
            movies.append({
                'rank': movie['rank'],
                'cover': movie['cover_url'],
                'title': movie['title'],
                'id': id,
                'attr':attr,
                'types': '/'.join(movie['types']),
                'score': movie['score'],
                'vote_count': movie['vote_count'],
                'release_date': movie['release_date'],
                'desc':desc

            })
        return movies

    def get_dec(self, id):
        api = f"subject/{id}/"
        response = self.get_pages(api)
        sel = Selector(response.text)
        attr = sel.xpath('(//span[@class="attrs"])[1]//text()').get()
        # 优先获取hide/没有话再取得【1】
        descNodes = sel.xpath('//div[@id="link-report-intra"]/span')
        desc = descNodes.css('span::text, span[class*=all]::text').getall()
        desc = self.desc_parse(desc)
        return attr, desc

    def desc_parse(self, desc):
        desc_ = ''
        if type(desc) == list:
            for des in desc:
                des = des.replace('\n', '').replace(' ', '')
                desc_ += '  ' + des + '\n'
        else:
            desc_ = desc
        return desc_

    def get_total_nums(self, type):
        api = 'j/chart/top_list_count'
        params = { "type": type, "interval_id": "100:90"}
        pages = self.get_pages(api, params).json()
        total = int(pages['total'])
        return total

    def test(self):
        id,name = 13, '爱情'
        i, limit = 0, 20
        type_movies = self.get_movie_list(id, i * 20, limit)
        # for mv in type_movies:
        #     print(mv)

    def save_to_json(self, path, datas):
        json.dump(datas, open(path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

    def main(self):
        result = {}
        self.get_movie_type()
        for id, name in self.type.items():
            result[name] = []
            total = self.get_total_nums(id)
            for i in range(total//20+1):
                limit = 20 if (total - i*20)>20 else total-i*20
                type_movies = self.get_movie_list(id, i*20, limit)
                for data in type_movies:
                    print(f"{data['title']}存储完毕")
                result[name].extend(type_movies)
        self.save_to_json('./datas/movies.json', result)


if __name__ == '__main__':
    ds = DoubanSpider()
    # ds.test()
    ds.main()