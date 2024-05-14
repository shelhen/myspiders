import requests

url = 'https://baike.baidu.com/item/%E5%8F%B6%E8%B5%AB%E8%80%81%E5%A5%B3'

sessions = requests.Session()
headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Host":"baike.baidu.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
}

sessions.headers=headers
response = sessions.get(url)
print(response.content.decode('gb2312'))