import requests
import json

class MovieSpider(object):
    def __init__(self):
        self.url='https://spa1.scrape.center/api/movie/'
        self.session = requests.session()
        self.limit = 10
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    def get_details(self, num):
        response = self.session.get(self.url + f"{num}/", headers=self.headers, timeout=10).json()
        movie = {
            'cover': response['cover'],
            'name': response['name'] + '-' + response['alias'],
            'categories': '/'.join(response['categories']),
            'published_at': response['published_at'],
            'drama': response['drama'],
            'score': response['score']
        }
        print(movie)
        return movie

    def save_txt(self, path, data):
        with open(path, 'w', encoding='utf8') as f:
            f.write(json.dumps(data))

    def main(self):
        movies = [self.get_details(i+1) for i in range(100)]
        self.save_txt('./datas/movies.txt', {'movies': movies})



if __name__ == '__main__':
    ms = MovieSpider()
    ms.main()


