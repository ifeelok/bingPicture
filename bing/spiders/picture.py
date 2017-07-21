# -*- coding: utf-8 -*-
import re

import pymysql
import scrapy

from bing.items import BingItem


class PictureSpider(scrapy.Spider):
    name = 'picture'
    allowed_domains = ['bing.ioliu.cn']
    url = 'https://bing.ioliu.cn'
    client = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='lyd0319!',
        db='bing',
        charset='utf8'
    )

    def start_requests(self):
        for i in range(1, 42):
            yield scrapy.Request(self.url + '/?p=' + str(i), meta={'page': str(i)}, callback=self.parse, )

    def parse(self, response):
        page = response.meta.get('page')
        items = response.css('.container .item .card')
        for item in items:
            pic = BingItem()
            pic_title = item.css('.description h3::text').extract_first()
            pic_time = item.css('.description .calendar em::text').extract_first()
            pic_location = item.css('.description .location em::text').extract_first()
            temp_href = item.css('div.options a::attr(href)').extract_first()
            pic_name = re.search('(.+)\?force=download', temp_href.split('/')[-1]).group(1)
            pic_href = self.url + temp_href

            pic['name'] = pic_name
            pic['title'] = pic_title
            pic['time'] = pic_time
            pic['location'] = pic_location
            pic['href'] = pic_href

            for key, value in pic.items():
                if value:
                    pic[key] = value.encode('utf-8')
            pic['name'] = pic['time'] + '-' + pic['name'].split('_')[0]

            sql = 'SELECT * FROM picture WHERE name="{}"'.format(pic['name'])
            cursor = self.client.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            # 该图片已经存在，则停止运行
            if not len(result):
                pic['file_urls'] = [pic_href]
                yield scrapy.Request(url=self.url+'/photo/'+pic_name+'?force=home_'+page, callback=self.parse_detail, meta=pic)

    def parse_detail(self, response):
        pic = response.meta
        pic['detail'] = response.css('.description .sub::text').extract_first().encode('utf-8')
        yield pic
