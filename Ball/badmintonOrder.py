import time
import os
from selenium.webdriver.support.wait import WebDriverWait


def SJTULogin(diver, username="melan_thompson", password="xwp13030"):
    def captchaOCR(filename, threshold=200):
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

    # 等待登录界面加载完成
    from selenium.webdriver.support.wait import WebDriverWait
    wait = WebDriverWait(driver, 10, 0.1)
    wait.until(lambda x: driver.find_element_by_id("user"),
               "Loading time exceeds limit or it is not a jaccount login page")
    currenturl = driver.current_url
    print(currenturl)

    while True:
        # 填入用户名和密码
        driver.find_element_by_id("user").send_keys(username)
        driver.find_element_by_id("pass").send_keys(password)

        # 验证码截图
        driver.find_element_by_id("captcha-img").screenshot("captcha.png")
        # 截图转化为文字
        driver.find_element_by_id("captcha").send_keys(captchaOCR("captcha.png"))
        # 提交
        driver.find_element_by_id("submit-button").click()
        time.sleep(0.1)
        nexturl = diver.current_url
        print(nexturl)
        if "jaccount.sjtu.edu.cn" not in nexturl:
            print("Successfully log in")
            break

    # 删除产生的文件
    os.remove("captcha.png")
    return driver


# 场地的Xpath定位
def xpathOfPlayground(timex, n):
    _xpath = "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[{}]/div[" \
             "{}]/div[1]/div[1]".format(timex - 6, n)
    print(_xpath)
    return _xpath


# 跳转到霍英东羽毛球预定界面
def goToPlayGroudOrder(driver):
    # 登录界面
    driver.find_element_by_xpath("//body/div[@id='app']/div[@id='logoin']/div[1]/div[1]/div[2]/button[1]").click()
    SJTULogin(driver)

    # 点击羽毛球
    time.sleep(0.1)
    driver.find_element_by_xpath(
        "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/ul[1]/li[5]/a[1]/img[1]").click()

    # 点击霍英东
    time.sleep(0.1)
    driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[1]/div[5]/div[2]/ul[1]/li[1]/div[1]").click()


# 点击场地，需要修改如果当场地被预定时的操作
def orderPlaygroud(driver, tt=[17, 18], num=12, numtooder=2):
    orderednum = 0
    orderlist = [8, 3, 1, 2, 4, 5, 9, 7, 6, 10, 11, 12]
    for ti in tt:
        print("开始抢时间 {} 的场地".format(ti))
        for i in range(num):
            xpath = xpathOfPlayground(ti, orderlist[i])
            driver.find_element_by_xpath(xpath).click()
            try:
                driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div["
                                             "1]/div[2]/div[1]/div[1]/div[" + str(orderednum + 1) + "]/div[1]")
            except:
                print("时间 {}:00, 场地 {} 选取失败".format(ti, orderlist[i]))
                continue
            else:
                print("时间 {}:00, 场地 {} 选取成功\n\n".format(ti, orderlist[i]))
                orderednum += 1
                break
        else:
            print("时间 {} 已经被抢完\n\n".format(ti))
        if orderednum == numtooder:
            print("成功抢到{}个场地!!!".format(orderednum))
            return True
    else:
        print("所有时间段都已经遍历完，但是没有抢到 {} 个场地".format(numtooder))
        return False

    # if len(tt) == 2:
    #     path2 = xpathOfPlayground(tt[1], numOfPlay[1])
    #     driver.find_element_by_xpath(path2).click()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from selenium import webdriver

    driver = webdriver.Chrome()
    driver.get("https://sports.sjtu.edu.cn/pc/?locale=zh#/Venue/1")

    goToPlayGroudOrder(driver)

    # while True:
    #     localtime = time.localtime(time.time())
    #     print(time.asctime(localtime))
    #     if localtime.tm_hour == 23 and localtime.tm_min == 26 and localtime.tm_sec >= 0:
    #         break

    time.sleep(0.1)#等待一下
    driver.refresh()
    # time.sleep(10)
    # 对应的日日期
    data = "2021-06-05"
    wait = WebDriverWait(driver, 2, 0.01)
    # 2s两个元素还没加载出来则刷新一下浏览器
    while True:
        try:
            wait.until(lambda x: driver.find_element_by_id("tab-" + data),
                       "场地加载超时")
            driver.find_element_by_id("tab-" + data).click()
            path = xpathOfPlayground(12, 1)
            # 点击场地,场地加载比较慢，所以需要等待
            wait.until(lambda x: driver.find_element_by_xpath(path),
                       "场地加载超时")
        except:
            driver.refresh()
        else:
            break

    if orderPlaygroud(driver, [12, 13, 9]):
        # 点击下单
        driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div["
                                     "3]/button[1]").click()

        # 点击本人已经阅读
        wait = WebDriverWait(driver, 10, 0.01)
        wait.until(lambda x: driver.find_element_by_xpath(
            "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div["
            "1]/label[1]/span[1]/span[1]"), "场地加载超时")
        driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div["
                                     "1]/label[1]/span[1]/span[1]").click()

        # driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div["
        #                              "2]/button[2]").click()

