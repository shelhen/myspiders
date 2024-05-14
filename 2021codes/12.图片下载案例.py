import requests
from parsel import Selector
import os

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

def save_img(path, datas):
    with open(path, 'wb') as f:
        f.write(datas)

base_url = 'https://pic.netbian.com'
for i in range(10):
    api = '/4kmeinv/index.html' if i ==0 else f"/4kmeinv/index_{i+1}.html"
    lists = requests.get(base_url+ api, headers=headers, timeout=10).content
    sel = Selector(lists.decode('gbk'))
    # /uploads/allimg/230619/002708-1687105628cd1d.jpg
    imgs_links = sel.xpath('//div[@class="slist"]/ul/li/a/img/@src').getall()
    for url in imgs_links:
        img_name = './datas/imgs3/' + url.split('/')[-1]
        real_url = base_url+url
        # headers[] = ''
        content = requests.get(real_url, headers=headers, timeout=10).content
        save_img(img_name, content)
        print(f"{img_name}下载成功！")