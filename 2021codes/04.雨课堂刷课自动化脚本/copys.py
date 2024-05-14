from gevent import monkey
monkey.patch_all()
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.util import parse_url
import requests, js2py
import gevent
import time, random, re
from subprocess import Popen, PIPE


class RainCourseSpider(object):

    def __init__(self):
        self.university_id = "3240"  # 江苏师范大学学校id
        self.url_root = "https://jsnuyjs.yuketang.cn/"  # 按需修改域名 example:https://*****.yuketang.cn/

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
        self.session = requests.session()

    def get_user_id(self):
        # 首先要获取用户的个人ID，即user_id,该值在查询用户的视频进度时需要使用
        user_id = self.session.get(self.url_root + "edu_admin/check_user_session/", headers=self.headers, timeout=10).json()['data']['user_id']
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
        print(self.headers)
        print(response)
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
        pdf_json = self.session.get(url, headers=self.headers).json()
        pdf_dic = {}
        try:
            for i in pdf_json["data"]["course_chapter"]:
                for j in i["section_leaf_list"]:
                    if "leaf_list" in j:
                        for z in j["leaf_list"]:
                            if z['leaf_type'] == self.leaf_type["homework"]:
                                pdf_dic[z["id"]] = z["name"]
                    else:
                        if j['leaf_type'] == self.leaf_type["homework"]:
                            pdf_dic[j["id"]] = j["name"]
            print(course_name + "共有" + str(len(pdf_dic)) + "个课后作业需要完成！")
            return pdf_dic
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
        # print(heartbeat_data_list)

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
            video_dic = self.get_videos(
                courses[number]["course_name"],
                courses[number]["classroom_id"],
                courses[number]["course_sign"]
            )
            for video in video_dic.items():  # video[0]=video_id;video[1]=video_name
                ccid = self.get_ccid(courses[number]["classroom_id"], video[0])
                duration = self.get_video_duration(ccid)  # 获取视频总时长，获取需要刷的视频列表
                # 根据视频时长计算向服务器反馈的数据及时间
                payloads = self.build_heartbeat_payloads(
                    courses[number]["course_id"], ccid, courses[number]["classroom_id"],
                    courses[number]["sku_id"], user_id, video[0], duration)
                url = self.url_root + "video-log/get_video_watch_progress/?cid=" + str(
                    courses[number]["course_id"]) + "&user_id=" + user_id + "&classroom_id=" + str(
                    courses[number]["classroom_id"]) + "&video_type=video&vtype=rate&video_id=" + str(
                    video[0]) + "&snapshot=1&term=latest&uv_id=" + self.university_id
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
                video_dic = self.get_videos(item["course_name"], item["classroom_id"], item["course_sign"])
                for video in video_dic.items():
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

    def do_homework(self, courses, number):
        if number:
            pass
        else:
            for course in courses:
                # course_name, classroom_id, course_sign
                homework_list = self.get_homework(course['course_name'], course['classroom_id'], course['course_sign'])
                print(homework_list)

    def show_detail(self):
        user_id = self.get_user_id()
        courses = self.get_courses()
        for course in courses:
            video_list = self.get_videos(  # course_name, classroom_id, course_sign
                course['course_name'],
                course['classroom_id'],
                course['course_sign']
            )
            for video in video_list:
                video_detail = self.get_video_detail(course['classroom_id'], user_id, video)
                print(video_detail)

    def submit_answer(self, problem_id, classroom_id, answer_list):
        submit_url = self.url_root + 'mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id='+self.university_id
        payload = {
            'problem_id': problem_id,
            'classroom_id': classroom_id,  # 目前来看班级id不会改变
            'answer': answer_list
        }
        # payload = {
        #     'problem_id': 8912869,
        #     'classroom_id': 11043336,  # 目前来看班级id不会改变
        #     'answer': ["C"]
        # }
        res = self.session.post(submit_url, headers=r.headers, json=payload, timeout=10)
        print(res.content.decode())

    def get_exercise_list(self):

        url = self.url_root + "mooc-api/v1/lms/exercise/get_exercise_list/" + '1037612'+'/'+'5027613'+'/?term=latest&uv_id='+self.university_id

    def main(self):
        user_id = self.get_user_id()
        courses = self.get_courses()  # 拿到了所有课程数据
        # [ course_name,classroom_id, course_sign,sku_id,course_id ]
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
                print('开始做课后作业')
                self.do_homework(courses,int(number))
                print('课后作业全部完成')
            else:
                flag = False  # 输入合法则不需要循环
                print('开始刷该课视频课程！')
                number = str(int(number) - 1)
                self.video_watch(user_id, courses, int(number))
                print('该课的视频课程已全部刷完！')
                print('开始阅读该课pdf文件')
                self.recomend_watch(courses, int(number))
                print('该课中的pdf文件已阅读完毕')
                print('开始做课后作业')

                print('该课的课后作业全部完成')


if __name__ == '__main__':
    rainspider = RainCourseSpider()
    rainspider.main()

