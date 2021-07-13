import time
import os
from selenium import webdriver
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


def b64decoding(string):
    import base64
    return base64.b64decode(str.encode(string)).decode()


if __name__ == '__main__':
    import json

    with open("../jaccount.json", mode='r', encoding='UTF-8') as f:
        setting = json.load(f)

    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

    driver = webdriver.Chrome(setting["chrome driver directory"])
    driver.get("https://ssc.sjtu.edu.cn/f/dae8d35a")
    SJTULogin(driver,username=b64decoding(setting["jaccount"]),password=b64decoding(setting["password"]))

    waitByXpath(driver,"/html[1]/body[1]/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply["
        "1]/div[1]/div[1]/qform-pc-form[1]/div[1]/div[3]/div[2]/qform-pc-form-control[1]/div[1]/div["
        "2]/qform-pc-radio[1]/qform-pc-radio-accessor[1]/div[1]/label[1]/span[1]",20)

    # 记录当前url
    url1 = driver.current_url

    # 点击
    driver.find_element_by_xpath(
        "/html[1]/body[1]/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/qform-pc-form[1]/div[1]/div[3]/div[2]/qform-pc-form-control[1]/div[1]/div[2]/qform-pc-radio[1]/qform-pc-radio-accessor[1]/div[1]/label[1]/span[1]").click()
    driver.find_element_by_xpath(
        "/html[1]/body[1]/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/div[2]/button[2]").click()

    # 跳转之后证明填写成功
    while True:
        if driver.current_url != url1:
            print("All done,Bye!!")
            driver.close()
            break
