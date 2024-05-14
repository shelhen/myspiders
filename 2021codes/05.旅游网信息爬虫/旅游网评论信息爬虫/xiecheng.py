import json
import random
import re
import time
import requests
from lxml import etree
from util import remark_save


class XiechengSpider(object):
    def __init__(self):
        self.placeId = [
            # 偶尔报错：'NoneType' object is not iterable/list indices must be integers or slices, not str
            # '17377',  # 龟山汉墓
            # '17383',  # 徐州博物馆
            # '116632',  # 汉文化景区
            # "98281800",  # 水下兵马俑_汉文化景区
            # '143867',  # 汉兵马俑_汉文化景区
            # '17380',  # 汉画石像馆_汉文化景区
            # '17378',  # 狮子山楚王陵_汉文化景区
            # '116633',  # 户部山
            # '17388',  # 戏马台_属于户部山
            # '17381',  # 沛县汉城
            # '141129',  # 沛县泗水亭
            # '133779',  # 丰县汉皇祖陵
            # '141113',  # 沛县歌风台
            '17385',  # 云龙湖景区
            # '142546',  # 窑湾古镇
        ]
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        self.session = requests.session()
        self.post_data = {
            "arg": {"channelType": 2, "collapseType": 0, "commentTagId": 0, "pageIndex": 0, "pageSize": 10,
                    "poiId": "", "sourceType": 1, "sortType": 3, "starType": 0},
            "head": {"cid": "", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                     "syscode": "09", "auth": "", "xsid": "", "extension": []}
        }
    def get_xhr(self, i, poiId, cliendId):
        # 构造url
        # Math.floor(1e7 * Math.random())=343991
        # Math.random() 产生[0,1)之间的随机数,乘以10的7次幂后向下取整数
        # x_traceID = ‘_fxpcqlniredt -’+timestamp + '-' + 随机数
        x_traceid = f"{cliendId}-{round(time.time() * 1000)}-{int(1e6*random.random())}"
        url = f"https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt={cliendId}&x-traceID={x_traceid}"
        self.post_data["arg"]['poiId'] = poiId  # 10536321
        self.post_data["arg"]['pageIndex'] = i
        self.post_data["head"]['cid'] = cliendId  #
        xhr_res = self.session.post(url, headers=self.headers,data=json.dumps(self.post_data),timeout=10).json()
        return xhr_res
    def get_poiId(self, id):
        """目的，绑定cookie,获取poiId,并且获取总页数"""
        url = "https://you.ctrip.com/sight/xuzhou230/" + str(id) + ".html"
        res = self.session.get(url, headers=self.headers, timeout=10)
        html = etree.HTML(res.text)
        # print(res.text)
        script_node = html.xpath("//div[@id='content']/script")[2]
        # 无法精确取到特定段的文本，只好选择使用正则表达式来暴力匹配，但是希望匹配的字符串尽可能地少。
        # js_text = script_node.xpath("./text()")[0]
        js_text = str(etree.tostring(script_node))
        # 缩小后，尝试使用Re拿具体数据
        commentCount = re.search('commentCount":([\d]+)', js_text).group(1)
        poiId= re.search(',"poiId":([\d]+)', js_text).group(1)
        # 获取cookei数据
        cliendId=res.cookies['GUID']
        return int(commentCount), poiId, cliendId
    def main(self):
        p = re.compile(r'[^\w，。！？,.、:；℃]')
        # 获取所需要的参数
        for id in self.placeId:
            try:
                commentCount, poiId, cliendId = self.get_poiId(id)
            except Exception as e:
                print(e, '该景区尚无评论信息')
                continue
            # 总评论数除以10如果能够整除就不用加一，如果不能整除，需要取整并且加一
            tatolNum=commentCount // 10 if commentCount %10==0 else (commentCount//10)+1
            # 0-91可迭代
            for i in range(tatolNum+1):
                try:
                    time.sleep(random.random() * 1.5)
                    result = self.get_xhr(i+1,poiId, cliendId)["result"]['items']
                    remarks = [{
                        'score': item['score'],
                        'content':p.sub('', item['content'].lower()),
                        'usefulCount':item['usefulCount'],
                        'Locate':item['ipLocatedName'],
                        'publishTime':int(item['publishTime'][6:16])
                    } for item in result]
                    # 注意这时存在某些'content'实际为空值
                    print(remarks)
                    remark_save( 'xiecheng',remarks)
                except Exception as e:
                    print(e)
                    continue
            print(f'完成爬取景区为{id}的所有评论')


if __name__ == '__main__':
    xiecheng=XiechengSpider()
    xiecheng.main()