# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleItem(scrapy.Item):
 	description = scrapy.Field()
 	downloadsNumber = scrapy.Field()
 	name = scrapy.Field()
 	reviewNumber = scrapy.Field()
 	ratingValue = scrapy.Field()
 	price = scrapy.Field()
 	currentVersion = scrapy.Field()
 	author = scrapy.Field()
