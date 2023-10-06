from django.http import HttpResponse


def index(requests):
    return HttpResponse("Hello world!")
