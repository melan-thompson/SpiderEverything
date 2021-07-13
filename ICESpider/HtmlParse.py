from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
from selenium.webdriver.support.wait import WebDriverWait

class HtmlParse(object):
    def parse_data(self,page_url,data):
        print("start analyzing data...")
        if page_url is None or data is None:
            return
        soup=BeautifulSoup(data,"lxml") #data is the requst text.
        urls=self.get_urls(soup)
        print("{0} urls is found in the site:".format(len(urls))+page_url)
        data=self.get_data(page_url,soup)
        return urls,data
    
    def get_urls(self,soup):
        urls=list()
        links=soup.select('a[href*="/tech/"]')
        for link in links:
            url=link['href']
            urls.append(url)
        return urls
    
    def get_data(self,page_url,soup):
        data={}
        data['url']=page_url
        title=soup.select_one('.cnbeta-article>header>h1')
        release_data=soup.select_one('.cnbeta-article>header>.meta>span')
        data['title']=title.get_text()
        data['release_data']=release_data.get_text()
        print("article url:{0}".format(page_url))
        print('data:{0}'.format(data))
        return data
    """description of class"""

##Elesvier上的表格爬取工具
def matchword(word,document):
    if re.match(word,document,re.I) is not None:
        return True
    else: return False

class Table():
    

    def __init__(self,table_name,table_contents):
        self.table_name=table_name
        self.table_contents=table_contents
        self.length=list()
        for each in self.table_contents:
            self.length.append(len(each))
        self.key_words=set(["Bore","Stoke","Compression ratio","Engine type","Displacement",
                  "Engine model"])

    

    def findKeyWords(self):
        for i in self.table_contents:
            for j in i:
                for k in self.key_words:
                    if matchword(k,j):
                        #print("match word "+k+" at row {}".format(self.table_contents.index(i)+1))
                        return self.table_contents.index(i)+1
        return 0

    def show(self):
        print('*'*len(self.table_name))
        print(self.table_name)
        print('-'*len(self.table_name))
        headline=self.findKeyWords()
        for each in self.table_contents:
            if self.table_contents.index(each)==headline-1:
                print('-'*len(self.table_name))
            print(each)
        print('-'*len(self.table_name))
        #for each in self.length:
         #   print(each)


def tableAnlysis(table):
    tablename=table.findChild('p').text
    record= table.find_all("tr")
    rec=list()
    for each in record:
        temp=list()
        for ele in each:
            temp.append(ele.text)
        rec.append(temp)
    ## 如果所有的record长度一样，则第一行就是表头
    result=Table(tablename,rec)
    return result

def getUrlTables(driver,url):
        wait = WebDriverWait(driver, 10, 0.5)
        wait.until(lambda x:driver.find_element_by_tag_name('table'),"Loading time exceeds limit")
        soup=BeautifulSoup(driver.page_source,'lxml')
        #print(soup.prettify())
        tables=soup.find_all('div',class_=re.compile(r'.*table.*'))
        print("url:"+url+" contains {} tables,They are:".format(len(tables)))
        for each in tables:
            temp=tableAnlysis(each)
            if temp.findKeyWords():
                print("Following table are what you are finding:")
                temp.show()
        # input()

if __name__=="__main__":
    url="https://www.sciencedirect.com/science/article/pii/S0960148119308663"
    driver=webdriver.Chrome()
    driver.get(url)
    lasturl=driver.current_url
    getUrlTables(driver,lasturl)
    while True:
        if lasturl!=driver.current_url:
            getUrlTables(driver,lasturl)
            lasturl=driver.current_url



