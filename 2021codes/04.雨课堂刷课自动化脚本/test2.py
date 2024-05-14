# 作业帮手

# 题目网址
# https://jsnuyjs.yuketang.cn/mooc-api/v1/lms/exercise/get_exercise_list/1037612/5027613/?term=latest&uv_id=3240
# term: latest
# uv_id: 3240
# 提交网址

# https://jsnuyjs.yuketang.cn/mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=3240
# post请求
# 单选题载荷  {"classroom_id":11043336,"problem_id":8912825,"answer":["B"]}
# 多选题载荷  {"classroom_id":11043336,"problem_id":8912825,"answer":["A","B","C"]}
# 判断题载荷  {"classroom_id":10619618,"problem_id":8916825,"answer":["true"]}
# 响应


# def login(self):
#     # 这里配置驱动参数，如增加代理和UA信息
#     opt = webdriver.ChromeOptions()
#     # opt.add_argument('--proxy-server=http://223.96.90.216:8085')
#     opt.add_argument(
#         '--user-agent=' + 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')
#     # 创建webdriver实例
#     driver = webdriver.Chrome(r'C:\chromedriver.exe', chrome_options=opt)
#     driver.get('https://changjiang.yuketang.cn/v2/web/index')
#     locatorapp = (webdriver.common.by.By.ID, 'app')
#     WebDriverWait(driver, 60, 1).until(EC.presence_of_element_located(locatorapp))
#     print('检测到登录成功，正在获取cookie...')
#     cookiesJar_dict = driver.get_cookies()
#     driver.quit()
#     cookie = ''
#     cookie_dict = {}
#     for i in cookiesJar_dict:
#         if i['domain'] == 'changjiang.yuketang.cn':
#             cookie += '{}={};'.format(i['name'], i['value'])
#     for item in cookie.split(';'):
#         if item != "":
#             key, value = item.strip().split('=')
#             cookie_dict[key] = value
#     return cookie_dict