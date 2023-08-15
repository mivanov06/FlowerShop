from django.shortcuts import render


def index(request):
    return render(request, template_name='pages/index.html')


def catalog(request):
    return render(request, template_name='pages/catalog.html')


def recommendations(request):
    pass


def contacts(request):
    return render(request, template_name='pages/catalog.html')


def selection_flowers(request):
    pass


def orders(request):
    pass
