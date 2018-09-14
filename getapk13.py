# coding=utf-8
import urllib
import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
def parser_apks(self, page_num , count=30 ):
    _root_url = "http://app.mi.com"  # 应用市场主页网址
    res_parser = {}
    # 设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推

    while count > 0:

        # 获取应用列表页面
        url = "http://app.mi.com/category/13#page=" + str(page_num)
        hea = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        #wbdata = requests.Session()
        #wbdata.get(url)

        driver = webdriver.PhantomJS(executable_path=r'F:\IDE\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        driver.get(url)
        # 等待加载完成
        time.sleep(5)
        #wbdata = requests.get(url,headers=hea).text
        #wbdata = driver.text
        #print(wbdata)
        print("开始爬取第" + url + "页")

        # 解析应用列表页面内容
        #soup = BeautifulSoup(wbdata, "html.parser")
        #targetDiv = soup.find(id='all-applist')
        #print("爬取apk数量为: " + str(targetDiv))
        #links = soup.find_all("a", href=re.compile("/details?"), class_="", alt="")
        links = driver.find_elements_by_xpath("/html/body/div[4]/div/div[1]/div[2]/ul/li/a")

        #print(links)
        print("开始爬取第" + str(page_num) + "页")
        for a in links:
            detail_link = a.get_attribute('href')

            package_name = detail_link.split("=")[1]
            download_page = requests.get(detail_link).text
            #解析应用详情页面
            soup1 = BeautifulSoup(download_page, "html.parser")
            download_link = soup1.find(class_="download")["href"]
            #获取直接下载的链接
            download_url = urllib.parse.urljoin(_root_url, str(download_link))
            # 解析后会有重复的结果，通过判断去重
            if download_url not in res_parser.values():
                res_parser[package_name] = download_url
            count = count - 1
            if count == 0:
                break

    print("爬取apk数量为: " + str(len(res_parser)))
    return res_parser

def craw_apks(self, count=2000, save_path="f:\\apk\\娱乐消遣\\"):
    page_num = 8
    while count:

        res_dic = parser_apks(30 , page_num)

        for apk in res_dic.keys():
            print("正在下载应用: " + apk + res_dic[apk])
            urllib.request.urlretrieve(res_dic[apk], save_path + apk + ".apk")
            print("下载完成")
        count = count - 30
        page_num = page_num + 1

if __name__ == "__main__":
    craw_apks(2000)