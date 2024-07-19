from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    city_id = models.BigIntegerField(null=True)
    lat = models.FloatField(null=True)  # широта
    lon = models.FloatField(null=True)  # долгота
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        CitiesStatistics.objects.get_or_create(
            city=self,
            defaults={'name': self.name, 'count_requests': 1}
        )

    class Meta:
        db_table = 'cities'
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Геоданные города'
        verbose_name_plural = 'Геоданные городов'


class CitiesStatistics(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, default=city.name)
    count_requests = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities_statistics'
        verbose_name = 'Статистика поиска города'
        verbose_name_plural = 'Статистика поиска городов'
