# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # images1 = scrapy.Field()  # 图片的链接
    # images2 = scrapy.Field()  # 图片的链接

    image_urls = scrapy.Field()
    # images = scrapy.Field()
    # print("---ScrapyspiderItem",str(scrapy))
    # print("---image_urls", image_urls)
