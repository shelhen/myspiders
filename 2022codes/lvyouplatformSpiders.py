import re
import time
import json
import random
import requests
from lxml import etree
import pymysql


class BaseSpider(object):

    def __init__(self, pids: list):
        self.session = requests.session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        }
        self.pids = pids
        self.p = re.compile(r'[^\w，。！？,.、:；℃]')

    def save_comments(self, table_name, comments):
        mysql = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='Password123.',
            port=3306,
            charset='utf8mb4',
            database='xuzhou_remarks'
        )
        db = mysql.cursor()
        table = (f'create table if not exists {table_name}(id int not null primary key auto_increment, score int(3) '
                 f'default 0, content varchar(9000) default null, location varchar(20) default null, datetime int(10) '
                 f'default 0)')
        for comment in comments:
            if comment['content'] == '' or comment['content'] =='用户未点评，系统默认好评。':
                continue
            # print(comment)
            sql_str1 = f"insert into {table_name}"
            sql_str2 = '(score, content, location, datetime) values (%s, %s, %s, %s)'
            sql_str = sql_str1 + sql_str2
            data = (comment['score'], self.p.sub("", comment['content']), comment['location'], comment['datetime'])
            try:
                # db.execute(database)  # 创建数据库
                db.execute(table)  # 构建表
                db.execute(sql_str, data)  # 插入MySQL
                mysql.commit()  # 提交事务
            except Exception as e:
                print(e, 'chucuo')
                continue
        db.close()  # 关闭游标连接
        mysql.close()  # 关闭数据库

    def get_cookie_by_webdriver(self, url):
        cookies = ''
        return cookies


