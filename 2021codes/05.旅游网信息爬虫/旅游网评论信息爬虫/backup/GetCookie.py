import time
import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
# from urllib.request import urlretrieve
from selenium.webdriver.common.action_chains import ActionChains


class CookieGet(object):
    def __init__(self, url):
        # 这里配置驱动参数，如增加代理和UA信息
        opt = webdriver.ChromeOptions()
        # 增加代理和UA信息
        # opt.add_argument('--proxy-server=http://223.96.90.216:8085')
        opt.add_argument(
            '--user-agent=' + "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        # 创建webdriver实例
        self.driver = webdriver.Chrome(r'C:\chromedriver.exe', chrome_options=opt)
        self.url = url

    def get_cookie(self,cookies):
        pass
        # cookies = {}
        # for itme in cookies:
        #     cookies[itme['name']] = itme['value']
        #     # outputPath = open('sgCookies.pickle', 'wb')  # 新建一个文件
        #     # pickle.dump(cookies, outputPath)
        #     # outputPath.close()
        #     return cookies
        # time.sleep(1)
        # self.driver.save_screenshot("reimgs/0.jpg")
        # iframe = self.driver.find_element(By.TAG_NAME, 'iframe')  # 主代码在iframe里面，要先切进去
        # self.driver.switch_to.frame(iframe)  # 切到内层
        # time.sleep(0.5)
        # self.driver.find_element(By.CLASS_NAME, 'account-tab-account').click()  # 模拟鼠标点击
        # time.sleep(0.2)
        # self.driver.find_element(By.ID, 'username').send_keys('********')  # 模拟键盘输入
        # time.sleep(0.1)
        # self.driver.find_element(By.ID, 'password').send_keys('*********')  # 模拟键盘输入
        # time.sleep(0.2)
        # self.driver.find_element(By.CSS_SELECTOR, '.btn-account').click()

    # def __del__(self):
    #     """
    #     调用内建的稀构方法，在程序退出的时候自动调用
    #     类似的还可以在文件打开的时候调用close，数据库链接的断开
    #     """
    #     self.driver.quit()

    def main(self):
        # self.get_cookie()
        self.driver.get(self.url)
        # res = self.driver.page_source

        cookies = self.driver.get_cookies()
        time.sleep(10)
        # print(res)
        print(cookies)
        # for item in cookies:
        #     pprint.pprint(item)
        self.driver.quit()



if __name__ == '__main__':
    # url = 'https://www.tuniu.com/g1742596/guide-0-0/'
    url = 'https://www.ly.com/scenery/BookSceneryTicket_20256.html'
    cgt = CookieGet(url)
    cgt.main()