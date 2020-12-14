# @Author  : Jacob-ZHANG
# @Author  : Jacob-ZHANG
import requests,base64
from PIL import Image
import csv
from selenium import webdriver
import time,random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


browser=webdriver.Chrome()
browser.maximize_window()
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
"source": """
     Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
   """ })
browser.implicitly_wait(10)
browser.get('https://pro.tianyancha.com/searchx')
time.sleep(random.randint(1, 2))
def get_code_image():
    #点击密码登录
    browser.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[3]/div[1]/div[2]').click()
    time.sleep(0.5)
    #输入账号密码，验证码才会出来
    browser.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[3]/form/div[2]/input').send_keys(
        'yaoy2013@qq.com')
    time.sleep(random.randint(1, 2))
    browser.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[3]/form/div[4]/input').send_keys('rrviqmvd')
    time.sleep(random.randint(1, 2))
    browser.save_screenshot('屏幕.png')#截图整个页面】
    left_angle=browser.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[3]/form/div[6]/img').location
    image=browser.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[3]/form/div[6]/img')
    size=image.size
    rangle = (int(left_angle['x']), int(left_angle['y'] ), int(left_angle['x'] + size['width'] + 230),

              int(left_angle['y'] + size['height'] + 300))
    open_image=Image.open('屏幕.png')
    jietu=open_image.crop(rangle)
    #最终获取验证码的截图。因为直接解析验证码的url，得到的图片是变化的会与原验证码不一致
    jietu.save('验证码.png')

