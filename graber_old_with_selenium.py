from selenium import webdriver
import time
import getpass
import os
import random

username = input('请输入用户名')
password = getpass.getpass('请输入密码')

'''
或者直接在这里输入用户名和密码
username = '这里输入用户名'
password = '这里输入密码'
gap = float('这里输入抢课间隔(单位s)')

'''

path = os.getcwd()

def grab():
    #模拟登录
    #browser = webdriver.Chrome(executable_path=os.path.join(path,'chromedriver.exe'))
    browser = webdriver.Firefox(executable_path=os.path.join(path,'geckodriver'))
    browser.get("http://xk.nju.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do")
    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_css_selector("#casLoginForm > p:nth-child(4) > button").click()
    random_sleep()

    '''
    #选择轮次
    browser.find_element_by_css_selector("tr.electiveBatch-row:nth-child(2) > td:nth-child(1) > div:nth-child(1) > input:nth-child(1)").click()
    browser.find_element_by_css_selector("#buttons > button.bh-btn.bh-btn-primary.bh-btn.bh-pull-right").click()
    '''

    browser.find_element_by_css_selector('#courseBtn').click()
    random_sleep()
    

    #开始抢课
    while (1):
        browser.implicitly_wait(3)
        #random_sleep()
        browser.find_element_by_css_selector("#cvPageHeadTab > li:nth-child(1) > a:nth-child(1)").click()
        browser.implicitly_wait(3)
        #random_sleep()
        browser.find_element_by_xpath('//a[text()="收藏"]').click()
        browser.implicitly_wait(3)
        #random_sleep()
        for each in browser.find_elements_by_css_selector('tr.course-tr> td:nth-child(8) > a:nth-child(2)[data-isfull=""]'):
            each.click()
            time.sleep(0.2)
            browser.implicitly_wait(3)
            #random_sleep()
            browser.find_element_by_css_selector(".cv-sure").click()
            time.sleep(1)
            #random_sleep()
            browser.find_element_by_css_selector(".cv-sure").click()
        random_sleep()
    browser.quit()

def random_sleep():
    gap = 1 + random.random() * 3
    time.sleep(gap)


#发现网络异常自动重新载入程序
while True:
    try:
        grab()
    except Exception as e:
        print(e)
