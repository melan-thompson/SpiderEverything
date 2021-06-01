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

if __name__ == '__main__':
    # import json
    #
    # with open("BadmintonCourtOrder/setting.json", mode='r', encoding='UTF-8') as f:
    #     setting = json.load(f)
    #
    # print(setting["login method"])
    import smtplib
    from email.mime.text import MIMEText

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    msg_from = '18373173350@163.com'  # 发送方邮箱
    passwd = 'xwp13030'  # 填入发送方邮箱的授权码
    passwd2="JYSQRSLFYZETICQW"
    msg_to = '1303061669@qq.com'  # 收件人邮箱
    mail_host = 'smtp.163.com'

    def send():
        subject = "python邮件测试"  # 主题
        msg = MIMEMultipart('related')
        cont="""
        <!doctype html>
        <html>
        <head>
        <meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
        <title></title>
        </head>
        <body><h1 id='场地预定成功通知'>场地预定成功通知</h1>
        <p>您的羽毛球场地已经成功下单，请使用支付宝扫描下方的二维码进行支付：</p>
        <p><img src="cid:image1" referrerpolicy="no-referrer" alt="Figure_4181"></p>
        <p>感谢您的使用！期待下次与您见面，谢谢！</p>
        <p>&nbsp;</p>
        </body>
        </html>
        """

        content = MIMEText(cont, 'html', 'utf-8')  # 正文
        # msg = MIMEText(content)
        msg.attach(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to

        msg.attach(addimg("Figure_4181.png",'image1'))


        try:
            s = smtplib.SMTP_SSL(mail_host, 465)  # 邮件服务器及端口号
            # s = smtplib.SMTP(host=mail_host)
            s.login(msg_from, passwd2)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print("Done")
        except Exception as e:
            print(e)
    send()


