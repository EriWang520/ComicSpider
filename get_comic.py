# -*- coding: utf-8 -*-
# coding=UTF-8

import requests
from lxml import etree, html
from urllib import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
from time import sleep
import os
import json

# 单个漫画爬取

# 漫画首页地址
url = "http://pufei8.com/manhua/17"
url2 = "https://ac.qq.com/Comic/ComicInfo/id/635142"
url3 = "http://atharori.net/-20PUOJ/F5Bcu?rndad=2105100218-1606312793"
url4 = "http://www.177pic.pw/"
url5 = "http://www.177pic.pw/html/category/tt/"   # 中文
url6 = "https://imhentai.com/gallery/593889/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

chrome_cache_path = 'D:/Program/spiderFile/driverData/chromeCache/'
screenshot_path = "D:/Program/spiderFile/driverData/chromeCache/"

down_path = "D:/Program/spiderFile/down/comic/"

down_path_linux = "r'/home/ericw/down'"
driver_path_linux = "r'/home/ericw/chromedriver'"

page_count = 1


# 获取漫画所有章节地址
def get_chapter_address_list():
    req = request.Request(url5, headers=headers)
    data = request.urlopen(req).read().decode('utf-8', 'ignore')
    ht = etree.HTML(data)
    chapter_list = ht.xpath("//h2[@class='grid-title']/a/@href")
    print("--------------------------------------------")
    print(chapter_list)
    return chapter_list


# 获取漫画
def get_book(chapter_list):
    for chapter_address in chapter_list:
        # 根据章节地址获取章节图片
        get_chapter(chapter_address)


# 获取单章节
def get_chapter(chapter_address):
    # 设置谷歌浏览器为无界面
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    # webdriver位置
    # webdriver_path = "D:/Program/Chrome/Application/"
    # browser = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)
    # browser = webdriver.Chrome(options=chrome_options)
    browser = webdriver.Chrome()

    # 开始请求章节地址
    print("开始请求章节地址")
    browser.get(chapter_address)
    print("请求完成")
    # 设置延迟缓冲
    sleep(3)

    try:
        # 设置自动下滑滚动条操作
        for i in range(1, 20):
            # 滑动距离设置
            js = 'window.scrollTo(0,%s)' % (500 * i)
            # 执行滑动选项
            browser.execute_script(js)
            print("执行滑动选项完成", i)
            # 延时,使图片充分加载
            sleep(1)

        sleep(2)
        # 获取当前页面源码
        source_data = browser.page_source
        print("获取当前页面源码完成")
        # 在当前文件夹下创建html文件,并将网页源码写入
        print("写入源码到本地")
        try:
            fh = open(chrome_cache_path + "comic.html", "w", encoding="utf-8")
            fh.write(source_data)

        except Exception as err:
            print(err)

        print("写入源码完成")
        fh.close()

        # 打开保存的html文件,提取其中的图片信息,并保存到文件夹中
        get_img(browser)
        print("关掉无界面浏览器")
        browser.quit()

        # 获取剩余页面
        page_link_list = get_page_link_list()
        page_num = 1
        for page_link in page_link_list:
            page_num = page_num + 1
            get_pages(page_link, page_num)

    # 若上述代码执行报错（大概率是由于付费漫画）,则执行此部分代码
    except Exception as err:
        # 跳过错误代码
        pass

# 配置谷歌浏览器请求地址
# def web_request():
#


# 获取剩余页面
def get_pages(page_link, page_num):
    browser = webdriver.Chrome()

    # 开始请求章节地址
    print("开始请求分页地址:",page_num)
    browser.get(page_link)
    print("请求完成")

    # 设置延迟缓冲
    sleep(3)

    try:
        # 设置自动下滑滚动条操作
        for i in range(1, 20):
            # 滑动距离设置
            js = 'window.scrollTo(0,%s)' % (500 * i)
            # js = 'var q=document.getElementById("mainView").scrollTop = ' + str(i * 1000)
            # 执行滑动选项
            browser.execute_script(js)
            print("执行滑动选项完成", i)
            # 延时,使图片充分加载
            sleep(2)

        sleep(2)
        # 获取当前页面源码
        source_data = browser.page_source
        print("获取当前页面源码完成")
        # 在当前文件夹下创建html文件,并将网页源码写入
        print("写入源码到本地")
        try:
            fh = open(chrome_cache_path + "comic.html", "w", encoding="utf-8")
            fh.write(source_data)
        except Exception as err:
            print(err)

        print("写入源码完成")
        fh.close()

        # 打开保存的html文件,提取其中的图片信息,并保存到文件夹中
        get_img(browser)
        print("关掉无界面浏览器")
        browser.quit()

    # 若上述代码执行报错（大概率是由于付费漫画）,则执行此部分代码
    except Exception as err:
        # 跳过错误代码
        print(err)
        pass


