from django.db import models


class WeatherData(models.Model):
    city_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField()
    description = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city_name} - {self.temperature}°C"
