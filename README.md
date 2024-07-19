[//]: # (# CitiesStatistics Project)

[//]: # ()
[//]: # (## Описание)

[//]: # ()
[//]: # (Проект `CitiesStatistics` предназначен для управления и обновления статистики запросов по городам с использованием Django и Django REST Framework &#40;DRF&#41;.)

[//]: # ()
[//]: # (## Установка)

[//]: # ()
[//]: # (1. Клонируйте репозиторий:)

[//]: # ()
[//]: # (    ```sh)

[//]: # (    git clone https://github.com/yourusername/CitiesStatistics.git)

[//]: # (    cd CitiesStatistics)

[//]: # (    ```)

[//]: # ()
[//]: # (2. Установите виртуальное окружение и активируйте его:)

[//]: # ()
[//]: # (    ```sh)

[//]: # (    python3 -m venv venv)

[//]: # (    source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`)

[//]: # (    ```)

[//]: # ()
[//]: # (3. Установите зависимости:)

[//]: # ()
[//]: # (    ```sh)

[//]: # (    pip install -r requirements.txt)

[//]: # (    ```)

[//]: # ()
[//]: # (4. Выполните миграции: ## если БД нет в проекте )

[//]: # ()
[//]: # (    ```sh)

[//]: # (    python manage.py migrate)

[//]: # (    ```)

[//]: # ()
[//]: # (5. Запустите сервер разработки:)

[//]: # ()
[//]: # (    ```sh)

[//]: # (    python manage.py runserver)

[//]: # (    ```)

# Weather Forecast project

## Описание

Проект `Weather Forecast` предназначен для получения ближайшего прогноза погоды по названию города. Разработан в рамках тестового задания.

## Содержание

- [Установка](#установка)
- [Использование](#использование)
- [API Эндпоинты](#api-эндпоинты)
- [Развертывание в Docker](#развертывание-в-docker)

## Установка

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/Pokatilov-s/weather_forecast.git
    cd weather_forecast
    ```

2. Установите виртуальное окружение и активируйте его:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
    ```

3. Установите зависимости:

    ```sh
    pip install -r requirements.txt
    ```

4. Выполните миграции: (если БД нет в проекте)

    ```sh
    python manage.py migrate
    ```

5. Запустите сервер разработки:

    ```sh
    python manage.py runserver
    ```

## Использование

1. Чтобы попасть на главную страницу поиска и просмотра погоды, перейдите по адресу: 
   
    ```
    http://127.0.0.1:8000/
    или
    http://localhost:8000/
    ```   

2. Для доступа к API эндпоинту списка статистики поиска городов перейдите по адресу:

    ```
    http://127.0.0.1:8000/cities_statistics/
    или
    http://localhost:8000/cities_statistics/
    ```

3. Пример использования API:

    ```sh
    curl -X GET http://127.0.0.1:8000/cities_statistics/
    ```

## API Эндпоинты

- `GET /weather?city={city}` - Возвращает прогноз погоды на сегодня и завтра по переданному названию города.
- `GET /cities/` - Возвращает список всех городов и их статистику запросов.

## Развертывание в Docker

1. Создайте Docker-образ:

    ```sh
    docker build -t weather_forecast .
    ```

2. Запустите контейнер:

    ```sh
    docker run -p 8000:8000 weather_forecast
    ```

3. Откройте веб-браузер и перейдите по адресу:

    ```
    http://localhost:8000/
    или 
    http://127.0.0.1:8000/
    ```

4. Убедитесь, что ваш `Dockerfile` содержит все необходимые инструкции для установки зависимостей и запуска приложения. Пример `Dockerfile`:

    ```Dockerfile
   FROM python:3.12-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   RUN python manage.py migrate
   
   EXPOSE 8000
   
   CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000"]
    ```
