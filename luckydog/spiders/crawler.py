# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from luckydog.items import LuckydogItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LuckydogSpider(CrawlSpider):
	name = 'luckydog'
	#allowed_domains = ["dmoz.org"]
	start_urls = [
		'https://www.luckydog.tw/view/家電/all/page1',
		'https://www.luckydog.tw/view/3C/all/page1',
	]
	rules = [
		Rule(LinkExtractor(allow=('/view/家電/all/page\d*')), callback='parse_list', follow=True),
		Rule(LinkExtractor(allow=('/view/3C/all/page\d*')), callback='parse_list', follow=True),

	]
	#domain = 'https://www.luckydog.tw'
	def parse_list(self, response):
		self.logger.info('info on %s', response.url)
		print 'crawled',response.url
		soup = BeautifulSoup(response.body)
		#print response.body
		domain = 'https://www.luckydog.tw'
		for link in soup.select('.news-content'):
			try:
				link = domain + link.select('a')[0]['href']
				#print link
				yield scrapy.Request(link,self.parse_detail)
			except:
				continue

	def parse_detail(self, response):
		soup = BeautifulSoup(response.body)
		item = LuckydogItem()
		item['title'] = soup.select('#title a')[0].text
		item['luckydog_link'] = response.url
		item['fb_link'] = soup.select('#title a')[0]['href']
		item['deadline'] = soup.select('.event-content div div')[2].text
		item['is_solved'] = False
		item['is_followed'] = False
		return item
		