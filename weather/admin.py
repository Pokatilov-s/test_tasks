from django.contrib import admin
from weather.models import City, CitiesStatistics


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city_id', 'lat', 'lon')
    search_fields = ('name',)


@admin.register(CitiesStatistics)
class CitiesStatisticsAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_requests')
    list_filter = ('count_requests',)
    search_fields = ('name',)
