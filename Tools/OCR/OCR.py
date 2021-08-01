import os

import requests


def ocr_space_file(filename, overlay=False, api_key='86106fd1dd88957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


def pngOCR(filename, lang="chs"):
    test_file = ocr_space_file(filename=filename, language=lang)
    import json
    user_dict = json.loads(test_file)
    return user_dict["ParsedResults"][0]["ParsedText"]


def file_name(file_dir):
    import os
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        file2 = [each for each in files if ".png" in each or ".jpg" in each]
        return file2


# Use examples:
if __name__ == "__main__":
    files = file_name(".")
    print("files in this directory:", files)

    from docx import Document

    Doc = Document()
    for each in files:
        result = pngOCR(each)
        print(each, "OCR result:", result)
        Doc.add_paragraph(result)
    Doc.save("Python_word.docx")

    os.system("start Python_word.docx")
