import random

import requests
import uuid
import re
import os

# 写一个函数，为每个请求设置哈希
name_dict = {
    '计算机网络': [{'id': 2, 'name': '计算机网络'}],
    '操作系统': [{'id': 4, 'name': '操作系统'}],
    'JavaSE': [{'id': 81, 'name': 'Java基础'}, {'id': 82, 'name': 'Java集合'},
                        {'id': 83, 'name': 'Java多线程'}, {'id': 105, 'name': 'IO'}],
    'Java虚拟机': [{'id': 87, 'name': 'Java虚拟机'}],
    '数据库': [{'id': 88, 'name': 'MySQL'}, {'id': 145, 'name': '分库分表'}, {'id': 146, 'name': 'Oracle'},
                        {'id': 147, 'name': '集群'}],
    'Redis': [{'id': 89, 'name': 'Redis'}],
    'JavaEE': [{'id': 107, 'name': 'JavaWeb'}, {'id': 108, 'name': 'Spring'}, {'id': 109, 'name': 'Mybatis'},
                        {'id': 110, 'name': 'SpringBoot'}, {'id': 188, 'name': 'SpringMVC'},
                        {'id': 277, 'name': 'Tomcat'}],
    '设计模式': [{'id': 117, 'name': '设计模式'}],
    'Golang': [{'id': 119, 'name': 'Go基础'}, {'id': 120, 'name': 'Go机制'}, {'id': 121, 'name': 'Gin框架'}],
    'C++': [{'id': 123, 'name': 'C++基础'}, {'id': 124, 'name': 'C++面向对象'}, {'id': 125, 'name': 'C++ STL'},
                     {'id': 126, 'name': 'C++内存管理'}, {'id': 268, 'name': 'C语言面试题'},
                     {'id': 278, 'name': 'C++11新特性'}],
    '前端基础': [{'id': 128, 'name': 'HTML5'}, {'id': 129, 'name': 'CSS'}, {'id': 130, 'name': 'JavaScript'},
                          {'id': 189, 'name': 'Node. js'}, {'id': 254, 'name': 'ES67'},
                          {'id': 255, 'name': 'TypeScript'}],
    '消息队列': [{'id': 116, 'name': '消息队列基础'}, {'id': 134, 'name': 'Kafka'},
                          {'id': 135, 'name': 'RabbitMQ'}, {'id': 136, 'name': 'RocketMQ'}],
    '微服务': [{'id': 138, 'name': '微服务架构'}, {'id': 139, 'name': 'Nacos'},
                        {'id': 187, 'name': 'Spring Cloud'}],
    'RPC': [{'id': 141, 'name': 'RPC基础'}, {'id': 142, 'name': 'Dubbo'}],
    '分布式': [{'id': 144, 'name': 'Zookeeper'}],
    'ElasticSearch': [{'id': 152, 'name': 'ElasticSearch'}],
    'Memcached': [{'id': 154, 'name': 'Memcached'}],
    'Mongodb': [{'id': 156, 'name': 'Mongodb'}],
    '大数据': [{'id': 183, 'name': '数据仓库'}, {'id': 184, 'name': 'Hadoop'}, {'id': 185, 'name': 'HDFS'},
                        {'id': 186, 'name': 'Spark'}, {'id': 197, 'name': 'Hive'}, {'id': 198, 'name': 'Hbase'}],
    'DevOps': [{'id': 191, 'name': '日志分析 ELK'}, {'id': 192, 'name': 'DevOps原理'},
                        {'id': 193, 'name': 'Docker 容器'}, {'id': 194, 'name': 'Jenkins'},
                        {'id': 195, 'name': 'Kubernetes'}, {'id': 196, 'name': 'Logstash'}],
    '软件测试': [{'id': 200, 'name': '测试场景考核'}, {'id': 201, 'name': '测试工具考核'},
                          {'id': 202, 'name': '接口API测试'}, {'id': 203, 'name': '软件测试基础'},
                          {'id': 204, 'name': '软件性能测试'}, {'id': 205, 'name': '移动端测试'},
                          {'id': 206, 'name': '自动化测试'}],
    'Python': [{'id': 216, 'name': '语言基础'}, {'id': 217, 'name': '面向对象'},
                        {'id': 218, 'name': 'Django框架'}, {'id': 219, 'name': '数据爬虫'}],
    '数据结构与算法': [{'id': 221, 'name': '数据结构'}],
    '前端框架': [{'id': 131, 'name': 'Vue'}, {'id': 132, 'name': 'React'}, {'id': 256, 'name': 'Angular'},
                          {'id': 257, 'name': 'JQuery'}, {'id': 258, 'name': 'UniAPP'},
                          {'id': 259, 'name': '工程模块化'}],
    'Git/Maven': [{'id': 261, 'name': 'Git'}, {'id': 262, 'name': 'Maven'}],
    'Linux': [{'id': 270, 'name': 'Linux 基础面试考题'}, {'id': 271, 'name': 'Linux 命令面试考题'},
                       {'id': 272, 'name': 'Linux 日志面试考题'}, {'id': 273, 'name': 'Linux 性能 面试考题'},
                       {'id': 274, 'name': 'Nginx面试考题'}, {'id': 275, 'name': 'Vi  Vim面试考题'},
                       {'id': 276, 'name': 'Bash Shell面试考题'}],
    '算法岗': [{'id': 313, 'name': '人工智能基础'}, {'id': 314, 'name': '机器学习'}, {'id': 315, 'name': '深度学习'}]
}
session = requests.Session()
session.headers = {
    "Host": "study-api.playoffer.cn",
    "Authorization": "Bearer uFR6tgtxJodUOKQmA60coOMkPyp+TDy/srCKzHBVt4cRloT65cuzfQqnLtelIyvc0AX5af0huAVCk05CuINb/A==",
    "xweb_xhr": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129",
    "os": "android/ios",
    "Content-Type": "application/json;charset=utf-8",
    'Referer': 'https://servicewechat.com/wxff4e596908aebc12/30/page-frame.html'
}
session.verify = "./data/FiddlerRoot.pem"

