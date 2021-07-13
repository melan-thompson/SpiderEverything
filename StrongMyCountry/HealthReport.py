import time
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def b64decoding(string):
    import base64
    return base64.b64decode(str.encode(string)).decode()


def waitByXpath(driver, XPATH="", waitTime=5, frequency=0.1):
    return WebDriverWait(driver, waitTime, frequency).until(EC.element_to_be_clickable((By.XPATH, XPATH)))


def waitById(driver, XPATH="", waitTime=5, frequency=0.1):
    return WebDriverWait(driver, waitTime, frequency).until(EC.element_to_be_clickable((By.ID, XPATH)))


def waitByCSS(driver, XPATH="", waitTime=5, frequency=0.1):
    return WebDriverWait(driver, waitTime, frequency).until(EC.element_to_be_clickable((By.CSS_SELECTOR, XPATH)))


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


def XpathOfArticle(num):
    return "/html[1]/body[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[" \
           "1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[" \
           "1]/div[1]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[" \
           "1]/div[1]/div[" + str(num) + "]/div[1]/div[1]/div[1]/span[1]"


def XpathOfVideo(row, col):
    return "//body/div[@id='root']/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[" \
           "1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[" \
           "1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[" \
           "1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/section[1]/div[1]/div[1]/div[1]/div[" \
           "1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[" \
           "1]/div[1]/section[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[" + str(row) + "]/div[" + str(
        col) + "]/section[1]/div[1]/div[1]/div[" \
               "1]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1] "


