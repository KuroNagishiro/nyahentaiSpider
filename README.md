# nyahentaiSpider （已失效）
nyahentai（喵绅士）本子爬取，以及随机爬取本子并发送至邮箱（可通过云函数实现定时发送）

## nyahentaiSpider

直接运行nyahentaiSpider.py即可，默认图片保存在D盘，有需要可自行更改

更改main()里面range的两个参数的值即可调节需要爬取的范围

更改main()里面的baseurl更改需要爬取的页面，例如可更改为其它标签页的网址满足自己xp来爬取含有特定tag的本子（）

因为页面有时候加载不出来导致连接超时出现异常，做过处理之后将会对超时的网址进行重试所以程序基本能一直跑下去不会中断

页面进行了懒加载src和data-src有时候对不上导致png格式的图片无法保存，不过大部分都是jpg所以可以保证绝大多数都可以保存，因为此情况发生较少所以遇到这种情况直接采用了跳过这张图片不进行保存来处理

## nyahentaiSpiderEmail

每次运行会从汉化页的第一页随机爬取一本发送至指定邮箱，利用云函数（有免费额度，个人使用完全足够）即可实现定时发送的功能。具体已经在[drinkEmail](https://github.com/KuroNagishiro/drinkEmail)中介绍过了
