from django.db import models

# Create your models here.

class Mobile(models.Model):
    brand = models.CharField(max_length=20)
    release_date = models.CharField(max_length=20)
    price = models.CharField(max_length=15)
    model = models.CharField(max_length=20)
    screen_size = models.IntegerField()
    resolution = models.CharField(max_length=25)
    dimensions = models.CharField(max_length=50)
    weight = models.IntegerField()
    ram = models.CharField(max_length=10)
    storage = models.CharField(max_length=10)
    rear_camera = models.CharField(max_length=40)
    front_camera = models.CharField(max_length=40)

    def __str__(self):
        return self.brand