class StrongMyCountry:
    def __init__(self, driver1):
        self.driver = driver1

    def login(self):
        # 点击我的学习
        waitByXpath(self.driver,
                    "/html[1]/body[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[4]/section[1]/div[2]").click()

        self.driver.switch_to.window(self.driver.window_handles[-1])

        # 扫描二维码，点击学习积分
        waitByXpath(self.driver,
                    "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/a[3]/div[1]/div[1]/div[1]",
                    30).click()
        self.MyxuexiPage = self.driver.window_handles[-1]

        self.driver.switch_to.window(self.driver.window_handles[-1])
        # 点击选读文章
        waitByCSS(self.driver,
                  "div.layout-body div.my-points div.my-points-section:nth-child(3) div.my-points-content div.my-points-card:nth-child(2) div.my-points-card-footer div.buttonbox > div.big").click()

        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.xuexiPage = self.driver.window_handles[-1]

    def readArticle(self, readtime=60):
        # 点击更多文章
        waitByXpath(self.driver,
                    "/html[1]/body[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section["
                    "1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section["
                    "1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[2]/section["
                    "1]/section[1]/span[1]").click()

        self.articlepage = self.driver.window_handles[-1]
        self.driver.switch_to.window(self.articlepage)

        for i in range(6):
            self.driver.switch_to.window(self.articlepage)
            waitByXpath(driver, XpathOfArticle(i + 1)).click()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(readtime)
            self.driver.close()

    def switchToMyScorePage(self):
        self.driver.switch_to.window(self.MyxuexiPage)

    def switchToxuexiPage(self):
        self.driver.switch_to.window(self.xuexiPage)

    def watchvideo(self, watchtime=2):
        self.driver.get(
            "https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html#1novbsbi47k-5")

        self.videopage=self.driver.window_handles[-1]
        self.driver.switch_to.window(self.videopage)
        for i in range(4):
            for j in range(4):
                self.driver.switch_to.window(self.videopage)
                waitByXpath(self.driver,XpathOfVideo(i+1,j+1)).click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(watchtime)
                self.driver.close()
        # waitByXpath(self.driver,"//a[contains(text(),'学习电视台')]").click()
        # waitByCSS(self.driver,"div.main-view section._3GhgGH8Y4Zh8H0uBP5aUMD._3mVsbsHWKWuZwBS5zIrFO9 div.oSnRgpdW2BnrDruxKh9We._3mVsbsHWKWuZwBS5zIrFO9 div.Iuu474S1L6y5p7yalKQbW.grid-gr div.grid-cell:nth-child(2) section._3GhgGH8Y4Zh8H0uBP5aUMD._3mVsbsHWKWuZwBS5zIrFO9 div.oSnRgpdW2BnrDruxKh9We._3mVsbsHWKWuZwBS5zIrFO9 div.Iuu474S1L6y5p7yalKQbW.grid-gr div.grid-cell section._3GhgGH8Y4Zh8H0uBP5aUMD._3mVsbsHWKWuZwBS5zIrFO9:nth-child(2) div.oSnRgpdW2BnrDruxKh9We._3mVsbsHWKWuZwBS5zIrFO9 div.Iuu474S1L6y5p7yalKQbW.grid-gr div.grid-cell:nth-child(1) section._3GhgGH8Y4Zh8H0uBP5aUMD._3mVsbsHWKWuZwBS5zIrFO9 div.oSnRgpdW2BnrDruxKh9We._3mVsbsHWKWuZwBS5zIrFO9 div.Iuu474S1L6y5p7yalKQbW.grid-gr div.grid-cell div._10m6vpT2QOWEy3X_bHR1kM div.more-wrap > p.text").click()

        # waitByXpath(self.driver,"//span[contains(text(),'第一频道')]").click()
        # waitByCSS(self.driver,"div.main-view section._3GhgGH8Y4Zh8H0uBP5aUMD._3mVsbsHWKWuZwBS5zIrFO9 div.oSnRgpdW2BnrDruxKh9We._3mVsbsHWKWuZwBS5zIrFO9 div.Iuu474S1L6y5p7yalKQbW.grid-gr div.grid-cell:nth-child(2) section._3GhgGH8Y4Zh8H0uBP5aUMD._3mVsbsHWKWuZwBS5zIrFO9 div.oSnRgpdW2BnrDruxKh9We._3mVsbsHWKWuZwBS5zIrFO9 div.Iuu474S1L6y5p7yalKQbW.grid-gr div.grid-cell section._3GhgGH8Y4Zh8H0uBP5aUMD._3mVsbsHWKWuZwBS5zIrFO9:nth-child(2) div.oSnRgpdW2BnrDruxKh9We._3mVsbsHWKWuZwBS5zIrFO9 div.Iuu474S1L6y5p7yalKQbW.grid-gr div.grid-cell:nth-child(2) section._3GhgGH8Y4Zh8H0uBP5aUMD._3mVsbsHWKWuZwBS5zIrFO9 div.oSnRgpdW2BnrDruxKh9We._3mVsbsHWKWuZwBS5zIrFO9 div.Iuu474S1L6y5p7yalKQbW.grid-gr div.grid-cell section._3GhgGH8Y4Zh8H0uBP5aUMD._3mVsbsHWKWuZwBS5zIrFO9._19bO69jmSWdAdrKAzSJzl7 div.oSnRgpdW2BnrDruxKh9We._3mVsbsHWKWuZwBS5zIrFO9 div.grid-gr:nth-child(1) div.Iuu474S1L6y5p7yalKQbW.grid-cell:nth-child(1) div.pTy8n09uynB02PTn3qVFj div.item-text > span.text").click()


