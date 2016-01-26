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


def GetPage(url, n):
	name = n
	# 三次url编码
	Url = url + urllib2.quote(urllib2.quote(urllib2.quote(name)))
	user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0'
	headers = {'User-Agent': user_agent}
	req = urllib2.Request(Url, headers=headers)
	page = urllib2.urlopen(req).read().decode('utf-8').encode('utf-8')
	soup = bs(page)
	#table = soup.table
	tag = soup.select('tr[logr]')
	path = 'c:/租房.csv'
	csvfile = file(path, 'ab+')
	writer = csv.writer(csvfile)
	if os.path.getsize(path) == 0:
		writer.writerow(['标题', '小区', '介绍', '总价'])

	for house in tag:
		#地区名或者小区名字

		title = house.select('.t').pop().get_text().strip()
		str = house.select('.qj-renaddr').pop().contents
		location = str[3].get_text() + str[5].get_text()
		location = location.strip()
		print location
		introduce = house.select('.showroom').pop().get_text().strip()
		#总价
		price = house.select('.pri').pop().get_text()

		if location.find(name) != -1:
			writer.writerow([title, location, introduce, price])

	print "[Result]:> 页面 信息保存完毕!"
	csvfile.close()


if __name__ == '__main__':
	for num in range(3):
		print num + 1
		GetPage(
			'http://hz.58.com/chuzu/pn' + str(
				num + 1) + '?final=1&PGTID=0d3090a7-0004-f334-5cb2-7ee681b87887&ClickID=1&searchtype=3&sourcetype=5&key=',
			'望江')
