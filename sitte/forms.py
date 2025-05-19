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
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'first_name_custom': 'Имя',
            'last_name_custom': 'Фамилия',
            'profile_picture': 'Аватар',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
            'first_name_custom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name_custom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

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
class AdImageForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['image']