import requests  # 导入requests库，requests库中封装了模拟发送web请求的系列方法属性
import pymysql  # 导入pymsql，其中封装了python与pymysql交互的方法
import re  # 导入re模块，其中封装了处理非结构化数据的正则表达式
import time  # 处理时间的库
import random  # 处理随机数的库
import json  # 处理json对象的库，目前在web中，许多数据都是基于json字符串的方式传输。


class JdCommentSpider(object):
    # 定义京东爬虫类，相当于设计生成爬虫对象的模板
    def __init__(self):
        # 初始化定义爬虫对象时其包含的属性包括：构造的专用请求头及session对象
        self.headers={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            'Host': 'club.jd.com',
            'Referer': 'https://item.jd.com/'
        }
        self.database_name = 'remarks'
        self.session=requests.session()
        self.p = re.compile(r'[^\w，。！？,.、:；℃]')

    def get_comments(self, pid, page):
        """
        定义获取评论方法，其包含两个参数，注意两点1.发送请求后返回的响应对象不是干净的json字符串，其中包含了部分噪音数据，
        因此，需要先使用正则表达式匹配，处理成干净的json字符串后再使用json模块转化为python:json字典。
        2.京东评论显示的页码和评论数据不匹配：首先，显示50w数据，事实上仅能爬取20-30页。其次，其中包含许多空页，即该页中并没有需要的评论数据。
        当爬取到这些页面时，爬虫程序无法像处理正常请求那样运行，因此，在这里加入了try-except语句截取报错，当程序出现错误时，将输出错误内容，并继续运行。
        :param pid: 即product_id,想要爬取评论的产品id
        :param page: page:当前需要爬取到页码
        :return: 返回爬取的json对象
        """
        URL = f"https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={pid}&score=0&sortType=5&page={page}&pageSize=10&isShadowSku=0&rid=0&fold=1"
        try:
            req = self.session.get(URL, headers=self.headers, timeout=10).content.decode("GBK")
            result = json.loads(re.findall(r"\{.*\}", req)[0])
            num = result['maxPage']
            comments = result['comments']
            return result
        except:
            print(f'当前爬取到{pid}商品第{page}页')


    def parse(self, result):
        """
        定义解析数据的方法，由于传来的数据时干净的json对象，因此直接使用列表推导式直接构造新的数据结构即可。
        :param result: json对象
        :return: 返回处理干净的数据: example：[{'id':10086,'中国移动'},{'id':10000,'中国电信'},...,]
        """
        datas = [{'id': comment['id'], "content": self.p.sub("", comment["content"].lower())} for comment in result['comments']]
        return datas

    def remark_save(self, remarks, tableName='Jdcomments'):
        mysql = pymysql.connect(host='127.0.0.1', user='root', password='Password123.', port=3306, charset='utf8mb4',
                                database=self.database_name)
        db = mysql.cursor()  # 创建游标
        # database = f'-- create database if not exists {database_name} charset=utf8;'  # 创建数据库
        table = f'create table if not exists {tableName}(id bigint(15) not null primary key, content varchar(10000) default null)'
        for remark in remarks:
            print(remark)
            if remark['content'] == '':
                continue
            sql1 = f"insert into {tableName}"
            sql = sql1 + "(id, content) values (%s, %s)"
            data = (remark['id'], remark['content'])
            try:
                db.execute(table)  # 构建表
                db.execute(sql, data)  # 插入MySQL
                mysql.commit()  # 提交事务
            except Exception as e:
                print(e)
                continue
        db.close()  # 关闭游标连接
        mysql.close()  # 关闭数据库

    def main(self):
        pids = [
            '100024077586',
            '10072028591499',
            '65659245179',
            '55725680675',
            '100029079354',
            '10072041382722',
            '10072028591501',
            '100026879515',
            '100028316449',
            '10069041043802',
            '100022548791',
            '10029018449469',
            '100039235800',
            '100025287116',
            '100033323170',
            '10056076461147',
            '10069041294106',
            '10069041327371',
            '100043383775',
            '10026591482568',
            '10069220086428',
            '100018876053',
            '10072857026971',
            '100042760128','10072028591498', '10036804421232', '10072613742660', '100034089562','53881180179','10072480417072', '100012404503', '10068430017450', '100012563721', '10020113863899', '100020960551','100047032958', '100037206665', '100024077584', '100031835562','100051661047', '100019073733', '100025521045', '100026230207','10069220086425', '10030451340439', '10072593758570', '10069849666055','10030040709955','100034089500', '100052282925', '10025876346471', '10051313224465', '10069220086423', '100031668538','100019169115', '100023741140', '10072553676046', '100034753269','100041100854', '10067783808654', '100029081920', '10001240 4409', '10072041240062', '10072028591485', '100012404509', '100012404505', '10066861309196', '100034753267','10023688636618','10048541776830','100042687200', '10071153410306', '100034753265','100030757499','10071101575924', '100022734401','10072028670479', '10020114124992', '100022734315', '53749250024','10028686929291', '10066133290829', '100004882361', '10029845862616', '10062848113879', '100016239357','10053452471731', '10071476225348', '10020114125005', '100026879519', '10056444361330','10026469926363', '10044228293064', '100012529857', '10067801275538', '10068500003922', '100030757521','100052282927', '100010156881','100033451064','10072593758569','100026417371','10072722240014','100022734319', '10020114124995', '10072041382713', '100012976226','100030757511', '10072481219794', '10068089446457', '65679377860','10051609943641', '70028588654', '100054890153','100045868190','10044756340662', '100034753263', '10055267695217', '49891822157', '10071320297592', '100051258859', '10047777898832', '10029489171449', '100026879567', '10067758152331','10072593758554','10048028610107', '55725680670', '100046606634'
        ]
        for pid in pids:
            time.sleep(random.random() * 6)
            print(f"当前爬取{pid}")
            num = int(self.get_comments(pid, '1')['maxPage'])
            try:
                for j in range(num):
                    time.sleep(random.random() * 3)
                    datas = self.parse(self.get_comments(pid, str(j + 1)))
                    self.remark_save(remarks=datas)
            except:
                continue

    def test(self):
        # datas = self.get_comments(pid="10026469926363", page="1")
        res = self.get_comments(pid="10026469926363", page='1')
        print(res['maxPage'])
        # self.remark_save(remarks=datas)


if __name__ == "__main__":
    jdSpider=JdCommentSpider()
    # jdSpider.test()
    jdSpider.main()


