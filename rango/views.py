from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page


def index(request):
    # Query the database for a list of All categories currently stored
    # Order the categories by number of likes in descending order.
    # Retrieve the top 5 categories only - or all if less than or equal to 5.
    # Place the list in our context_dict dictionary that will be passed to the template engine

    category_list = Category.objects.order_by('-likes')[:5]
    # The expression above queries the Category model to retrieve top five categories.
    # It uses order_by() method to sort by the number of likes in descending order.
    # The - in `-likes` denotes that we would like them in descending order
    # If we removed the `-` and kept it just `likes` it would return it in ascending order
    # The [:5] is to return the first five items only (index 0 through 4)

    pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list,
                    'pages': pages_list}

    # Render the response and send it back!
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Deep Sukhwani'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns on method instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all associated pages
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # Add our results list to the template context dictionary under name pages
        context_dict['pages'] = pages

        # We also add category object from the database to the context dictionary.
        # We will use this in the template to verify the category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category (i.e. - the category name slug requested was invalid)
        # Don't do anything - the template will display "no category" message for us

        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client
    return render(request, 'rango/category.html', context=context_dict)

"""
All view functions defined as part of a Django application must take at least one parameter. This is typically called
request and provides access to information related to the given HTTP request made by the user.
When parameterizing URLs, you supply additional named parameters to the signature for the given view.
That is why our show_category() view was defined as def show_category(request, category_name_slug).
"""