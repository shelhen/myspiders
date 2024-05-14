import re
import time
import requests
import random
from util import remark_save, get_cookie

class TongSpider(object):
    def __init__(self):
        self.pliId= [
            '20256',  # 汉文化景区20256
            '860',  # 戏马台
            '10565',  # 户部山
            '624',  # 龟山汉墓
            '705',  # 云龙湖景区
        ]
        self.p = re.compile(r'[^\w，。！？,.、:；℃]')
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            "Host": "www.ly.com",
        }
        self.session=requests.session()
    def get_cookies(self, id):
        url = "https://www.ly.com/scenery/BookSceneryTicket_"+ id +".html"
        cookies = get_cookie(url)
        # print(cookies)
        self.session.cookies.update(cookies)

    def get_commets(self, id,i):
        self.headers['Referer']='https://www.ly.com/scenery/BookSceneryTicket_'+id+'.html'
        url = "https://www.ly.com/scenery/AjaxHelper/DianPingAjax.aspx?"
        params={
            "action": "GetDianPingList",
            "sid": id,
            "page": i,
            "pageSize": 10,
            "labId": 1,
            "sort": 0,
            "iid": random.random()
        }
        res = self.session.get(url,headers=self.headers,timeout=10,params=params)
        return res.json()

    def parse(self,datas):
        Access = {"好评": 5, '中评': 3, '差评': 1}
        remarks = [{
            "publishTime": int(time.mktime(time.strptime(data["dpDate"], "%Y-%m-%d"))),
            "content": self.p.sub("", data["dpContent"].lower()),
            "Locate": data["DPLocation"],
            "usefulCount": data["zanCount"],
            "score": Access[data["lineAccess"]],
        }for data in datas]
        return remarks

    def main(self):
        for id in self.pliId:
            self.get_cookies(id)
            # 测试和获取页码
            tatolNum = int(self.get_commets(id, 1)["pageInfo"]["totalPage"])
            for i in range(tatolNum):
                datas = self.get_commets(id, i+1)["dpList"]
                try:
                    remarks = self.parse(datas)
                except Exception as e:
                    print(e,i)
                    continue
                for remark in remarks:
                    print(remark)
                print(f"已完成{i}/{tatolNum}页")
                remark_save('tongcheng', remarks)


if __name__ == '__main__':
    tongcheng=TongSpider()
    tongcheng.main()

