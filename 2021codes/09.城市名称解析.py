import requests
from jsonpath import jsonpath
from parsel import Selector

urls = [
    "https://www.aqistudy.cn/historydata/",
    "https://www.lagou.com/lbs/getAllCitySearchLabels.json"
]
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
# response = requests.get(urls[0], headers=headers, timeout=10)
# sel = Selector(response.text)
# hotCityName = sel.xpath('//div[@class="hot"]/div/ul/li/a/text()').getall()
# allCityName = sel.xpath('//div[@class="all"]/div/ul/div/li/a/text()').getall()
# print(f'热门城市:\n{hotCityName}')
# print(f'全部城市:\n{allCityName}')

response_ = requests.get(urls[1],headers=headers,timeout=10).json()
print(jsonpath(response_, '$..name'))
