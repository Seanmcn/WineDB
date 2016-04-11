# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Wine, History


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('url', 'wine_count', 'date')
    list_filter = ['wine_count']
    search_fields = ['url']


def set_deleted(modeladmin, request, queryset):
    queryset.update(deleted='Red')


def set_color_red(modeladmin, request, queryset):
    queryset.update(color='Red')


def set_color_white(modeladmin, request, queryset):
    queryset.update(color='White')


def set_color_rose(modeladmin, request, queryset):
    queryset.update(color='Rosé')


def set_color_orange(modeladmin, request, queryset):
    queryset.update(color='Orange')


def set_not_a_wine(modeladmin, request, queryset):
    queryset.update(is_wine=False)


set_deleted.short_description = "Delete selected wines"
set_color_red.short_description = "Mark selected wines as Red"
set_color_white.short_description = "Mark selected wines as White"
set_color_rose.short_description = "Mark selected wines as Rosé"
set_color_orange.short_description = "Mark selected wines as Orange"
set_not_a_wine.short_description = "Mark selected records as not being wine!"


class WineAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'variety', 'region', 'sub_region', 'vintage', 'price')
    list_filter = ['color', 'variety', 'region', 'sub_region', 'vintage']
    search_fields = ['name', 'price', 'vintage', 'region', 'sub_region']
    actions = [set_deleted, set_color_red, set_color_white, set_color_rose, set_color_orange, set_not_a_wine]

    def get_actions(self, request):
        # Disable delete
        actions = super(WineAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ("was_modified",)
        form = super(WineAdmin, self).get_form(request, obj, **kwargs)
        return form

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Wine, WineAdmin)
admin.site.register(History, HistoryAdmin)