class XieCheng(BaseSpider):

    def __init__(self, pids :list):
        super(XieCheng, self).__init__(pids)

    def get_sessions(self, pid):
        response = self.session.get(f"https://you.ctrip.com/sight/xuzhou230/{pid}.html", timeout=10)
        return re.findall(r',"poiId":(\d+)', response.content.decode())[0]

    def get_remarks(self, pid, index):
        poiId = self.get_sessions(pid)

        # 获取关键参数并且补充请求cookie信息
        guid = self.session.cookies['GUID']
        url = f"https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt={guid}&x-traceID={guid}-{round(time.time() * 1000)}-{int(1e6 * random.random())}"
        post_data = {
            "arg": {"channelType": 2, "collapseType": 0, "commentTagId": 0, "pageIndex": index, "pageSize": 10,
                    "poiId": poiId, "sourceType": 1, "sortType": 3, "starType": 0},
            "head": {"cid": guid, "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                     "syscode": "09", "auth": "", "xsid": "", "extension": []}
        }
        response = self.session.post(url, data=json.dumps(post_data), timeout=10).json()
        # ["result"]['items']
        return response["result"]

    def parse(self, result):
        remarks = [{
            'score': item['score'],
            'content': item['content'].lower(),
            'location': item['ipLocatedName'],
            'datetime': int(item['publishTime'][6:16])
        } for item in result]
        # 注意这时存在某些'content'实际为空值
        return remarks

    def main(self):
        for pid in self.pids:
            # 得到第一个pid
            try:
                # 获取总页数，同时如果返回了正确的总页数说明pid是正确的
                totalCount = self.get_remarks(pid, 0)['totalCount']
                # 总评论数除以10如果能够整除就不用加一，如果不能整除，需要取整并且加一
                tatolNum = totalCount // 10 if totalCount %10==0 else (totalCount//10)+1
            except Exception as e:
                print(e, '该景区尚无评论信息')
                continue
            print(f'开始爬取pid为:{pid}的景区，共{tatolNum}页')
            for i in range(1, tatolNum+1):
                # i 属于 1-tatolNum+1
                try:
                    time.sleep(random.random() * 1.5)
                    result = self.get_remarks(pid, i)['items']
                    remarks = self.parse(result)
                    for remark in remarks:print(remark)
                    self.save_comments(self.__class__.__name__, remarks)
                except Exception as e:
                    print(e)
                    continue
            print(f'pid为:{pid}的景区全部评论爬 取完毕！')


class Qunaer(BaseSpider):

    def __init__(self, pids):
        super(Qunaer, self).__init__(pids)

    def get_csrf(self):
        b = "123456789poiuytrewqasdfghjklmnbvcxzQWERTYUIPLKJHGFDSAZXCVBNM"
        csft = ""
        for r in range(32):
            csft += b[int(random.random() * 1e8) % len(b)]
        return csft

    def get_cpid(self, QN):
        h = 0
        for c in QN:
            h = (31 * h + ord(c)) & 0xFFFFFFFF
        e = ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
        return "0" + str(0 - e) if e < 0 else "" + str(e)

    def get_session(self):
        self.session.get('https://www.qunar.com/', timeout=10)
        cpid = self.get_cpid(self.session.cookies['QN1'])
        csrf = self.get_csrf()
        self.session.cookies.update({
            "unar-assist": '{%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}	',
            "QN205": "organic",
            "QN277": "organic",
            "QN267": cpid,
            "csrfToken": csrf,
        })

    def get_remarks(self, pid, index):
        # 爬取太快会遭到网站暂时断开链接
        url = f'https://piao.qunar.com/ticket/detailLight/sightCommentList.json'
        params = { 'sightId': pid, 'index': index, 'page': index, 'pageSize': 10, 'tagType': 0}
        response = self.session.get(url, params=params).json()
        return response['data']

    def parse(self, result):
        remarks = [{
            "datetime": time.mktime(time.strptime(data["date"], "%Y-%m-%d")),
            "score": data['score'],
            "content": data["content"].lower(),
            "location": data['replyCityName']
        } for data in result]
        return remarks

    def main(self, flag=False):
        if flag:
            self.get_destination_comments()
        self.get_session()
        for pid in self.pids:
            try:
                # 获取总页数，同时如果返回了正确的总页数说明pid是正确的
                totalCount = self.get_remarks(pid, 0)['commentCount']
                # 总评论数除以10如果能够整除就不用加一，如果不能整除，需要取整并且加一
                tatolNum = totalCount // 10 if totalCount %10==0 else (totalCount//10)+1
            except Exception as e:
                print(e, '该景区尚无评论信息')
                continue
            print(f'开始爬取pid为:{pid}的景区，共{tatolNum}页')
            for i in range(1, tatolNum+1):
                # i 属于 1-tatolNum+1
                try:
                    time.sleep(random.random() * 2 + 1)
                    result = self.get_remarks(pid, i)['commentList']
                    remarks = self.parse(result)
                    for remark in remarks:print(remark)
                    self.save_comments(self.__class__.__name__, remarks)
                except Exception as e:
                    print(e)
                    continue
            print(f'pid为:{pid}的景区全部评论爬 取完毕！')

    def get_destination_comments(self):
        # 'https://travel.qunar.com/p-oi702927-guishanhanmu',
        poids = [
            '708482-ximatai',
            '706508-xuzhouhanwenhuajingqu',
            '10006697-hubushan',
            '702927-guishanhanmu',
            '706232-xuzhoubowuguan',
            '715377-hanbingmayongbowuguan',
            '706114-shizishanchuwangling',
            '707040-xuzhouhanhuaxiangshiguan'
        ]
        for poid in poids:
            response = self.session.get(f'https://travel.qunar.com/p-oi{poid}', timeout=10)
            totalCount = int(re.search(r'共(\d+)条点评', response.text).group(1))
            tatolNum = totalCount // 10 if totalCount %10==0 else (totalCount//10)+1
            for i in range(1, tatolNum+1):
                remarks = self.get_comments(poid, i)
                for remark in remarks:print(remark)
                self.save_comments(self.__class__.__name__, remarks)

    def get_comments(self, poid, index):
        remarks = []
        url = f'https://travel.qunar.com/place/api/html/comments/poi/{poid.split("-")[0]}?poiList=true&sortField=1&rank=0&pageSize=10&page={index}'
        response = self.session.get(url, timeout=10).json()
        html= etree.HTML(response['data'])
        nodes = html.xpath("//ul[@id='comment_box']/li//div[@class='e_comment_main_inner']")
        for node in nodes:
            content = ''.join(node.xpath("./div[@class='e_comment_content']/p/text()"))
            datetime = node.xpath("./div[@class='e_comment_add_info']/ul/li[1]/text()")[0]
            remarks.append({
                "score": 0,
                "location": '',
                'content': content.replace(' ', '').replace('<br>', '').replace('<br />', '').replace('<br/>', ''),
                'datetime': time.mktime(time.strptime(datetime, "%Y-%m-%d"))
            })
        return remarks


class MaFeng(BaseSpider):

    def __init__(self, pids):
        super(MaFeng, self).__init__(pids)

    def get_remarks(self, pid ,index):
        self.session.headers['Referer']='https://www.mafengwo.cn/poi/' + pid + '.html'
        url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?'
        params = { 'params': '{"poi_id":' + pid + ',"page":"' + str(index) + '","just_comment":1}'}
        response = self.session.get(url, params=params, timeout=10).json()
        return response['data']

    def parse(self, result):
        # 日期正则
        date_pattern = r'<a class="btn-comment _j_comment" title="添加评论">评论</a>.*?\n.*?<span class="time">(.*?)</span>'
        # 评分正则
        star_pattern = r'<span class="s-star s-star(\d)"></span>'
        # 评论正则
        comment_pattern = r'<p class="rev-txt">([\s\S]*?)</p>'
        date_list = re.compile(date_pattern).findall(result)
        star_list = re.compile(star_pattern).findall(result)
        comment_list = re.compile(comment_pattern).findall(result)
        remarks=[]
        for i in range(0, len(date_list)):
            comment = comment_list[i].replace(' ', '').replace('<br>', '').replace('<br />', '').replace('<br/>', '')
            remarks.append({
                'datetime': time.mktime(time.strptime(date_list[i], "%Y-%m-%d %H:%M:%S")),
                'score': star_list[i],
                'content': comment.lower(),
                'location': ''
            })
        return remarks

    def main(self):
        for pid in self.pids:
            # 获取总页数，同时如果返回了正确的总页数说明pid是正确的
            totalCount = int(self.get_remarks(pid,1)['controller_data']['comment_count'])
            # 总评论数除以10如果能够整除就不用加一，如果不能整除，需要取整并且加一
            tatolNum = totalCount // 10 if totalCount %10==0 else (totalCount//10)+1
            # print(totalCount, tatolNum)
            for i in range(1,tatolNum+1):
                result = self.get_remarks(pid, i)['html']
                remarks = self.parse(result)
                for remark in remarks:print(remark)
                self.save_comments(self.__class__.__name__, remarks)


class Qiongyou(BaseSpider):
    def __init__(self, pids):
        super(Qiongyou, self).__init__(pids)

    def get_remarks(self, pid, index):
        params={ "action": "comment", "page": index, "order": 5, "poiid": pid, "starLevel": "all"}
        response = self.session.get("https://place.qyer.com/poi.php?", params=params, timeout=10).json()
        return response['data']

    def parse(self, result):
        remarks = [{
            "datetime": time.mktime(time.strptime(data["date"], "%Y-%m-%d")),
            "score": data['starlevel'],
            "content": data["content"].lower(),
            "location": ''
        } for data in result]
        return remarks

    def main(self):
        for pid in self.pids:
            totalCount = int(self.get_remarks(pid, 1)['total'])
            tatolNum = totalCount // 10 if totalCount %10==0 else (totalCount//10)+1
            for i in range(1, tatolNum+1):
                result = self.get_remarks(pid, i)['lists']
                remarks = self.parse(result)
                for remark in remarks:print(remark)
                self.save_comments(self.__class__.__name__, remarks)
            print(f'已完成id为{pid}地区的评论爬取')


class TongCheng(BaseSpider):
    def __init__(self, pids):
        super(TongCheng, self).__init__(pids)

    def get_sessions(self, pid):
        url = f'https://www.ly.com/scenery/AjaxHelper/ValidPic.aspx?action=PRICECODE&sid={pid}&itype=12&pcrefId=215909561&pctype=15'
        gmt_format = '%a %b %d %Y %H:%M:%S GMT+0800 (中国标准时间)'
        params={
            'channel': 'scenery',
            'action': 'getBulletin',
            'asyncRefid': 0,
            'asyncUniqueKey':'undefined',
            'data': time.strftime(gmt_format, time.localtime(time.time())),
            '_dAjax': 'callback',
            'callback':'tc24714826653'
        }
        self.session.get(url, timeout=10)
        self.session.get('https://www.ly.com/AjaxHelper/TopLoginHandler.aspx',params=params, timeout=10)
        self.session.cookies['_dx_uzZo5y'] = f'{int(time.time()*1000)}' + self.get_csrf()

    def get_csrf(self):
        b = "123456789poiuytrewqasdfghjklmnbvcxzQWERTYUIPLKJHGFDSAZXCVBNM"
        csft = ""
        for r in range(32):
            csft += b[int(random.random() * 1e8) % len(b)]
        return csft

    def get_remarks(self, pid, index):
        url = 'https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx'
        params= {
            'action': 'GetDianPingList',
            'sid': pid,
            'page': index,
            'pageSize': 10,
            'labId': 1,
            'sort': 0,
            'iid': random.random()
        }
        response = self.session.get(url, params=params).json()
        return response

    def parse(self,result):
        Access = {"好评": 5, '中评': 3, '差评': 1}
        remarks = [{
            "datetime": int(time.mktime(time.strptime(data["dpDate"], "%Y-%m-%d"))),
            "content": data["dpContent"].lower(),
            "location": data["DPLocation"],
            "score": Access[data["lineAccess"]],
        } for data in result]
        return remarks

    def main(self):
        self.get_sessions(random.choice(self.pids))
        for pid in self.pids:
            totalCount = int(self.get_remarks(pid,1)['totalNum'])
            tatolNum = totalCount // 10 if totalCount %10==0 else (totalCount//10)+1
            for i in range(1, tatolNum+1):
                result = self.get_remarks(pid, i)['dpList']
                remarks = self.parse(result)
                for remark in remarks:print(remark)
                self.save_comments(self.__class__.__name__, remarks)


class DaZhong(BaseSpider):
    def __init__(self, pids):
        super(DaZhong, self).__init__(pids)

    def get_lxsdk_s(self, key:int):
        e = [hex(int( key*random.random() +1))[3:] for i in range(4)]
        e[0] = hex(int(time.time()*1000))[2:]
        return '-'.join(e) + f'%7C%7C{14+int(random.random()*100)}'

    def get_session(self):
        self.session.cookies.update({
            '_lxsdk_cuid': '18dcc5b834dc8-095c96939fd5dd-4c657b58-1fa400-18dcc5b834dc8',
            '_lxsdk': '18dcc5b834d-abd-909-069%7C%7C183',
            '_hc.v': 'b60dc585-750c-13a7-c03a-47b6f6c27e10.1708530567',
            'WEBDFPID': '6ux389xwzx265v0616y71222uy57966481wxx4y30v197958284812y7-2023890566882-1708530566061KWGAKMOfd79fef3d01d5e9aadc18ccd4d0c95077381',
            'ctu': 'e687aa638a8a4bc9923020468f3a67a049c06872bdab113cd8c3b0b4365e47c4',
            'Hm_lvt_602b80cf8079ae6591966cc70a3940e7': '1708460238',
            'fspop': 'test',
            'cy': '92',
            'cye': 'xuzhou',
            's_ViewType': '10',
            'll': '7fd06e815b796be3df069dec7836c3df',
            'ua': '%E7%82%B9%E5%B0%8F%E8%AF%849627621309',
            'Hm_lpvt_602b80cf8079ae6591966cc70a3940e7': f'{int(time.time())}',
            '_lxsdk_s': self.get_lxsdk_s(65535),
            'HMACCOUNT_BFESS':'F7FEEF7CE88F1423',
            'qruuid':'0f948cb1-664d-443d-b3d9-7b1815ad2090',
            'dplet':'859d832c3ce52fbc230fff2f9680bc3b',
        })
        self.session.cookies.update({
'dper':'0202781feaaab523b040cbb62828e83fcadbbac424a47598021391263e38a8cf57ef9dfd791bd1385fefb96ab16e0b77482b032cab2cb4f0fd6a00000000501e0000b6c4dacb09b45dc0294627add602ab720907939612395787d8351b45f3d409bb2618349982d60b2d4b4cb95d4e93e7cf'
        })

    def get_remarks(self, pid, index):
        url = f'https://www.dianping.com/shop/{pid}/review_all/p{index}'
        return self.session.get(url, timeout=10).text

    def parse(self, result):
        self.get_session()
        remarks = []
        html = etree.HTML(result)
        nodes = html.xpath("//div[@class='main-review']")
        for node in nodes:
            content = node.xpath("./div[contains(@class,'review-words')]/text()")[0]
            datetime = re.search(r'\d+-\d+-\d+ \d+:\d+', node.xpath(".//span[@class='time']/text()")[0])
            rank = node.xpath("./div[@class='review-rank']/span/@class")[0]
            remarks.append({
                'datetime': time.mktime(time.strptime(datetime.group(0), "%Y-%m-%d %H:%M")),
                'score': float(re.search(r'sml-str(\d+)', rank).group(1))/10,
                "location":'',
                "content": content.replace(' ', '').replace('<br>', '').replace('<br />', '').replace('<br/>', '').lower(),
            })
        return remarks

    def main(self):
        self.get_session()
        for pid in self.pids:
            try:
                totalCount = int(re.search(r'class="reviews">(\d+)条评价', self.get_remarks(pid, 2)).group(1))
                tatolNum = totalCount // 10 if totalCount %10==0 else (totalCount//10)+1
            except Exception as e:
                print(e, 'cookie已经失效，请重新获取。')
                continue
            print(f'开始爬取pid为:{pid}的景区，共{tatolNum}页')
            for i in range(87, tatolNum+1):
                print(f'当前第{i+1}页码')
                # time.sleep(random.random() * 3 + 1)
                result = self.get_remarks(pid, i)
                remarks = self.parse(result)
                for remark in remarks: print(remark)
                self.save_comments(self.__class__.__name__, remarks)
            print(f'pid为:{pid}的景区全部评论爬 取完毕！')


if __name__ == '__main__':
    xiecheng_place_id = [
        '17377',  # 龟山汉墓
        '17383',  # 徐州博物馆
        '116632',  # 汉文化景区
        "98281800",  # 水下兵马俑_汉文化景区
        '143867',  # 汉兵马俑_汉文化景区
        '17380',  # 汉画石像馆_汉文化景区
        '17378',  # 狮子山楚王陵_汉文化景区
        '133846'  # 圣旨博物馆_汉文化景区
        '116633',  # 户部山
        '17388',  # 戏马台_户部山
        '133862'  # 户部山古建筑
    ]
    qunaer_place_id = [
        '1468',  # 龟山汉墓
        '5483',  # 徐州博物馆
        '5158',   # 汉文化景区
        '14602',  # 汉兵马俑_汉文化景区
        '4760',  # 狮子山楚王陵_汉文化景区
        '507307',  # 汉画石像馆_汉文化景区
        '7253',  # 戏马台_户部山
    ]
    mafeng_place_id = [
        '6326847',  # 汉文化景区
        '5437286',  # 龟山汉墓
        "5437294",  # 徐州博物馆
        '5437288',  # 汉兵马俑
        '1880916'  # 汉化石像馆
        "1871598",  # 狮子山楚王陵
        "5429508",  # 戏马台
        '14891634'  # 户部山
    ]
    qiongyou_place_id = [
        '1485376',  # 汉文化景区
        '1469634',  # 徐州博物馆
        '1485359',  # 龟山汉墓
        '1469637',  # 汉兵马俑博物馆
        '1485374',  # 狮子山楚王陵
        '1485363',  # 戏马台
        '1485385',  # 水下兵马俑
        '1469633',  # 汉化石像馆
        '1485361'  # 户部山
    ]
    tongcheng_place_id = [
        '20256',  # 汉文化景区
        '860',  # 戏马台
        '10565',  # 户部山
        '624',  # 龟山汉墓
        '705',  # 云龙湖景区
    ]
    xiecheng = XieCheng(xiecheng_place_id)
    mafeng = MaFeng(mafeng_place_id)
    qunaer = Qunaer(qunaer_place_id)
    qiongyou = Qiongyou(qiongyou_place_id)
    tongcheng = TongCheng(tongcheng_place_id)

    # mafeng.main()
    # qiongyou.main()
    # tongcheng.main()
    # qunaer.main()
    # xiecheng.main()
    pids = [
        'l2aeLAg7AjPtPrJb',
        'lahBuBCDGjHBBsiw',
        'G1O0B4wm6pwQFmCc',
        'l4nZkUk4LD0mLlvM',
        'G7x9T9SelGJVn1D3',
        'G2Elbq1uqYUyQ9HO'
    ]
    dazhong = DaZhong(pids)
    dazhong.main()