from django.db import models

# Create your models here.

class DeviceData(models.Model):
    mac = models.CharField(max_length=17, unique=True)  # Assuming MAC address is unique and has a fixed length
    dbms = models.JSONField()  # Storing dbms as JSON
    # x = models.FloatField(null=True, blank=True)
    # y = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=250, default="")
    under_attack = models.CharField(max_length=5)   
    timestamp = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.mac}'
