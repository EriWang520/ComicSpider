import requests
from lxml import etree, html
from urllib import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import os


# 漫画首页地址
url = "http://pufei8.com/manhua/17"
url2 = "https://ac.qq.com/Comic/ComicInfo/id/635142"
url3 = "http://atharori.net/-20PUOJ/F5Bcu?rndad=2105100218-1606312793"
url4 = "http://www.177pic.pw/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

title_str = "//header[@class='entry-header']/h1/text()"
down_path = "D:/Program/spiderFile/down/comic/"
chrome_cache_path = "D:/Program/spiderFile/down/driverData/chromeCache/"
down_path_linux = "r'/home/ericw/down'"
webdriver_path_linux = "r'/home/ericw/chromedriver'"


def get_chapter(chapter):
    # chapter_url = url4 + str(chapter)
    page_name = get_xpath(chapter, title_str)
    # 以章节名命名文件夹
    print("以章节名命名文件夹")
    os.makedirs(down_path + str(page_name))

    # 设置谷歌无界面浏览器
    print("设置谷歌无界面浏览器")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    # webdriver位置
    # webdriver_path = "D:/Program/Chrome/Application/chromedriver_win32"
    # browser = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)
    browser = webdriver.Chrome(options=chrome_options)

    # 开始请求章节地址
    print("开始请求章节地址")
    browser.get(chapter)
    print("请求完成")

    # 设置延迟缓冲
    sleep(3)

    try:
        # 设置自动下滑滚动条操作
        for i in range(1, 100):
            # 滑动距离设置
            js = 'window.scrollTo(0,%s)' % (100 * i)
            # js = 'var q=document.getElementById("mainView").scrollTop = ' + str(i * 1000)
            # 执行滑动选项
            print("执行滑动选项")
            browser.execute_script(js)
            print("执行滑动选项完成", i)
            # 延时,使图片充分加载
            sleep(3)

        sleep(3)
        # 将打开的界面截图保存,证明无界面浏览器确实打开了网页
        print("正在保存打开的界面截图")
        browser.get_screenshot_as_file(chrome_cache_path + str(page_name) + ".png")
        # 获取当前页面源码
        print("获取当前页面源码")
        data = browser.page_source
        # 在当前文件夹下创建html文件,并将网页源码写入
        fh = open(chrome_cache_path + "dongman.html", "w", encoding="utf-8")
        # 写入操作
        fh.write(data)
        # 关掉无界面浏览器
        print("关掉无界面浏览器")
        fh.close()
        browser.quit()  # **************

        # 下面的操作为打开保存的html文件,提取其中的图片信息,并保存到文件夹中

        # 用beautifulsoup打开本地文件
        html_new = BeautifulSoup(open(chrome_cache_path + 'dongman.html', encoding='utf-8'), features='html.parser')
        # 提取html文件中的主体部分
        soup = html_new.find(id="mainView")
        # 设置变量i,方便为保存的图片命名
        i = 0

        # 提取出主体部分中的img标签（因为图片地址保存在img标签中）
        for items in soup.find_all("img"):
            # 提取图片地址信息
            print("提取图片地址信息")
            item = items.get("src")
            # 请求图片地址
            print("请求图片地址")
            comic_pic = requests.get(item).content
            try:
                # 打开文件夹,将图片存入
                with open(down_path + str(page_name) + '/' + str(i + 1) + '.jpg', 'wb') as f:
                    # print('正在下载第 ', (i + 1), ' 张图片中')
                    print('正在下载', str(page_name), '-', str(page_name), '- 第', (i + 1), '张图片')
                    # 写入操作
                    f.write(comic_pic)
                    # 更改图片名,防止新下载的图片覆盖原图片
                    i += 1
            # 若上述代码执行报错,则执行此部分代码
            except Exception as err:
                # 跳过错误代码
                pass
    # 若上述代码执行报错（大概率是由于付费漫画）,则执行此部分代码
    except Exception as err:
        # 跳过错误代码
        pass


def get_xpath(chapter_address, xpath_str):
    req = request.Request(chapter_address, headers=headers)
    data = request.urlopen(req).read().decode("utf-8", "ignore")
    ht = etree.HTML(data)
    xpath_list = ht.xpath(xpath_str)
    return xpath_list


if __name__ == '__main__':
    chapter = "http://www.177pic.pw/html/2020/11/3919568.html"
    get_chapter(chapter)