# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    bookid = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    image = scrapy.Field()

    isbn13 = scrapy.Field()
    publisher = scrapy.Field()
    pubdate = scrapy.Field()
    price = scrapy.Field()
    pages = scrapy.Field()
    translator = scrapy.Field()
    summary = scrapy.Field()
    #catalog = scrapy.Field()
    lookcount = scrapy.Field()
    pass
