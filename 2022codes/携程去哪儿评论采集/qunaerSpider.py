import random
import time
import re
import pymysql
import requests


def get_session():
    # 网站设置了cookie反爬，尝试模拟补充其cookie信息
    def get_csrf():
        b = "123456789poiuytrewqasdfghjklmnbvcxzQWERTYUIPLKJHGFDSAZXCVBNM"
        csft = ""
        for r in range(32):
            csft += b[int(random.random() * 1e8) % len(b)]
        return csft

    def get_cpid(QN):
        h = 0
        for c in QN:
            h = (31 * h + ord(c)) & 0xFFFFFFFF
        e = ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
        return "0" + str(0 - e) if e < 0 else "" + str(e)

    # 创建会话对象session
    session = requests.session()
    # 配置请求头
    session.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    # 创建正则规则以清洗不必要的信息。
    session.get('https://www.qunar.com/', timeout=10)
    cpid = get_cpid(session.cookies['QN1'])
    csrf = get_csrf()
    session.cookies.update({
        "unar-assist": '{%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}	',
        "QN205": "organic",
        "QN277": "organic",
        "QN267": cpid,
        "csrfToken": csrf,
    })
    return session


def get_comments(session, pid, index):
    # 爬取太快会遭到网站暂时断开链接
    url = f'https://piao.qunar.com/ticket/detailLight/sightCommentList.json'
    params = {
        'sightId': pid,
        'index': index,
        'page': index,
        'pageSize': 10,
        'tagType': 0
    }
    return session.get(url, params=params)


def parse_comments(xhr):
    p = re.compile(r'[^\w，。！？,.、:；℃]')
    result = xhr.json()["data"]['commentList']
    comments = [{
        "publishTime": time.mktime(time.strptime(data["date"], "%Y-%m-%d")),
        "score": data['score'],
        "content": p.sub("", data["content"].lower()),
        "Locate": data['replyCityName']
    } for data in result]
    return comments


def save_comments(database_name, username, password, table_name, comments):
    mysql = pymysql.connect(host='127.0.0.1', user=username, password=password, port=3306,
                            charset='utf8mb4', database=database_name)
    # 创建游标
    db = mysql.cursor()
    table = f'create table if not exists {table_name}(id int not null primary key auto_increment, score int(3) default 0, content varchar(9000) default null, location varchar(20) default null, datetime int(10) default 0)'
    for comment in comments:
        # 若内容为空则不进行保存
        if comment['content'] == '':
            continue
        sql = f"insert into {table_name}"
        sql_str = sql + "(score,content,location,datetime) values (%s,%s,%s,%s)"
        data = (comment['score'], comment['content'], comment['Locate'], comment['publishTime'])
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


def main(pid, database_name, username, password, table_name):
    session = get_session()
    total_count = int(get_comments(session, pid, 2).json()['data']['commentCount'])
    pages = total_count // 10 if total_count % 10 == 0 else (total_count // 10) + 1
    print(f'合计{total_count}条评论，需要爬取{pages}页。')
    for i in range(pages):
        time.sleep(random.random() * 2 + 1)
        xhr = get_comments(session, pid, i + 1)
        comments = parse_comments(xhr)
        save_comments(database_name, username, password, table_name, comments)


if __name__ == '__main__':
    # 泰山景区id
    pid = '11414'
    # 配置数据库信息
    database_name = 'remarks'
    username = 'root'
    password = 'Password123.'
    table_name = 'qunaer'
    main(pid, database_name, username, password, table_name)

