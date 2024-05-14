import pymysql
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def remark_save(tableName,remarks):
    """
    :param remarks:
    [{id,score,content,up,scores,time}]
    :return:
    """
    database_name = 'remarks'
    mysql = pymysql.connect(host='127.0.0.1', user='root', password='Password123.', port=3306, charset='utf8mb4',
                            database=database_name)
    db = mysql.cursor()  # 创建游标
    # database = f'-- create database if not exists {database_name} charset=utf8;'  # 创建数据库
    table = f'create table if not exists {tableName}(id int not null primary key auto_increment, score int(3) default 0, content varchar(6000) default null, up int(3) default 0, location varchar(20) default null, datetime int(10) default 0)'
    for remark in remarks:
        if remark['content']=='':
            continue
        sql1 = f"insert into {tableName}"
        sql = sql1 + "(score,content,up,location,datetime) values (%s,%s,%s,%s,%s)"
        data = (remark['score'], remark['content'], remark['usefulCount'], remark['Locate'], remark['publishTime'])
        try:
            # db.execute(database)  # 创建数据库
            db.execute(table)  # 构建表
            db.execute(sql, data)  # 插入MySQL
            mysql.commit()  # 提交事务
        except Exception as e:
            print(e)
            continue
    db.close()  # 关闭游标连接
    mysql.close()  # 关闭数据库


def get_cookie(url):
    # 这里配置驱动参数，如增加代理和UA信息
    opt = webdriver.ChromeOptions()
    # 增加代理和UA信息
    # opt.add_argument('--proxy-server=http://223.96.90.216:8085')
    opt.add_argument(
        '--user-agent=' + "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    # 创建webdriver实例
    driver = webdriver.Chrome(r'C:\chromedriver.exe', chrome_options=opt)

    driver.get(url)
    time.sleep(3)
    # 往下翻动以便于触发所有动作
    cookielist = driver.get_cookies()
    cookies = {cookie['name']:cookie['value'] for cookie in cookielist}
    driver.quit()
    return cookies
