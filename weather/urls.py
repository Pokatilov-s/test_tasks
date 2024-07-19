from django.urls import path
from weather.views import weather, index, CitiesStatisticsList

urlpatterns = [
    path('weather', weather, name='weather'),
    path('', index, name='index'),
    path('cities_statistics/', CitiesStatisticsList.as_view(), name='cities_statistics')
]