# 打开保存的html文件,提取其中的图片信息,并保存到文件夹中
def get_img(browser):
    # 用beautifulsoup打开本地文件
    html_new = BeautifulSoup(open(chrome_cache_path + "comic.html", encoding='utf-8'), features='html.parser')
    # 提取html文件中的主体部分
    soup = html_new.find(id="main")
    print("提取html文件中的主体部分完成")
    h1 = soup.find("h1")
    chapter_name = h1.text

    # 将打开的界面截图保存,证明无界面浏览器确实打开了网页
    # print("正在保存打开的界面截图")
    # browser.get_screenshot_as_file(chrome_cache_path + str(chapter_name) + ".png")

    # 如果不存在则以章节名命名文件夹
    if not os.path.exists(down_path + str(chapter_name)):
        print("以章节名命名文件夹")
        os.makedirs(down_path + str(chapter_name))

    # 设置变量i,方便为保存的图片命名
    i = 0
    img_src_list = []

    print("提取图片地址信息")
    # 提取出主体部分中的img标签（因为图片地址保存在img标签中）
    for img in soup.find_all("img"):
        # 提取图片地址信息
        img_src = img.get("src")
        if img_src not in img_src_list:
            img_src_list.append(img_src)

    print("提取图片地址信息完成")

    global page_count

    for img_src in img_src_list:
        # 请求图片地址
        print("请求图片地址:", img_src)
        comic_pic = requests.get(img_src).content
        try:
            # 打开文件夹,将图片存入
            with open(down_path + str(chapter_name) + '/' + str(page_count) + '.jpg', 'wb') as f:
                # print('正在下载第 ', (i + 1), ' 张图片中')
                print('正在下载', str(chapter_name), '- 第', page_count, '张图片')
                # 写入操作
                f.write(comic_pic)
                # 更改图片名,防止新下载的图片覆盖原图片
                i += 1
                page_count += 1

        # 若上述代码执行报错,则执行此部分代码
        except Exception as err:
            # 跳过错误代码
            print(err)
            pass


def get_xpath(chapter_address, xpath_str):
    req = request.Request(chapter_address, headers=headers)
    data = request.urlopen(req).read().decode("utf-8", "ignore")
    ht = etree.HTML(data)
    xpath_list = ht.xpath(xpath_str)
    return xpath_list


def get_page_link_list():
    data = open(chrome_cache_path + "comic.html", encoding='utf-8')
    html = data.read()
    selector = etree.HTML(html)
    page_link_list = []
    page_links = selector.xpath("//div[@class='page-links']/a/@href")
    # 返回的连接有两个重复的在头尾，要把它们去掉
    for link in page_links:
        if len(page_link_list) < len(page_links) - 1:
            page_link_list.append(link)

    page_link_list.remove(page_link_list[1])
    print(page_link_list)
    return page_link_list



def test():
    # 用beautifulsoup打开本地文件
    html_new = BeautifulSoup(open(chrome_cache_path + "comic.html", encoding='utf-8'), features='html.parser')
    data = open(chrome_cache_path + "comic.html", encoding='utf-8')
    html = data.read()
    selector = etree.HTML(html)
    page_link_list = selector.xpath("//div[@class='page-links']/a/@href")
    print(page_link_list)


if __name__ == '__main__':
    # get_page_link_list()
    # test()
    chapter_address = "http://www.177pic.pw/html/2020/11/3995720.html"
    link2 = "http://www.177pic.pw/html/2020/11/3905130.html"
    get_chapter(link2)

