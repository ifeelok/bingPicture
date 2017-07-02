# -*- coding: utf-8 -*-
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import pymysql
import os
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BingPipeline(object):
    def __init__(self, host, dbname, user, passwd):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.passwd = passwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            dbname = crawler.settings.get('MYSQL_DBNAME'),
            user = crawler.settings.get('MYSQL_USER'),
            passwd = crawler.settings.get('MYSQL_PASSWD')
        )

    def open_spider(self, spider):
        self.client = pymysql.connect(
            host = self.host,
            port = 3306,
            user = self.user,
            password = self.passwd,
            db = self.dbname,
            charset='utf8'
        )

    # def close_spider(self, spider):
    #     self.client.close()

    def process_item(self, item, spider):
        sql = 'INSERT INTO picture VALUES ("{}", "{}", "{}", "{}", "{}")'\
            .format(item['name'], item['description'], item['time'], item['location'], item['href'])
        self.client.cursor().execute(sql)
        self.client.commit()
        return item

class SavePicturePipeline(FilesPipeline):

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        print image_paths[0], 'full/'+item['name']+'.jpg'
        os.rename('D:/files/'+image_paths[0], 'C:/Users/lydon/Pictures/bing/'+item['name']+'.jpg')
        return item

