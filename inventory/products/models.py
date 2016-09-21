from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    status = models.IntegerField(default=1)

class Stat(models.Model):
    category_count = models.IntegerField()
