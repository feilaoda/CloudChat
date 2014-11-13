
import os
import sys


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
from scheduler.producthunt import run as producthunt_run



hackernews_run()
producthunt_run()