if __name__ == '__main__':
    import json

    with open("../jaccount.json", mode='r', encoding='UTF-8') as f:
        setting = json.load(f)

    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

    driver = webdriver.Chrome(setting["chrome driver directory"])
    driver.get("https://www.xuexi.cn/")

    C = StrongMyCountry(driver)
    C.login()
    # C.readArticle(1)
    # C.switchToxuexiPage()
    C.watchvideo(70)

    # # #点击我的学习
    # # waitByXpath(driver,"/html[1]/body[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[4]/section[1]/div[2]").click()
    # #
    # # all_handles = driver.window_handles
    # # driver.switch_to.window(all_handles[-1])
    # #
    # # #扫描二维码，点击学习
    # # waitByXpath(driver,"/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/a[3]/div[1]/div[1]/div[1]",30).click()
    #
    # time.sleep(1)
    # all_handles = driver.window_handles
    # print(all_handles)
    # driver.switch_to.window(all_handles[-1])
    #
    # #点击选读文章
    # waitByCSS(driver,"div.layout-body div.my-points div.my-points-section:nth-child(3) div.my-points-content div.my-points-card:nth-child(2) div.my-points-card-footer div.buttonbox > div.big").click()
    #
    # all_handles = driver.window_handles
    # # print(all_handles)
    # driver.switch_to.window(all_handles[-1])
    #
    # #点击更多
    # waitByXpath(driver,"/html[1]/body[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[2]/section[1]/section[1]/span[1]").click()
    # SJTULogin(driver,username=b64decoding(setting["jaccount"]),password=b64decoding(setting["password"]))

    # waitByXpath(driver,"/html[1]/body[1]/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/qform-pc-form[1]/div[1]",20)

    # 记录当前url
    # url1 = driver.current_url

    # 点击
    # waitByXpath(driver,"//body/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/qform-pc-form[1]/div[1]/div[9]/div[1]/qform-pc-form-control[1]/div[1]/div[3]/qform-address[1]/qform-address-accessor[1]/nz-cascader[1]/div[1]/div[1]/input[1]",20)

    # driver.find_element_by_xpath(
    #     "/html[1]/body[1]/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/qform-pc-form[1]/div[1]/div[3]/div[2]/qform-pc-form-control[1]/div[1]/div[2]/qform-pc-radio[1]/qform-pc-radio-accessor[1]/div[1]/label[1]/span[1]").click()
    # driver.find_element_by_xpath(
    #     "/html[1]/body[1]/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/div[2]/button[2]").click()

    # driver.find_element_by_xpath("//body/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/qform-pc-form[1]/div[1]/div[9]/div[1]/qform-pc-form-control[1]/div[1]/div[3]/qform-address[1]/qform-address-accessor[1]/nz-cascader[1]/div[1]/div[1]/i[1]/*[1]").click()
    #
    # try:
    #     waitByXpath(driver,"/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/ul[1]/li[10]").click()
    #     waitByXpath(driver, "/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/ul[1]/li[9]").click()
    # except:
    #     waitByXpath(driver,"/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/ul[1]/li[9]").click()
    # # waitByXpath(driver,"//body/div[2]/div[2]/div[1]/div[1]/ul[1]/li[9]/span[2]/i[1]/*[1]").click()
    #
    # # 上海市
    # try:
    #     waitByXpath(driver,"/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/ul[2]/li[1]").click()
    # except:
    #     driver.find_element_by_xpath("//body/div[2]/div[2]/div[1]/div[1]/ul[2]/li[1]/span[2]/i[1]/*[1]").click()
    #
    # # 闵行区
    # waitByXpath(driver,"//body/div[2]/div[2]/div[1]/div[1]/ul[3]/li[8]").click()
    #
    # time.sleep(3)
    # waitByCSS(driver,"qf-pages.ng-star-inserted:nth-child(2) qf-app-item.ng-star-inserted:nth-child(2) qf-app-initiate.ng-star-inserted:nth-child(2) div.initiate-content div.initiate-form-content qf-initiate-apply:nth-child(1) div.main-content.ng-star-inserted div.form-wrapper div.form-footer:nth-child(3) > button.ant-btn.ant-btn-primary").click()
    #
    # # driver.find_element_by_css_selector("qf-pages.ng-star-inserted:nth-child(2) qf-app-item.ng-star-inserted:nth-child(2) qf-app-initiate.ng-star-inserted:nth-child(2) div.initiate-content div.initiate-form-content qf-initiate-apply:nth-child(1) div.main-content.ng-star-inserted div.form-wrapper div.form-footer:nth-child(3) > button.ant-btn.ant-btn-primary").click()
    # # driver.find_element_by_xpath("//body/div[2]/div[4]/div[1]/div[1]/div[2]/div[1]/qf-apply-side-modal[1]/div[1]/div[3]/qf-initiate-apply[1]/div[1]/div[1]/div[2]/button[2]").click()
    # #
    # # waitByXpath(driver,"/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/div[2]/div[1]/qf-apply-side-modal[1]/div[1]/div[3]/qf-initiate-apply[1]/div[1]/div[1]/div[2]/button[2]").click()
    # # driver.find_element_by_xpath("//body/div[2]/div[2]/div[1]/div[1]/ul[1]/li[9]/span[2]/i[1]/*[1]").click()
    #
    # # 跳转之后证明填写成功
    # while True:
    #     if driver.current_url != url1:
    #         print("All done,Bye!!")
    #         driver.close()
    #         break
