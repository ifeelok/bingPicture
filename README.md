## 项目描述
使用`Scrapy`爬取[必应壁纸](https://bing.ioliu.cn)的图片，保存相关信息到`MySQL`数据库。增量爬取。

## 再描述

最近想换电脑壁纸，但是没有找到好看的，逛知乎看到了`(https://bing.ioliu.cn)`，看到是高清图片，挺不错的，但是一张一张下载太慢了就想写个爬虫，一下子全爬下来。爬取完成之后才知道，这个网站本来就是别人从`cn.bing.com`爬取的，好吧，二次工作。原作者也有一个项目，还提供了接口。请看这里[简介](https://bing.ioliu.cn/static/about.html)，项目[地址](https://github.com/xCss/bing)。

## 工具

- `Scrapy`
- `MySQL`

## 技术含量

- 简单
- 一天即可完工

## 使用方法
- 更改一下`settings.py`和`spiders/picture.py`里面的`passwd`即可
- 执行`scrapy crawl picture`