# -*- codeing = utf-8 -*-
# 网页解析，获取数据
from bs4 import BeautifulSoup
# 正则表达式，进行文字匹配
import re
# 制定URL，获取网页数据
import urllib.request, urllib.error
from pathlib import Path
import os

# 正则表达式
# 本子链接
findLink = re.compile(r'<a class="cover target-by-blank" href="(.*?)"')
# 本子名字
findName = re.compile(r'<div class="caption">(.*?)<')
# 本子图片的url
findUrl = re.compile(r'<img alt=".*" class="list-img lazyload" data-src="(.*?)"')
# 本子的上传日期


# 爬取本子并保存到本地
def main():
    for i in range(1, 10):# range中两个数值决定需要爬取第几页到第几页
        i = str(i)
        print("准备开始爬取第" + i + "页")

        baseurl = "https://zha.qqhentai.com/language/chinese/page/"# 在这里更改爬取的页面

        baseurl = baseurl + i
        print("准备开始爬取的页面网址：" + baseurl)

        datalists = getData(baseurl)  # 爬取网页

        for data in datalists:
            saveImg2(data)

# 爬取网页
def getData(baseurl):
    # 用于存放每本本子
    datalist = []
    # 获取html中的内容
    url = baseurl
    print("主页加载中...")
    html = askURL(url)
    print("加载主页成功...")

    # 解析数据
    soup = BeautifulSoup(html, "html.parser")
    soupData = soup.findAll('div', class_="gallery")

    for item in soupData:  # 遍历每一个本子的链接和名字
        data = []
        item = str(item)

        # 本子的链接
        baselink = re.findall(findLink, item)[0]
        link = 'https://zha.qqhentai.com' + baselink + 'list2/'
        data.append(link)

        # 本子的名字
        name = re.findall(findName, item)
        data.append(name)

        datalist.append(data)  # 将本子存入
    print("本页本子信息爬取成功")
    return datalist


# 得到指定的一个url网页的数据
def askURL(url):
    # 模拟浏览器头部信息，向服务器发送消息
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Referer": "https://zha.qqhentai.com/"
            }
    request = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(request, timeout=15)
        html = response.read().decode("utf-8")
    except Exception as e:
        print("连接超时，重试...")
        html = askURL(url)

    return html


def saveImg2(data):
    url = data[0]
    name = data[1][0]
    name = nameCheck(name)
    print("准备开始保存：" + name)

    count = int(0)
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Referer": "https://zha.qqhentai.com/"
            }

    savepath = "D://本子//" + name

    my_file = Path(savepath)  # 用于判断文件夹是否存在

    if my_file.exists():
        print("本子已存在,不保存")
    else:
        print("本子不存在，创建文件夹")
        os.mkdir(savepath)

        print("打开本子页中...")
        html = askURL(url)

        print("准备开始获取本子图片的所有的url")
        mangaSoup = BeautifulSoup(html, "html.parser")
        # 通过遍历获取该本子所有的图片url，每次循环获取一张
        for manga in mangaSoup.findAll(class_="list-img lazyload"):
            manga = str(manga)

            count = int(count) + 1
            count = str(count)

            mangaUrl = re.findall(findUrl, manga)[0]

            saveImg3(mangaUrl, count, savepath, head)

        print(name + "保存成功")

# 将图片保存到本地
def saveImg3(mangaUrl, count, savepath, head):
    request = urllib.request.Request(mangaUrl, headers=head)
    try:
        response = urllib.request.urlopen(request)
        content = response.read()

        filename = count + ".jpg"
        filename = savepath + "//" + filename
        with open(filename, "wb") as f:
            f.write(content)
            response.close()
        print("正在保存：" + mangaUrl)
        print("保存完成第" + count + "张")
    except urllib.error.URLError as e:
        print("png图片,跳过")
        pass
    except Exception as e:
        print("图片保存发生错误，跳过")
        pass
    except ConnectionResetError as e:
        saveImg3(mangaUrl, count, savepath, head)


def nameCheck(name):
    name = name.replace("/", "")
    name = name.replace("\\", "")
    name = name.replace(":", "")
    name = name.replace("?", "")
    name = name.replace("*", "")
    name = name.replace("\"", "")
    name = name.replace("<", "")
    name = name.replace(">", "")
    return name


if __name__ == '__main__':
    main()
    print("爬取完毕")
