# !/usr/bin/env python
# -*-coding: utf-8 -*-
import re
import urllib2
from bs4 import BeautifulSoup as bs
import csv
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def GetPage(url):
	Url = url
	user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0'
	headers = {'User-Agent': user_agent}
	req = urllib2.Request(Url, headers=headers)
	page = urllib2.urlopen(req).read().decode('utf-8').encode('utf-8')
	soup = bs(page)
	#table = soup.table
	tag = soup.select('tr[logr]')
	path = 'c:/jin.csv'
	csvfile = file(path, 'ab+')
	writer = csv.writer(csvfile)
	if os.path.getsize(path) == 0:
		writer.writerow(['标题', '小区', '介绍', '总价', '单价', '单价（去中文）'])
	

	for house in tag:
		title = house.select('.t').pop().get_text().strip()
		str = house.select('.qj-listleft').pop().contents
		location = str[5].get_text()+str[6]
		location = location.strip()
		introduce = ''.join([i+' ' for i in house.select('.qj-listleft').pop().get_text().split()])
		#总价
		price = house.select('.pri').pop().get_text()
		#单价
		price1 = house.select('.qj-listright').pop().contents[2].split().pop()
		price2 = None
		if price1.find(u'元') != -1:
			price2 = price1[:price1.find(u'元')]
		if len(location) < 10 and location.find('金城花苑') != -1:
			writer.writerow([title, location, introduce, price + '', price1, price2])

	print "[Result]:> 页面 信息保存完毕!"
	csvfile.close()


if __name__ == '__main__':
	for num in range(20):
		print num+1
		GetPage(
		'http://xx.58.com/jiaochengqu/ershoufang/pn'+str(num+1)+'/?key=%E9%87%91%E5%9F%8E%E8%8A%B1%E8%8B%91&PGTID=0d30000c-01f1-05eb-7f2b-f1ab4b902008&ClickID=1')
