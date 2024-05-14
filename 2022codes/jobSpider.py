import random
import requests
import re
import time

base_url = 'https://www.chinahr.com'
data = {
    'keyWord': "",
    'localId': "1",
    "maxSalary": 'null',
    'minSalary': 'null',
    'page': 0,
    'pageSize': '20'
}
headers={
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
    'Referer': 'https://www.chinahr.com/job',
    'Origin': 'https://www.chinahr.com'
}
page = 191
result = []


def get_jb_ids(i, flag=False):
    api = '/newchr/open/job/search'
    data['page']= i
    response = requests.post(base_url + api, json=data,headers=headers)
    # 这里可以获取所有需要的信息。
    if flag:
        jb_ids=[(item['salary'], item['degree'], item['workExp']) for item in response.json()['data']['jobItems']]
    else:
        jb_ids = [item['jobId'] for item in response.json()['data']['jobItems']]
    return jb_ids


def get_page(id:str):
    api = '/detail/'+id
    html = requests.get(base_url+api, headers=headers).text
    salary = re.search(r'<span class="detail-top_left-title-salary" data-v-\w{8}>([-/\w\.]+)</span>', html).group(1)
    p_info = re.compile(r'<span data-v-\w{8}>([\u4E00-\u9FFF\d]+)\s<i data-v-\w{8}')
    info = p_info.findall(html)
    if len(info)==1:
        degree = '无'
        workExp = info[0]
    else:
        degree=info[0]
        workExp=info[1]
    return salary, workExp, degree


def save(result:list):
    with open('result.csv', 'w', encoding='utf8') as f:
        f.write('\n'.join(result))


def main():
    for i in range(0, page):
        print(f'第{i+1}页')
        jb_ids = get_jb_ids(i)
        for id in jb_ids:
            time.sleep(random.random()*2)
            salary, workExp, degree = get_page(id)
            print(f'{salary},{degree},{workExp}')
            result.append(f'{salary},{degree},{workExp}')


def test():
    for i in range(0, page):
        print(f'第{i+1}页')
        jb_ids = get_jb_ids(i, flag=True)
        for jb in jb_ids:
            print(jb)
            result.append(f'{jb[0]},{jb[1]},{jb[2]}')

# 基于正则爬取
main()
# 基于json爬取，推荐这个。
# test()
save(result)




