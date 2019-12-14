# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutofarbaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    data = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    image = scrapy.Field()


class VaitItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    data = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()

