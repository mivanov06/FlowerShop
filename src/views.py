import phonenumbers
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from phonenumber_field.phonenumber import PhoneNumber

from src.models import Event, TIME_SLOT, Client, Order, Consultation

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
    if request.method == 'POST':
        fname = request.POST['fname']
        tel = request.POST['tel']
        client, _ = Client.objects.get_or_create(name=fname, phonenumber=tel)
        consultation = Consultation.objects.create(client=client, status=False)

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
    order = None
    error = None
    if request.method == 'POST':
        try:
            bouquet = Bouquet.objects.get(id=pk)
            customer_name = request.POST.get('fname')
            customer_phone = PhoneNumber.from_string(
                phone_number=request.POST.get('tel'),
                region='RU').as_e164
            customer_address = request.POST.get('address')
            delivery_time_slot = request.POST.get('orderTime')

            client, _ = Client.objects.update_or_create(
                name=customer_name,
                phonenumber=customer_phone,
            )

            order = Order.objects.create(
                bouquet=bouquet,
                price=bouquet.price,
                client=client,
                delivery_time=delivery_time_slot,
                address=customer_address

            )
        except phonenumbers.phonenumberutil.NumberParseException:
            error = 'Не правильный номер. Формат + 7 (999) 000 00 00'
    return render(
        request,
        template_name='pages/order.html',
        context={'times': TIME_SLOT, 'order': order, 'error': error}
    )
