import requests
from multipledispatch import dispatch
from requests.exceptions import HTTPError
from typing import Tuple
from weather.services import add_city, check_city

api_key = '70b7fd9960272ae531f165e3d174b819'


class ServiceUnavailableError(Exception):
    pass


def _get_weather(params, write_to_db=False):
    """Произвести запрос на получение погоды"""

    params_base = {
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru'
    }
    params.update(params_base)
    try:
        response = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=params)
        response.raise_for_status()
        if write_to_db:
            city = response.json().get('city', {})
            add_city(name=city.get('name'), city_id=city.get('id'), lat=city.get('coord').get('lat'),
                     lon=city.get('coord').get('lon'))
        return response.json()

    except HTTPError as e:

        if e.response.status_code == 404:
            raise ValueError("Город не найден")

        elif 500 >= e.response.status_code < 600:
            raise ServiceUnavailableError("Сервис геоданных не доступен")

        else:
            raise Exception(f"Произошла непредвиденная ошибка: {e}")

    except Exception as e:
        raise RuntimeError(f"Произошла непредвиденная ошибка: {e}")


@dispatch(str)
def _get_weather_four_days(city_name):
    """Получить погоду по названию города"""
    params = {
        'q': city_name,
    }

    return _get_weather(params, write_to_db=True)


@dispatch(int)
def _get_weather_four_days(id_city):
    """Получить погоду id города"""
    # Рекомендованный геосервисом способ

    params = {
        'id': id_city,
    }

    return _get_weather(params)


@dispatch(tuple)
def _get_weather_four_days(args: Tuple[float, float]):
    """Получить погоду координатам города"""
    # Второй в приоритете использования

    params = {
        'lat': args[0],
        'lon': args[1],
    }

    return _get_weather(params)


def get_weather_four_days(city):
    """Входная функция для получения погоды"""

    valid_city = check_city(city)
    if valid_city:
        return _get_weather_four_days(valid_city)

    return _get_weather_four_days(city)
