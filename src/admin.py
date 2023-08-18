from django.contrib import admin

from src.models import Event, Client, Bouquet, Order, Consultation


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    ...


class ClientOrdersInline(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientOrdersInline]


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    ...


# @admin.register(ActiveOrder)
# class ActiveOrderAdmin(admin.ModelAdmin):
#     ...
