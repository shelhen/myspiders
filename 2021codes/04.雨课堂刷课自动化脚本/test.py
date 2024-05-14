import requests
from lxml import etree
import re
from difflib import SequenceMatcher

class Findanswers(object):

    def __init__(self):
        self.url = 'https://www.chatiba.com/s?'
        self.session = requests.session()
        self.headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }

    def login(self):
        data = {
            'email': 'shelhen@163.com',
            'password': '21284825ss'
        }
        self.session.post(self.url[:-2]+ 'login_', data=data, headers=self.headers, timeout=10)

    def search(self, word):
        # self.session.get(self.url[:-2], headers=self.headers, timeout=10)
        params={'s': word}
        response = self.session.get(self.url, headers=self.headers, params=params, timeout=10)
        html = etree.HTML(response.content.decode())
        queslist_items = html.xpath('//div[@class="queslist-item"]')
        detail_url_list = []
        for item in queslist_items:
            url = str(item.xpath('./a[@target="_blank"]/@href')[0])
            detail_url_list.append(url)
        return detail_url_list[:3]

    def get_answer(self, url_list):
        answer_list = []
        for url in url_list:
            detail_page = self.session.get(url, headers=self.headers, timeout=10).content.decode()
            csrf_torken = re.search('<meta name="csrf-token" content="(\w{40})">', detail_page).group(1)
            html2 = etree.HTML(detail_page)
            node = html2.xpath('//div[@class="quesinfo"]')[0]
            data_id = node.xpath('./div[@class="getanswer"]/@data-id')[0]
            content = ''.join(node.xpath('./div[@class="quesinfo-text"]/h1/text()')).strip()
            options = node.xpath('./div[@class="quesinfo-options"]/p/text()')

            options_dict = {}
            for op in options:  # op是个字符串
                options_dict[op.split(' ')[1][:-1]]= op.split(' ')[-1]
            data = {'id': data_id}
            self.session.headers.update({'X-CSRF-TOKEN': csrf_torken})
            res = self.session.post(self.url[:-2]+'get_answer', headers=self.headers, data=data, timeout=10).json()
            answer = res['data']['question']['answer']
            analysis = res['data']['question']['analysis']
            answers = {}
            if answer in ['正确', '错误','答案：正确','答案：错误']:
                # 如果是判断题，也是直接题目 + 答案
                if answer == '正确' or '答案：正确':
                    Options = True
                else:
                    Options = False
                answers.update({
                    'Content': content,
                    'ProblemType': 6,
                    'Options': Options,
                    'Analysis': analysis
                })
            elif answer in ['A', 'B', 'C', 'D']:
                # 如果是单选题，直接返回  题目+答案即可，多余选项不需要 ,answer中应该包含A,B,C,D其一，若为A,则匹配
                answers.update({
                    'Content': content,
                    'ProblemType': 1,
                    'Options': options_dict[answer],
                    'Analysis': analysis
                })
            elif answer in ['AB', 'AC', 'AD', 'BC', 'BD', 'CD', 'ABC', 'ABD', 'ACD', 'BCD', 'ABCD']:
                # 如果是多选题呢，需要将选项拆分构造字典{key:题干,value:[答案1，答案2，答案3，答案4]}
                options_list = [options_dict[op] for op in options_dict if op in answer]
                answers.update({
                    'Content': content,
                    'ProblemType': 2,
                    'Options': options_list,
                    'Analysis': analysis
                })
            else:
                # 填空题呢？暂时不处理
                answers.update({
                    'Content': content,
                    'ProblemType': 4,
                    'Options': answer,
                    'Analysis': analysis
                })
            answer_list.append(answers)
        return answer_list

    def Matcher(self,a,b):
        return SequenceMatcher(None, a, b).ratio()


    def main(self):

        word1 = '某大学老师做社会学实验，召集了养老院的一些老人，让他们观看南京大屠杀的影像资料，并用专用仪器测量他们由于痛苦回忆带来的脑电波变动。该老师违反了哪条学术规范'
        word2 = '科研伦理与学术规范应当秉持什么样的价值导向'
        word3 = '学术道德就是指从事学术活动的主体在进行学术研究、学术评价或学术评审 、学术批评以及学术制度制定、学术奖励等活动的整个过程及结果中所应遵循的行为准则和规范的总和。'
        url_list = self.search(word3)
        self.login()
        answer_list = self.get_answer(url_list)
        for item in answer_list:
            print(item['Content'])
            print(item['Options'])
            print(self.Matcher(item['Content'], word3))
        # print(answer_list)


if __name__ == '__main__':
    fa = Findanswers()
    fa.main()


