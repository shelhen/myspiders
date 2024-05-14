import requests  # 导入requests库，requests库中封装了模拟发送web请求的系列方法属性
from parsel import Selector
import pymysql  # 导入pymsql，其中封装了python与pymysql交互的方法
import re  # 导入re模块，其中封装了处理非结构化数据的正则表达式
import time  # 处理时间的库
import random  # 处理随机数的库
from urllib.parse import quote


class JDcommentsSpider(object):
    def __init__(self):
        self.session = requests.session()
        self.session.headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
        }
        # 设置数据库信息
        self.database_name = 'remarks'
        self.username = 'root'
        self.password = 'Password123.'
        self.tablename = 'jd'

    def get_sku_ids(self, keyword):
        search_url = f'https://search.jd.com/Search?keyword={quote(keyword)}'
        html = self.session.get(search_url).text
        sel = Selector(html)
        return sel.xpath('//div[@id="J_goodsList"]/ul/li/@data-sku').getall()

    def get_comments(self, pid, index):
        uuid = f'122270672.{int(time.time()*1000)}{int(2147483647 * random.random())}.{int(time.time())}.{int(time.time())}.{int(time.time())}.3'
        url = (f'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client'
               f'=pc&clientVersion=1.0.0&t={int(time.time()*1000)}&loginType=3&uuid={uuid}&productId={pid}&score=0&sortType=5&page={index}&pageSize=10&isShadowSku=0&rid=0&fold=1&bbtf=&shield=')
        return self.session.get(url)

    def parse_comments(self, json):
        p = re.compile(r'[^\w，。！？,.、:；℃]')
        datas = json.json()['comments']
        comments = [{"content": p.sub("", comment["content"].lower()),
                     'datetime': time.mktime(time.strptime(comment["creationTime"], "%Y-%m-%d %H:%M:%S")),
                  'location': comment.get('location') if comment.get('location') != None else '中国'}
                 for comment in datas]
        return comments

    def save_comments(self, comments):
        mysql = pymysql.connect(host='127.0.0.1', user=self.username, password=self.password, port=3306,
                                charset='utf8mb4', database=self.database_name)
        db = mysql.cursor()
        table = f'create table if not exists {self.tablename}(id int not null primary key auto_increment, content varchar(256) not null unique, location varchar(20) default null, datetime int(10) default 0)'
        for comment in comments:
            # 若内容为空则不进行保存
            if (comment['content'] == '') or (comment['location']=='中国'):
                continue
            sql = f"insert into {self.tablename}"
            sql_str = sql + "(content,location,datetime) values (%s,%s,%s)"
            data = (comment['content'], comment['location'], comment['datetime'])
            print(data)
            try:
                # db.execute(database)  # 创建数据库
                db.execute(table)  # 构建表
                db.execute(sql_str, data)  # 插入MySQL
                mysql.commit()  # 提交事务
            except Exception as e:
                print(e)
                continue
        db.close()  # 关闭游标连接
        mysql.close()  # 关闭数据库


if __name__ == '__main__':
    keyword = '颐莲喷雾'
    jds = JDcommentsSpider()
    pids = jds.get_sku_ids(keyword)
    for pid in pids[:5]:
        for i in range(40):
            time.sleep(1 + random.random())
            print(pid, i)
            json = jds.get_comments(pid, i + 1)
            try:
                comments = jds.parse_comments(json)
                jds.save_comments(comments)
            except Exception as e:
                print(e)
                break

