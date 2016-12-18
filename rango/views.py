from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("Rango says, Hey there Partner! <a href='/rango/about'>About Page</a>")
    context_dict = {'boldmessage': 'Some bold message on About page'}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Main Page</a>")