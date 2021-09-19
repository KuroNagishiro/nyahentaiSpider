# -*- codeing = utf-8 -*-
# 网页解析，获取数据
from bs4 import BeautifulSoup
# 正则表达式，进行文字匹配
import re
# 制定URL，获取网页数据
import urllib.request, urllib.error
# 进行excel操作
import xlwt
import random
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header

# 本程序爬取汉化第一页的25本并随机抽取一本发送至指定邮箱


# 正则表达式
# 本子链接
findLink = re.compile(r'<a class="cover target-by-blank" href="(.*?)"')
# 本子名字
findName = re.compile(r'<div class="caption">(.*?)<')
# 本子图片的url
findUrl = re.compile(r'<img alt=".*" class="list-img lazyload" data-src="(.*?)"')


# findUrl = re.compile(r'<img class="list-img lazyload" src="(.*?)" data-src="')


# 该程序可获取nyahentai汉化漫画页的第一页的25本，并通过邮件随机发送一本至指定邮箱
def main():
    baseurl = "https://zha.qqhentai.com/language/chinese/"

    datalist = getData(baseurl)  # 爬取网页
    print("返回成功，准备打印")

    emailSend(datalist)  # 发邮件


# 爬取网页
def getData(baseurl):
    # 用于存放每本本子
    datalist = []
    # 用于存放其中某一个本子的图片的url
    imgData = []
    # 1.获取html中的内容
    url = baseurl
    print("主页加载中...")
    html = askURL(url)
    print("加载主页成功...")

    # 2.解析数据
    soup = BeautifulSoup(html, "html.parser")
    soupDatas = soup.findAll('div', class_="gallery")
    ranNum = random.randint(0, len(soupDatas) - 1)  # 生成随机数
    print("获取第一页的第" + str(ranNum + 1) + "本")
    soupData = soupDatas[ranNum]  # 取出每一个本子的链接和名字
    soupData = str(soupData)
    data = []

    # 本子的链接
    link = re.findall(findLink, soupData)[0]
    link = 'https://zha.qqhentai.com' + link + 'list2/'
    data.append(link)

    # 本子的名字
    name = re.findall(findName, soupData)
    data.append(name)

    # 打开本子的链接从里面取出图片的url
    print("获取图片url中...")
    html = askURL(link)
    print("图片url获取成功...")
    mangaSoup = BeautifulSoup(html, "html.parser")
    for manga in mangaSoup.findAll(class_="list-img lazyload"):
        manga = str(manga)
        # 通过遍历获取该本子所有的图片url
        mangaUrl = re.findall(findUrl, manga)[0]

        imgData.append(mangaUrl)  # 将图片的url存入

    data.append(imgData)  # 将本子的图片存入

    datalist.append(data)  # 将本子存入
    print("成功，准备返回")
    return datalist


# 得到指定的一个url网页的数据
def askURL(url):
    # 模拟浏览器头部信息，向服务器发送消息
    # head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"}
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Referer": "https://zha.qqhentai.com/"
            }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request, timeout=7)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e.reason):
            print(e.reason)
    return html


# 发送邮件
def emailSend(datalist):
    data = datalist[0]
    imgData = data[2]
    name = str(data[1])
    print("本子名：" + name)
    imgUrl = ""
    for i in imgData:
        i = str(i)
        imgUrl1 = '<img src="' + i + '" height="100%"></br>'
        imgUrl = imgUrl + imgUrl1

    # 发送的内容
    mail_msg = """
        <h2 style="color:#f00">手冲时间到啦</h2></br>
        """ + imgUrl

    message = MIMEText(mail_msg, 'html', 'utf-8')

    message['From'] = Header("提醒手冲机器人", 'utf-8')

    message['To'] = Header("开冲", 'utf-8')

    subject = name
    message['Subject'] = Header(subject, 'utf-8')

    # 发件人
    sender = 'xxx@qq.com'

    # 收件人可以多位，每个收件人用 , 隔开，最后一位后面不需要逗号
    receiver = [
        'xxx@qq.com'
    ]

    smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 此处使用的是qq的smtp服务发送邮件
    smtpObj.login(sender, "xxxxx")  # 此处填入获取到发件人邮箱的授权码
    smtpObj.sendmail(sender, receiver, message.as_string())
    smtpObj.quit()

    print("邮件发送成功")


if __name__ == '__main__':
    main()
    print("完毕")
