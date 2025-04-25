from django import forms
from .models import Ad
from django.contrib.auth import get_user_model
from django import forms
from .models import Product
User = get_user_model()
from .models import CustomUser
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name_custom', 'last_name_custom', 'profile_picture']

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category', 'image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'category', 'description']
from django import forms
from accounts.models import CustomUser  # Импорт правильной модели пользователя

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
