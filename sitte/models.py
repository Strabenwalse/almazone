
from django import forms
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser

# Кастомный пользователь

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from accounts.models import CustomUser

# Кастомный пользователь
# models.py
from django.utils import timezone  # Добавь это

from django.contrib.auth.models import AbstractUser
from django.db import models



# accounts/forms.py
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


# Модель категории
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

# Модель продукта
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def price_in_kzt(self):
        return round(self.price * 5, 2)  # Примерный курс руб → тенге

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

# Модель объявления
class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ads/')

    def __str__(self):
        return self.title




    @property
    def price_in_kzt(self):
        return round(self.price * 5, 2)

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

# Форма для продукта
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'category', 'description']

# Форма для объявления
class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category', 'image']
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name_custom', 'last_name_custom']  # Правильные поля