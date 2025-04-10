from django import forms
from .models import Ad

class AdForm(forms.Form):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'contact', 'image_url']
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
