import re,time
import requests
from util import remark_save

class Mafeng(object):
    def __init__(self):
        self.poioId = [
            '6326847',  # 汉文化景区
            '5437286',  # 龟山汉墓
            "5437294",  # 徐州博物馆
            '1880916'  # 汉化石像馆
            "1871598",  # 狮子山楚王陵
            "5429508",  # 户部山——戏马台
            '7051442'  # 汉皇祖陵
            '5437299',  # 沛县汉城
            "6326840",  # 云龙湖
            '5428263',  # 窑湾古镇
        ]
        self.session = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        self.p = re.compile(r'[^\w，。！？,.、:；℃]')

    def get_coments(self, page, id):
        # {"poi_id":6583819,"page":"2","just_comment":1}
        self.headers['Referer']='https://www.mafengwo.cn/poi/'+id+'.html'
        url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?'
        params = { 'params': '{"poi_id":' + id + ',"page":"' + str(page) + '","just_comment":1}'}
        response = self.session.get(url, params=params, headers=self.headers, timeout=10).json()['data']
        return response

    def parse(self, html):
        # 日期正则
        date_pattern = r'<a class="btn-comment _j_comment" title="添加评论">评论</a>.*?\n.*?<span class="time">(.*?)</span>'
        # 评分正则
        star_pattern = r'<span class="s-star s-star(\d)"></span>'
        # 评论正则
        comment_pattern = r'<p class="rev-txt">([\s\S]*?)</p>'
        date_list = re.compile(date_pattern).findall(html)
        star_list = re.compile(star_pattern).findall(html)
        comment_list = re.compile(comment_pattern).findall(html)
        remarks=[]
        for i in range(0, len(date_list)):
            comment = comment_list[i].replace(' ', '').replace('<br>', '').replace('<br />', '').replace('<br/>', '')
            remarks.append({
                'publishTime': time.mktime(time.strptime(date_list[i], "%Y-%m-%d %H:%M:%S")),
                'score': star_list[i],
                'content': self.p.sub("", comment.lower()),
                'Locate': '',
                'usefulCount': 0
            })
        return remarks

    def main(self):
        for id in self.poioId:
            # 第一步尝试发送请求得出一共多少页
            commentCount = int(self.get_coments(1,id)['controller_data']['comment_count'])
            tatolNum = commentCount // 15 if commentCount % 15 == 0 else (commentCount // 15) + 1
            for i in range(tatolNum):
                html = self.get_coments(i, id)['html']
                remarks = self.parse(html)
                for remark in remarks:
                    print(remark)
                remark_save('mafengwo',remarks)


if __name__ == '__main__':
    mafeng=Mafeng()
    mafeng.main()