def parse_code():
    #用百度API解析图片
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
    f = open('验证码.png', 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    access_token = '24.8e241cd5478ed0f6d680d702f0506ce2.2592000.1608467531.282335-19004069'#2020/11/20更新12/20过期
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    #得到解析结果
    dictionary=response.json()

    #得到验证码
    yanzhengma=dictionary['words_result'][0]['words']
    #录入验证码
    browser.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[3]/form/div[6]/input').send_keys(yanzhengma)
    # 点击登录按钮
    time.sleep(random.randint(1, 2))
    browser.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[3]/form/div[8]').click()



def set_para(i,cap_min,cap_max):
    a=i+1
    # 点更多选项，长一点好看
    click_gengduoxuanxian = browser.find_element_by_xpath(
        '//*[@id="web-content"]/div/div[2]/div[1]/div[2]/div[1]')
    browser.execute_script("arguments[0].click();", click_gengduoxuanxian)
    # 点时间自定义
    click_time_zidingyi = browser.find_element_by_xpath(
        '//*[@id="_custom-area-container"]')
    browser.execute_script("arguments[0].click();", click_time_zidingyi)
    # 获取自定义中显示的初始年份和终止年份
    start_year = browser.find_element_by_xpath(
        '//*[@id="layui-laydate100001"]/div[1]/div[1]/div/span[1]').text
    end_year = browser.find_element_by_xpath(
        '//*[@id="layui-laydate100001"]/div[2]/div[1]/div/span[1]').text

    # 提取初始年份和终止年份
    start_year = int(re.findall("\d+", start_year)[0])
    end_year = int(re.findall("\d+", end_year)[0])
    #点开始年份
    click_start_year = browser.find_element_by_xpath(
        '//*[@id="layui-laydate100001"]/div[1]/div[1]/div/span[1]')
    browser.execute_script("arguments[0].click();", click_start_year)

    ##############################################设年头
    #判断距离今年是否在第一页
    if (start_year - 8) < i < (start_year - 1):

        # 选年份
        choose_year = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[1]/div[2]/ul/li[contains(text(),'+str(i)+')]')
        browser.execute_script("arguments[0].click();", choose_year)
        # 点击月份选项
        click_month = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[1]/div[1]/div/span[2]')
        browser.execute_script("arguments[0].click();", click_month)
        # 点击1月
        choose_month = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[1]/div[2]/ul/li[1]')
        browser.execute_script("arguments[0].click();", choose_month)
#选择该年该月的1号
        choose_day = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[1]/div[2]/table/tbody/tr[1]/td[(text()=1)]')
        browser.execute_script("arguments[0].click();", choose_day)

    #不在第一页，就按多余的点击翻页
    else:
        #计算翻几页
        page_numbers=(start_year-8-i)//15+1

        #点击翻页
        click_pages_number = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[1]/div[1]/i[1]')

        #根据page_numbers循环，循环一次翻一页
        for id in range(page_numbers):
            browser.execute_script("arguments[0].click();", click_pages_number)

        time.sleep(2)
        #选年份
        choose_year = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[1]/div[2]/ul/li[contains(text(),'+str(i)+')]')
        browser.execute_script("arguments[0].click();", choose_year)
        time.sleep(2)
        # 点击月份选项
        click_month = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[1]/div[1]/div/span[2]')
        browser.execute_script("arguments[0].click();", click_month)
        time.sleep(2)

        # 点击1月
        choose_month = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[1]/div[2]/ul/li[1]')
        browser.execute_script("arguments[0].click();", choose_month)
        time.sleep(2)
        # 选择该年该月的1号
        choose_day = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[1]/div[2]/table/tbody/tr[1]/td[(text()=1)]')
        browser.execute_script("arguments[0].click();", choose_day)

    ##############################################设年尾
        # 点结束年份
    click_end_year = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[1]/div/span[1]')
    browser.execute_script("arguments[0].click();", click_end_year)
    if (end_year - 8) < a < (end_year - 1):
        # 选年份
        choose_year = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[2]/ul/li[contains(text(),'+str(a)+')]')
        browser.execute_script("arguments[0].click();", choose_year)
        # 点击月份选项
        click_month = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[1]/div/span[2]')
        browser.execute_script("arguments[0].click();", click_month)
        # 点击1月
        choose_month = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[2]/ul/li[1]')
        browser.execute_script("arguments[0].click();", choose_month)
#选择该年该月的1号
        choose_day = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[2]/table/tbody/tr[1]/td[(text()=1)]')
        browser.execute_script("arguments[0].click();", choose_day)

    #不在第一页，就按多余的点击翻页
    else:
        #计算翻几页
        page_numbers=(start_year-8-a)//15+1

        #点击翻页
        click_pages_number = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[1]/i[1]')

        #根据page_numbers循环，循环一次翻一页
        for id in range(page_numbers):
            browser.execute_script("arguments[0].click();", click_pages_number)
#选年份
        choose_year = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[2]/ul/li[contains(text(),' + str(a) + ')]')
        browser.execute_script("arguments[0].click();", choose_year)
        # 点击月份选项
        click_month = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[1]/div/span[2]')
        browser.execute_script("arguments[0].click();", click_month)
        # 点击1月
        choose_month = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[2]/ul/li[1]')
        browser.execute_script("arguments[0].click();", choose_month)
        # 选择该年该月的1号
        choose_day = browser.find_element_by_xpath(
            '//*[@id="layui-laydate100001"]/div[2]/div[2]/table/tbody/tr[1]/td[(text()=1)]')
        browser.execute_script("arguments[0].click();", choose_day)

#点时间确定
    click_time_confirm = browser.find_element_by_xpath(
        '//*[@id="layui-laydate100001"]/div[3]/div[2]/span[2]')
    browser.execute_script("arguments[0].click();", click_time_confirm)


    # 等待页面企业数加载完毕
    time.sleep(50)
#点资本自定义
    click_cap_zidingyi = browser.find_element_by_xpath(
        '//*[@id="web-content"]/div/div[2]/div[1]/div[1]/div[9]/div[4]/div[2]/div/div[1]/span[1]')
    browser.execute_script("arguments[0].click();", click_cap_zidingyi)



    browser.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[1]/div[1]/div[9]/div[4]/div[2]/div/div[2]/div[1]/div/input').send_keys(str(cap_min))
    time.sleep(random.randint(1, 2))
    browser.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[1]/div[1]/div[9]/div[4]/div[2]/div/div[2]/div[2]/div/input').send_keys(str(cap_max))
    #点资本确定
    click_cap_confirm = browser.find_element_by_xpath(
        '//*[@id="web-content"]/div/div[2]/div[1]/div[1]/div[9]/div[4]/div[2]/div/div[2]/div[3]')
    browser.execute_script("arguments[0].click();", click_cap_confirm)

get_code_image()
parse_code()
time.sleep(50)
set_para(1968,500,1000)#第一个参数年份设定，小于当前年份即可。后面俩为注册资本，单位万元。