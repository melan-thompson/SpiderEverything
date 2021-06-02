import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def addimg(src, imgid):
    fp = open(src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', imgid)
    return msgImage


class EmailMaster:
    def __init__(self, settingfile="EmailSenderSetting.json", subject="Hello"):
        import json
        with open(settingfile, mode='r', encoding='UTF-8') as f:
            setting = json.load(f)

        self.emailaddress = setting["mail user"]

        try:
            self.server = smtplib.SMTP_SSL(setting["mail host"], setting["port"])
            self.server.login(setting["mail user"], setting["mail password"])
        except Exception as e:
            print("Email log in error", e)
        else:
            print("Email successfully log in")
        self.message = MIMEMultipart('related')
        self.message["From"] = setting["mail user"]
        self.message["Subject"] = subject

    def usetemplate1(self, image):
        content = """
                <!doctype html>
                <html>
                <head>
                <meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
                <title></title>
                </head>
                <body><h1 id='场地预定成功通知'>场地预定成功通知</h1>
                <p>您的羽毛球场地已经成功下单，请使用微信扫描下方的二维码进行支付：</p>
                <p><img src="cid:image1" referrerpolicy="no-referrer" alt="Figure_4181"></p>
                <p>感谢您的使用！期待下次与您见面，谢谢！</p>
                <p>&nbsp;</p>
                </body>
                </html>
                """
        msg = MIMEText(content, 'html', 'utf-8')
        self.message.attach(msg)
        self.message.attach(addimg(image, "image1"))
        # print(self.message)

    def send(self, contacts=["1303061669@qq.com"]):
        import time
        try:
            for each in contacts:
                self.message["To"]=each
                self.server.sendmail(self.emailaddress, each, self.message.as_string())
        except Exception as e:
            print("Email sending error!!")
            print(e)
        else:
            print("Successfully send email")
        finally:
            self.server.quit()
            self.server.close()


if __name__ == "__main__":
    import time

    for i in range(5):
        mail = EmailMaster(subject="羽毛球预定成功")
        mail.usetemplate1("../Figure_4181.png")
        mail.send()
        time.sleep(4)
