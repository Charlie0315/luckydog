# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
class LuckydogPipeline(object):
	def open_spider(self, spider):
		self.conn = sqlite3.connect('luckydog.sqlite')
		self.cur = self.conn.cursor()
		self.cur.execute('create table if not exists luckydog(fb_link varchar(100) primary key not null, title varchar(100), luckydog_link varchar(100), deadline varchar(20), is_solved boolean, is_followed boolean);')

	def close_spider(self, spider):
		self.conn.commit()
		self.conn.close()

	def process_item(self, item, spider):
		col = ','.join(item.keys())
		placeholders = ','.join(len(item) * '?')
		sql = 'insert into luckydog({}) values({})'
		try: self.cur.execute(sql.format(col,placeholders), item.values())
		except: pass
		return item
