# coding:utf-8
import os
from PyPDF3 import PdfFileReader
from PyPDF3 import PdfFileWriter
 
 
def get_reader(filename, password=None):
    # 打开文件
    try:
        old_file = open(filename, 'rb')
        print('文件{}打开成功！'.format(filename))
    except Exception as err:
        print('文件打开失败！' + str(err))
        return None
 
    # 创建读实例
    pdf_reader = PdfFileReader(old_file, strict=False)
 
    # 如果被加密了则进行解密操作
    if pdf_reader.isEncrypted:
        if password is None:
            raise Exception("{}文件被加密，需要密码!".format(filename))
        else:
            if pdf_reader.decrypt(password) != 1:
                raise Exception("{}密码不正确!".format(filename))
    
    # 关闭文件
    if old_file in locals():
        old_file.close()

    print(pdf_reader.getDocumentInfo())
    
    return pdf_reader
 
# 会有版本问题，高版本的不能解密
def decrypt_pdf(filename, password, decrypted_filename=None):
    """
    将加密的文件及逆行解密，并生成一个无需密码pdf文件
    :param filename: 原先加密的pdf文件
    :param password: 对应的密码
    :param decrypted_filename: 解密之后的文件名
    :return:
    """
    # 生成一个Reader和Writer
    pdf_reader = get_reader(filename, password)
    if not pdf_reader.isEncrypted:
        print('文件没有被加密，无需操作！')
        return
    pdf_writer = PdfFileWriter()
 
    pdf_writer.appendPagesFromReader(pdf_reader)
 
    if decrypted_filename is None:
        decrypted_filename = "".join(filename[:-4]) + '_' + 'decrypted' + '.pdf'
 
    # 写入新文件
    pdf_writer.write(open(decrypted_filename, 'wb'))
 

# opens a PDF with restrictive editing enabled, but that still
# allows printing.可以行得通
def pdf_Crack(startFile,password,endFile=None):
    from pikepdf import open
    try:
        open(startFile)
        print("文件{}未加密".format(startFile))
    except Exception as e:
        print(e)
        if endFile is None:endFile=startFile
        with open(startFile,password=password,allow_overwriting_input=True) as pdf:
            try:
                pdf.save(endFile)
            except PermissionError:
                raise Exception("请先关闭文件！！")
        print("成功解密文件{}".format(startFile))

def file_name(file_dir):
    import os
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        file2 = [each for each in files if ".pdf" in each]
        return file2

def getAllFiles(targetDir,fileter=".pdf"):
    files = []
    listFiles = os.listdir(targetDir)
    for i in range(len(listFiles)):
        path = os.path.join(targetDir, listFiles[i])
        if os.path.isdir(path):
            files.extend(getAllFiles(path))
        elif os.path.isfile(path):
            if fileter in path:
                files.append(path)
    return files

if __name__=="__main__":
    # get_reader("UserCodeC.pdf")
    # get_reader("CFDCoupling.pdf")
    # decrypt_pdf("CFDCoupling.pdf","IntegratedCAE")
    print(getAllFiles("C:\\Program Files (x86)\\GTI\\v2016\\documents"))

    for each in getAllFiles("C:\\Program Files (x86)\\GTI\\v2016\\documents"):
        pdf_Crack(each,"IntegratedCAE")
    # print(file_name("."))
    # pdf_Crack("ControlsCouplingAndRealTime.pdf","IntegratedCAE")
