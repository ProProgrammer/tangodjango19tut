from django.contrib import admin

from rango.models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
    def page_count(self, obj):
        return obj.page_set.count()

    list_display = ['name', 'page_count', 'views', 'likes']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
