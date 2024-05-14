from selenium import webdriver
import time
import re
import xlrd
import os
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.lagou.com/')
driver.find_element_by_xpath('//*[@id="changeCityBox"]/p[1]/a').click()
elem =driver.find_element_by_xpath('//*[@id="search_input"]')
elem.clear()
time.sleep(1)
capt = input('请输入需要查询的职位')
driver.find_element_by_xpath('//*[@id="search_input"]').send_keys(capt)
driver.find_element_by_xpath('//*[@id="search_button"]').click()
data=driver.page_source
# print(data)
a=1
position_re = 'data-positionname="(.*?)" data-companyid'
position = re.compile(position_re,re.S).findall(data)
salary_re='data-salary="(.*?)" data-company='
salary = re.compile(salary_re,re.S).findall(data)
company_re='data-company="(.*?)" data-positionname='
company = re.compile(company_re,re.S).findall(data)
print(position,salary,company)

while True:
    try:
        a = a + 1
        if a<=5:
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="s_position_list"]/div[2]/div/span[6]').click()
            data2=driver.page_source
            position_re2 = 'data-positionname="(.*?)" data-companyid'
            position2 = re.compile(position_re2,re.S).findall(data2)
            salary_re2 = 'data-salary="(.*?)" data-company='
            salary2 = re.compile(salary_re2,re.S).findall(data2)
            company_re2 = 'data-company="(.*?)" data-positionname='
            company2 = re.compile(company_re2,re.S).findall(data2)
            print("**************当前页码：",a,"*************")
            # print(data2)
            print(position2, salary2, company2)
        else:
            break
    except:
        print("猫熊")