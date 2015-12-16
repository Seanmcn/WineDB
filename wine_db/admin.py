from django.contrib import admin
from .models import Wine, History


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('url', 'wine_count', 'date')
    list_filter = ['wine_count']
    search_fields = ['url']


class WineAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'variety', 'region', 'sub_region', 'vintage', 'price')
    list_filter = ['color', 'variety', 'region', 'sub_region',  'vintage']
    search_fields = ['name', 'price', 'vintage', 'region', 'sub_region']

admin.site.register(Wine, WineAdmin)
admin.site.register(History, HistoryAdmin)
