# -*- coding: utf-8 -*-
import json
import requests
import js2py
import re
import time
from bs4 import BeautifulSoup
from random import random
# from lxml import etree
# from fake_useragent import UserAgent


class JsdClock(object):

    def __init__(self,account,password):
        self.account = account
        self.password = password
        self.session = requests.session()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        self.urls = [
            'https://ehall.jsnu.edu.cn/infoplus/form/DB_XXHC_JKDKSTU/start',
            'https://authserver.jsnu.edu.cn/',
            'https://ehall.jsnu.edu.cn/infoplus/interface/',
        ]
        self.rand = str(random() * 999)
        self.b = 'fieldSQRxzwzxxdd,fieldSQRjchbryxm,fieldSQRjghb,fieldSQRxjzdsf,fieldSQRglsm,fieldSQRjcrdd,fieldSQRzy,fieldSQRszbm,fieldSQRhjcs,fieldSQRsbsj,fieldSQRdqtwzt,fieldSQRjchbrybz,fieldSQRjjlxrdh,fieldSQRjchbrystzk,fieldSQRtjyqyzdqlksj,fieldSQRjcqzysryjcrq,fieldDTRxm,fieldSQRsbrq,fieldSQRstzk,fieldSQRjcryxm,fieldSQRhjsf,fieldSQRjcrygx,fieldSQRjjlxr,fieldSQRtjyqyzdqsf,fieldFDD2,fieldFDD3,fieldSQRxm,fieldFDD6,fieldSQRjcrystzk,fieldFDD4,fieldFDD5,fieldSQRxb,fieldSQRxjzdxxdz,fieldSQRjcqzysryxm,fieldSQRjcqzysrygx,fieldSQRdh,fieldSQRhjqx,fieldDTRdh,fieldSQRcsrq,fieldSQRxq,fieldSQRjchbryrq,fieldSQRxjzdqx,fieldSQRxykh,fieldSQRjchbry,fieldSQRxjzdcs,fieldSQRsfdt,fieldSQRbj,fieldSQRtjyqyzdqddsj,fieldSQRjcqzysryjcdd,fieldSQRtjyqyzdqcs,fieldSQRjcqzysrystzk,fieldSQRsjsfbd,fieldSQRss,fieldSQRjcqzry,fieldSQRyqyzdq,fieldSQRbz,fieldSQRglcs,fieldSQRzlsm,fieldSQRhjlx,fieldSQRszwz'
        self.start_dict = {
            'fieldQR': True,
            '_VAR_ACTION_INDEP_ORGANIZES_Codes': '0088',
            '_VAR_ACTION_REALNAME': '',
            '_VAR_ACTION_ORGANIZE': '0088',
            '_VAR_ACTION_INDEP_ORGANIZE': '0088',
            '_VAR_ACTION_INDEP_ORGANIZE_Name': '商学院',
            '_VAR_ACTION_ORGANIZE_Name': '商学院',
            '_VAR_OWNER_ORGANIZES_Codes': '0088',
            '_VAR_ADDR': '',
            '_VAR_OWNER_ORGANIZES_Names': '商学院',
            '_VAR_URL': "https://ehall.jsnu.edu.cn/infoplus/form/DB_XXHC_JKDKSTU/start",
            '_VAR_URL_Name': "https://ehall.jsnu.edu.cn/infoplus/form/DB_XXHC_JKDKSTU/start",
            '_VAR_URL_Attr': '{}',
            '_VAR_RELEASE': 'true',
            '_VAR_TODAY': '',
            '_VAR_NOW_MONTH': '',
            '_VAR_ACTION_USERCODES': '',
            '_VAR_ACTION_EMAIL': '',
            '_VAR_ACTION_ACCOUNT_FRIENDLY': '',
            '_VAR_ACTION_ACCOUNT': '',
            '_VAR_ACTION_INDEP_ORGANIZES_Names': '商学院',
            '_VAR_OWNER_ACCOUNT': '',
            '_VAR_ACTION_ORGANIZES_Names': '商学院',
            '_VAR_OWNER_PHONE': '',
            '_VAR_OWNER_USERCODES': '',
            '_VAR_NOW_DAY': '',
            '_VAR_OWNER_EMAIL': '2020220062@jsnu.edu.cn',
            '_VAR_OWNER_REALNAME': '',
            '_VAR_NOW': '',
            '_VAR_ENTRY_NUMBER': '-1',
            '_VAR_OWNER_ACCOUNT_FRIENDLY': '',
            '_VAR_POSITIONS': '',
            '_VAR_ACTION_PHONE': '19895626933',
            '_VAR_ACTION_ORGANIZES_Codes': '0088',
            '_VAR_NOW_YEAR': '2022',
            '_VAR_ENTRY_NAME': '',
            '_VAR_ENTRY_TAGS': '',
        }

    def encryptAES(self, _p0, _p1):
        context = js2py.EvalJs(enable_require=True)
        with open("encrypt.js", 'r', encoding='utf8') as f:
            context.execute(f.read())
        passwordEncrypt = context.encryptAES(_p0, _p1)
        return passwordEncrypt

    def get_csrfToken(self):
        response = self.session.get(self.urls[0], headers=self.headers, timeout=10)
        # html = etree.HTML(response.text)
        # service = html.xpath('//form[@id="casLoginForm"]/@action')[0]
        # input_node_list = html.xpath('//form[@id="casLoginForm"]/input[@type="hidden"]/@value')
        soup = BeautifulSoup(response.text, features="html")
        form_soup = soup.select('#casLoginForm')[0]
        service = form_soup.attrs['action']
        input_node_list = [input.attrs['value'] for input in form_soup.find_all(attrs={'type': "hidden"})]
        pwdDefaultEncrypt = self.encryptAES(self.password, input_node_list[5])
        post_data = {
            'username': self.account,
            'password': pwdDefaultEncrypt,
            'lt': input_node_list[0],
            'dllt': input_node_list[1],
            'execution': input_node_list[2],
            '_eventId': input_node_list[3],
            'rmShown': input_node_list[4],
        }
        data = self.session.post(self.urls[1] + service[1:], headers=self.headers, data=post_data, timeout=10).content.decode()
        workflowId = re.search(r'workflowId = "[a-zA-Z0-9\-]*', data).group()[14:]
        csrfToken = re.search(r'itemscope="csrfToken" content="[\w]*', data).group()[-32:]
        return workflowId, csrfToken

    def get_formStepId(self, csrfToken):
        post_data = {
            'idc': 'DB_XXHC_JKDKSTU',
            'release': '',
            'csrfToken':  csrfToken,
            'formData': json.dumps(self.start_dict, ensure_ascii=False)
        }
        render_url = self.session.post(self.urls[2] + 'start', headers=self.headers, data=post_data, timeout=10).json()["entities"][0]
        formStepId = render_url[-15:-7]
        return formStepId

    def get_predata(self, workflowId, csrfToken):
        t = f"{time.strftime('%Y-%m-%d', time.localtime())} 00:00:00"  # 获取当前时间数据，结构化为  时间元组字符串
        daystample = int(time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S")))
        data = {
            'workflowId': workflowId,
            'rand': self.rand,
            'width': '750',
            'csrfToken': csrfToken
        }
        res = self.session.post(self.urls[2] + 'preview', data=data, headers=self.headers, timeout=10).json()['entities'][0]['data']
        self.start_dict['_VAR_ACTION_REALNAME'] = res['fieldDTRxm']
        self.start_dict['_VAR_OWNER_REALNAME'] = res['fieldDTRxm']
        self.start_dict['_VAR_ADDR'] = res['_VAR_ADDR']
        self.start_dict['_VAR_TODAY'] = str(daystample)
        self.start_dict['_VAR_NOW'] = str(int(time.time()))
        self.start_dict['_VAR_ACTION_EMAIL'] = res['_VAR_ACTION_EMAIL']  # 邮箱
        self.start_dict['_VAR_OWNER_EMAIL'] = res['_VAR_ACTION_EMAIL']
        self.start_dict['_VAR_ACTION_USERCODES'] = res['fieldSQRxykh']   # 校园号
        self.start_dict['_VAR_ACTION_ACCOUNT_FRIENDLY'] = res['fieldSQRxykh']  # 校园卡号
        self.start_dict['_VAR_ACTION_ACCOUNT'] = res['fieldSQRxykh']  # 校园卡号
        self.start_dict['_VAR_OWNER_ACCOUNT_FRIENDLY'] = res['fieldSQRxykh']
        self.start_dict['_VAR_OWNER_USERCODES'] = res['fieldSQRxykh']
        self.start_dict['_VAR_OWNER_ACCOUNT'] = res['fieldSQRxykh']  #
        self.start_dict['_VAR_OWNER_PHONE'] = res['_VAR_ACTION_PHONE']  # 系统预留手机号
        self.start_dict['_VAR_ACTION_PHONE'] = res['_VAR_ACTION_PHONE']
        self.start_dict['_VAR_POSITIONS'] = res['_VAR_POSITIONS']
        self.start_dict['_VAR_NOW_YEAR'] = res['_VAR_NOW_YEAR']

    def make_formdata(self, stepId, csrfToken):
        tmdel = 39742
        t = f"{time.strftime('%Y-%m-%d', time.localtime())} 00:00:00"  # 获取当前时间数据，结构化为  时间元组字符串
        daystample = int(time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S")))
        post_data={
            'stepId': stepId,
            'instanceId': '',
            'admin': 'false',
            'rand': self.rand,
            'width': '750',
            'lang': 'zh',
            'csrfToken': csrfToken,
        }
        self.session.headers.update({'Referer': self.urls[0][:-21] + stepId + 'render'})
        entities_dict = self.session.post(self.urls[2] + 'render', headers=self.headers, data=post_data, timeout=10).json()['entities'][0]['data']
        print(entities_dict)
        formData_dict = {
            '_VAR_ACTION_ACCOUNT': entities_dict['_VAR_ACTION_ACCOUNT'],
            '_VAR_ACTION_ORGANIZES_Names': entities_dict['_VAR_ACTION_ORGANIZES_Names'],
            '_VAR_ACTION_ACCOUNT_FRIENDLY': entities_dict['_VAR_ACTION_ACCOUNT_FRIENDLY'],
            '_VAR_ACTION_EMAIL': entities_dict['_VAR_ACTION_EMAIL'],
            '_VAR_ACTION_INDEP_ORGANIZE': entities_dict['_VAR_ACTION_INDEP_ORGANIZE'],
            '_VAR_ACTION_INDEP_ORGANIZES_Codes': entities_dict['_VAR_ACTION_INDEP_ORGANIZES_Codes'],
            '_VAR_ACTION_INDEP_ORGANIZES_Names': entities_dict['_VAR_ACTION_INDEP_ORGANIZES_Names'],
            '_VAR_ACTION_INDEP_ORGANIZE_Name': entities_dict['_VAR_ACTION_INDEP_ORGANIZE_Name'],
            '_VAR_ACTION_ORGANIZE': entities_dict['_VAR_ACTION_ORGANIZE'],
            '_VAR_ACTION_ORGANIZES_Codes':entities_dict['_VAR_ACTION_ORGANIZES_Codes'],
            '_VAR_ACTION_ORGANIZE_Name': entities_dict['_VAR_ACTION_ORGANIZE_Name'],
            '_VAR_ACTION_PHONE': entities_dict['_VAR_ACTION_PHONE'],
            '_VAR_ACTION_REALNAME': entities_dict['_VAR_ACTION_REALNAME'],
            '_VAR_ACTION_USERCODES': entities_dict['_VAR_ACTION_USERCODES'],
            '_VAR_ADDR': entities_dict['_VAR_ADDR'],
            '_VAR_ENTRY_NAME': '健康申报',
            '_VAR_ENTRY_NUMBER': entities_dict['_VAR_ENTRY_NUMBER'],
            '_VAR_ENTRY_TAGS': '健康申报',
            '_VAR_EXECUTE_INDEP_ORGANIZE': entities_dict['_VAR_EXECUTE_INDEP_ORGANIZE'],
            '_VAR_EXECUTE_INDEP_ORGANIZES_Codes': entities_dict['_VAR_EXECUTE_INDEP_ORGANIZES_Codes'],
            '_VAR_EXECUTE_INDEP_ORGANIZES_Names': entities_dict['_VAR_EXECUTE_INDEP_ORGANIZES_Names'],
            '_VAR_EXECUTE_INDEP_ORGANIZE_Name': entities_dict['_VAR_EXECUTE_INDEP_ORGANIZE_Name'],
            '_VAR_EXECUTE_ORGANIZE': entities_dict['_VAR_EXECUTE_ORGANIZE'],
            '_VAR_EXECUTE_ORGANIZES_Codes': entities_dict['_VAR_EXECUTE_ORGANIZES_Codes'],
            '_VAR_EXECUTE_ORGANIZES_Names': entities_dict['_VAR_EXECUTE_ORGANIZES_Names'],
            '_VAR_EXECUTE_ORGANIZE_Name': entities_dict['_VAR_EXECUTE_ORGANIZE_Name'],
            '_VAR_EXECUTE_POSITIONS': entities_dict['_VAR_EXECUTE_POSITIONS'],
            '_VAR_EXECUTE_USERCODES': entities_dict['_VAR_EXECUTE_USERCODES'],
            '_VAR_NOW': str(int(time.time())),  # 该秒的时间戳
            '_VAR_NOW_DAY': str(entities_dict['_VAR_NOW_DAY']),  # 计算获取该天00：00：00的时间戳
            '_VAR_NOW_MONTH':t[6:7],  # 该天的属于——月
            '_VAR_NOW_YEAR':t[:4],
            '_VAR_OWNER_ACCOUNT':entities_dict['_VAR_OWNER_ACCOUNT'],

            '_VAR_OWNER_ACCOUNT_FRIENDLY': entities_dict['_VAR_OWNER_ACCOUNT_FRIENDLY'],
            '_VAR_OWNER_EMAIL': entities_dict['_VAR_OWNER_EMAIL'],
            '_VAR_OWNER_ORGANIZES_Codes':entities_dict['_VAR_OWNER_ORGANIZES_Codes'],
            '_VAR_OWNER_ORGANIZES_Names':entities_dict['_VAR_OWNER_ORGANIZES_Names'],
            '_VAR_OWNER_PHONE': entities_dict['_VAR_OWNER_PHONE'],
            '_VAR_OWNER_REALNAME': entities_dict['_VAR_OWNER_REALNAME'],
            '_VAR_OWNER_USERCODES': entities_dict['_VAR_OWNER_USERCODES'],
            '_VAR_POSITIONS': entities_dict['_VAR_POSITIONS'],
            '_VAR_RELEASE': str(entities_dict['_VAR_RELEASE']).lower(),
            '_VAR_STEP_CODE': entities_dict['_VAR_STEP_CODE'],
            '_VAR_STEP_NUMBER': stepId,
            '_VAR_TODAY': str(daystample),
            '_VAR_URL': 'https://ehall.jsnu.edu.cn/infoplus/form/' + stepId + '/render',
            '_VAR_URL_Attr': entities_dict['_VAR_URL_Attr'],
            '_VAR_URL_Name': self.urls[0],

            'fieldDTRdh': entities_dict['fieldDTRdh'],
            'fieldDTRxm': entities_dict['fieldDTRxm'],
            'fieldFDD2': entities_dict['fieldFDD2'],
            'fieldFDD3': entities_dict['fieldFDD3'],
            'fieldFDD4':entities_dict['fieldFDD4'],
            'fieldFDD5':entities_dict['fieldFDD5'],
            'fieldFDD6':entities_dict['fieldFDD6'],
            'fieldSQRbj':entities_dict['fieldSQRbj'],
            'fieldSQRbz': entities_dict['fieldSQRbz'],
            'fieldSQRcsrq': int(entities_dict['fieldSQRcsrq']),
            'fieldSQRdh': entities_dict['fieldSQRdh'],
            'fieldSQRdqtwzt': entities_dict['fieldSQRdqtwzt'],
            'fieldSQRglcs': entities_dict['fieldSQRglcs'],
            'fieldSQRglcs_Name': entities_dict['fieldSQRglcs_Name'],
            'fieldSQRglsm': entities_dict['fieldSQRglsm'],

            'fieldSQRhjsf': entities_dict['fieldSQRhjsf'],  #42000
            'fieldSQRhjsf_Name': entities_dict['fieldSQRhjsf_Name'],

            'fieldSQRhjcs': entities_dict['fieldSQRhjcs'],  # 420800
            'fieldSQRhjcs_Attr': '{"_parent":"'+ entities_dict['fieldSQRhjsf'] +'"}', #
            'fieldSQRhjcs_Name': entities_dict['fieldSQRhjcs_Name'],
            'fieldSQRhjlx': entities_dict['fieldSQRhjlx'],

            'fieldSQRhjqx':entities_dict['fieldSQRhjqx'], # 420881
            'fieldSQRhjqx_Attr': '{"_parent":"' + entities_dict['fieldSQRhjcs'] + '"}',
            'fieldSQRhjqx_Name': entities_dict['fieldSQRhjqx_Name'],

            'fieldSQRjchbry': entities_dict['fieldSQRjchbry'],
            'fieldSQRjchbrybz': entities_dict['fieldSQRjchbrybz'],
            'fieldSQRjchbryxm':entities_dict['fieldSQRjchbryxm'],

            'fieldSQRjcqzry': entities_dict['fieldSQRjcqzry'],
            'fieldSQRjcqzysrygx': entities_dict['fieldSQRjcqzysrygx'],
            'fieldSQRjcqzysryjcdd': entities_dict['fieldSQRjcqzysryjcdd'],
            'fieldSQRjcqzysrystzk': entities_dict['fieldSQRjcqzysrystzk'],
            'fieldSQRjcqzysrystzk_Name': entities_dict['fieldSQRjcqzysrystzk_Name'],
            'fieldSQRjcqzysryxm': entities_dict['fieldSQRjcqzysryxm'],
            'fieldSQRjcrdd': entities_dict['fieldSQRjcrdd'],
            'fieldSQRjcrygx': entities_dict['fieldSQRjcrygx'],
            'fieldSQRjcrystzk': entities_dict['fieldSQRjcrystzk'],
            'fieldSQRjcrystzk_Name': entities_dict['fieldSQRjcrystzk_Name'],
            'fieldSQRjcryxm': entities_dict['fieldSQRjcryxm'],
            'fieldSQRjghb': entities_dict['fieldSQRjghb'],
            'fieldSQRjjlxr': entities_dict['fieldSQRjjlxr'],
            'fieldSQRjjlxrdh': entities_dict['fieldSQRjjlxrdh'],
            'fieldSQRsbrq': int(time.time()) + tmdel,  # 过期时间
            'fieldSQRsbsj': int(time.time()) + tmdel,  # 过期时间
            'fieldSQRsfdt': entities_dict['fieldSQRsfdt'],
            # fieldSQRsjsfbd  ,# entities_dict['fieldSQRsjsfbd']
            'fieldSQRsjsfbd': '1',
            'fieldSQRss': entities_dict['fieldSQRss'],
            'fieldSQRstzk': entities_dict['fieldSQRstzk'],
            'fieldSQRstzk_Name': entities_dict['fieldSQRstzk_Name'],
            'fieldSQRszbm': entities_dict['fieldSQRszbm'],

            'fieldSQRszbm_Name': entities_dict['fieldSQRszbm_Name'],
            'fieldSQRszwz': entities_dict['fieldSQRszwz'],
            'fieldSQRtjyqyzdqcs': entities_dict['fieldSQRtjyqyzdqcs'],
            'fieldSQRtjyqyzdqcs_Attr': ['{"_parent":""}'],
            'fieldSQRtjyqyzdqcs_Name': entities_dict['fieldSQRtjyqyzdqcs_Name'],
            'fieldSQRtjyqyzdqsf': entities_dict['fieldSQRtjyqyzdqsf'],
            'fieldSQRtjyqyzdqsf_Name': entities_dict['fieldSQRtjyqyzdqsf_Name'],
            'fieldSQRxb': entities_dict['fieldSQRxb'],

            'fieldSQRxjzdsf': entities_dict['fieldSQRxjzdsf'],  # 320000
            'fieldSQRxjzdsf_Name': entities_dict['fieldSQRxjzdsf_Name'],

            'fieldSQRxjzdcs': entities_dict['fieldSQRxjzdcs'],  # 320300
            'fieldSQRxjzdcs_Attr': '{"_parent":"'+ entities_dict['fieldSQRxjzdsf'] +'"}',
            'fieldSQRxjzdcs_Name': entities_dict['fieldSQRxjzdcs_Name'],
            'fieldSQRxjzdqx': entities_dict['fieldSQRxjzdqx'],
            'fieldSQRxjzdqx_Attr': '{"_parent":"'+ entities_dict['fieldSQRxjzdcs'] +'"}',
            'fieldSQRxjzdqx_Name':entities_dict['fieldSQRxjzdqx_Name'],

            'fieldSQRxjzdxxdz': entities_dict['fieldSQRxjzdxxdz'],
            'fieldSQRxm': entities_dict['fieldSQRxm'],
            'fieldSQRxq':entities_dict['fieldSQRxq'],

            'fieldSQRxq_Name': entities_dict['fieldSQRxq_Name'],
            'fieldSQRxykh': entities_dict['fieldSQRxykh'],
            'fieldSQRxzwzxxdd': entities_dict['fieldSQRxzwzxxdd'],
            'fieldSQRyqyzdq':entities_dict['fieldSQRyqyzdq'],
            'fieldSQRzlsm': entities_dict['fieldSQRzlsm'],
            'fieldSQRzy': entities_dict['fieldSQRzy'],

            'fieldSQRtjyqyzdqddsj':[''],
            'fieldSQRtjyqyzdqlksj': [''],
            'fieldSQRjcqzysryjcrq': [''],
            'fieldSQRjchbryrq': [''],
            'fieldSQRjchbrystzk':[''],
            'fieldSQRjchbrystzk_Name':[''],
            'groupSQRjchbrymdList': [0],
            'groupSQRjcqzysryList': [0],
            'groupSQRjcryList': [0],
            'groupSQRtjyqyzdqList': [0]
        }
        return json.dumps(formData_dict, ensure_ascii=False)

    def get_clock(self, csrfToken, formStepId, formDate_json):
        post_data = {
            'stepId': formStepId,
            'actionId': '3',
            'formData': formDate_json,
            'timestamp': str(int(time.time() * 1000)),
            'rand': self.rand,
            'boundFields': self.b,
            'csrfToken': csrfToken,
            'lang': 'zh',
        }
        self.session.headers.update({'Referer': self.urls[0]})
        self.session.post(self.urls[2] + 'listNextStepsUsers', headers=self.headers, data=post_data, timeout=10)

    def do_action(self, csrfToken, formStepId, formDate_json):
        post_data = {
            'actionId': '3',
            'formData': formDate_json,  #
            'remark': '',
            'rand': self.rand,
            'nextUsers': '{}',
            'stepId': formStepId,
            'timestamp': str(int(time.time())),
            'boundFields': self.b,
            'csrfToken': csrfToken,
            'lang': 'zh'
        }
        self.session.headers.update({'Referer': 'https://ehall.jsnu.edu.cn/infoplus/form/' + formStepId + '/render'})
        return self.session.post(self.urls[2] + 'doAction', headers=self.headers, data=post_data, timeout=10)

    def main(self):
        workflowId, csrfToken= self.get_csrfToken()
        self.get_predata(workflowId, csrfToken)
        formStepId = self.get_formStepId(csrfToken)
        formDate_json = self.make_formdata(formStepId, csrfToken)
        self.get_clock(csrfToken, formStepId, formDate_json)
        self.do_action(csrfToken, formStepId, formDate_json)


if __name__ == '__main__':
    xhh_jsdclock = JsdClock('2020220062','21284825ss')
    # cg_jsdclock = JsdClock('2020220060', 'cg20000118..')
    xhh_jsdclock.main()
    # cg_jsdclock.main()



