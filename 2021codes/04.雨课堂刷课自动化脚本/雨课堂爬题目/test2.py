import json
from difflib import SequenceMatcher

with open('problem.json', 'r') as f:
    problems = json.load(f)

while True:
    keyword = input("请输入要查询的题目：")
    for problem in problems:
        if SequenceMatcher(None, keyword, problem['Content']).ratio() > 0.8:
            print(problem['Content'])
            print(problem['Options'])
            print(problem['answer'])

# {
#                     'ProblemType': problem['content']['ProblemType'],  # 问题类别，用来帮助选择答案
#                     'Content': content ,  # 问题内容，
#                     'Options': opts_list,  # 问题选项{A:...,B:...,C:...};{true:正确,false:错误}
#                     'answer': problem['user']['answer']
#                 }
# problem = {
#     'ProblemType':'1',
#     'Content':'',
#     'Options':'',
#     'answer':'[B]'
# }

# with open('problem2.json', 'a') as f:
#     json.dump(problem, f)