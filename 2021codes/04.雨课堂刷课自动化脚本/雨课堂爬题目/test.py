import re
import json
import requests


class RainCourseSpider(object):

    def __init__(self):
        self.university_id = "3240"  # 江苏师范大学学校id
        self.url_root = "https://jsnuyjs.yuketang.cn/"  # 按需修改域名 example:https://*****.yuketang.cn/

        self.csrftoken = 'OE1pk6pV0guhl4zNDxdd04gYbNWDA9qM'
        self.sessionid = 'gxgr78hfs27ri2jdxszxb6hgom51f701'
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
        self.session = requests.session()

    def get_ccid(self, classroom_id, video_id):
        url = self.url_root + 'mooc-api/v1/lms/learn/leaf_info/' + str(classroom_id) + '/' + str(video_id) + '/'
        ccid = requests.get(url, headers=self.headers).json()['data']['content_info']['media']['ccid']
        return ccid

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

    def get_homework(self, classroom_id, course_sign):
        url = self.url_root + "mooc-api/v1/lms/learn/course/chapter?cid=" + str(
            classroom_id) + "&term=latest&uv_id=" + self.university_id + "&sign=" + course_sign
        homework_json = self.session.get(url, headers=self.headers).json()
        homework_dict = {}
        try:
            for i in homework_json["data"]["course_chapter"]:
                for j in i["section_leaf_list"]:
                    if "leaf_list" in j:
                        for z in j["leaf_list"]:
                            if z['leaf_type'] == 6:
                                homework_dict[z["id"]] = z["name"]
                    else:
                        if j['leaf_type'] == 6:
                            homework_dict[j["id"]] = j["name"]
            return homework_dict
        except:
            raise Exception("出错，未能拿到 课后作业 数据，请重试！！")

    def get_exercise_list(self, classroom_id, sku_id, homework_id):
        get_leaf_type_id_url = self.url_root + "mooc-api/v1/lms/learn/leaf_info/" + classroom_id + "/" + homework_id + "/?term=latest&uv_id=" + self.university_id
        response = self.session.get(url=get_leaf_type_id_url, headers=self.headers, timeout=10)
        leaf_id = str(response.json()['data']['content_info']['leaf_type_id'])
        url = self.url_root + "mooc-api/v1/lms/exercise/get_exercise_list/" + leaf_id + '/' + sku_id + '/?term=latest&uv_id=' + self.university_id
        problems = self.session.get(url, headers=self.headers, timeout=10).json()['data']['problems']
        problems_list = []
        for problem in problems:
            option_dict = {i['key']: i["value"] for i in problem['content']['Options']}
            opts_list = []
            for opts in option_dict.items():
                try:
                    res = re.search("<p>(.*)</p>", opts[1]).group(1).replace('&nbsp;','').replace(r'<br/>','').replace('<p>','').replace('</p>','')
                    opts_list.append({ opts[0]: res })
                except:
                    pass
            content = re.search("<p>(.*)</p>",problem['content']['Body']).group(1).replace('&nbsp;','').replace(r'<br/>','').replace('<span class="blank-item" style="display:inline-block;">','').replace('</span>','').replace('<span style="color: #606266; background-color: #FFFFFF;">','').replace('<p>','').replace('填空','').replace('</p>','').replace('<img class="" src id="loading_l5gevtjm"/>','')
            try:
                problems_list.append({
                    'ProblemType': problem['content']['ProblemType'],  # 问题类别，用来帮助选择答案
                    'Content': content ,  # 问题内容，
                    'Options': opts_list,  # 问题选项{A:...,B:...,C:...};{true:正确,false:错误}
                    'answer': problem['user']['answer']
                })
            except:
                problems_list.append({
                    'ProblemType': problem['content']['ProblemType'],  # 问题类别，用来帮助选择答案
                    'Content': content,  # 问题内容，
                    'Options': opts_list,  # 问题选项{A:...,B:...,C:...};{true:正确,false:错误}
                    'answer': problem['user']['answers']
                })
        return problems_list

    def main(self):
        problems = []
        courses = self.get_courses()  # 拿到了所有课程数据
        classroom_id = courses[1]['classroom_id']
        course_sign = courses[1]['course_sign']
        sku_id = courses[1]['sku_id']
        homowork_dict = self.get_homework(classroom_id, course_sign)
        for homowork in homowork_dict.items():
            problems_list = self.get_exercise_list(str(classroom_id), str(sku_id), str(homowork[0]))
            for item in problems_list:
                problems.append(item)
        print(problems)
        with open('problem.json', 'a') as f:
            json.dump(problems, f)


if __name__ == '__main__':
    rainspider = RainCourseSpider()
    rainspider.main()