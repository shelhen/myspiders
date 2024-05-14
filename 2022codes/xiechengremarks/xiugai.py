import requests
import time
import random
import json


class HotelSpider(object):

    def __init__(self):
        self.session = requests.session()
        self.session.headers={
            'Referer':'https://accounts.ctrip.com/',
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
        }

    def get_cookies(self, hotel_id):
        #  https://m.ctrip.com/html5/hotel/hoteldetail/2077353.html
        detail_url = f'https://m.ctrip.com/html5/hotel/hoteldetail/{hotel_id}.html'
        self.session.get(detail_url, timeout=10)
        cookies={
            'nfes_isSupportWebP':'1',
            '_pd':'%7B%22_o%22%3A2%2C%22s%22%3A130%2C%22_s%22%3A0%7D',
            'librauuid':'',
            '_ubtstatus':f'%7B%22vid%22%3A%22{int(time.time()*1e3)}.9q1sdl%22%2C%22sid%22%3A1%2C%22pvid%22%3A1%2C%22pid%22%3A228032%7D',
            'hotelhst':'1164390341',
            'UBT_VID':f'{int(time.time()*1e3)}.9q1sdl',  # 时间戳
            'MKT_Pagesource':'H5',
            'Union':f'OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&exmktID=&createtime={int(time.time())}&Expires={int(time.time()+321)}',
            '_bfa':f'1.{int(time.time()*1e3)}.9q1sdl.1.{int(time.time()*1e3)}.{int(time.time()*1e3)}.1.4.153002',
            'cticket':'4DCCBE65897F5DB0ADC7216418E862B4DD8B5298726D98E958040BC588730178',
            'login_type':'0',
            'login_uid':'D7DB099065B596E9AF7E63F7F29FC702',
            'DUID':'u=C23F56EF0CBC99A4D4D376F570654C53&v=0',
            'IsNonUser':'F',
            'AHeadUserInfo': 'VipGrade=10&VipGradeName=%BB%C6%BD%F0%B9%F3%B1%F6&UserName=&NoReadMessageCount=0'
        }
        self.session.cookies.update((cookies))

    def get_remarks(self, id, num):
        self.get_cookies(id)
        guid = self.session.cookies['GUID']
        params={
            '_fxpcqlniredt':guid,
            'x-traceID':f'{guid}-{round(time.time() * 1000)}-{int(1e6 * random.random())}'
        }
        url = 'https://m.ctrip.com/restapi/soa2/24626/commentlist'
        head = {
            'aid':"66672",
            'auth':'',
            'cid':guid,
            'ctok':'',
            'cver':"1694598225472",
            'extension':[{'name':"supportWebP",'value':"true"}],
            'lang':"01",
            'ouid':"",
            'sid':"1693366",
            'syscode':"09",
            'vid':f"{int(time.time()*1e3)}.9q1sdl",
            'xsid':""
        }
        post_data = {
            'commentTagV2List':[],
            'commonStatisticList': [1],
            'ftype':"",
            'head':head,
            "hotelId":id,
            'orderBy':0,
            'pageIndex': num,
            'pageSize': 10,
            'repeatComment':1,
            # 'session':self.get_session()
        }
        comments =  self.session.post(url,params=params, data=json.dumps(post_data), timeout=10).json()
        statistic = {statistic['name']:statistic['commentCount'] for statistic in comments['statisticList']}
        count = statistic['差评']
        return count, comments

    def parse(self, comments,):
        remarks=[]
        for comment in comments['groupList'][0]['commentList']:
            content = comment['content'].lower().replace('/', '').replace('\n', ' ')
            checkin = comment['checkin']
            roomname = comment['roomName']
            feedback = comment['feedbackList'][0]['content'].lower().replace('/', '').replace('\n', ' ')
            remark=f'{checkin}/{roomname}/{content}/{feedback}'
            print(remark)
            remarks.append(remark)
        return remarks


if __name__ == '__main__':
    hs = HotelSpider()
    id = '95472738'
    count, comments = hs.get_remarks(id,1)
    tnum = count//10 if count % 10 == 0 else (count // 10) + 1
    for i in range(1, tnum+1):
        count, comments_ = hs.get_remarks(id,i)
        try:
            remarks = hs.parse(comments_)
            for remark in remarks:
                print(remark)
        except Exception as e:
            print(e)
            continue