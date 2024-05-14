import requests
import re
from urllib.parse import urljoin


class MoviesSpiders(object):

    def __init__(self):
        self.session = requests.session()
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.account = 'admin'
        self.pwd = 'admin'
        self.totalpages=10
        self.url = "https://login2.scrape.center/"

    def login(self, login_url):
        self.session.get(login_url,headers=self.headers,timeout=10)
        data={ 'username': self.account, 'password': self.pwd}
        response = self.session.post(login_url,headers=self.headers,data=data,timeout=10)
        print()
        if "https://login2.scrape.center/"==response.request.url:
            return True
        else:
            return False

    def parse_detail(self, html):
        cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
        name_pattern = re.compile('<h2.*?>(.*?)</h2>')
        categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
        published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
        drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
        score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)
        cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None
        name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
        categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []
        published_at = re.search(published_at_pattern, html).group(1) if re.search(published_at_pattern, html) else None
        drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
        score = float(re.search(score_pattern, html).group(1).strip()) if re.search(score_pattern, html) else None
        return {
            'cover': cover,
            'name': name,
            'categories': '/'.join(categories),
            'published_at': published_at,
            'drama': drama,
            'score': score
        }

    def parse_index(self, html):
        pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
        items = re.findall(pattern, html)
        if not items:
            return []
        for item in items:
            detail_url = urljoin(self.url, item)
            yield detail_url

    def scrape_page(self, url):
        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text

    def scrape_index(self, page):
        index_url = f'{self.url[:-1]}/page/{page}'
        return self.scrape_page(index_url)

    def scrape_detail(self, url):
        return self.scrape_page(url)

    def save_to_csv(self, path, datas, mode='w'):
        '''
        :param path:
        :param data: [{},{},{},...]
        :param mode:
        :return:
        '''
        import csv
        with open(path, mode, encoding='utf-8', newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['name', 'categories', 'published_at','score','cover','drama'])
            writer.writeheader()
            # for data in datas:
            writer.writerow(datas)

    def main(self):
        login_url = 'https://login2.scrape.center/login'
        flag = self.login(login_url)
        if flag:
            result = []
            for page in range(1, self.totalpages + 1):
                index_html = self.scrape_index(page)
                detail_urls = self.parse_index(index_html)
                for detail_url in detail_urls:
                    detail_html = self.scrape_detail(detail_url)
                    data = self.parse_detail(detail_html)
                    print(data)
                    result.append(data)
            self.save_to_csv('./datas/doubanmovie2.csv',result)
        else:
            print('模拟登陆失败，请重试！')


if __name__ == '__main__':
    ws = MoviesSpiders()
    ws.main()