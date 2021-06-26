# def sendEmail():
#     import time
#
#     from PIL import ImageGrab
#     import smtplib
#     from email.mime.image import MIMEImage
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText
#     from email.header import Header
#
#     endDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
#     # img = ImageGrab.grab()
#     # img.save('E:\\12.png')
#     my_sender = '123@qq.com'  # 发件人邮箱账号
#     my_pass = 'tmugmde3333ad'  # 发件人邮箱密码
#     my_user = '123@qq.com'  # 收件人邮箱账号，我这边发送给自己
#     sender = “123 @ qq.com”
#     receivers = ['123@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
#     msgRoot = MIMEMultipart('related')
#     msgRoot['From'] = Header(str(endDate) + " 大盘趋势", 'utf-8')
#     msgRoot['To'] = Header("测试", 'utf-8')
#     subject = str(endDate) + ' 趋势'
#     msgRoot['Subject'] = Header(subject, 'utf-8')
#
#     msgAlternative = MIMEMultipart('alternative')
#     msgRoot.attach(msgAlternative)
#
#     mail_msg = """
#     <p>大盘趋势</p>
#     <p>图片演示：</p>
#     <p><img src="cid:image1"></p>
#     """
#     msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
#
#     # 指定图片为当前目录
#     fp = open('E:\\12.png', 'rb')
#     msgImage = MIMEImage(fp.read())
#     fp.close()
#
#     # 定义图片 ID，在 HTML 文本中引用
#     msgImage.add_header('Content-ID', '<image1>')
#     msgRoot.attach(msgImage)
#
#     try:
#         smtpObj = smtplib.SMTP()
#         smtpObj.connect('smtp.qq.com', 25)  # 25 为 SMTP 端口号
#         smtpObj.login(my_user, my_pass)
#         smtpObj.sendmail(sender, receivers, msgRoot.as_string())
#         print("邮件发送成功")
#     except smtplib.SMTPException:
#         print("Error: 无法发送邮件")
#     ————————————————
#     版权声明：本文为CSDN博主「坚持学习的菜鸟」的原创文章，遵循CC
#     4.0
#     BY - SA版权协议，转载请附上原文出处链接及本声明。
#     原文链接：https: // blog.csdn.net / tianjingle_blog / article / details / 110153165

def addimg(src,imgid):
    fp = open(src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', imgid)
    return msgImage

def b64encoding(string):
    import base64
    return base64.b64encode(str.encode(string)).decode()

def b64decoding(string):
    import base64
    return base64.b64decode(str.encode(string)).decode()

if __name__ == '__main__':
   import base64
   a=b64encoding("melan_thompson")
   print(a)
   b=b64decoding(a)
   print(b)

def b64encoding(string):
    import base64
    return base64(str.encode(string))

