from django.contrib import admin
from .models import Wines, History


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('url', 'wine_count', 'date')
    list_filter = ['wine_count']
    search_fields = ['url']


class WinesAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'grape', 'rating', 'date')
    list_filter = ['color', 'grape', 'rating']
    search_fields = ['name', 'color', 'grape']

admin.site.register(Wines, WinesAdmin)
admin.site.register(History, HistoryAdmin)
