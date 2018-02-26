# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class QQnewsItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	title = scrapy.Field()
	newstype = scrapy.Field()
	publisher = scrapy.Field()
	time = scrapy.Field()
	content = scrapy.Field()

