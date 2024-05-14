import re
import os
import time
import requests
import multiprocessing
import pandas as pd
pd.options.io.excel.xlsx.writer = 'xlsxwriter'


class ReportSpider(object):
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'Host': 'www.cninfo.com.cn',
            'Origin': 'http://www.cninfo.com.cn',
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip,deflate',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json,text/plain,*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.paths = [
            r'.\data\10.26-股票代码.xlsx',
            r".\data\年报链接(未处理).txt",
            r'.\data\miss_data.txt',
            r'.\data\下载链接(清洗后).txt',
            r'D:\reports'
        ]
        self.exclude_keywords = ['英文', '摘要', '已取消', '公告', '核查意见', 'h股', '财务报表']
        self.has_storages = self.get_has_storages()
        self.orgs = self.get_orgs()


    def get_orgs(self):
        szse_url = 'http://www.cninfo.com.cn/new/data/szse_stock.json'
        bj_url = 'http://www.cninfo.com.cn/new/data/bj_stock.json'
        szse_orgs = self.session.get(szse_url, timeout=10).json()["stockList"]
        bj_orgs = self.session.get(bj_url, timeout=10).json()["stockList"]
        szse_orgs.extend(bj_orgs)
        return {org['code']: org['orgId'] for org in szse_orgs}

    def get_has_storages(self):
        with open(self.paths[1], 'r', encoding='utf8') as f:
            content = f.read().split('\n')
        return {f"{cont.split(',')[0]}:{cont.split(',')[1]}" for cont in content if len(cont.split(','))>1}

    def get_data(self, scode: str, year: int):
        if int(scode) > 600000:
            plate, column = 'sh', 'sse'
        else:
            plate, column = 'sz', 'szse'
        if year > 2020:
            plate, column = '', 'szse'
        data = {
            'pageNum': '1',
            "pageSize": "30",
            "tabName": "fulltext",
            "stock": f'{scode},{self.orgs[scode]}',
            "seDate": f"{year+1}-01-01~{year+1}-12-30",
            "column": column,
            "category": "category_ndbg_szsh",
            "isHLtitle": "true",
            'sortName': '',
            'sortType': '',
            'plate': plate,
            'searchkey': '',
            'secid': '',
        }
        return data

    def get_report_history(self, scode: str, year: int):
        p = re.compile(r'\W')
        data = self.get_data(scode, year)
        url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
        try:
            reports = self.session.post(url, data=data, timeout=10).json()
            announcements = reports["announcements"]
            if announcements:
                for report in announcements:
                    title = p.sub("", report['announcementTitle'].lower())
                    print(title)
                    if self.filter(title):
                        self.parse(report, scode, year, title)
            else:
                with open(self.paths[2], 'a', encoding='utf8') as f:
                    f.write(f'{scode},{year}\n')
                print(f'{scode},{year}文件获取失败。')
        except:
            # print(self.session.post(url, data=data, timeout=10).text)
            with open(self.paths[2], 'a', encoding='utf8') as f:
                f.write(f'{scode},{year}\n')
            print(scode, year,'出错了，不知为啥')

    def get_all_links(self, start_=None):
        """
        ,断点续下，终止程序后，参数中传入 start_=code，即可从code继续下载。
        :param start_:
        :return:
        """
        print("链接爬取程序开始运行，由于速度太快会封ip，因此无法用多进程，用时大约1小时左右，请耐心等待……")
        codes = pd.read_excel(self.paths[0], dtype={'证券代码': 'object'})['证券代码'].tolist()
        index = codes.index(start_) if start_ else 0
        for i in range(index, len(codes)):
            for year in range(2015, 2023):
                if f"{codes[i]}:{year}" in self.has_storages:
                    print(f'{codes[i]}:{year}已经下载，跳过')
                else:
                    # time.sleep(random.random()*0.5)
                    self.get_report_history(codes[i], int(year))
        print('年报链接全部保存完毕')
        self.check()


    def filter(self, title):
        # 除了需要排除以上以外，还需要注意，有些报告中不含有'年报'或'年度报' 甚至有的全是英文
        # 还包括名字中不含有摘要的摘要
        flag = True
        for kw in self.exclude_keywords:
            if kw in title:
                flag = False
                break
        return flag

    def parse(self, report, scode, year, title):
        """
        仅仅用于格式化标题和保存下载链接，不下载pdf文件。
        :param report:
        :param stock:
        :param title:
        :return:
        """
        down_url = report['adjunctUrl']
        announcements = report['announcementTime']
        shortname = report['secName'].replace('*', '').replace(' ', '')
        bulletinId = down_url.split('/')[2][:-4]
        pdfurl = "http://static.cninfo.com.cn/" + down_url
        filename = f"{scode},{year},{announcements},{shortname},{bulletinId},{title},{pdfurl}"
        with open(self.paths[1], 'a', encoding='utf8') as f:
            f.write(filename + "\n")
        print(f"{filename}存储成功！")

    def check(self):
        with open(self.paths[1], 'r', encoding='utf8') as f:
            contents = f.read().split('\n')
        result = {cont for cont in contents if len(cont.split(','))==7}
        with open(self.paths[1], 'w', encoding='utf8') as f:
            f.write('\n'.join(list(result)))

    def clean(self):
        print('链接清理程序开始运行，删除非年报数据 更新后年报 >>> 更新前年报')
        def extrac_year(name):
            publish = int(name.split('-')[1])
            title = name.split('-')[0]
            try:
                year = re.search(r'20\d{2}', title).group(0)
            except:
                year = publish-1
            return year
        dataset_ = pd.read_csv(self.paths[1],index_col=None, header=None, names=['股票代码','截止时间','时间戳','股票简称','素材id','年报标题','下载链接'],dtype={'股票代码':'object'})
        dataset_.drop_duplicates(subset=['下载链接', '素材id', '股票代码'],inplace=True)
        dataset_['公布年份'] = dataset_['下载链接'].apply(lambda x:x.split('/')[4][:4])
        dataset_['年报标题2'] = dataset_['年报标题'] + '-' + dataset_['公布年份']
        dataset_['年报年份'] = dataset_['年报标题2'].apply(lambda x: extrac_year(x))
        dataset_['时间戳'] = dataset_['时间戳'].apply(lambda x:int(x)/1e3)
        dataset_.sort_values(['股票代码','年报年份'],inplace=True)
        dataset_.reset_index(level=0, inplace=True)
        dataset_.drop(['index', '年报标题2','公布年份','素材id'], axis=1, inplace=True)
        dataset_['截止时间'] = dataset_['截止时间'].astype('int')
        dataset_['年报年份'] = dataset_['年报年份'].astype('int')
        dataset_ = dataset_[['股票代码', '股票简称', '年报年份', '年报标题', '时间戳', '下载链接']]
        # 拿到所有链接，初步筛选去除标题名称不符合要求的所有数据
        delitems = dataset_[(~dataset_['年报标题'].str.contains('年度报'))&(~dataset_['年报标题'].str.contains('年报'))][['年报标题']].index.tolist()
        dataset = dataset_.drop(list(delitems))
        # 删除各年内地修订数据
        secids = set(dataset['股票代码'].tolist())
        result=[]
        def delfun(items):
            result_=[]
            while len(items) >1:
                res_ = {item.split(':')[1]:item.split(':')[0] for item in items}
                name_ = min(res_, key=res_.get)
                result_.append(int(name_))
                items.remove(f"{res_[name_]}:{name_}")
            return result_

        for secid in secids:
            _dataset = dataset[dataset['股票代码']==secid]
            years = set(_dataset['年报年份'].tolist())
            for year in years:
                res=[]
                for idx,row in _dataset.iterrows():
                    if year == row[2]:
                        content=f"{int(row[4])}:{row.name}"
                        res.append(content)
                if len(res)>1:
                    result.extend(delfun(res))
        dataset.drop(list(result),inplace=True)  # sorted(delitems)
        # 再次去除重复
        dataset_.drop_duplicates(subset=['股票代码','年报年份'])
        # 组装为目标格式
        dataset['年报年份'] = dataset['年报年份'].astype('str')
        dataset['title'] = dataset['股票代码'] + '-' + dataset['年报年份'] + '-' + dataset['股票简称'] + '-' +'年度报告.pdf'
        result = dataset[['title','下载链接']]
        result.to_csv(self.paths[3], header=None, index=None)
        print('所有链接清洗完毕！')

    def get_url(self):
        with open(self.paths[3], 'r', encoding='utf8') as f:
            content = f.read().split('\n')
        return {url.split(',')[0]:url.split(',')[1] for url in content if url!=''}

    def pdf_download(self, save_path, url):
        def pdf_save(url, save_path):
            try:
                with requests.get(url, stream=True, timeout=10, verify=False) as r:
                    with open(save_path, 'ab') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f'保存“{save_path}”文件成功！')
            except requests.exceptions.RequestException as e:
                print(f"下载{save_path}文件失败：{e}")
                return False
            else:
                return True
        retry_count = 3
        while retry_count > 0:
            if pdf_save(url, save_path):
                break
            else:
                retry_count -= 1
        if retry_count == 0:
            print(f"下载失败：{url}")
            return

    def download_main(self):
        print("pdf年报下载程序开始运行，用时大约2小时左右，请耐心等待……")
        url_dicts = self.get_url()
        need_2 = self.buchong()
        with multiprocessing.Pool() as pool:
            for name, url in url_dicts.items():
                if name not in need_2:
                    continue
                else:
                    save_path = os.path.join(self.paths[4], name)
                    if os.path.exists(save_path):
                        print(f"{name}已经下载,跳过")
                    else:
                        pool.apply_async(self.pdf_download, args=(save_path, url))
            pool.close()
            pool.join()
        print('pdf年报全部下载完成')

    def test(self,sktcode):
        for year in range(2015, 2023):
            self.get_report_history(sktcode, int(year))
        # self.check()

    def buchong(self):
        with open('./data/test.txt', 'r',encoding='utf8') as f:
            content = f.read().split('\n')
        return [cont for cont in content if cont !='']



if __name__ == '__main__':
    rp = ReportSpider()
    # 爬取年报链接，单线程如果还报错，可以在110行增加随机等待时间。
    # 打印信息为  文件获取失败 表示 该网站不存在指定年报，不存在的年报 代码及年份被存放在 ./data/miss_data.txt
    # 该网站不存在指定年报有多重含义：1.已经ST/*ST/倒闭/退市；2.当年尚未上市，如可能2021年尚未上市，甚至2022年刚上市还没有2022年报；3.网站缺失字段。

    # rp.get_all_links()

    # 实现更新后年报替换更新前年报
    # rp.clean()

    # 下载pdf文档

    rp.download_main()
    # rp.test('688126')
    # rp.buchong()



