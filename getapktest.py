# coding=utf-8
import urllib
import requests
import re
from bs4 import BeautifulSoup

def parser_apks(self, count=30):
    _root_url = "http://app.mi.com"  # 应用市场主页网址
    res_parser = {}
    # 设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
    page_num = 0
    while count:
        # 获取应用列表页面
        wbdata = requests.get("http://app.mi.com/category/1#page=" + str(page_num)).text
        print("开始爬取第" + str(page_num) + "页")
        # 解析应用列表页面内容
        soup = BeautifulSoup(wbdata, "html.parser")
        targetDiv = soup.find(id='all-applist')
        #print("爬取apk数量为: " + str(targetDiv))
        links = targetDiv.find_all("a", href=re.compile("/details?"), class_="", alt="")
        for link in links:
             # 获取应用详情页面的链接
            detail_link = urllib.parse.urljoin(_root_url, str(link["href"]))
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
        if count > 0:
            page_num = page_num + 1
    print("爬取apk数量为: " + str(len(res_parser)))
    return res_parser

def craw_apks(self, count=2000, save_path="d:\\apk\\金融理财\\"):
    while count:

        res_dic = parser_apks(30)

        for apk in res_dic.keys():
            print("正在下载应用: " + apk)
            urllib.request.urlretrieve(res_dic[apk], save_path + apk + ".apk")
            print("下载完成")
        count = count - 30

if __name__ == "__main__":
    craw_apks(2000)