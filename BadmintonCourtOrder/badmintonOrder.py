import time
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def waitByXpath(driver, XPATH="", waitTime=5, frequency=0.1):
    return WebDriverWait(driver, waitTime, frequency).until(EC.element_to_be_clickable((By.XPATH, XPATH)))


def waitById(driver, XPATH="", waitTime=5, frequency=0.1):
    return WebDriverWait(driver, waitTime, frequency).until(EC.element_to_be_clickable((By.ID, XPATH)))


def captchaOCR(filename, threshold=200):
    """
    OCR图片转文字函数
    :param filename: 图片文件名
    :param threshold:
    :return:OCR结果
    """
    from PIL import Image
    import pytesseract
    im = Image.open(filename)
    gray = im.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = gray.point(table, '1')
    return pytesseract.image_to_string(out).strip()


def SJTULogin(driver, username="melan_thompson", password="xwp13030", loginMethod="auto"):
    try:
        # 等待元素加载完成
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "user")))
    except Exception as e:
        print("Loading time exceeds limit or it is not a jaccount login page", e)
    currenturl = driver.current_url
    print("Now logging in into the SJTU account")
    if loginMethod == "auto":
        while True:
            ## 首先清空输入框
            waitById(driver, "user").clear()
            driver.find_element_by_id("pass").clear()
            driver.find_element_by_id("captcha").clear()

            # 填入用户名和密码
            driver.find_element_by_id("user").send_keys(username)
            driver.find_element_by_id("pass").send_keys(password)

            # 验证码截图
            driver.find_element_by_id("captcha-img").screenshot("captcha.png")
            # 截图转化为文字
            OCRresult = captchaOCR("captcha.png")
            print("OCR captcha result is {}".format(OCRresult))
            driver.find_element_by_id("captcha").send_keys(OCRresult)
            # 提交
            waitById(driver, "submit-button").click()
            # driver.find_element_by_id("submit-button").click()
            time.sleep(0.1)
            nexturl = driver.current_url

            if "jaccount.sjtu.edu.cn" not in nexturl:
                print("Successfully log in. Next url to be visited is {}".format(nexturl))
                # 删除产生的文件
                os.remove("captcha.png")
                break
    elif loginMethod == "manul":
        ## 首先清空输入框
        waitById(driver, "user").clear()
        driver.find_element_by_id("pass").clear()
        driver.find_element_by_id("captcha").clear()
        driver.find_element_by_id("user").send_keys(username)
        driver.find_element_by_id("pass").send_keys(password)
        while True:
            time.sleep(2)
            nexturl = driver.current_url
            if "jaccount.sjtu.edu.cn" not in nexturl:
                print("Successfully log in. Next url to be visited is {}".format(nexturl))
                break
            else:
                print("请输入验证码登录账号！！！")
    else:
        raise Exception("No such login method {},only 'auto' and 'manul' are allowed".format(loginMethod))

    return driver


# 场地的Xpath定位
def xpathOfPlayground(timex, n):
    _xpath = "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[{}]/div[" \
             "{}]/div[1]/div[1]".format(timex - 6, n)
    # print(_xpath)
    return _xpath


# 点击场地，需要修改如果当场地被预定时的操作
def orderPlaygroud(driver, tt=[17, 18], numtooder=2, booking_order=[8, 3, 1, 2, 4, 5, 9, 7, 6, 10, 11, 12]):
    orderednum = 0
    for ti in tt:
        print("开始抢 {}:00 的场地".format(ti))
        for i in range(len(booking_order)):
            xpath = xpathOfPlayground(ti, booking_order[i])
            waitByXpath(driver, xpath).click()
            # driver.find_element_by_xpath(xpath).click()
            try:
                path = "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[" + str(
                    orderednum + 1) + "]/div[1]"
                driver.find_element_by_xpath(path)
            except:
                print("时间 {}:00, 场地 {} 选取失败".format(ti, booking_order[i]))
                continue
            else:
                print("时间 {}:00, 场地 {} 选取成功\n\n".format(ti, booking_order[i]))
                orderednum += 1
                break
        else:
            print("时间 {}:00 的场地已经被抢完\n\n".format(ti))
        if orderednum == numtooder:
            print("成功抢到{}个场地!!!".format(orderednum))
            return orderednum
    else:
        print("所有时间段都已经遍历完，但是没有抢到 {} 个场地，只抢到{}个场地".format(numtooder, orderednum))
        return orderednum

    # if len(tt) == 2:
    #     path2 = xpathOfPlayground(tt[1], numOfPlay[1])
    #     driver.find_element_by_xpath(path2).click()


