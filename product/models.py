from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    qty = models.IntegerField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'<{self.code}: {self.name}>'
