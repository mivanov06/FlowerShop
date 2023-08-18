from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

TIME_SLOT = (
    (1, 'Как можно скорее'),
    (2, 'С 10:00 до 12:00'),
    (3, 'С 12:00 до 14:00'),
    (4, 'С 14:00 до 16:00'),
    (5, 'С 16:00 до 18:00'),
    (6, 'С 18:00 до 20:00'),
)


class Event(models.Model):
    name = models.CharField(
        'Название события',
        max_length=100
    )

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(
        'Имя',
        max_length=200
    )
    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
        db_index=True
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Bouquet(models.Model):
    name = models.CharField(
        'Название букета',
        max_length=100,
        unique=True,
        db_index=True
    )
    image = models.ImageField(
        'Картинка'
    )
    price = models.IntegerField(
        'Цена',
        db_index=True
    )
    description = models.TextField(
        'Описание',
        max_length=5000
    )
    compound = models.TextField(
        'Состав',
        max_length=5000
    )
    height = models.IntegerField(
        'Высота',
        default=30
    )
    width = models.IntegerField(
        'Ширина',
        default=30
    )
    events = models.ManyToManyField(
        Event,
        verbose_name='Для событий',
        related_name='bouquet'
    )

    def compound_as_list(self):
        return self.compound.split(',')

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'

    def __str__(self):
        return self.name


class OrderQuerySet(models.QuerySet):
    def is_activity(self):
        return self.filter(status=True)


class Order(models.Model):
    bouquet = models.ForeignKey(
        Bouquet,
        verbose_name='Заказанный букет',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    price = models.IntegerField(
        'Цена букета'
    )
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    delivery_date = models.DateField(
        'Дата доставки',
        auto_now_add=True,
        db_index=True
    )
    delivery_slot = models.IntegerField(
        'Время доставки',
        choices=TIME_SLOT
    )
    address = models.CharField(
        'Адрес доставки',
        max_length=1000
    )
    status = models.BooleanField(
        'Заказ доставлен',
        db_index=True,
        default=False
    )
    comment = models.CharField(
        'Комментарий',
        max_length=1000,
        blank=True,
        default=''
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.bouquet} - {self.address}'

    object = OrderQuerySet.as_manager()


class ActiveOrder(Order):
    class Meta:
        proxy = True

    def get_queryset(self):
        return self.object.is_activity()


class Consultation(models.Model):
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='consultations'
    )
    status = models.BooleanField(
        'Консультация проведена',
        db_index=True,
        default=False
    )

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'

    def __str__(self):
        return f'{self.client.name} - {self.client.phonenumber}'
