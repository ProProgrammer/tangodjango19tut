import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_django_project.settings')

import django
django.setup()
from rango.models import Category, Page


def populate():
    # First we will create a list of dictionaries containing the pages we want to add into each category
    # The we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing but it allows us to iterate through each data structure, and add the
    # data to our models

    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/2/tutorial/'},
        {'title': 'How to think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/'},
        {'title': 'Learn Python in 10 minutes',
         'url': 'http://www.korokithakia.net/tutorials/python/'},
    ]

    django_pages = [
        {'title': "Official Django tutorial",
         'url': "https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {'title': "Django Rocks",
         'url': "http://www.djangorocks.com/"},
        {'title': "How to Tango with Django",
         'url': "http://www.tangowithdjango.com/"},
    ]

    other_pages = [
        {'title': "Bottle",
         "url": "http://bottlepy.org/docs/dev/"},
        {"title": "Flask",
         "url": "http://flask.pocoo.org"}
    ]

    cats = {"Python": {"pages": python_pages},
            "Django": {"pages": django_pages},
            "Other Frameworks": {"pages": other_pages}}

    # If you want to add more categories or pages, add them to the dictionaries above
    # The code below goes through the cats dictionary, then adds each category and then adds all the associated pages
    #  for that category
    # If you are using Python 2.x then use cats.iteritems()
    # If you are using Python 3.x, then use cats.items()
    # See http://docs.quantifiedcode.com/python-anti-patterns/readability/ for more info about how to iterate over a
    # dictionary properly

    for cat, cat_data in cats.iteritems():
        user_category = add_cat(cat)
        for user_page in cat_data["pages"]:
            add_page(user_category, user_page["title"], user_page["url"])

    # Print out the categories and their pages we have added
    for category in Category.objects.all():
        for page in Page.objects.filter(category=category):
            print "{0} - {1}".format(str(category), str(page))


def add_cat(category_name):
    category = Category.objects.get_or_create(name=category_name)[0]

    if category_name == 'Django':
        category.views = 64
        category.likes = 32
    elif category_name == 'Python':
        category.views = 128
        category.likes = 64
    elif category_name == 'Other Frameworks':
        category.views = 32
        category.likes = 16

    category.save()
    return category


def add_page(category_obj, page_title, page_url, page_views=0):
    page = Page.objects.get_or_create(category=category_obj, title=page_title)[0]
    page.url = page_url
    page.views = page_views
    page.save()
    return page


if __name__ == '__main__':
    print "Starting Rango Population Script"
    populate()
