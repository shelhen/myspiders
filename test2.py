import requests


num = 1
res = requests.get('https://www.baidu.com')
print(res.content.decode())