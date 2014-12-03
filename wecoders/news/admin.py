from django.contrib import admin

# Register your models here.
from models import NewsSite

class NewsSiteAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(NewsSite, NewsSiteAdmin)

