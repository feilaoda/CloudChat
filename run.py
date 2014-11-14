
import os
import sys
import datetime
import logging

logging.basicConfig(format='%(levelname)s:%(thread)d:%(message)s', level=logging.DEBUG)


PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]
try:
    # 
    import site
    site.addsitedir(ROOTDIR)
except ImportError:
    print('Development of keepcd')


import settings

from scheduler.hackernews import run as hackernews_run
from scheduler.producthunt_api import run as producthunt_run
from scheduler.designernews import run as designernews_run


from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

now = datetime.datetime.utcnow()
scheduler.add_job(hackernews_run,'interval', minutes=10,  id='hackernews', next_run_time=now)
scheduler.add_job(producthunt_run,'interval', minutes=10,  id='producthunt', next_run_time=now)
scheduler.add_job(designernews_run,'interval', minutes=10,  id='producthunt', next_run_time=now)
scheduler.start()

# hackernews_run()
# producthunt_run()
designernews_run()
