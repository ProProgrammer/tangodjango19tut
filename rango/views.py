from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category


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

    context_dict = {'categories': category_list}

    # Render the response and send it back!
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Deep Sukhwani'}
    return render(request, 'rango/about.html', context=context_dict)