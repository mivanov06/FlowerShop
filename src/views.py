from django.shortcuts import render
from django.shortcuts import get_object_or_404

from src.models import Event
from src.models import Bouquet
from src.utils import get_recommended_bouquet


def catalog_bouquets_serialize(bouquets):
    serialized = []
    for bouquet in bouquets:
        serialized.append(
            {
                'pk': bouquet.pk,
                'name': bouquet.name,
                'image_url': bouquet.image.url,
                'price': bouquet.price
            }
        )
    return serialized


def index(request):
    return render(request, template_name='pages/index.html')


def catalog(request):
    events = Event.objects.all()
    event = request.POST.get("event", False)
    if event:
        bouquets = Bouquet.objects.filter(events__in=event)
    else:
        bouquets = Bouquet.objects.all()
    context = {
        'bouquets': catalog_bouquets_serialize(bouquets),
        'events': events
    }

    return render(request, template_name='pages/catalog.html', context=context)


def recommendations(request):
    step = 1
    events = Event.objects.all()
    event = request.session.get('event')
    price = request.session.get('price')
    bouquet = None

    if request.method == 'GET':
        request.session.pop('event', '')
        request.session.pop('price', '')

    if request.method == 'POST' and not event:
        request.session['event'] = request.POST.get('event')
        step = 2

    if request.method == 'POST' and event and not price:
        request.session['price'] = request.POST.get('price')
        price = request.POST.get('price').split('-')
        bouquet = get_recommended_bouquet(int(event), tuple(price))
        step = 3

    return render(
        request,
        template_name='pages/recommendations.html',
        context={
            'events': events,
            'step': step,
            'bouquet': bouquet,
        }
    )


def contacts(request):
    return render(request, template_name='pages/contacts.html')


def bouquet_card(request, pk):
    bouquet = get_object_or_404(Bouquet, pk=pk)
    return render(
        request,
        template_name='pages/card.html',
        context={'bouquet': bouquet}
    )


def order(request, pk):
    return render(request, template_name='pages/order.html')
