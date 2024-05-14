import requests
from parsel import Selector



headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}
session = requests.Session()

def download(imgs_links):
    # //scpic.chinaz.net/files/default/imgs/2023-06-21/e06f91c412a69b3c_s.jpg
    def save_img(path, datas):
        with open(path, 'wb') as f:
            f.write(datas)
    for url in imgs_links:
        img_name = './datas/imgs4/' + url.split('/')[-1]
        real_url = 'https:' + url
        content = session.get(real_url, headers=headers, timeout=10).content
        save_img(img_name, content)
        print(f"{img_name}下载成功！")

for i in range(10):
    url = 'https://sc.chinaz.com/tupian/meinvtupian.html' if i==0 else f'https://sc.chinaz.com/tupian/meinvtupian_{i+1}.html'
    print(url)
    lists = session.get(url, headers=headers, timeout=10).content
    sel = Selector(lists.decode())
    imgs_links = sel.xpath('//div[has-class("item")]/img/@data-original').getall()
    download(imgs_links)