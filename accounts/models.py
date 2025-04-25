from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    first_name_custom = models.CharField("Имя", max_length=100)
    last_name_custom = models.CharField("Фамилия", max_length=100)
    phone_number = models.CharField("Телефон", max_length=20, blank=True, null=True)
    city = models.CharField("Город", max_length=100, blank=True, null=True)
    profile_picture = models.ImageField("Аватар", upload_to='profile_pictures/', null=True, blank=True)

    DARK_THEME = 'dark'
    LIGHT_THEME = 'light'
    THEME_CHOICES = [
        (DARK_THEME, 'Темная'),
        (LIGHT_THEME, 'Светлая'),
    ]
    theme = models.CharField(max_length=5, choices=THEME_CHOICES, default=LIGHT_THEME)

    def __str__(self):
        return self.username
