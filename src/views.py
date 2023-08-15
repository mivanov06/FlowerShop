from django.shortcuts import render


def index(request):
    return render(request, template_name='pages/index.html')


def catalog(request):
    return render(request, template_name='pages/catalog.html')


def recommendations(request):
    return render(request, template_name='pages/recommendations.html')


def contacts(request):
    return render(request, template_name='pages/contacts.html')


def selection_flowers(request):
    pass


def orders(request):
    pass
