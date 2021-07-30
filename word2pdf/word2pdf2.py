from win32com.client import Dispatch
import os


def doc2pdf(filePath, file):
    fileabspath=filePath+"\\"+file
    print("正在转换:",fileabspath)
    word = Dispatch('Word.Application')
    try:
        doc = word.Documents.Open(fileabspath)
    except Exception as e:
        print(e)
        raise Exception("can not open file "+fileabspath)
    outFile = filePath +"\\pdf\\"+ file.split('.')[0] + ".pdf" #生成pdf文件路径名称
    doc.SaveAs(outFile, FileFormat=17)
    doc.Close()
    print(outFile,"转换成功\n\n")
    word.Quit()

if __name__ == "__main__":

    # doc2pdf(os.getcwd(),"03-项目研究2020年度1季度阶段性总结报告.docx")
    import json

    with open("seeting.json", mode='r', encoding='UTF-8') as f:
        setting = json.load(f)

    if setting["wordDir"] is None:
        wordDir=os.getcwd()

    if setting["pdfDir"] is None:
        try:
            os.mkdir(os.getcwd()+"\\pdf",777)
        except:
            pass

    filelist = os.listdir(wordDir)
    print(filelist)
    for file in filelist:
        if (file.endswith(".doc") or file.endswith(".docx") or file.endswith(".docm")) and ("~$" not in file):
            doc2pdf(wordDir, file)
    print ("所有word文件转PDF文件已完成！！！")
