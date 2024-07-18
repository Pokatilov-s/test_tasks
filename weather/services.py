from datetime import datetime, timedelta
import copy


def get_wind_direction(degree):
    directions = ('Северный', 'Северо-Восточный', 'Восточный', 'Юго-Восточный', 'Южный', 'Юго-Западный',
                  'Западный', 'Северо-Западный',)
    idx = round(degree / 45) % 8
    return directions[idx]


def format_response(data_jason):
    data_jason_copy = copy.deepcopy(data_jason)

    del data_jason_copy['cod']
    del data_jason_copy['message']
    del data_jason_copy['cnt']

    today = datetime.strptime(data_jason_copy['list'][0]['dt_txt'].split(' ')[0], '%Y-%m-%d').date()
    tomorrow = today + timedelta(days=1)

    new_list = list(filter(
        lambda x: datetime.strptime(x['dt_txt'].split(' ')[0], '%Y-%m-%d').date() <= tomorrow,
        data_jason_copy['list']))

    data_jason_copy['list'] = new_list
    for obj in data_jason_copy['list']:

        del obj['dt']

        delite_key = ("temp_min", "temp_max", "sea_level", "grnd_level", "temp_kf", "pressure")
        obj['main'] = {k: v for k, v in obj['main'].items() if k not in delite_key}

        obj['weather'] = obj.get('weather', [{}])[0].get('description')

        obj['clouds'] = obj.get('clouds', {}).get('all')

        obj['wind']['deg'] = get_wind_direction(obj.get('wind', {}).get('deg'))

        obj['rain'] = obj.get('rain', {}).get('3h')

        del obj['pop']
        del obj['sys']

    return data_jason_copy
