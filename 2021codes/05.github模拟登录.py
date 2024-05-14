import requests
from lxml import etree # 导入数据解析模块 都是第三方模块需要安装

url = 'https://github.com/'
s = requests.Session()  # 创建Session会话对象
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'referer': url,
}

def get_data(username, password):
    # 发送登录页面的网络请求
    res = s.get(url+'login', headers=headers, timeout=20)
    if res.status_code == 200:  # 判断请求是否成功
        html = etree.HTML(res.text)  # 解析html
        # 提取authenticity_token信息
        token = html.xpath('//*[@id="login"]/div[4]/form/input[1]/@value')[0]
        return_to = html.xpath('//*[@id="login"]/div[4]/form/div/input[5]/@value')[0]
        ts = html.xpath('//*[@id="login"]/div[4]/form/div/input[10]/@value')[0]
        ts_sercet = html.xpath('//*[@id="login"]/div[4]/form/div/input[11]/@value')[0]
    data = {
        'commit': 'Sign in',
        'authenticity_token': token,
        'login': username,
        'password': password,
        'trusted_device': '',
        'webauthn-support': 'supported',
        'webauthn-iuvpaa-support': 'unsupported',
        'return_to': return_to,
        'allow_signup': '',
        'client_id': '',
        'integration': '',
        'required_field_3e6e': '',
        'timestamp': ts,
        'timestamp_secret': ts_sercet,
    }
    return data  # 返回信息


def login(username, password):
    data = get_data(username, password)
    print(data)
    res = s.post(url+'session', headers=headers, data=data, timeout=20)
    with open('github.html', 'wb') as f:
        f.write(res.content)
    if res.status_code == 200:  # 判断请求是否成功
        html = etree.HTML(res.text)  # 解析html
        # 获取注册账户名
        register_name = html.xpath('//meta[@name="user-login"]/@content')[0]

        print(f"注册号码为: {register_name}")
    else:
        print("登录失败")


username = str(input('请输入您的用户名：'))
password = str(input('请输入您的密码：'))
login(username, password)