import requests
import re
import js2py


def get_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    # response.text  # 出现乱码
    # response.content.decode() # 报错
    return requests.get(url, headers=headers,timeout=10).content


def img_download(base_path, img_src_list):
    def save_img(path, datas):
        with open(path, 'wb') as f:
            f.write(datas)
    for img_src in img_src_list:
        img_src = 'http:' + img_src
        img_name = base_path + img_src.split('/')[-1]
        content = requests.get(img_src)
        save_img(img_name, content.content)
        print(f'{img_name}下载成功！')


def use_re_parse(response):
    # ex = '<LI>.*?<IMG.*?src="(.*?)" style.*?</LI>'
    # match_ = re.findall(ex, response.content.decode('gbk'), re.S)
    # 真正的图片地址是有js动态加载出来的
    ex_ = '<script.*?src = "(.*?)"; </script>'
    img_src_list = re.findall(ex_, response, re.S)
    return img_src_list


def use_js_parse(response):
    script = """
    var result=[]
    var imgs={}
    var document={
        getElementById:function(name){  
            imgs[name]={}
            return imgs[name]
        }
    }
    function summery(obj){
        for(let i in obj){
            result.push(obj[i].src)
        }
    }
    """
    ex = '<script type="text/javascript">(.*?)</script>'
    match_ = re.findall(ex, response, re.S)
    context = js2py.EvalJs(enable_require=True)
    context.execute(script)
    for ma in match_:
        if 'document.getElementById' in ma:
            context.execute(ma)
    context.summery(context.imgs)
    return list(context.result)


for i in range(5):
    url = f"http://md.itlun.cn/a/nhtp/list_2_{i+1}.html"
    response = get_content(url).decode('gbk')
    # img_src_list = use_re_parse(response)
    img_src_list = use_js_parse(response)
    # 解析出的图片地址，是不完整的，缺少http:
    img_download('./datas/imgs1/', img_src_list)