import requests
from parsel import Selector


def get_contents(session, url):
    return session.get(url, timeout=10).content

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
base_url = f"https://sc.chinaz.com/jianli/"
session = requests.Session()
session.headers = headers
for i in range(10):
    api ='free.html' if(i ==0) else f"free_{i+1}.html"
    list = get_contents(session, base_url+api)
    sel = Selector(list.decode())
    nodes = sel.xpath('//div[@id="main"]/div/div/a/@href')
    for node in nodes:
        deatil =get_contents(session, node.get())
        sel_ = Selector(deatil.decode())
        down_url = sel_.xpath('(//div[@id="down"]//li)[4]/a/@href').get()
        name = down_url.split('/')[-1]
        print(f"{name}下载成功")
        with open(f'./datas/jianli/{name}', 'wb') as f:
            f.write(get_contents(session, down_url))

