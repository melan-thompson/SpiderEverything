#提前登录
from splinter.browser import Browser
from time import sleep
import time
# traceback模块被用来跟踪异常返回信息
import traceback

# 场地时间定义
date = '2021-06-01'
# 场地定义
# 1号场地
Row_1 = 12  # 行号
Column_1 = 1  # 列号(不用改)
# 2号场地
Row_2 = 13  # 行号
Column_2 = 1  # 列号(不用改)
# 开抢时间定义 12:00:00
hour = 12
minute = 0
second = 0

# 账户1
user_1 = 'Txuyang'
pass_1 = 'Txy17853143230'
# 账户2
user_2 = 'Txuyang'
pass_2 = 'Txy17853143230'

# 场地数量
court_num = 12  #霍英东15 气膜12

login_url = 'https://my.sjtu.edu.cn'


def login(username, password):
    bwr.find_by_id('user').fill(username)
    bwr.find_by_id('pass').fill(password)


def rob(username, password):
    global bwr
    global Row_1
    global Column_1
    global Row_2
    global Column_2
    Court_1 = 'Failed'
    Court_2 = 'Failed'

    bwr = Browser(driver_name='chrome')

    bwr.visit(login_url)

    login(username, password)
    while True:
        if bwr.url[:22] == login_url:
            print(bwr.url[:22])
            break

    # bwr.find_by_text(u'服务大厅').click()
    bwr.visit('https://sports.sjtu.edu.cn/pc?locale=zh')
    bwr.find_by_text(u'校内人员登录').click()
    sleep(0.5)
    # 选择体育馆
    bwr.find_by_xpath('//*[@id="app"]/div[2]/div[2]/div[4]/ul/li[4]/div/div/div[1]/img').click()    # 气膜体育馆
    #bwr.find_by_xpath('//*[@id="app"]/div[2]/div[2]/div[4]/ul/li[5]/div/div/div[1]/img').click()    #霍英东体育馆
    # 定时
    while True:
            localtime = time.localtime(time.time())
            print(time.asctime(localtime))
            if localtime.tm_hour == hour and localtime.tm_min == minute and localtime.tm_sec >= second:
                break
    sleep(0.5)
    bwr.reload()
    bwr.reload()
    sleep(0.5)
    bwr.find_by_id('tab-' + date).click()
    # 勾选场地
    sleep(0.5)
    for num in range(1, court_num + 1):

        Row_1_str = str(Row_1)
        Column_1_str = str(Column_1)
        Row_2_str = str(Row_2)
        Column_2_str = str(Column_2)

        try:
            if Court_1 == 'Failed':
                bwr.find_by_xpath(
                    '//*[@id="apointmentDetails"]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/div[' + Row_1_str + ']/div[' + Column_1_str + ']/div/div/img').click()
                # if bwr.is_element_present_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div/p'):
                #     break
                try:
                    msg_1 = bwr.find_by_xpath('//*[@id="apointmentDetails"]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div/div[1]').first.value
                except:
                    print('1#预约失败')
                else:
                    Court_1 = 'Successful'
                    print('1#预约成功')

            if Court_2 == 'Failed':
                bwr.find_by_xpath(
                    '//*[@id="apointmentDetails"]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/div[' + Row_2_str + ']/div[' + Column_2_str + ']/div/div/img').click()
                # if bwr.is_element_present_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div/p'):
                #     break
                try:
                    msg_2 = bwr.find_by_xpath('//*[@id="apointmentDetails"]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]').first.value
                except:
                    print('2#预约失败')
                else:
                    Court_2 = 'Successful'
                    print('2#预约成功')

        except:
            bwr.find_by_xpath('/html/body/div[2]/div/div[3]/button/span').click()
            break

        Column_1 = Column_1 + 1
        Column_2 = Column_2 + 1
        if Court_1 == 'Successful' and Court_2 == 'Successful':
            break

    # 确认
    bwr.find_by_xpath('//*[@id="apointmentDetails"]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[3]/button/span').click()
    bwr.find_by_xpath('//*[@id="apointmentDetails"]/div[2]/div[2]/div[3]/div/div[3]/div/div[1]/label/span[2]').click()
    bwr.find_by_xpath('//*[@id="apointmentDetails"]/div[2]/div[2]/div[3]/div/div[3]/div/div[2]/button[2]').click()
    sleep(0.5)
    bwr.find_by_xpath('//*[@id="orderDetails"]/div[5]/div[2]/button').click()
    bwr.find_by_xpath('//*[@id="orderDetails"]/div[6]/div/div[3]/span/button[2]/span').click()


if __name__ == "__main__":

    rob(user_1, pass_1)
