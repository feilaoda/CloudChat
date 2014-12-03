from django.db import models


class NewsSite(models.Model):
    # id = models.IntegerField(default=0)
    uri = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=255, default=None, blank=True)
    sorts = models.IntegerField(default=0)
    domain = models.CharField(max_length=200, default=None, blank=True)
    author = models.CharField(max_length=200, default=None, blank=True)
    bg_color = models.CharField(max_length=200, default=None, blank=True)
    status = models.IntegerField(default=0)
    show_votes = models.IntegerField(default=0)
    show_comments = models.IntegerField(default=0)

    class Meta:
        db_table = "news_site"

    def __unicode__(self):              # __unicode__ on Python 2
        return "%s - %s - %s" %(self.name , self.title, self.domain)