import requests
from parsel import Selector

def get_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        'Referer':'https://blog.sina.com.cn/s/blog_01ebcb8a0102zi2o.html?tj=1'
    }
    return requests.get(url, headers=headers,timeout=10).content

def save_img(path, datas):
    with open(path, 'wb') as f:
        f.write(datas)

html = get_content("https://blog.sina.com.cn/s/blog_01ebcb8a0102zi2o.html?tj=1")
sel = Selector(html.decode())
Nodes = sel.xpath('//div[@id="sina_keyword_ad_area2"]/div/a/img')
url_list = [node.attrib['real_src'] for node in Nodes]
for url in url_list:
    img_name = './datas/imgs2/' + url.split('/')[-1] + '.jpg'
    content = get_content(url)
    save_img(img_name, content)
    print(f"{img_name}下载成功！")
