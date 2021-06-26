def b64encoding(string):
    import base64
    return base64.b64encode(str.encode(string)).decode()


def b64decoding(string):
    import base64
    return base64.b64decode(str.encode(string)).decode()


if __name__=="__main__":
    # jaccount={"jaccount":b64encoding(input("please input your jaccount:")),"password":b64encoding(input("please input your jaccount password:"))}
    import json
    with open("jaccount.json", mode='r', encoding='UTF-8') as f:
        setting = json.load(f)

    setting["jaccount"]=b64encoding(input("please input your jaccount:"))
    setting["password"]=b64encoding(input("please input your jaccount password:"))
    with open("jaccount.json",'w') as fp:
        fp.write(json.dumps(setting, indent=4))

    print("jaccount is: ",b64decoding(setting["jaccount"]))
    print("password is: ",b64decoding(setting["password"]))
