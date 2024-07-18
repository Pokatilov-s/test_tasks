import requests
from multipledispatch import dispatch

api_key = '70b7fd9960272ae531f165e3d174b819'


def _get_weather(params):
    params_base = {
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru'
    }

    params.update(params_base)

    response = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=params)
    return response.json()


@dispatch(str)
def get_weather_four_days(city_name):

    params = {
        'q': city_name,
    }

    return _get_weather(params)


@dispatch(int)
def get_weather_four_days(id_city):

    params = {
        'id': id_city,
    }

    return _get_weather(params)


@dispatch(float, float)
def get_weather_four_days(latitude, longitude):

    params = {
        'lat': latitude,
        'lon': longitude,
    }

    return _get_weather(params)


