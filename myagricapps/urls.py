from django.urls import path
from . import views



urlpatterns = [
    path('',views.apphome, name='myapps'),
    path('weather',views.weather, name='weather_app'),
    path('prices',views.prices, name='price_app'),
]
