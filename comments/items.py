# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # zone, name, title, status tag, ctype, content, postTime, reply, replyTime
    
    zone = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    tag = scrapy.Field()
    ctype = scrapy.Field()
    content = scrapy.Field()
    posttime = scrapy.Field()
    reply = scrapy.Field()
    replyTime = scrapy.Field()
