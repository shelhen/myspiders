from gevent import monkey
monkey.patch_all()
from urllib3.util import parse_url
import requests, js2py
import gevent
from lxml import etree
import time, random, re
from subprocess import Popen, PIPE
from difflib import SequenceMatcher


class RainCourseSpider(object):

    def __init__(self):
        self.university_id = "3240"  # 江苏师范大学学校id
        self.url_root = "https://jsnuyjs.yuketang.cn/"  # 按需修改域名 example:https://*****.yuketang.cn/
        self.csrftoken = '5pOTZAIL4abVaVpG4JzE3XM8nxyJnSj4'
        self.sessionid = 'zresf4uamzn0qcp08q7cpvsg6u9rzcwh'
        self.url = 'https://www.chatiba.com/s?'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'Cookie': 'csrftoken=' + self.csrftoken + '; sessionid=' + self.sessionid + '; university_id=' + self.university_id + '; platform_id=3; platform_type=1',
            'x-csrftoken': self.csrftoken,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'university-id': self.university_id,
            'xtbz': 'cloud',
        }
        self.leaf_type = {
            "video": 0,
            "homework": 6,  # 课后作业
            "exam": 5,  # 考试
            "recommend": 3,  # pdf
            "discussion": 4  # 讨论
        }
        self.problem_type = {
            'SingleChoice': 1,
            'MultipleChoice': 2,
            'FillBlank': 4,
            'Judgement': 6,
        }
        self.rate = 0.75
        self.session = requests.session()

    def get_user_id(self):  # 首先要获取用户的个人ID，即user_id,该值在查询用户的视频进度时需要使用
        url = self.url_root + "edu_admin/check_user_session/"
        user_id = self.session.get(url, headers=self.headers, timeout=10).json()['data']['user_id']
        return user_id

    def get_ccid(self, classroom_id, video_id):
        url = self.url_root + 'mooc-api/v1/lms/learn/leaf_info/' + str(classroom_id) + '/' + str(video_id) + '/'
        ccid = requests.get(url, headers=self.headers).json()['data']['content_info']['media']['ccid']
        return ccid

    def get_auth_key(self, ccid):
        # for i in data.keys():
        #     auth_url = data[i][0]
        #     domain = parse_url(data[i][0]).host
        #     auth_key = url.split('?')[1].split('=')[1]
        url = self.url_root + 'api/open/audiovideo/playurl?video_id='+str(ccid) + '&provider=cc&file_type=1&is_single=0&domain=changjiang.yuketang.cn'
        data = self.session.get(url, headers=self.headers, timeout=10).json()['data']['playurl']['sources']
        return data

    def get_courses(self):
        courses = []
        url = self.url_root + "mooc-api/v1/lms/user/user-courses/?status=1&page=1&no_page=1&term=latest&uv_id=" + self.university_id
        response = self.session.get(url, headers=self.headers, timeout=10).json()
        for product in response["data"]["product_list"]:
            courses.append({
                    'course_name': product["course_name"],  # 课程名字
                    'classroom_id': product["classroom_id"],  # 班级id
                    'course_sign': product["course_sign"],  # 课程特征值
                    'sku_id': product["sku_id"],  # 课程sku值
                    'course_id': product["course_id"],  # 课程id
                })
        return courses

    def get_recommend(self, course_name, classroom_id, course_sign):
        url = self.url_root + "mooc-api/v1/lms/learn/course/chapter?cid=" + str(
            classroom_id) + "&term=latest&uv_id=" + self.university_id + "&sign=" + course_sign
        pdf_json = self.session.get(url, headers=self.headers).json()
        pdf_dic = {}
        try:
            for i in pdf_json["data"]["course_chapter"]:
                for j in i["section_leaf_list"]:
                    if "leaf_list" in j:
                        for z in j["leaf_list"]:
                            if z['leaf_type'] == self.leaf_type["recommend"]:
                                pdf_dic[z["id"]] = z["name"]
                    else:
                        if j['leaf_type'] == self.leaf_type["recommend"]:
                            pdf_dic[j["id"]] = j["name"]
            print(course_name + "共有" + str(len(pdf_dic)) + "个pdf需要观看！")
            return pdf_dic
        except:
            raise Exception("出错，未能拿到 pdf 数据，请重试！！")

    def get_videos(self, course_name, classroom_id, course_sign):
        url = self.url_root + "mooc-api/v1/lms/learn/course/chapter?cid=" + str(
            classroom_id) + "&term=latest&uv_id=" + self.university_id + "&sign=" + course_sign
        video_json = self.session.get(url, headers=self.headers).json()
        video_dic = {}
        try:
            for i in video_json["data"]["course_chapter"]:
                for j in i["section_leaf_list"]:
                    if "leaf_list" in j:
                        for z in j["leaf_list"]:
                            if z['leaf_type'] == self.leaf_type["video"]:
                                video_dic[z["id"]] = z["name"]
                    else:
                        if j['leaf_type'] == self.leaf_type["video"]:
                            video_dic[j["id"]] = j["name"]
            print(course_name + "共有" + str(len(video_dic)) + "个视频需要刷！")
            return video_dic
        except:
            raise Exception("出错，未能拿到 视频 数据，请重试！！")

    def get_homework(self, course_name, classroom_id, course_sign):
        url = self.url_root + "mooc-api/v1/lms/learn/course/chapter?cid=" + str(
            classroom_id) + "&term=latest&uv_id=" + self.university_id + "&sign=" + course_sign
        homework_json = self.session.get(url, headers=self.headers).json()
        homework_dict = {}
        try:
            for i in homework_json["data"]["course_chapter"]:
                for j in i["section_leaf_list"]:
                    if "leaf_list" in j:
                        for z in j["leaf_list"]:
                            if z['leaf_type'] == self.leaf_type["homework"]:
                                homework_dict[z["id"]] = z["name"]
                    else:
                        if j['leaf_type'] == self.leaf_type["homework"]:
                            homework_dict[j["id"]] = j["name"]
            print(course_name + "共有" + str(len(homework_dict)) + "个课后作业需要完成！")
            return homework_dict
        except:
            raise Exception("出错，未能拿到 课后作业 数据，请重试！！")

    def get_video_detail(self, classroom_id, user_id, video_id):
        url = self.url_root + 'video-log/detail/?classroom_id=' + str(classroom_id) + '&user_id='+ str(user_id) + '&video_id=' + str(video_id)
        video_detail = self.session.get(url, headers=self.headers, timeout=10).json()['data']['heartbeat']
        return video_detail

    def get_video_duration(self, ccid):
        url = 'https://changjiang.yuketang.cn/api/open/audiovideo/playurl?video_id=' + ccid + '&provider=cc&file_type=1&is_single=0&domain=changjiang.yuketang.cn'
        response = requests.get(url, headers=self.headers)
        data = response.json()['data']['playurl']['sources']
        for i in data.keys():
            p = Popen('./ffprobe.exe -print_format json {}'.format(data[i][0]), stdout=PIPE, stderr=PIPE, stdin=PIPE)
            p.wait()
            output = p.communicate()[1].decode()
            time_string = re.findall('Duration: (.*?),', output)[0]
            h, m, s = time_string.split(':')
            time = int(h) * 3600 + int(m) * 60 + round(float(s), 1)
            return time

    def build_heartbeat_payloads(self, course_id, ccid, classroom_id, sku_id, user_id, video_id, duration):

        count = 1
        data = self.get_auth_key(ccid)
        for i in data.keys():
            play_domain = parse_url(data[i][0]).host
        pg = js2py.eval_js('function func(x){return x.toString(36)}')(int((1 + random.random()) * 1048576))
        magic_time = 4.7
        def build_payload(played_time: float, duration: float, type: str, sq: int, timestamp: int):
            return {
                'c': course_id,
                'cc': ccid,
                'classroomid': classroom_id,
                'cp': played_time,  # 当前观看时长
                'd': duration,  # 暂时第一次请求为0，后面需要改为视频总长度duraction
                'et': type,
                'fp': 0,  # 未知参数，一直为0
                'i': 5,
                'lob': 'cloud4',
                'n': play_domain,  # play_domain
                'p': 'web',
                'pg': str(video_id) + '_' + pg,
                'skuid': sku_id,
                'sp': 1,  # 视频播放速度参数
                'sq': sq,  # 发送hert数据的总计数目，每次加一
                'slide': 0,  # 未知参数，一直为0
                't': 'video',
                'tp': 0,
                'ts': str(timestamp),
                'u': user_id,
                'uip': "",
                'v': video_id,
                'cards_id': 0,
                'v_url': "",
            }
        payloads = []
        payloads.append(build_payload(played_time=0, duration=0, type='loadstart', sq=count,
                                      timestamp=int(time.time() * 1000)))
        count += 1
        payloads.append(build_payload(played_time=0, duration=duration, type='loadeddata', sq=count,
                                      timestamp=int(time.time() * 1000)))
        count += 1
        payloads.append(build_payload(played_time=0, duration=duration, type='play', sq=count,
                                      timestamp=int(time.time() * 1000)))
        count += 1
        payloads.append(build_payload(played_time=0, duration=duration, type='playing', sq=count,
                                      timestamp=int(time.time() * 1000)))
        count += 1
        for i in range(int((duration - magic_time) / 5) + 5):
            if magic_time + i * 5 <= duration:
                payloads.append(
                    build_payload(played_time=magic_time + i * 5, duration=duration, type='heartbeat',
                                  sq=count, timestamp=int(time.time() * 1000)))
                count += 1
            else:
                break
        payloads.append(
            build_payload(played_time=duration, duration=duration, type='videoend', sq=count,
                          timestamp=int(time.time() * 1000)))
        return payloads

    def send_heartbeats(self, video_id, payloads, url, coroutine=False):
        pos = 0
        heartbeat_data_list = []
        for i in range(int(len(payloads) / 5)):
            heartbeat_data = {'heart_data': payloads[pos:pos + 5]}
            heartbeat_data_list.append(heartbeat_data)
            pos += 5
        heartbeat_data_list.append({'heart_data': payloads[pos:]})

        def send_packet(json_data):
            return self.session.post(self.url_root + "video-log/heartbeat/", headers=self.headers, json=json_data).json()

        def watch_video_progress(url, video_id):
            response = self.session.get(url, headers=self.headers, timeout=10).json()
            try:
                rate = float(response[video_id]["rate"])
            except:
                rate = 0.0
            return rate

        if not coroutine:
            for i in heartbeat_data_list:
                response = send_packet(i)
                rate = watch_video_progress(url, video_id)
                print(f'学习进度为：\t{rate:.2%}/100%')
                # 正常情况下，response为空，若response不为空，则遇到了延迟
                try:
                    s = response['code']
                    self.apply_delay(response['message'],i)
                except:
                    pass
        else:
            gevent.joinall([gevent.spawn(send_packet, i) for i in heartbeat_data_list])

    def apply_delay(self, response, data):
        try:
            delay_time = re.search(r'Expected available in(.+?)second.', response).group(1).strip()
            print("由于网络阻塞，万恶的雨课堂，要阻塞" + str(delay_time) + "秒")
            # 执行等待
            time.sleep(float(delay_time) + 0.5)
            print("恢复工作啦～～")
            submit_url = self.url_root + "mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=" + self.university_id
            self.session.post(url=submit_url, headers=self.headers, data=data)
        except:
            pass

    def video_watch(self, user_id, courses, number):
        if int(number):
            # 刷选中视频
            video_dict = self.get_videos(
                courses[number]["course_name"], courses[number]["classroom_id"],
                courses[number]["course_sign"])
            for video in video_dict.items():  # video[0]=video_id;video[1]=video_name
                ccid = self.get_ccid(courses[number]["classroom_id"], video[0])
                duration = self.get_video_duration(ccid)  # 获取视频总时长，获取需要刷的视频列表
                # 根据视频时长计算向服务器反馈的数据及时间
                payloads = self.build_heartbeat_payloads(
                    courses[number]["course_id"], ccid, courses[number]["classroom_id"],
                    courses[number]["sku_id"], user_id, video[0], duration)
                url = self.url_root + "video-log/get_video_watch_progress/?cid=" + str(courses[number]["course_id"]) + "&user_id=" + str(user_id) + "&classroom_id=" + str(courses[number]["classroom_id"]) + "&video_type=video&vtype=rate&video_id=" + str(video[0]) + "&snapshot=1&term=latest&uv_id=" + self.university_id
                heartbeat_data = self.get_video_detail(courses[number]["classroom_id"], user_id, video[0])
                try:
                    completed = heartbeat_data['completed']
                    if completed:
                        print(f'{video[1]} 视频已刷完，将跳转至下一视频！')
                        continue
                    else:
                        # 视频没刷完
                        self.send_heartbeats(str(video[0]), payloads, url)
                        print(f"视频{video[0]}----{video[1]}学习完成！")
                except:
                    # 视频没刷
                    self.send_heartbeats(str(video[0]), payloads, url)
        else:
            # 刷全部视频
            for item in courses:
                video_dict = self.get_videos(item["course_name"], item["classroom_id"], item["course_sign"])
                for video in video_dict.items():
                    ccid = self.get_ccid(item["classroom_id"], video[0])
                    duration = self.get_video_duration(ccid)

                    payloads = self.build_heartbeat_payloads(
                        item["course_id"], ccid, item["classroom_id"],
                        item["sku_id"], user_id, video[0], duration)

                    url = self.url_root + "video-log/get_video_watch_progress/?cid=" + str(
                        item["course_id"]) + "&user_id=" + user_id + "&classroom_id=" + str(
                        item["classroom_id"]) + "&video_type=video&vtype=rate&video_id=" + str(
                        video[0]) + "&snapshot=1&term=latest&uv_id=" + self.university_id

                    heartbeat_data = self.get_video_detail(item["classroom_id"], user_id, video[0])

                    try:
                        completed = heartbeat_data['completed']
                        if completed:
                            print(f'{video[1]} 视频已刷完，将跳转至下一视频！')
                            continue
                        else:
                            # 视频没刷完
                            self.send_heartbeats(str(video[0]), payloads, url)
                            print(f"视频{video[0]}----{video[1]}学习完成！")
                    except:
                        self.send_heartbeats(str(video[0]), payloads, url)  # 视频没刷

    def recomend_watch(self, courses, number):
        # 用来刷pdf阅读，
        if int(number):
            pdf_dict = self.get_recommend(
                courses[number]['course_name'],
                courses[number]['classroom_id'],
                courses[number]['course_sign'])
            for pdf in pdf_dict.items():
                url = self.url_root + 'pro/lms/' + courses[number]['course_sign'] + '/' + str(
                    courses[number]['classroom_id']) + '/graph/' + str(pdf[0])
                self.session.get(url, headers=self.headers, timeout=10)
        else:
            for course in courses:
                # course_name, classroom_id, course_sign
                pdf_dict = self.get_recommend(course['course_name'], course['classroom_id'], course['course_sign'])
                for pdf in pdf_dict.items():
                    url = self.url_root + 'pro/lms/' + course['course_sign'] + '/' + str(
                        course['classroom_id']) + '/graph/' + str(pdf[0])
                    self.session.get(url, headers=self.headers, timeout=10)

    def search_answers(self, keyword):
        username = 'shelhen@163.com'
        password = '21284825ss'
        params = {'s': keyword}
        response = self.session.get(self.url, headers=self.headers, params=params, timeout=10)
        html = etree.HTML(response.content.decode())
        queslist_items = html.xpath('//div[@class="queslist-item"]')
        url_list = [str(item.xpath('./a[@target="_blank"]/@href')[0]) for item in queslist_items]
        answers_list = []
        for url in url_list:
            detail_page = self.session.get(url, headers={'User-Agent': self.headers['User-Agent']}, timeout=10)
            csrf_torken = re.search('<meta name="csrf-token" content="(\w{40})">', detail_page.content.decode()).group(1)
            html2 = etree.HTML(detail_page.content.decode())
            node = html2.xpath('//div[@class="quesinfo"]')[0]
            try:
                data_id = node.xpath('./div[@class="getanswer"]/@data-id')[0]
                content = ''.join(node.xpath('./div[@class="quesinfo-text"]/h1/text()')).strip()
                options = node.xpath('./div[@class="quesinfo-options"]/p/text()')
                options_dict = {op.split(' ')[1][:-1]: op.split(' ')[-1] for op in options}
                data = {'id': data_id}
                data2 = {'email': username, 'password': password}
                self.session.post(self.url[:-2] + 'login_', data=data2, headers={'User-Agent': self.headers['User-Agent']},timeout=10)
                self.session.headers.update({'X-CSRF-TOKEN': csrf_torken})
                res = self.session.post(self.url[:-2]+'get_answer', headers={'User-Agent': self.headers['User-Agent']},data=data, timeout=10)
                answer = res.json()['data']['question']['answer']
                analysis = res.json()['data']['question']['analysis']
                answers = {}
                # 分析，这里用answers_list并不好用，首先，待会提取答案麻烦，其次，
                if answer in ['正确', '错误', '答案：正确', '答案：错误']:
                    # 如果是判断题，也是直接题目 + 答案
                    if answer == '正确' or '答案：正确':
                        Option = '正确'
                    else:
                        Option = '错误'
                    answers.update({
                        'Content': content,
                        'ProblemType': 6,
                        'Options': Option,
                        'Analysis':analysis
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
                answers_list.append(answers)
            except:
                pass
        return answers_list

    def get_exercise_list(self, classroom_id, sku_id, homework_id):
        get_leaf_type_id_url = self.url_root + "mooc-api/v1/lms/learn/leaf_info/" + classroom_id + "/" + homework_id + "/?term=latest&uv_id=" + self.university_id
        response = self.session.get(url=get_leaf_type_id_url, headers=self.headers, timeout=10)
        leaf_id = str(response.json()['data']['content_info']['leaf_type_id'])
        url = self.url_root + "mooc-api/v1/lms/exercise/get_exercise_list/" + leaf_id + '/' + sku_id + '/?term=latest&uv_id=' + self.university_id
        problems = self.session.get(url, headers=self.headers, timeout=10).json()['data']['problems']
        problems_list = []
        for problem in problems:
            option_dict = {i['key']: i["value"] for i in problem['content']['Options']}
            try:
                problems_list.append({
                    'Problem_id': problem['problem_id'],  # 问题id，用来帮助提交
                    'ProblemType': problem['content']['ProblemType'],  # 问题类别，用来帮助选择答案
                    'Content': problem['content']['Body'] ,  # 问题内容，
                    'Options': option_dict,  # 问题选项{A:...,B:...,C:...};{true:正确,false:错误}
                    'Is_answer': problem['user']['is_show_answer'],  # is_show_answer为true说明已回答，是否会打
                    'Score': problem['user']['my_score']
                })
            except:
                problems_list.append({
                    'Problem_id': problem['problem_id'],  # 问题id，用来帮助提交
                    'ProblemType': problem['content']['ProblemType'],  # 问题类别，用来帮助选择答案
                    'Content': problem['content']['Body'],  # 问题内容，
                    'Options': option_dict,  # 问题选项{A:...,B:...,C:...};{true:正确,false:错误}
                    'Is_answer': problem['user']['is_show_answer'],  # is_show_answer为true说明已回答，是否会打
                })
        return problems_list

    def do_homework(self, courses, number):
        print('开始做课后作业')
        # 实现做作业
        if int(number):
            count = 0
            snum = 0
            homowork_dict = self.get_homework(
                courses[number]['course_name'],
                courses[number]['classroom_id'],
                courses[number]['course_sign'])
            for homowork in homowork_dict.items():
                problems_list = self.get_exercise_list(str(courses[number]['classroom_id']),str(courses[number]['sku_id']),str(homowork[0]))
                for problem in problems_list:
                    snum += 1
                    if problem["Is_answer"]:  # 问题已经回单完毕
                        print(f"{courses[number]['course_name']}中{problem['Problem_id']}作业已完成。将跳转下一作业。")
                        if eval(problem['Score']) > 0:  # 回答正确
                            count += 1   # 问题回答过，查看是否回答正确，如果回答正确+1，回答错误不加
                        continue
                    answers_list = self.search_answers(problem['Content'])  # 得到答案列表[{答案1},{答案2},{答案3}]
                    if problem['ProblemType'] == self.problem_type['SingleChoice'] or self.problem_type['Judgement'] or self.problem_type['Judgement']:
                        for answer in answers_list:  # 匹配题干信息
                            if problem['ProblemType'] != answer['ProblemType']:
                                continue
                            else:
                                if SequenceMatcher(None, problem['Content'], answer['Content']).ratio() > self.rate:
                                    # 似乎匹配到了正确答案
                                    answer_list = []
                                    for op in problem['Options'].items():
                                        if SequenceMatcher(None, op[1], answer['Options']).ratio() > self.rate:
                                            answer_list.append(op[0])   # 匹配到了正确答案 op,加入答案列表
                                    reslut = self.submit_answer(problem['Problem_id'], courses[number]['classroom_id'],answer_list)
                                    # 开始提交答案
                                    print(f'回答成功,结果{reslut}')
                                    if reslut == 'true':
                                        count+=1
                        # 遍历完所有答案没找到正确答案，跳出改题目循环，不回答改题目。
                        print('问题答案匹配率过低，为安全起见跳过，请手动答题～')
                    else:
                        print('问题类型很奇怪，安全起见跳过～')
                        continue
            print(f'课后作业全部完成，正确/作业{count}/{snum}\t正确率:\t{count/snum:.2%}/100%')
        else:
            for course in courses:
                homowork_dict = self.get_homework(course['course_name'],course['classroom_id'],course['course_sign'])
                for homowork in homowork_dict.items():
                    problems_list = self.get_exercise_list(str(course['classroom_id']), str(course['sku_id']), str(homowork[0]))
                    for problem in problems_list:
                        if problem["Is_answer"]:
                            continue

    def submit_answer(self, problem_id, classroom_id, answer_list):
        # 单选题，多选题都可以这样，判断题呢？
        submit_url = self.url_root + 'mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id='+self.university_id
        payload = {
            'problem_id': problem_id,
            'classroom_id': classroom_id,  # 目前来看班级id不会改变
            'answer': answer_list  # ["C"];["true"];["A","B","C"]
        }
        result = self.session.post(submit_url, headers=self.headers, json=payload, timeout=10).json()
        # 在提交答案后，应该简要记录回答正确题目个数与回答错误题目个数，并简单计算得分
        return result['data']["is_right"]  # [true; false]

    def show_detail(self):
        user_id = self.get_user_id()
        courses = self.get_courses()
        for course in courses:
            video_dict = self.get_works(  # course_name, classroom_id, course_sign
                course['course_name'],
                course['classroom_id'],
                course['course_sign']
            )[0]
            for video in video_dict:
                video_detail = self.get_video_detail(course['classroom_id'], user_id, video)
                print(video_detail)

    def main(self):
        user_id = self.get_user_id()
        courses = self.get_courses()  # 拿到了所有课程数据
        # [course_name,classroom_id, course_sign,sku_id,course_id ]
        for index, value in enumerate(courses):
            print("编号：" + str(index + 1) + " 课名：" + str(value["course_name"]))
        flag = True
        while flag:
            number = input("请输入需要刷的课程编号,输入0表示刷全部课程:")
            if not (number.isdigit()) or int(number) > len(courses):
                print("输入不合法,请重新输出！")
                continue
            elif int(number) == 0:
                flag = False  # 输入合法则不需要循环
                print('开始刷全部视频课程！')
                # self.video_watch(user_id, courses, int(number))
                print('课程全部刷完！')
                print('开始阅读全部pdf文件')
                # self.recomend_watch(courses, int(number))
                print('pdf文件阅读完毕')
                # self.do_homework(courses, int(number))

            else:
                flag = False  # 输入合法则不需要循环
                print('开始刷该课视频课程！')
                number = str(int(number) - 1)
                # self.video_watch(user_id, courses, int(number))
                print('该课的视频课程已全部刷完！')
                print('开始阅读该课pdf文件')
                # self.recomend_watch(courses, int(number))
                print('该课中的pdf文件已阅读完毕')
                self.do_homework(courses, int(number))


if __name__ == '__main__':
    rainspider = RainCourseSpider()
    rainspider.main()


