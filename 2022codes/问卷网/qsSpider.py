# -*- coding:utf-8 -*-
import os, re, json, time, random
import execjs, js2py
import requests
from parsel import Selector


class WenjuanWang(object):

    def __init__(self, id, is_exam=False):
        self.sessions = requests.session()
        self.shortId = id
        self.is_exam = is_exam
        self.origin = 'https://www.wenjuan.pub' if self.is_exam else 'https://www.wenjuan.com'
        self.appkey = ''
        self.pid = ''

    def get_cookies(self, index_url, proxy):
        """
        获取首页响应内容，为sessesion补充cookie信息。
        :param proxy:
        :return:
        """
        self.sessions.headers["User-Agent"] ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        response = self.sessions.get(index_url, proxies=proxy, timeout=10)
        cookie_str = response.headers['Set-Cookie']
        browser_id = re.search('browser_id=([0-9a-f]{24})', cookie_str).group(1)
        self.sessions.cookies.update({
            'origin_path': f'/s/{self.shortId}/',
            '_zvt': f"{int(time.time() * 1000) - 384}.{int(time.time() * 1000)}",
            'origin_referer': 'default',
            '_zver': 'c.1.0',
            '_za': self.get_za(),
            'hawkeye_mid': '',
            'browser_id': browser_id
        })
        url = 'https://s0.wenjuan.com/wj-rspdssr/static/81b238f0/js/app.b2169ac0.chunk.js'
        res_js = self.sessions.get(url, proxies=proxy, timeout=10).content.decode()
        self.appkey = re.search(r'appkey:"(\w+)",', res_js).group(1)
        return response.content.decode()

    def get_za(self):
        """
        :return: cookie参数za
        """
        rand_str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        randtumple = (rand_str[random.randrange(0, len(rand_str))] for i in range(0, 21))
        return random.choice(rand_str[:10]) + ''.join(randtumple)

    def get_parameters(self, params, is_uuid=False):
        """
        调用js获取参数idy_uuid和signature，其中idy_uuid随机生成，signature根据传入的参数params计算而得出，
        :param params:
        :return: signature
        """
        os.environ["EXECJS_RUNTIME"] = "Node"
        node = execjs.get()
        with open('signature.js', 'r', encoding='utf8') as f:
            script = f.read()
        context = node.compile(script)
        if is_uuid:
            params['idy_uuid'] = context.eval("getUuid()")
        return context.call("get_sign", json.dumps(params), self.appkey)

    def get_answer(self, content):
        """
        传入首页响应内容，根据题目类型将其解析为答案字符串并返回。
        :param content: 首页响应
        :return:答案字符串
        """
        sel = Selector(content)
        js_text = 'var index' + sel.xpath('//script/text()').getall()[1][24:-121]
        context = js2py.EvalJs(enable_require=True)
        context.execute(js_text)
        questions = context.index['QUESTION_DICT'].to_dict()
        self.pid = context.index["projectId"]
        self.answerPath = context.index["currentPageId"]
        questions_dict = {}
        for k, v in questions.items():
            if v["question_type"] == 2:
                # 单选题：id:[opid]/id:[opid,'其他内容']
                option = random.choice(v['option_list'])
                questions_dict[k] = [option['_id']['$oid'], '其他补充内容'] if option['is_open'] else [option['_id']['$oid']]
            elif v["question_type"] == 3:
                # 多选题：id:[[opid1], [opid2],..,[opidn,'其他内容']]
                ops = v["option_list"]
                sum = len(ops)
                num = random.choice([i + 1 for i in range(sum - 1)])
                target_ops = random.sample(ops, num)
                questions_dict[k] = [[op['_id']['$oid'], '其他补充内容'] if op['is_open'] else [op['_id']['$oid']] for op in target_ops]
            elif v["question_type"] == 6:
                # 填空题 ： id:{opid__open:'text'}
                questions_dict[k] = {v["option_id_list"][0] + '_open': '填空题文本内容'}
            elif v["question_type"] == 7:
                # 多项评分题: id:{row_id:{op_id:'1'},...}
                custom_attr = v['custom_attr']
                range_ = [str(i) for i in range(int(custom_attr['min_answer_num']), int(custom_attr['max_answer_num']))]
                matrixrows = v['matrixrow_id_list']
                questions_dict[k] = {item:{v["option_id_list"][0]: random.choice(range_)} for item in matrixrows}
            elif v["question_type"] == 50:
                # 量表题：id:{opid:["1"]}
                # 有的范围1-5；有的0-10
                custom_attr = v['custom_attr']
                range_ = [str(i) for i in range(int(custom_attr['min_answer_num']), int(custom_attr['max_answer_num']))]
                questions_dict[k] = {v["option_id_list"][0]: [random.choice(range_)]}
        return questions_dict

    def save_answers(self, total_answers_dict, proxy):
        save_url = 'https://www.wenjuan.pub/api/rspd/save_page_answers/'
        data = {
            'appkey': self.appkey,
            'assess_accuracy': 1,
            'page_rspd_data_str': json.dumps(total_answers_dict),
            'short_id': self.shortId,
            'timestamp': int(time.time()*1000),
            'web_site': "wenjuan_web"
        }
        data['signature'] = self.get_parameters(data)
        response = self.sessions.post(save_url, json=data, timeout=10, proxies=proxy).json()["data"]
        question_score_map_dict = response['question_score_map']
        assess_question_correct_dict = {'question_correct_list':response['question_correct_list'],'option_correct_list': response['option_correct_list']}
        return question_score_map_dict, assess_question_correct_dict

    def main(self, proxy=None):
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        index_url = self.origin + f'/s/{self.shortId}/'
        content = self.get_cookies(index_url, proxy=proxy)
        total_answers_dict = self.get_answer(content)
        self.sessions.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': self.origin,
            'Pragma': 'no-cache',
            'Referer': index_url,
            'Host':  self.origin[8:],
            'X-Requested-With': 'XMLHttpRequest',
            'X-WJ-ORIGIN-SURVEY-URL': index_url,
        })
        if self.is_exam:
            submit_url = self.origin + f"/api/rspd/a/{self.shortId}/"
            total_answers = {"answers": total_answers_dict, "answer_path": [self.answerPath]}
            question_score_map_dict, question_correct_dict = self.save_answers(total_answers, proxy)
            score = sum(question_score_map_dict.values())
            data = {
                'appkey': self.appkey,
                'assess_question_correct_info': json.dumps(question_correct_dict),
                'auto_submit_post': 'false',
                'finish_status': "1",
                'project_version': 1,
                'question_captcha_map_str': "{}",
                'question_ids_skipped_by_time': "{}",
                'question_score_map_str': json.dumps(question_score_map_dict),
                'queston_id_str': json.dumps(list(total_answers_dict.keys())),
                'score': int(score),
                'timestamp': int(time.time()*1000),
                'timestr': timestr,  # 访问问卷时间
                'total_answers_str': json.dumps(total_answers_dict),
                'web_site': "wenjuan_web",
                'wx_user_info_str': "{}",
            }
        else:
            submit_url = self.origin + f"/api/rspd/s/{self.shortId}/"
            data = {
                'appkey': self.appkey,
                'auto_submit_post': 'false',
                'finish_status': "1",
                'project_version': 1,
                'question_captcha_map_str': "{}",
                'question_ids_skipped_by_time': "{}",
                'timestamp': int(time.time() * 1000),  # 提交时间
                'timestr': timestr,  # 访问问卷时间
                'total_answers_str': json.dumps(total_answers_dict),
                'web_site': "wenjuan_web",
                'wx_user_info_str': "{}",
            }
        data['signature'] = self.get_parameters(data, is_uuid=True)
        res = self.sessions.post(submit_url, json=data, timeout=10, proxies=proxy)
        result = res.json()
        score = f',得分{result["score"]}' if 'score' in result.keys() else ''
        print(f"已完成第{result['seq']}次{score}")


if __name__ == '__main__':
    # https://www.wenjuan.com/s/IVrmyuI/
    # https://www.wenjuan.pub/s/6be2ye0/

    id = 'IVrmyuI'  # 普通问卷
    # id = '6be2ye0'  # 考试问卷
    wjw = WenjuanWang(
        id,  # 问卷id
        is_exam=False  # 是否为考试试卷，提交网页的api不一样。
    )
    # wjw.main(proxy=None)
    for i in range(10):
        wjw = WenjuanWang(id)
        wjw.main(proxy=None)