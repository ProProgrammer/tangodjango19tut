from django.contrib import admin

from rango.models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
    def page_count(self, obj):
        return obj.page_set.count()

    list_display = ['name', 'page_count', 'views', 'likes']

    """
    We have a problem with slug field being user editable and not pre-populated.
    Currently when creating a new category, say "Python User Groups" Django will not let you save it unless you fill
    in the slug field too.
    While we could type in python-user-groups this is error prone.
    It would be better to have the slug automatically generated

    (Another way would have been to set blank=True on slug field as:
    slug = models.SlugField(blank=True
    But this is not a good idea either)

    Lets customize the admin interface so that it automatically pre-populates the slug field as you type in the
    category name
    """
    prepopulated_fields = {'slug': ('name', )}


class PageAdmin(admin.ModelAdmin):
    def page_url(self, obj):
        return obj.url

    page_url.short_description = 'URL'
    list_display = ['title', 'category', 'page_url', 'views']
    list_filter = ['category']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
