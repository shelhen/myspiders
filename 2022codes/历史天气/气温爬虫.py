import requests
import csv
from parsel import Selector

# citydic = {'上海': '58362', '南京': '58238', '苏州': '58357', '无锡': '58354', '常州': '58343', '扬州': '58245', '徐州': '58027', '泰州': '58246', '南通': '58259', '镇江': '58248', '淮安': '58141', '宿迁': '58131', '连云港': '58044', '盐城': '58151', '杭州': '58457', '宁波': '58465', '温州': '58659', '绍兴': '58453', '嘉兴': '58452', '台州': '58651', '金华': '58549', '湖州': '58450', '衢州': '58633', '舟山': '58477', '丽水': '58646', '合肥': '58321', '淮北': '58116', '亳州': '58102', '宿州': '58122', '蚌埠': '58221', '阜阳': '58203', '淮南': '58224', '滁州': '58236', '六安': '58311', '马鞍山': '58336', '芜湖': '58334', '宣城': '58433', '铜陵': '58429', '池州': '58427', '安庆': '58424', '黄山': '70931'}
citydic = {'北京': '54511', '天津': '54527', '石家庄': '53698', '太原': '53772', '呼和浩特': '53463', '沈阳': '54342', '长春': '54161', '哈尔滨': '50953', '上海': '58362', '南京': '58238', '杭州': '58457', '合肥': '58321', '福州': '58847', '南昌': '58606', '济南': '54823', '郑州': '57083', '武汉': '57494', '长沙': '57687', '广州': '59287', '南宁': '59431', '海口': '59758', '重庆': '57516', '成都': '56294', '贵阳': '57816', '昆明': '56778', '拉萨': '55591', '西安': '57036', '兰州': '52889', '西宁': '52866', '银川': '53614', '乌鲁木齐': '51463'}
result = []
for key, value in citydic.items():
    for year in range(2015, 2022):
        # year = 2021
        for month in range(1, 13):
            url = f'https://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D={value}&areaInfo%5BareaType%5D=2&date%5Byear%5D={year}&date%5Bmonth%5D={month}'
            data = requests.get(url).json()['data']
            sel = Selector(data)
            nodes = sel.xpath('//table[@class="history-table"]//tr[position()>1]')
            for node in nodes:
                date = node.xpath('./td[1]/text()').get().split(' ')[0]
                tem = node.xpath('./td[2]/text()').get().replace('°', '')
                if tem:
                    # with open('./datas/省会城市气温2015-2021.txt', 'a', encoding='utf8') as f:
                    #     f.write(f'{key} {date} {tem}\n')
                    print((key, date, tem))
                    result.append((key, date, tem))
                else:
                    print(url)

for item in result:
    with open('./datas/省会城市气温2015-2021.txt', 'a', encoding='utf8') as f:
        f.write(f'{item[0]} {item[1]} {item[2]}\n')
