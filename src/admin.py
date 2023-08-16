from django.contrib import admin

from src.models import Event, Client, Bouquet, Order, Consultation


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    ...


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    ...


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    ...
