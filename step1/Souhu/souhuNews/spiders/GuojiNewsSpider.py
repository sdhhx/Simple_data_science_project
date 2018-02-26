# -*- coding: utf-8 -*-

import scrapy
from souhuNews.items import SouhunewsItem

class souhuNewsSpider(scrapy.Spider):
	name = 'souhuGuoji'

	start_urls = ['http://news.sohu.com/guojixinwen.shtml']

	def parse(self, response):
		yield scrapy.Request(response.url, callback=self.parse_url)
		for i in range(1,100):
			url = "http://news.sohu.com/guojixinwen_" + str(6819-i) + ".shtml"
			print "当前url为: " + url
			yield scrapy.Request(url, callback=self.parse_url)

	def parse_url(self, response):
		for url in response.xpath('//div[@class = "article"]/p/a/@href').extract():
			yield scrapy.Request(url, callback=self.parse_news)

	def parse_news(self, response):
		newstype = u"国际"
		item = SouhunewsItem()
		item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
		item['publisher'] = response.xpath('//span[@id="media_span"]/span/text()').extract_first()
		item['type'] = newstype
		item['time'] = response.xpath('//div[@class="time"]/text()').extract_first()
		item['content'] = "\n".join(response.xpath('//div[@itemprop="articleBody"]/p/text()').extract())
		if not item['content']:
			item['content'] = "\n".join(response.xpath('//div[@itemprop="articleBody"]/text()').extract())
		print item['title']
		print item['publisher']
		print item['type']
		print item['time']
		print item['content']
		print isinstance(item['content'], unicode)
		yield item
