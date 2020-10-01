from selenium import webdriver
import time
import getpass
import os

username = input('请输入用户名')
password = getpass.getpass('请输入密码(代码自动隐藏，直接回车完成输入)')
gap = float(input('请输入抢课间隔(单位s)'))

'''
或者直接在这里输入用户名和密码，然后注释上边的输入代码，去掉这里的注释符号
username = '这里输入用户名'
password = '这里输入密码'
gap = float('这里输入抢课间隔(单位s)')

'''

path = os.getcwd()

def grab():
    #模拟登录
    browser = webdriver.Firefox(executable_path=os.path.join(path,'geckodriver.exe'))
    browser.get("http://xk.nju.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do")
    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_css_selector("#casLoginForm > p:nth-child(4) > button:nth-child(1)").click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="courseBtn"]').click()
    time.sleep(1)

    #开始抢课
    while (1):
        browser.implicitly_wait(3)
        browser.find_element_by_css_selector("#cvPageHeadTab > li:nth-child(1) > a:nth-child(1)").click()
        browser.implicitly_wait(3)
        browser.find_element_by_css_selector("#cvPageHeadTab > li:nth-child(8) > a:nth-child(1)").click()
        browser.implicitly_wait(3)
        for each in browser.find_elements_by_css_selector(
                'tr.course-tr> td:nth-child(8) > a:nth-child(2)[data-isfull=""]'):
            each.click()
            time.sleep(0.2)
            browser.implicitly_wait(3)
            browser.find_element_by_css_selector(".cv-sure").click()
            time.sleep(1)
            browser.find_element_by_css_selector(".cv-sure").click()
        time.sleep(gap)

    browser.quit()

#发现网络异常自动重新载入程序
while True:
    try:
        grab()
    except Exception:
        pass
