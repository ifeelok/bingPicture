# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    detail = scrapy.Field()
    time = scrapy.Field()
    location = scrapy.Field()
    href = scrapy.Field()
    file_urls = scrapy.Field()
