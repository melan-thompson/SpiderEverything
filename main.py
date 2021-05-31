
if __name__ == '__main__':
    import json
    with open("BadmintonCourtOrder/setting.json",mode='r', encoding='UTF-8') as f:
        setting=json.load(f)
    print(setting["jaccount"])
    print(type(setting["booking order"]))
    print(setting["date"])

