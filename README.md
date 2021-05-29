# SpiderEverything

# 开发工具

## 谷歌浏览器ChroPath插件
能够一键审查元素XPath、css的插件，再也不用自己去手动写了。

# 运行环境

## selenium driver

```
pip install selenium
```

下载对应的浏览器驱动，注意要下载跟浏览器对应版本的driver,然后复制到chrome.exe所在的文件夹下面，一般是C:\Program Files\Google\Chrome\Application

输入
```
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
```
如果能正常打开百度页面，则说明浏览器驱动安装正确。

## Tesseract OCR的安装
一般进入某个组织的网站都是需要登录的，输入用户名和密码之后还需要输入验证码，验证码有两种处理方式，一种人工输入，一种使用OCR将验证码的图片中的文字识别出来。Tesseract是由Google开发的开源的OCR项目，能够识别包含数字和字母的验证码。
Tesseract的安装分为两步：
1. 使用pip安装Tesseract:``pip install pytesseract``
2. 安装Tesseract-ocr。在Windows系统下，官方不提供最新版本的平台安装包，只有旧的3.02.02版本的工具，其[exe程序的下载地址](https://sourceforge.net/projects/tesseract-ocr-alt/files/)
