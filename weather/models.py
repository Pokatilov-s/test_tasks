from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    city_id = models.BigIntegerField(null=True)
    lat = models.FloatField(null=True)  # широта
    lon = models.FloatField(null=True)  # долгота
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cities'
        indexes = [models.Index(fields=['name'])]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        CitiesStatistics.objects.get_or_create(
            city=self,
            defaults={'name': self.name, 'count_requests': 1}
        )


class CitiesStatistics(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, default=city.name)
    count_requests = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'cities_statistics'
