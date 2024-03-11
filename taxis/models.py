from django.db import models
from datetime import datetime


class Taxi(models.Model):
    plate = models.CharField(max_length=80)

    def __str__(self):
        return self.plate


class Trajectory(models.Model):
    taxi = models.ForeignKey("taxis.Taxi", on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.taxi.plate} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
