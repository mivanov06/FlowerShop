from django.shortcuts import render


def index(request):
    return render(request, template_name='index.html')


def catalog(request):
    pass


def recommendations(request):
    pass


def contacts(request):
    pass


def selection_flowers(request):
    pass


def orders(request):
    pass
