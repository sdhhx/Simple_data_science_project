#-*- coding:utf-8 -*-
import scrapy
from QQNews.items import QQnewsItem
import urlparse
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import choice

class QQNewsSpider(scrapy.Spider):
	name = "QQNewsSpider"
	allowed_domains = ["news.qq.com"]
	start_urls = ['http://roll.news.qq.com/']

	def parse(self, response):
		driver = webdriver.Chrome()
		driver.get(response.url)
		driver.implicitly_wait(1)
		try:
			refresh = driver.find_element_by_xpath("//div[@class='Refresh']/a[1]")
			refresh.click()
		except:
			print "Close AutoRefresh Fail"
		maxpage = int(driver.find_element_by_xpath("//div[@id='pageArea']/a[last()-1]").text)
		url_set = set()

		print u"****************收集URL中****************"

		for i in range(1, maxpage + 1):
			time.sleep(1)
			sel_list = driver.find_elements_by_xpath("//div[@class='list c']/ul/li/a")
			url_list = [sel.get_attribute("href") for sel in sel_list]  
			url_set |= set(url_list)
			try:
				driver.implicitly_wait(1)
				time.sleep(2)
				
				element = driver.find_element_by_xpath("//div[@id='pageArea']/a[last()]")
				element.click()
			except:
				print "get QQNews nextPage failed"

		print u"****************开始爬取****************"
		for url in url_set:
			print url
			yield scrapy.Request(url, callback=self.parse_content)  

	def parse_content(self, response):
		title = response.xpath("//div[@class='qq_article']/div[@class='hd']/h1/text()").extract_first()
		if title:
			item = QQnewsItem()
			item["title"] = title
			item["newstype"] = response.xpath("//span[@class='a_catalog']/a/text()").extract_first()
			item["publisher"] = response.xpath("//span[@class='a_source']/a/text()").extract_first()
			item["time"] = response.xpath("//span[@class='a_time']/text()").extract_first()
			item["content"] = "\n".join(response.xpath("//div[@id='Cnt-Main-Article-QQ']/p/text()").extract())
			yield item