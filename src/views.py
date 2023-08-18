import phonenumbers

from phonenumber_field.phonenumber import PhoneNumber

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from src.models import Event
from src.models import TIME_SLOT
from src.models import Client
from src.models import Order
from src.models import Consultation
from src.models import Bouquet

from src.utils import get_random_bouquets
from src.utils import get_recommended_bouquet
from src.utils import catalog_bouquets_serialize


def index(request):
    bouquets = get_random_bouquets()
    return render(
        request,
        template_name='pages/index.html',
        context={'bouquets': bouquets},
    )


def consultation(request):
    consultation = None
    error = ''
    if request.method == 'POST':
        try:
            name = request.POST.get('fname')
            tel = PhoneNumber.from_string(
                phone_number=request.POST.get('tel'),
                region='RU'
            ).as_e164

            client, _ = Client.objects.get_or_create(
                name=name,
                phonenumber=tel
            )
            consultation = Consultation.objects.create(
                client=client,
                status=False
            )
        except phonenumbers.phonenumberutil.NumberParseException:
            error = 'Не правильный номер. Формат + 7 (999) 000 00 00'

    return render(
        request,
        template_name='pages/consultation.html',
        context={'consultation': consultation, 'error': error},
    )


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
        print('GJGFK')
        try:
            bouquet = Bouquet.objects.get(id=pk)
            customer_name = request.POST.get('fname')
            customer_phone = PhoneNumber.from_string(
                phone_number=request.POST.get('tel'),
                region='RU'
            ).as_e164
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
                delivery_slot=delivery_time_slot,
                address=customer_address

            )
            print(order)
        except phonenumbers.phonenumberutil.NumberParseException:
            error = 'Не правильный номер. Формат + 7 (999) 000 00 00'
    return render(
        request,
        template_name='pages/order.html',
        context={'times': TIME_SLOT, 'order': order, 'error': error}
    )