def get_categorys(cid):
    url = f'https://study-api.playoffer.cn/wxQuestion/selectByCategoryId?categoryId={cid}&page=1'
    response = session.get(url).json()  # , verify=r"./data/FiddlerRoot.pem"
    return [{'title': item["title"], "answerId": item["answerId"]} for item in response["content"]["list"]]


def get_detail(aid):
    url = f'https://study-api.playoffer.cn/wxQuestion/selectAnswer?answerId={aid}'
    response = session.get(url).json()
    return response['content']


def num_to_chinese(num):
    digits = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    tens = ['十', '二十', '三十', '四十', '五十', '六十', '七十', '八十', '九十']
    if 0 <= num < 10:
        return digits[num]
    elif 10 <= num < 20:
        return '十' + digits[num % 10] if num % 10 != 0 else '十'
    elif 20 <= num <= 99:
        return tens[num // 10 - 1] + (digits[num % 10] if num % 10 != 0 else '')
    else:
        return '不支持的数字'


def main():
    pattern = re.compile(r'[<>:"/\\|?*]')
    id = 1
    for key, value in name_dict.items():
        # 创建一个名为key的md文档{:02}
        name = f'{id:02}.{pattern.sub("", key)}.md'
        file = open(f'./result/{name}', 'a', encoding='utf8')
        i=1
        for title in value:
            # 一级标题
            name_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'{key}-{title["name"]}-{title["id"]}'))
            with open('./success.txt', 'r', encoding='utf8') as f:
                lines = {line.strip() for line in f.readlines() if line}
            file.write(f'# {num_to_chinese(i)}、{title["name"]}\n')
            if name_uuid in lines:
                # print(f'{key}-{title["name"]}-{title["id"]}已爬取过了！')
                continue
            else:
                categorys = get_categorys(title['id'])
                j = 1
                i += 1
                if len(categorys) == 0:
                    print(f"{key}-{title["name"]}-{title["id"]} 爬取失败")
                    continue
                for category in categorys:
                    file.write(f'## {j:02}.{category["title"]}\n')
                    content = get_detail(category["answerId"])
                    j+=1
                    file.write(f'{content}\n')
                with open('./success.txt', 'a', encoding='utf8') as f:
                    f.write(name_uuid+'\n')

        file.close()
        id += 1


if __name__ == '__main__':
    main()