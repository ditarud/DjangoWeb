from django.db import models

# Create your models here.

class Mobile(models.Model):
    brand = models.CharField(max_length=20)
    release_date = models.CharField(max_length=20, blank=True, null=True)
    price = models.CharField(max_length=15)
    model = models.CharField(max_length=50)
    screen_size = models.IntegerField(blank=True, null=True)
    resolution = models.CharField(max_length=25, blank=True, null=True)
    dimensions = models.CharField(max_length=50, blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    ram = models.CharField(max_length=10,blank=True, null=True)
    storage = models.CharField(max_length=10,blank=True, null=True)
    rear_camera = models.CharField(max_length=40,blank=True, null=True)
    front_camera = models.CharField(max_length=40,blank=True, null=True)
    score = models.CharField(max_length=10,blank=True, null=True)
    shop = models.CharField(max_length=30)
    link = models.CharField(max_length=300, blank=True, null=True)
    thumbnail = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.brand

