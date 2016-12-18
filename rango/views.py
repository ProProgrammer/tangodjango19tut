from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("Rango says, Hey there Partner! <a href='/rango/about'>About Page</a>")
    context_dict = {'boldmessage': 'Some bold message on About page'}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Deep Sukhwani'}
    return render(request, 'rango/about.html', context=context_dict)