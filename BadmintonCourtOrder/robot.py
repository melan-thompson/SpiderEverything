import requests
import urllib
import itchat


def qingyunke(msg):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
    html = requests.get(url)
    return html.json()["content"]


if __name__=="__main__":
    # from itchat.content import TEXT
    #
    #
    # @itchat.msg_register(TEXT)
    # def simple_reply(msg):
    #     print(msg['Text'])
    #
    #
    # itchat.auto_login(hotReload=True)
    # itchat.run()
    # itchat.dump_login_status()



    for i in range(100):
        msg = '你是谁'
        print("原话>>", msg)
        res = qingyunke(msg)
        print("青云客>>", res)
