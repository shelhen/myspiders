import requests
import pymysql

url='https://s.ccxe.com.cn/api/companies/search'


def saveInfo(result):
    """
    :param result:
    :return:
    """
    with open("result.txt", "a") as f:
        f.write(result)



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}


params={
    'province': '江苏省',
    'induSmaPar': '',
    'sartTime': '',
    'endTime': '',
    'minRegCap': '',
    'maxRegCap':'' ,
    'orgSta': '',
    'orgAttr': '',
    'curyName': '',
    'years': '',
    'tel': '',
    'mail': '',
    'comWeb': '',
    'orgChaStatus': '',
    'orgEquityStatus': '',
    'taxViolStatus': '',
    'envirViolStatus': '',
    'macLandMortStatus': '',
    'orgMortgageStatus': '',
    'orgOperAbndStatus': '',
    'orgPunishmentStatus': '',
    'keyword': '',
    'pageNum': 1,
    'pageSize': 30,
    'source': 'person',
}

for i in range(34):
    params['pageNum']=i+1
    response = requests.get(url=url,params=params,headers=headers,timeout=10).json()['data']['list']
    for item in response:
        if item['extra'] == {}:
            continue
        try:
            industry=item['induSmaPar']
            name = item['name']
            stkCode= item['extra']['stkCode']
            stkUniCode = item['extra']['stkUniCode']
        except:
            continue
        res = f"{stkCode} {stkUniCode} {industry} {name}\n"
        print(res)
        saveInfo(res)

