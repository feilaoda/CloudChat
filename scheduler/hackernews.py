
#https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty
import json
import requests
import re
from scrapy import Selector

from news import session, delete_news,save_news,save_cache

hackernews_url = 'https://news.ycombinator.com/news'

Site="HackerNews"

def fetch(url):
	response = requests.get(url, timeout=60)
	if response.status_code != requests.codes.ok:
	    return dict(code=response.status_code)
	return dict(code=200, html=response.text)


def fetch_news(url, page):
	res = fetch(url)
	if res['code'] != 200:
		return []
	html = res['html']
	print html
	hxs = Selector(text=html)
	trs = hxs.xpath('//body/center/table/tr[3]/td/table/tr')
	cnt = len(trs)
	i=0
	print "count:",cnt
	news_list = []
	while i<cnt:
		tr0 = trs[i]
		source_link = tr0.xpath('./td[@class="title"]/a/@href').extract()
		title = tr0.xpath('./td[@class="title"]/a/text()').extract()
		sub_title = tr0.xpath('./td[@class="title"]/span[@class="comhead"]/text()').extract()
		
		tr1 = trs[i+1]
		points = tr1.xpath('./td[@class="subtext"]/span/text()').extract()
		comments = tr1.xpath('./td[@class="subtext"]/a/text()').extract()
		comments_link = tr1.xpath('./td[@class="subtext"]/a/@href').extract()
		if len(source_link) > 0:
			source_link = source_link[0]
		else:
			source_link=None
		if len(title)>0:
			title = title[0]
		else:
			title = None

		if len(sub_title)>0:
			sub_title = sub_title[0]
		else:
			sub_title = None

		if len(points)>0:
			m = re.findall('(\d+)', points[0])
			if len(m)>0:
				points = m[0]
			else:
				points = 0
		else:
			points = 0

		if len(comments)>1:
			m = re.findall('(\d+)', comments[1])
			if len(m)>0:
				comments = m[0]
			else:
				comments = 0
		else:
			comments = 0
		nid = None
		if len(comments_link)>1:
			m = re.findall('item\?id=(\d+)', comments_link[1])
			if len(m)>0:
				nid = m[0]
		if nid is None and len(comments_link)>0:
			m = re.findall('item\?id=(\d+)', comments_link[0])
			if len(m)>0:
				nid = m[0]
		if nid is None:
			news_link = source_link
		else:
			news_link = "https://news.ycombinator.com/item?id=%s"%(nid)

		if title is None:
			i+=3
			continue

		news = dict()
		news['site'] = Site
		news['title'] = title
		news['subTitle']  = sub_title
		news['sourceUrl'] = source_link
		news['voteCount'] = points
		news['commentCount'] = comments
		news['url'] = news_link
		# print link, title, points, comments, news_link
		print news
		news_list.append(news)
		i+=3

	save_news(Site,news_list,page)
	return news_list

def run():
	delete_news(Site)
	news = []
	lst = fetch_news("https://news.ycombinator.com/news", 1)
	if lst is not None:
		news.extend(lst)
	lst = fetch_news("https://news.ycombinator.com/news?p=2", 2)
	if lst is not None:
		news.extend(lst)
	lst = fetch_news("https://news.ycombinator.com/news?p=3", 3)
	if lst is not None:
		news.extend(lst)

	save_cache(Site, news)

