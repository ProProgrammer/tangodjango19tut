from django.conf.urls import url
from rango import views

app_name = 'rango'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),

    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),

    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),

    url(r'^register/$', views.register, name='register'),

    url(r'^login/$', views.user_login, name='login'),

    url(r'^restricted/$', views.restricted, name='restricted'),

    url(r'^logout/$', views.user_logout, name='logout'),
]
"""
We have added a rather complex entry that will invoke view.show_category() when the URL pattern r'^category/(
P<category_name_slug>[\w\-]+)/$' is matched.

There are two things to note here.
First we have added a parameter name within the URL pattern, i.e. <category_name_slug>, which we will be able to
access in our view later on. When you create a parameterized URL you need to ensure that the parameters that you
include in the URL are declared in the corresponding view.

Using parentheses around a pattern "captures" the text matched by that pattern and sends it as an argument to the
view function; ?P<category_name_slug> defines the name that will be used to identify the matched pattern.

Also [0-9]+ is a regular expression to match a sequence of digits (i.e., a number).

The next thing to note is that the regular expression [\w\-]+) will look for any sequence of alphanumeric characters
e.g. a-z, A-Z or 0-9 denoted by \w and any hyphens (-) denoted by \-, and we can match as many of these as we link
denoted by the [ ]+ expression.

The URL pattern will match a sequence of alphanumeric characters and hyphens which are between the /rango/category
and the trailing /. This sequence will be stored in the parameter category_name_slug and passed to
view.show_category().

For example, the URL rango/category/python-books/ would result in the category_name_slug having the value,
python-books. However if the URL was rango/category/python_books or rango/category/$$$$$-$$$$$/ then the sequence of
characters between rango/category and the trailing / would not match the regular expressions and a 404 Not Found
error would result because there would be no matching URL pattern
"""
