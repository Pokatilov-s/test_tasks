from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from weather.services import format_response
from weather.weather_service import get_weather_four_days


def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def weather(request):
    if request.method == 'GET':
        params = request.query_params
        data = get_weather_four_days(params.get('city'))
        format_data = format_response(data)

    return Response(format_data)
