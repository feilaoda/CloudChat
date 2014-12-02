import os
import feedparser
import re
import time
from datetime import datetime

from news import session, delete_news,save_news,save_cache, update_sites,reset_news

from settings import load_config

def fetch_feed(site, url, id_pattern=None):
	print "fetch %s"%site
	feed = feedparser.parse(url)
	news_list = []
	for entry in feed['entries']:
		#print entry.keys()
		#print entry['id'], entry['published_parsed'], type(entry['published_parsed']),datetime.fromtimestamp(time.mktime(entry['published_parsed']))

		news = dict()
		# if id_pattern:
		# 	m = re.findall(id_pattern, entry['link'])
		# 	if len(m)>0:
		# 		news['newsId'] = m[0]
		# 		print m[0]
		# 	else:
		# 		news['newsId'] = entry['link']
		if entry.has_key('id'):
			news['newsId'] = entry['id']
		else:
			news['newsId'] = entry['link']
		news['site'] = site
		news['title'] = entry['title']
		news['subTitle'] = None
		news['sourceUrl'] = entry['link']
		news['voteCount'] = 0
		news['commentCount'] = 0
		news['url'] = entry['link']
		news['sorts'] = int(time.mktime(entry['published_parsed']))
		news['createAt'] = datetime.fromtimestamp(time.mktime(entry['published_parsed']))
		news_list.append(news)
	save_news(site, news_list)

def run():
	config = load_config("rss.yaml")
	for site in config.sites:
		fetch_feed(site.name, site.feed)	


