import requests
import time,re
import random
from RemarkSaver import remark_save


class MeituanSpider(object):
    # https://xz.meituan.com/s/龟山汉墓/
    def __init__(self):
        self.ploid=[
            935504,  # 龟山汉墓
            935632,  # 徐州博物馆
            162985980,  # 水下兵马俑
            2075692,  # 户部山景区
            2075679,  # 戏马台
            63445067,  # 汉文化景区
            # 41062772,  # 云龙湖
            2075868,  # 沛县汉城
            133779,  # 汉皇祖陵
            2075870,  # 沛县泗水亭


        ]
        self.session = requests.session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            "mtgsig": ''
                        }
        self.cookies={
            "uuid": "7aaa8281c72b4f189180.1677323",
            "_lxsdk_cuid": "18688445a8fc8-0857abafe77527-26031951-144000-18688445a8fc8	.",
            "_lxsdk_s": "18688445a91-a27-277-4f2%7C%7C1",
            "WEBDFPID": ''
        }
    def get_page(self, id):
        p = re.compile(r'[^\w，。！？,.、:；℃]')
        ts = int(time.time()*1000)
        self.cookies['WEBDFPID']=str(ts)+"EMKUSOAfd79fef3d01d"
        s = {
            "a1":"1.0",
            "a2":ts,
            "a3":str(ts) +"EMKUSOAfd79fef3d01d5e9aadc18ccd4d0c95072470",
            "a4":"005cded6130d4166d6de5c0066410d13ff83188899c2159b",
            "a5":"b1h+qcGszLSbgz4rGsAG62atCCFTEbmzN4KeYG+h683dygN2EuxPAr9F/tgwTVZhNhwUyXEc9fdFULvCCvld3XvGzTkFFGGvSNNm7odkVmAC7MbXMugzC5m6m6/7IWmZscfZ6l73Mo2kdIF/PeVtxPDEUzj4RTYiZpVyI3LRm1Sektj7",
            "a6":"h1.2mLAfjaFhQREuZ93bx833EvXsO0RpYeAyjzBDsOjwsmN1am7pJEIhhYVSPZq9yKxxACkpsQ53FZTB9+MmIF4F77RP9MHxh8kysZrokjIAlt7HZeukG/buWjo2j3QfecS9w0ISkhoi15yZVxesOUKc2eWkkCvVJuU8FXzLi6hRfkklz0p/70yOA+n0vbE3I6+w3VM+bOm4v9mxrzPDPSAvXj05cGW8DijuGJYg6TgaMtUdr7t1OQeSewioltz9+c3l2xaTIH/y5OcQT18ReZ+tqjtS31Rw/6cb3tdvn2VrLxqNwtO86CkkCIlODzrp/+FtaRX0v+tfmvOJTzxWF8nqTUimKaVf6xZqbQtM6g6X/15NuqY15a1or/fq9X4BRoXV2MhGD6EKRRFSPhYdiEQm1ymJs+jNwOSOhy82/RaJSrDaOfzQnXcnsUs2gjrZv6DNKOicPgMb4OLvY8GLa3s0tg==",
            "a7":"74184a6674b9a3dbf96188660657414839c601afcc2bdd391091fa86bde978c7",
            "x0":4,
            "d1":"9e49067a7a5a3da11161d9860a1625bd"
        }
        self.session.cookies.update(self.cookies)
        self.headers['mtgsig']=str(s)
        response1 = self.session.get(f"https://www.meituan.com/ptapi/poi/getcomment?id={id}&offset=0&pageSize=10&mode=0&sortType=1&enableGuard=true", headers=self.headers, timeout=10)
        # print(response1.content.decode())
        commentCount= int(response1.json()["total"])
        tatolNum = commentCount // 10 if commentCount % 10 == 0 else (commentCount // 10) + 1
        remarks=[]
        for i in range(tatolNum):
            # time.sleep(random.random() * 5)
            url = f"https://www.meituan.com/ptapi/poi/getcomment?id={id}&offset={i*10}&pageSize=10&mode=0&sortType=1&enableGuard=true"
            response = self.session.get(url, headers=self.headers, timeout=10)
            try:
                ss = [{
                    "score":int(item["star"])/10,
                    "content": p.sub('', str(item["comment"]).lower()),
                    'usefulCount':item["zanCnt"],
                    'Locate':'None',
                    "publishTime":str(item["commentTime"])[0:10],
                } for item in response.json()["comments"] if item["comment"]!=""]
                remarks.extend(ss)
            except Exception as e:
                print(i+1,e)
                i-=1
                continue
        return remarks

    def main(self):
        for id in self.ploid:

            remarks = self.get_page(id)
            remark_save(remarks)
            print(f"已经完成{id}")
            # for remark in remarks:
            #     print(len(remark))


if __name__ == '__main__':
    mei = MeituanSpider()
    mei.main()