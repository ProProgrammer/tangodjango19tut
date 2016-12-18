from django.http import HttpResponse


def index(request):
    return HttpResponse("Rango says, Hey there Partner! <a href='/rango/about'>About Page</a>")


def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Main Page</a>")