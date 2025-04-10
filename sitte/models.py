from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)  # Добавим
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)  # Добавим

    def __str__(self):
        return self.title

