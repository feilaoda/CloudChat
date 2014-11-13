
import json
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
import settings


engine = create_engine(settings.database)

session = sessionmaker()
session.configure(bind=engine)


Base = declarative_base()

pool = redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port)
client =  redis.Redis(connection_pool=pool)


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    site = Column(String)
    title = Column(String)
    sub_title = Column(String)
    source_url = Column(String)
    url = Column(String)
    vote_count = Column(Integer)
    comment_count = Column(Integer)
    create_at = Column(DateTime, default=func.now())

def delete_news(site_id):
	db = session()
	db.execute("delete from news where site = '%s'"%site_id)
	db.commit()

def save_news(site,news_list, page):
	db = session()
	for item in news_list:
		news = News()
		news.site = item['site']
		news.title = item['title']
		news.sub_title = item.get('subTitle')
		news.source_url = item['sourceUrl']
		news.url = item['url']
		news.vote_count = item['voteCount']
		news.comment_count = item['commentCount']
		db.add(news)
	db.commit()
	
	return len(news_list)

def save_cache(site, news_list):
	size = len(news_list)
	i=0
	p = 1
	while i<size:
		if i+30 >= size:
			slide = news_list[i:]
		else:
			slide = news_list[i:i+30]
		res = json.dumps(slide)
		client.set('news:'+site+":"+str(p), res)
		p=p+1
		i=i+30
	key = 'news:'+site+":count"
	client.set(key, size)


