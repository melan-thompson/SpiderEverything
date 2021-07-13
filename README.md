# SpiderEverything

运行前先点击preRun.bat设置jaccount，为了防止jaccount泄露采用加密的方式，

# 运行环境

## selenium driver

1. python selenium 安装

```
pip pip install selenium
```

2. 下载对应的浏览器驱动，推荐[下载地址1](https://npm.taobao.org/mirrors/chromedriver/)，[下载地址2](http://chromedriver.storage.googleapis.com/index.html)，注意要下载跟浏览器对应版本的driver,然后复制到chrome.exe所在的文件夹下面，一般是C:\Program Files\Google\Chrome\Application，目录DependentSoftwares下有最新版本的Chrome driver。
3. 将Chrome.exe所在目录加入到环境变量中
4. 验证是否安装成功，运行以下python语句

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
2. 安装Tesseract-ocr。在Windows系统下，官方不提供最新版本的平台安装包，只有旧的3.02.02版本的工具，其[exe程序的下载地址](https://sourceforge.net/projects/tesseract-ocr-alt/files/)，目录DependentSoftwares下也有下载好的Windows安装包，可以直接双击运行。



# 开发工具

## 谷歌浏览器ChroPath插件

能够一键审查元素XPath、css的插件，再也不用自己去手动写了。

## APP数据的爬取

参考[^3][^5]





# 参考文献

[^1]:[（美）LINDSAY BASSETT著；魏嘉汛译.图灵程序设计丛书 JSON必知必会[M].北京：人民邮电出版社.2016.](https://book.duxiu.com/bookDetail.jsp?dxNumber=000030163180&d=4F0A3CF4EDDF6C8673E256D7CBB09AD0&fenlei=1817040302&sw=json%E5%BF%85%E7%9F%A5%E5%BF%85%E4%BC%9A)
[^2]:[唐松，陈智铨编著.Python网络爬虫从入门到实践[M].北京：机械工业出版社.2017.](https://book.duxiu.com/bookDetail.jsp?dxNumber=000016779339&d=B010419C1F95CAA000598D5541AFA9CD&fenlei=18170403010205&sw=python%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%AE%9E%E6%88%98)
[^3]:[使用python抓取APP数据](https://blog.csdn.net/qq_37275405/article/details/81181439)
[^4]:[（中国）东郭大猫.Scrapy网络爬虫实战[M].北京：清华大学出版社.2019.](https://book.duxiu.com/bookDetail.jsp?dxNumber=000018618625&d=C0F52B336A110031FBC52FEB2B1EF0D6&fenlei=18170403010205&sw=scrapy%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB)
[^5]:[肖睿陈磊. Python网络爬虫[M]. 北京：人民邮电出版社, 2020.01. ](https://book.duxiu.com/bookDetail.jsp?dxNumber=000018836678&d=B7D241515EFC54622FF391712BE31A34&fenlei=18170403010205&sw=python%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB)
[^6]:[selenium-python](https://github.com/baijum/selenium-python)

[^7]:[官方文档](https://www.selenium.dev/documentation/en/)