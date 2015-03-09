from django.db import models

# Create your models here.
class Neighbours(models.Model):
    route = models.CharField(max_length=64)
    start_stop = models.CharField(max_length=64)
    end_stop = models.CharField(max_length=64)