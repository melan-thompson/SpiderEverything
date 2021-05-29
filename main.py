
import time

def SJTULogin(diver,username="melan_thompson",password="xwp13030"):
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
    wait.until(lambda x: driver.find_element_by_id("user"), "Loading time exceeds limit or it is not a jaccount login page")
    currenturl = driver.current_url
    print(currenturl)

    # # 填入用户名和密码
    # driver.find_element_by_id("user").send_keys(username)
    # driver.find_element_by_id("pass").send_keys(password)

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
        nexturl=diver.current_url
        print(nexturl)
        if "jaccount.sjtu.edu.cn" not in nexturl:
            print("Successfully log in")
            break

    return driver


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("https://ssc.sjtu.edu.cn/f/dae8d35a")
    SJTULogin(driver)

    from selenium.webdriver.support.wait import WebDriverWait
    wait = WebDriverWait(driver, 10, 0.1)
    wait.until(lambda x: driver.find_element_by_xpath("/html[1]/body[1]/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/qform-pc-form[1]/div[1]/div[3]/div[2]/qform-pc-form-control[1]/div[1]/div[2]/qform-pc-radio[1]/qform-pc-radio-accessor[1]/div[1]/label[1]/span[1]"), "Loading time exceeds limit or it is not a jaccount login page")
    # 记录当前url
    url1=driver.current_url

    # 点击
    driver.find_element_by_xpath("/html[1]/body[1]/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/qform-pc-form[1]/div[1]/div[3]/div[2]/qform-pc-form-control[1]/div[1]/div[2]/qform-pc-radio[1]/qform-pc-radio-accessor[1]/div[1]/label[1]/span[1]").click()
    driver.find_element_by_xpath("/html[1]/body[1]/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/div[2]/button[2]").click()

    # 跳转之后证明填写成功
    while True:
       if driver.current_url!=url1:
            driver.close()
            break


    time.sleep(15)

    driver.get("https://sports.sjtu.edu.cn/pc/?locale=zh#/Venue/1")
    # driver.f
    # SJTULogin(driver)
    driver.find_element_by_xpath("//body/div[@id='app']/div[@id='logoin']/div[1]/div[1]/div[2]/button[1]").click()
    SJTULogin(driver)

    # 点击羽毛球
    time.sleep(0.1)
    driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/ul[1]/li[5]/a[1]/img[1]").click()

    # 点击霍英东
    time.sleep(0.1)
    driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[1]/div[5]/div[2]/ul[1]/li[1]/div[1]").click()

    time.sleep(0.1)
    driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[9]").click()

    time.sleep(1)
    driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[6]/div[1]/div[1]/div[1]").click()
    # driver.find_element_by_xpath("//body/div[@id='app']/div[@id='apointmentDetails']/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[6]/div[1]/div[1]/div[1]").click()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/