from django.contrib import admin

from rango.models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
    def page_count(self, obj):
        return obj.page_set.count()

    list_display = ['name', 'page_count', 'views', 'likes']


class PageAdmin(admin.ModelAdmin):
    def page_url(self, obj):
        return obj.url

    page_url.short_description = 'URL'
    list_display = ['title', 'category', 'page_url']
    list_filter = ['category']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
