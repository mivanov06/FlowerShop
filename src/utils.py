import random

from django.db.models import Max

from src.models import Bouquet


def get_recommended_bouquet(event: int, price: tuple):
    max_id = Bouquet.objects.filter(
        events__id=event,
        price__range=price
    ).aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        bouquet = Bouquet.objects.filter(pk=pk).first()
        if bouquet:
            return bouquet


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