class BadmintonCourtOrderer:
    def __init__(self, url="https://sports.sjtu.edu.cn/pc/?locale=zh#/Venue/1", chrome_driver_dirc=".", OrderDate=None):
        from selenium import webdriver

        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

        self.driver = webdriver.Chrome(chrome_driver_dirc)
        self.driver.get(url)

        # 计算预定时间
        from datetime import datetime, timedelta
        now = datetime.now()
        afterAWeek = now + timedelta(days=7)
        self.deadline = datetime(afterAWeek.year, afterAWeek.month, afterAWeek.day, 12, 0, 0, 0)
        if OrderDate is None:
            # 默认预定时间为今天后一周
            self.OrderDate = self.deadline.strftime("%Y-%m-%d")
        else:
            # 预定时间转化为datetime
            # temp=datetime.strptime(OrderDate, '%Y-%m-%d')
            # deltime = self.deadline - datetime.strptime(OrderDate, '%Y-%m-%d')
            if datetime.strptime(OrderDate, '%Y-%m-%d')<datetime.strptime(now.strftime("%Y-%m-%d"),'%Y-%m-%d'):
                raise Exception("预定时间已过，只能预定{}之后的场地".format(
                    datetime(now.year, now.month, now.day, 0, 0, 0, 0).strftime("%Y-%m-%d")))
            elif datetime.strptime(OrderDate, '%Y-%m-%d') > datetime.strptime(self.deadline.strftime("%Y-%m-%d"),'%Y-%m-%d'):
                raise Exception("预定时间过早，过几天再来预定")
            else:
                self.OrderDate = datetime.strptime(OrderDate, '%Y-%m-%d').strftime('%Y-%m-%d')
        print("即将预定{}这一天的场地".format(self.OrderDate))

    def login(self, username="melan_thompson", password="xwp13030", loginMethod="auto"):
        # try:
        # 登录界面
        import time
        waitByXpath(self.driver, "//body/div[@id='app']/div[@id='logoin']/div[1]/div[1]/div[2]/button[1]").click()

        SJTULogin(self.driver, username=username, password=password, loginMethod=loginMethod)

        # 点击羽毛球
        time.sleep(0.5)
        waitByXpath(self.driver,
                    "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/ul[1]/li[5]/a[1]/img[1]").click()
        # 点击霍英东
        time.sleep(0.5)
        waitByXpath(self.driver, "/html[1]/body[1]/div[1]/div[2]/div[1]/div[5]/div[2]/ul[1]/li[1]/div[1]").click()

        time.sleep(0.5)
        self.driver.refresh()

    def wait(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        if self.deadline.strftime('%Y-%m-%d')==self.OrderDate and now + timedelta(days=7) < self.deadline:
            print("您预定的时间暂时还未开抢，请等待开抢！！")
            while True:
                now = datetime.now()
                print("现在是时间是{}，还有{}s开抢".format(now.strftime('%H:%M:%S'), (self.deadline - now).seconds))
                if now + timedelta(days=7) >= self.deadline:
                    time.sleep(0.01)  # 等待一下
                    self.driver.refresh()
                    return
        else:
            print("您预定的时间已经开抢，现在开始捡漏")
            time.sleep(0.01)  # 等待一下
            self.driver.refresh()
            return

    def refresh(self, refreshIntervel=2, DetectFrequency=0.01):
        print("开始抢{}的场地".format(self.OrderDate))
        # self.driver.refresh()
        # 两个元素还没加载出来则刷新一下浏览器
        while True:
            try:
                # 等待tab可以按
                waitById(self.driver, "tab-" + self.OrderDate, refreshIntervel, DetectFrequency).click()

                # waitByXpath(self.driver,"/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]")

                # WebDriverWait(self.driver, refreshIntervel, DetectFrequency).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.w:nth-child(2) div.lists:nth-child(2) div.chart div.clearfix:nth-child(2) > div.tables.fl.el-loading-parent--relative")))
                # 等待加载中消失
                WebDriverWait(self.driver, refreshIntervel, DetectFrequency).until(EC.invisibility_of_element_located((
                    By.CSS_SELECTOR,
                    "div.w:nth-child(2) div.lists:nth-child(2) div.chart div.clearfix:nth-child(2) > div.tables.fl.el-loading-parent--relative")))
                # WebDriverWait(self.driver, refreshIntervel, DetectFrequency).until(EC.staleness_of((By.CSS_SELECTOR,"div.w:nth-child(2) div.lists:nth-child(2) div.chart div.clearfix:nth-child(2) > div.tables.fl.el-loading-parent--relative" )))

                # 等待场地可以按
                waitByXpath(self.driver, xpathOfPlayground(12, 1), 2)
            except Exception as e:
                print("加载超时", e)
                self.driver.refresh()
            else:
                return True

    def tickAndOrder(self, orderTime=[18, 19], booking_order=[8, 3, 1, 2, 4, 5, 9, 7, 6, 10, 11, 12]):
        if orderPlaygroud(self.driver, orderTime, booking_order=booking_order) > 0:
            # 点击下单
            # waitByXpath(self.driver,"/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/button[1]").click()
            # time.sleep(1)
            # oldurl = self.driver.current_url
            button = self.driver.find_element_by_xpath(
                "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/button[1]")
            self.driver.execute_script("arguments[0].click();", button)

            # 点击本人已经阅读
            waitByXpath(self.driver, "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div["
                                     "1]/label[1]/span[1]/span[1]").click()

            # 下单
            self.driver.find_element_by_xpath(
                "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div["
                "2]/button[2]").click()

            try:
                #如果没有跳转则继续刷新
                waitByXpath(self.driver,"//body/div[@id='app']/div[@id='orderDetails']/div[4]",1)
                # self.driver.find_element_by_xpath("//body/div[@id='app']/div[@id='orderDetails']/div[4]")
            except Exception as e:
                print(e)
                if self.refresh():
                    self.tickAndOrder(orderTime, booking_order)

        else:
            if self.refresh():
                self.tickAndOrder(orderTime, booking_order)

    def email(self, mailaddress=["1303061669@qq.com"]):
        """
        将微信或者支付宝支付的二维码图片发送到邮箱
        :param mail:
        :return:
        """
        try:
            waitByXpath(self.driver, "/html[1]/body[1]/div[1]/div[2]/div[5]/div[2]/button[1]").click()
            waitByXpath(self.driver, "/html[1]/body[1]/div[1]/div[2]/div[6]/div[1]/div[3]/span[1]/button[2]").click()

            # 微信支付
            waitByXpath(self.driver,
                        "/html[1]/body[1]/table[3]/tbody[1]/tr[1]/td[1]/table[2]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[8]/td[1]/input[2]").click()
            waitByXpath(self.driver,
                        "/html[1]/body[1]/div[4]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[1]/td[2]/table[1]/tbody[1]/tr[2]/td[2]").click()

            waitByXpath(self.driver, "//div[@id='code_url']")
            self.driver.find_element_by_xpath("//div[@id='code_url']").screenshot("paymentQRcode.png")
        except Exception as e:
            print(e)
        else:
            import sys
            sys.path.append("../EmailSending")
            from EmailSender import EmailMaster
            email = EmailMaster(settingfile="../EmailSending/EmailSenderSetting.json", subject="羽毛球场预定成功通知")
            email.usetemplate1("paymentQRcode.png")
            email.send(mailaddress)
            os.remove("paymentQRcode.png")


def b64decoding(string):
    import base64
    return base64.b64decode(str.encode(string)).decode()

if __name__ == '__main__':
    # 读取json设置
    import json

    with open("setting.json", mode='r', encoding='UTF-8') as f:
        setting = json.load(f)

    with open("../jaccount.json", mode='r', encoding='UTF-8') as f:
        setting1 = json.load(f)

    order = BadmintonCourtOrderer(OrderDate=setting["date"], chrome_driver_dirc=setting1["chrome driver directory"])
    order.login(username=b64decoding(setting1["jaccount"]), password=b64decoding(setting1["password"]), loginMethod=setting["login method"])

    order.wait()
    order.refresh()
    order.tickAndOrder(orderTime=setting["order time"], booking_order=setting["booking order"])

    order.email(setting["emails to receive message"])
