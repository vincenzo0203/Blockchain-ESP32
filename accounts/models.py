from django.db import models

class Person(models.Model):
    rfid = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - RFID: {self.rfid}"