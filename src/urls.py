from django.urls import path

from src import views


urlpatterns = [
    path('', views.index, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('contacts/', views.contacts, name='contacts'),
    path('bouquet/<int:pk>', views.bouquet_card, name='bouquet_card'),
    path('order/', views.order, name='order'),
]
