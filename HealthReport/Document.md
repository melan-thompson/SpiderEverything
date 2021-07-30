# 使用python脚本自动填写健康日报

[TOC]



## 版本2.1

发布日期：2021/7/30

1. 修改 click interrupt的问题
   是上面的下拉框元素覆盖了下面下拉框的元素定位，才会导致报错。解决办法有2种：

```python
element = driver.find_element_by_css(‘div[class*=“loadingWhiteBox”]’)
driver.execute_script(“arguments[0].click();”, element)

element = driver.find_element_by_css(‘div[class*=“loadingWhiteBox”]’)
webdriver.ActionChains(driver).move_to_element(element ).click(element ).perform()
```

## 版本2.0

发布日期：2021年暑假，取消一键三连。

今日所在地区

```
//body/qf-root[1]/qf-pages[1]/qf-app-item[1]/qf-app-initiate[1]/div[1]/div[1]/qf-initiate-apply[1]/div[1]/div[1]/qform-pc-form[1]/div[1]/div[9]/div[1]/qform-pc-form-control[1]/div[1]/div[3]/qform-address[1]/qform-address-accessor[1]/nz-cascader[1]/div[1]/div[1]/input[1]
```

先点苏州，如果报错这时候就能看到上海，再点上海。



## 如何每天定时运行？

将script.bat添加进进程，参考[window中怎么添加定时任务](https://www.cnblogs.com/gcgc/p/11594467.html)

```
compmgmt.msc
```







