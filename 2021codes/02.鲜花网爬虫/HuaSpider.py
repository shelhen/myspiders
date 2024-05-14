import time
import requests
from lxml import etree
from datetime import datetime
import pymysql  # MySQL操作
import hashlib
import os
import random


class HuaSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        self.session = requests.session()
        self.urls = {
            1: 'https://www.hua.com/aiqingxianhua/',
            6: 'https://www.hua.com/daoqianxianhua/',
            5: 'https://www.hua.com/tanbingweiwenxianhua/',
        }
        self.goodsUrls = {
            1: 'https://www.hua.com/aiqingxianhua/',
            2: 'https://www.hua.com/businessFlower/kaiyehualan/',
            3: ['https://www.hua.com/youqingxianhua/', 'https://www.hua.com/zhufuqinghexianhua/'],
            4: ['https://www.hua.com/songzhangbeixianhua/', 'https://www.hua.com/songlaoshixianhua/'],
            5: 'https://www.hua.com/tanbingweiwenxianhua/',
            6: 'https://www.hua.com/daoqianxianhua/',
            7: ['https://www.hua.com/hunqingxianhua/','https://www.hua.com/zhufuqinghexianhua/'],
        }
        self.pageNum = 20  # 爬取的花语新闻页码数目，不应超过43
        self.projectPath = 'C:\\CodesHub'
        self.stock = 100
        self.database = 'flower'
        self.username = 'root'
        self.pwd = 'Password123.'

    def get_news(self):
        # for i in range(self.pageNum):
        for i in range(self.pageNum):
            res = self.session.get("https://www.hua.com/huayu/huayu" + str(i + 1) + '.html', headers=self.headers,
                                   timeout=10)
            html = etree.HTML(res.text)
            nodes = html.xpath('//div[@class="Item_Brief"]/a')
            try:
                datas = [self.get_content(node.xpath('./@href')[0][7:12],
                                          node.xpath('./text()')[0].replace('中国鲜花礼品网（花礼网）', '花里有花鲜花网')) for
                         node in nodes]
            except:
                continue
            # print(datas)
            self.save_news(datas)
            print(f'保存第{i + 1}页花语新闻成功')

    def get_content(self, id, intro):
        # 实际href = https: // www.hua.com / huayu / + id +.html
        new_url = "https://www.hua.com/huayu/" + str(id) + ".html"
        res = self.session.get(new_url, headers=self.headers, timeout=10)
        html = etree.HTML(res.text)
        title = html.xpath('//div[@class="title"]/h4/text()')[0]

        article = html.xpath('//div[@class="article"]')[0]
        text_nodes = article.xpath('//div[@class="article"]//text()')
        text = ''
        for text_node in text_nodes:
            text_node = text_node.replace('\r', '').replace('\n', '').replace('\t', '').replace('花礼网',
                                                                                                ' 花里有花网 ').replace(
                ' ', '').replace(' ','')
            text += text_node
        img_nodes = article.xpath('./p//img/..|./div//img/..')
        if img_nodes != []:
            imgs = []
            for node in img_nodes:
                try:
                    target_id = node.xpath('./@href')[0][9:16] if not node.xpath('./@href')==[] else '9999999'
                    img_url = self.save_img("floweryland", 'https:' + node.xpath('.//img/@data-original')[0])
                except:
                    continue
                imgs.append({
                    "id": target_id,
                    "img_url":img_url
                })
            return [id, title, intro, text, imgs]

    def get_detail(self, url):
        ''' 保存详情页上的部分数据 '''
        res = self.session.get(url, headers=self.headers, timeout=10).text
        html = etree.HTML(res)
        detail = html.xpath('//div[@class="huayu"]/div[2]/p/text()')[0]
        material = html.xpath('//div[@class="huayu"]/div[3]/p/text()')[0]
        pack = html.xpath('//div[@class="huayu"]/div[4]/p/text()')[0]
        caption = html.xpath('//span[@class="title-point"]/text()')[0][1:-1] if html.xpath(
            '//span[@class="title-point"]/text()') != [] else str(datetime.now())[0:4] + "畅销热卖款"
        # print(detail,material,pack)
        img_urls = html.xpath('//div[@class="preview-list-item"]/img/@src')
        images = [self.save_img("products", 'https:' + img_url) for img_url in img_urls]
        imgNodes = html.xpath(
            '//div[@class="detail-product-content"]/img|//div[@class="detail-product-content"]/p/img|//div[@class="detail-product-content"]/div/img')
        detailimgs = [self.save_img("details", 'https:' + imgNode.xpath('./@data-original')[0]) for imgNode in imgNodes]
        return caption, detail, material, pack, images, detailimgs[:-1]

    def get_page_num(self, url):
        res = self.session.get(url, headers=self.headers, timeout=10)
        html = etree.HTML(res.text)
        page = int(html.xpath('//p[@class="total-page"]/text()')[0][2])
        for i in range(page):
            return url+"?r=0&pg="+str(i+1)

    def get_product_info(self, url, category_id):
        """每页只爬取第一页数据数据测试使用"""
        datas = []  # 空列表
        res = self.session.get(url, headers=self.headers, timeout=10)
        html = etree.HTML(res.text)
        itemcodes = ''
        for i in html.xpath('//span/@data-pp'):  # //span/@data-pp
            itemcodes += i + ','
        self.session.get('https://www.hua.com/home/CheckAgent', headers=self.headers, timeout=10)
        products = self.session.post('https://www.hua.com/home/GetProductListPrice', headers=self.headers,
                                     data={'itemcodes': itemcodes, 'perf': ''}, timeout=10).json()
        for product in products['Datas']['ProductPrices']:
            try:
                caption, detail, material, pack, images, detailimgs = self.get_detail(
                    'https://www.hua.com//product/' + product['ItemCode'] + '.html')
                default_image = self.save_img("products",
                                              'https://img01.hua.com/uploadpic/newpic/' + product['ItemCode'] + '.jpg')
            except:
                continue
            # 封装为字典，并返回
            item = {
                'id': product['ItemCode'],
                'title': product['Cpmc'],
                'intro': product['Instro'],
                'caption': caption,
                'price': product['Price'],
                'mprice': product['LinePrice'],
                'sales': int(
                    float(product['Sales'][:-1]) * 10000 if product['Sales'][-1] == '万' else float(product['Sales'])),
                'sales2': product['Sales'],
                'detail': detail,
                'material': material,
                'pack': pack,
                'default_image': default_image,
                'category_id': int(category_id),
                'images': images,
                'detail_images': detailimgs
            }
            datas.append(item)
        return datas

    def save_img(self, dirname, img_url):
        """存储图片，并需要返回存储路径"""
        os.chdir(self.projectPath + '\\flowershop\\flowershop\\static\\imgs')
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        response = self.session.get(img_url, headers=self.headers, timeout=10).content
        filename = hashlib.md5(response)
        path = '\\static\\imgs\\' + dirname + '\\' + filename.hexdigest() + '.jpg'
        with open(dirname + '\\' + filename.hexdigest() + '.jpg', 'wb') as f:
            f.write(response)
        return path

    def save_news(self, datas):
        mysql = pymysql.connect(host='127.0.0.1', user=self.username, password=self.pwd, port=3306, charset='utf8',
                                database=self.database)
        db = mysql.cursor()  # 创建游标
        for data in datas:
            time.sleep(0.1)
            if data == None:
                continue
            count = random.randint(1, 999)
            sql = 'insert into tb_content(id,create_time, update_time,title,intro,count, image,text) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            data1 = (data[0], str(datetime.now())[0:-7], str(datetime.now())[0:-7], data[1], data[2], count, data[4][0]['img_url'], data[3])
            try:
                db.execute(sql, data1)
                mysql.commit()
            except Exception as e:
                print(e)
                continue
            for img in data[4]:
                time.sleep(0.1)
                sql2 = 'insert into tb_content_image(create_time, update_time, image, content_id, good_id) values(%s,%s,%s,%s,%s)'
                data2 = (str(datetime.now())[0:-7], str(datetime.now())[0:-7], img['img_url'], data[0], img['id'])
                try:
                    db.execute(sql2, data2)
                    mysql.commit()
                except Exception as e:
                    print(e)
                    continue
        db.close()  # 关闭游标连接
        mysql.close()  # 关闭数据库

    def save_goods(self, datas):
        mysql = pymysql.connect(host='127.0.0.1', user=self.username, password=self.pwd, port=3306, charset='utf8',
                                database=self.database)
        db = mysql.cursor()  # 创建游标
        # database = 'create database if not exists flowershop charset=utf8;'    # 创建数据库
        # 创建表
        # table = 'create table if not exists tb_goods(id int not null primary key auto_increment,)'
        for item in datas:
            time.sleep(0.1)
            # 插入MySQL数据库
            sql = 'insert into tb_goods(id, create_time, update_time, name,intro, caption, price, cost_price, market_price, stock, sales,sales2, comments, material, desc_detail, desc_pack, is_launched, default_image, category_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            data = (
                item['id'], str(datetime.now())[0:-7], str(datetime.now())[0:-7], item['title'], item['intro'], item['caption'], item['price'],
                float(item['price']) - 20.00, item['mprice'], self.stock, item['sales'], item['sales2'],
                0, item['material'], item['detail'], item['pack'], 1, item['default_image'], item['category_id'])
            try:
                # db.execute(database) # 创建数据库
                # db.execute(table)  # 构建表
                db.execute(sql, data)  # 插入MySQL
                mysql.commit()  # 提交事务
            except Exception as e:
                print(e)
                continue
                # mysql.rollback()

            for img in item['images']:
                time.sleep(0.1)
                sql2 = 'insert into tb_good_image(create_time,update_time,image, good_id) values(%s,%s,%s,%s)'
                data2 = ( str(datetime.now())[0:-7], str(datetime.now())[0:-7], img, item['id'])
                try:
                    db.execute(sql2, data2)
                    mysql.commit()
                except Exception as e:
                    print(e)
                    continue
            for i in item['detail_images']:
                time.sleep(0.1)
                sql3 = 'insert into tb_detail_image(create_time,update_time,image, good_id) values(%s,%s,%s,%s)'
                data3 = ( str(datetime.now())[0:-7], str(datetime.now())[0:-7], i, item['id'])
                try:
                    db.execute(sql3, data3)
                    mysql.commit()
                except Exception as e:
                    print(e)
                    continue
        db.close()  # 关闭游标连接
        mysql.close()  # 关闭数据库

    def preaction(self):
        mysql = pymysql.connect(host='127.0.0.1', user=self.username, password=self.pwd, port=3306, charset='utf8',
                                database=self.database)
        db = mysql.cursor()  # 创建游标
        url="http://127.0.0.1:8000"
        with open('slides.txt', 'r',encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '').split('	')
                sql = 'insert into tb_slide(create_time, update_time, name,image,url) values(%s,%s,%s,%s,%s)'
                data = (str(datetime.now())[0:-7], str(datetime.now())[0:-7],'banner_0'+str(line[0]), line[4],url)
                try:
                    db.execute(sql, data)
                    mysql.commit()
                except Exception as e:
                    print(e)
                    continue
        with open('goodcategory.txt', 'r',encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '').split('	')
                sql2 = 'insert into tb_goods_category(create_time, update_time, name) values(%s,%s,%s)'
                data2 = (str(datetime.now())[:-7], str(datetime.now())[:-7],line[3])
                try:
                    db.execute(sql2, data2)
                    mysql.commit()
                except Exception as e:
                    print(e)
                    continue

        db.close()  # 关闭游标连接
        mysql.close()  # 关闭数据库

    def main(self):
        self.preaction()
        time.sleep(1)
        self.get_news()
        for urls in self.goodsUrls.items():
            time.sleep(0.1)
            if type(urls[1]) == list:
                for url in urls[1]:
                    time.sleep(0.1)
                    new_url = self.get_page_num(url)
                    print(f"开始爬取类型为{urls[0]}中url为{url}的商品")
                    datas = self.get_product_info(new_url, urls[0])
                    self.save_goods(datas)
                    print(f"保存类型为{urls[0]}中url为{url}的商品数据成功")
            else:
                new_url = self.get_page_num(urls[1])
                print(f"开始爬取类型为{urls[0]}中的商品")
                datas = self.get_product_info(new_url, urls[0])
                self.save_goods(datas)
                print(f"保存类型为{urls[0]}中的商品数据成功")



if __name__ == '__main__':
    hua = HuaSpider()
    hua.main()
