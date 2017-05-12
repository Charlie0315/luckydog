import scrapy


class LuckydogItem(scrapy.Item):
	title = scrapy.Field()
	luckydog_link = scrapy.Field()
	fb_link = scrapy.Field()
	deadline = scrapy.Field()
	is_solved = scrapy.Field()
	is_followed = scrapy.Field()
