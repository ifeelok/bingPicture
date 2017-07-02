# -*- coding: utf-8 -*-
import scrapy
import re
from bing.items import BingItem
import sys
import pymysql


class PictureSpider(scrapy.Spider):
    name = 'picture'
    allowed_domains = ['bing.ioliu.cn']
    url = 'https://bing.ioliu.cn'
    client = pymysql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            password = 'lyd0319!',
            db = 'bing',
            charset='utf8'
        )

    def start_requests(self):
        for i in range(1, 2):
            yield scrapy.Request(self.url+ '/?p=' +str(i), callback=self.parse, )

    def parse(self, response):
        items = response.css('.container .item .card')
        for item in items:
            pic = BingItem()
            pic_description = item.css('.description h3::text').extract_first()
            pic_time = item.css('.description .calendar em::text').extract_first()
            pic_location = item.css('.description .location em::text').extract_first()
            temp_href = item.css('div.options a::attr(href)').extract_first()
            pic_name = re.search('(.+)\?force=download', temp_href.split('/')[-1]).group(1)
            pic_href = self.url + temp_href

            pic['name'] = pic_name
            pic['description'] = pic_description
            pic['time'] = pic_time
            pic['location'] = pic_location
            pic['href'] = pic_href

            for key,value in pic.items():
                if value:
                    pic[key] = value.encode('utf-8')

            sql = 'SELECT * FROM picture WHERE name="{}"'.format(pic['name'])
            cursor = self.client.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            # 该图片已经存在，则停止运行
            if len(result):
                sys.exit()
            pic['file_urls'] = [pic_href]

            yield pic

