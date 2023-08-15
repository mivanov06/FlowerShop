from django.shortcuts import render


def index(request):
    return render(request, template_name='pages/index.html')


def catalog(request):
    return render(request, template_name='pages/catalog.html')


def recommendations(request):
    return render(request, template_name='pages/recommendations.html')


def contacts(request):
    return render(request, template_name='pages/contacts.html')


def bouquet_card(request, pk):
    return render(request, template_name='pages/card.html')


def order(request):
    return render(request, template_name='pages/order.html')
