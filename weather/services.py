from datetime import datetime, timedelta
import copy
from django.db.models import F
from weather.models import City, CitiesStatistics


def _get_wind_direction(degree):
    """Определить направление ветра"""
    directions = ('Северный', 'Северо-Восточный', 'Восточный', 'Юго-Восточный', 'Южный', 'Юго-Западный',
                  'Западный', 'Северо-Западный',)
    idx = round(degree / 45) % 8
    return directions[idx]


def format_response(data_jason):
    """Форматировать ответ от геосервиса"""
    data_jason_copy = copy.deepcopy(data_jason)

    today = datetime.strptime(data_jason_copy['list'][0]['dt_txt'].split(' ')[0], '%Y-%m-%d').date()
    tomorrow = today + timedelta(days=1)

    new_list = list(filter(
        lambda x: datetime.strptime(x['dt_txt'].split(' ')[0], '%Y-%m-%d').date() <= tomorrow,
        data_jason_copy['list']))

    data_jason_copy['list'] = new_list

    data_jason_copy['message'] = 'success'
    del data_jason_copy['cnt']

    for obj in data_jason_copy['list']:

        del_key_main = ("temp_min", "temp_max", "sea_level", "grnd_level", "temp_kf", "pressure")
        obj['main'] = {k: v for k, v in obj['main'].items() if k not in del_key_main}

        obj['weather'] = obj.get('weather', [{}])[0].get('description')

        obj['clouds'] = obj.get('clouds', {}).get('all')

        obj['wind']['deg'] = _get_wind_direction(obj.get('wind', {}).get('deg'))

        obj['rain'] = obj.get('rain', {}).get('3h')

        del obj['dt']
        del obj['pop']
        del obj['sys']

    return data_jason_copy


def add_city(name, city_id, lat, lon):
    """Добавить геоданные города"""
    if not City.objects.filter(name=name).exists():
        City.objects.create(name=name, city_id=city_id, lat=lat, lon=lon)


def check_city(city):
    """Проверить наличие геоданных города """
    city_geo_data = City.objects.filter(name=city).values('city_id', 'lat', 'lon').first()

    if city_geo_data is not None:
        update_statistics(city)
        if city_geo_data['city_id'] is not None:
            return city_geo_data['city_id']
        else:
            return city_geo_data['lat'], city_geo_data['lon']

    return None


def update_statistics(city):
    """Обновить запросов статистику по городу"""
    CitiesStatistics.objects.filter(name=city).update(count_requests=F('count_requests') + 1)
