from django.urls import path

from src import views


urlpatterns = [
    path('', views.index, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('contacts/', views.contacts, name='contacts'),
    path('selection_flowers/', views.selection_flowers, name='selection_flowers'),
    path('orders/', views.orders, name='orders'),
]
