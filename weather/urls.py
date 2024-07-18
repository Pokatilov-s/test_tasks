from django.urls import path
from weather.views import weather, index

urlpatterns = [
    path('weather', weather, name='weather'),
    path('', index, name='index'),
]
