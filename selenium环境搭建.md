``
pip install selenium
``

下载对应的[浏览器驱动](https://npm.taobao.org/mirrors/chromedriver/)，注意要下载跟浏览器对应版本的driver,然后复制到chrome.exe所在的文件夹下面，我的是C:\Program Files\Google\Chrome\Application

输入
```
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
```
如果能正常打开百度页面，则说明浏览器驱动安装正确。
