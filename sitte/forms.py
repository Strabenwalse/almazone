from django import forms
from .models import Ad

from django import forms
from .models import Product

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category', 'image']
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'category', 'description']
