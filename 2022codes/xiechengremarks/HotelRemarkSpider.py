import requests
import time
import random
import json
import re

class HotelSpider(object):

    def __init__(self):
        self.session = requests.session()
        self.session.headers={
            'Referer':'https://accounts.ctrip.com/',
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
        }

    def get_hotels(self):
        # https://m.ctrip.com/html5/hotel/hoteldetail/95472738.html
        return {
            '高评分':[
                {'name':'上海国际旅游度假区荷逸唐酒店','score':'4.9','id':'95472738'},
                {'name':'云和夜泊酒店(上海国际旅游度假区店)','score':'4.9','id':'6657909'},
                {'name':'上海五角场逸扉酒店','score':'4.9','id':'2382332'},
                {'name':'上海兰墅智慧酒店(金山百联店)','score':'4.9','id':'1380784'},
                {'name':'麦新格国际酒店(上海国际旅游度假区店周浦地铁站店)','score':'4.8','id':'1496646'},
                {'name':'崇明金茂凯悦酒店','score':'4.9','id':'781302'},
            ],
            '低评分':[
                {'name':'上海礼辉宾馆','score':'1.5','id':'13364345'},
                {'name':'上海依依宾馆','score':'1.6','id':'2077353'},
                {'name':'上海中心旅社','score':'1.1','id':'962321'},
                {'name':'上海久久缘宾馆','score':'1.4','id':'2321072'},
                {'name':'速8酒店(上海浦东机场晨阳路店)','score':'4.1','id':'479849'},
                {'name':'布丁酒店(上海浦东机场店)','score':'4.1','id':'1563694'},
            ],
            '受欢迎':[
                {'name':'汉庭酒店(上海虹桥火车站沪青平公路店)','score':'4.1','id':'823807'},
                {'name':'上海浦东国际机场迪航酒店','score':'4.8','id':'6870954'},
                {'name':'宿适轻奢酒店(上海虹桥中心店)','score':'4.7','id':'42110698'},
                {'name':'上海新时空嘉廷酒店','score':'4.3','id':'446917'},
                {'name':'上海中山公园云睿酒店','score':'4.6','id':'686139'},
            ],
            '商务型':[
                {'name':'如家商旅酒(上海陆家嘴世博中心店)','score':'4.5','id':'63054594'},
                {'name':'上海虹桥雅高美爵酒店','score':'4.6','id':'345044'},
            ],
            '度假型':[
                {'name':'上海浦东香格里拉大酒店','score':'4.7','id':'373052'},
                {'name':'上海太阳岛度假酒店','score':'4.7','id':'1706857'},
                {'name':'上海南京路步行街假日酒店','score':'4.7','id':'72812393'},
                {'name':'宿适奢华酒店(上海日月光打浦桥地铁站店)','score':'4.6','id':'435499'},
                {'name':'上海外滩大悦城欢喜酒店','score':'4.5','id':'62541808'}
            ],
            '高端型':[
                {'name':'上海虹桥金臣皇冠假日酒店','score':'4.7','id':'65568600'},
                {'name':'上海虹桥祥源希尔顿酒店','score':'4.7','id':'425587'},
                {'name':'上海南新雅皇冠假日酒店','score':'4.6','id':'375528'},
                {'name':'上海华夏假日酒店','score':'4.6','id':'75391073'},
            ],
            '经济型':[
                {'name':'锦江之星风尚(上海浦东机场镇店)','score':'4.5','id':'5099462'},
                {'name':'汉庭酒店(上海陆家嘴东方路店)','score':'4.6','id':'2313513'},
                {'name':'麗枫酒店(上海虹桥火车站国家会展中心店)','score':'4.6','id':'7253324'},
            ],
            '亲子型':[
                {'name':'维纳国际酒店(上海野生动物园浦东机场店)','score':'4.8','id':'1421091'},
                {'name':'上海南京东路铂金万澳酒店','score':'4.6','id':'101132081'},
                {'name':'浦天美泊酒店(上海国际旅游度假区店)', 'score':'4.6', 'id':'60932554'},
                {'name':'上海松江开元名都大酒店', 'score':'4.8', 'id':'445563'},
                {'name':'上海玩具总动员酒店', 'score':'4.6', 'id':'4687213'},
            ]
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
        # print(self.session.cookies.items())

    def get_remarks(self, hotel, num):
        self.get_cookies(hotel['id'])
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
            'commonStatisticList': [1, 3],
            'ftype':"",
            'head':head,
            "hotelId":hotel['id'],
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

    def parse(self, comments, need):
        # p = re.compile(r'[^\w，。！？,.、:；℃]')
        remarks=[]
        for comment in comments['groupList'][0]['commentList']:
            name = hotel['name']
            score = hotel['score']
            id = hotel['id']
            content = comment['content'].lower().replace('/', '').replace('\n', ' ')
            checkin = comment['checkin']
            roomname = comment['roomName']
            feedback = comment['feedbackList'][0]['content'].lower().replace('/', '').replace('\n', ' ')
            remark=f'{id}/{name}/{need}/{score}/{checkin}/{roomname}/{content}/{feedback}'
            print(remark)
            remarks.append(remark)
        return remarks


if __name__ == '__main__':
    hs = HotelSpider()
    names=['高评分','低评分','受欢迎','商务型','度假型','高端型','经济型','亲子型']
    hotypes = hs.get_hotels()
    # 酒店名称 需求类型 房间类型 评分 评论文本 来源【酒店/用户】
    for name in names:
        hotels = hotypes[name]
        # print(hotels)
        for hotel in hotels:
            # 测试有多少页？
            count, comments = hs.test(hotel,1)
            tnum = count//10+1
            for i in range(1, tnum+1):
                count, comments_ = hs.test(hotel,i)
                try:
                    remarks = hs.parse(comments_, name)
                    with open('./hotels.txt','a',encoding='utf8') as f:
                        f.write('\n'.join(remarks))
                        f.write('\n')
                except Exception as e:
                    print(e)
                    continue




