import requests
import random
import time
import json
import pymysql
import re


class XieChengRemarkSpider(object):

    def __init__(self, placeid):
        self.placeId = placeid
        # 创建session实例
        self.session = requests.session()
        # 设置请求头
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/110.0.0.0 Safari/537.36'
        }
        # 设置数据库信息
        self.database_name = 'remarks'
        self.username = 'root'
        self.password = 'Password123.'
        self.tablename = 'xiecheng'

    def get_pid(self):
        url = f"https://you.ctrip.com/sight/xuzhou230/{self.placeId}.html"
        response = self.session.get(url, timeout=10)
        pid = re.findall(',"poiId":([\d]+)', response.content.decode())[0]
        return pid

    def get_remarks(self, pid, index):
        """
        :param index: 当前爬取页数
        :return: remarks评论响应结果
        """
        # 获取关键参数并且补充请求cookie信息
        guid = self.session.cookies['GUID']
        # x_traceID = ‘_fxpcqlniredt -’+timestamp + '-' + 随机数
        url = f"https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt={guid}&x-traceID={guid}-{round(time.time() * 1000)}-{int(1e6 * random.random())}"
        post_data = {
            "arg": {"channelType": 2, "collapseType": 0, "commentTagId": 0, "pageIndex": index, "pageSize": 10,
                    "poiId": pid, "sourceType": 1, "sortType": 3, "starType": 0},
            "head": {"cid": guid, "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                     "syscode": "09", "auth": "", "xsid": "", "extension": []}
        }
        return self.session.post(url, data=json.dumps(post_data), timeout=10)

    def parse_remarks(self, xhr):
        # 文本清洗特殊字符的正则表达式
        p = re.compile(r'[^\w，。！？,.、:；℃]')
        result = xhr.json()["result"]['items']
        remarks = [{
            'score': item['score'],
            'content': p.sub('', item['content'].lower()),
            'Locate': item['ipLocatedName'],
            'publishTime': int(item['publishTime'][6:16])
        } for item in result]
        # 注意这时存在某些'content'实际为空值
        return remarks

    def save_remarks(self, remarks):
        mysql = pymysql.connect(host='127.0.0.1', user=self.username, password=self.password, port=3306,
                                charset='utf8mb4', database=self.database_name)
        # 创建游标
        db = mysql.cursor()
        table = f'create table if not exists {self.tablename}(id int not null primary key auto_increment, score int(3) default 0, content varchar(256) not null unique, location varchar(20) default null, datetime int(10) default 0)'
        for remark in remarks:
            # 若内容为空则不进行保存
            if remark['content'] == '':
                continue
            sql = f"insert into {self.tablename}"
            sql_str = sql + "(score,content,location,datetime) values (%s,%s,%s,%s)"
            data = (remark['score'], remark['content'], remark['Locate'], remark['publishTime'])
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
    xcrs = XieChengRemarkSpider('56337')
    pid = xcrs.get_pid()
    total_count = int(xcrs.get_remarks(pid, 1).json()['result']['totalCount'])
    # 总评论页码数除以10如果能够整除就不用加一，如果不能整除，需要取整并且加一
    pages = total_count // 10 if total_count % 10 == 0 else (total_count // 10) + 1
    print(f'合计{total_count}条评论，需要爬取{pages}页。')

    for i in range(80):
        time.sleep(random.random()*0.6)
        xhr = xcrs.get_remarks(pid, i+1)
        try:
            remarks = xcrs.parse_remarks(xhr)
            xcrs.save_remarks(remarks)
        except Exception as e:
            time.sleep(10 + random.random()*5)
            print(e)
            break
