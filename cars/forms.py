from django import forms
from .models import Car, Brand
from datetime import datetime


class CarForm(forms.ModelForm):
    CURRENT_YEAR = datetime.now().year
    YEAR_CHOICES = [(y, y) for y in range(CURRENT_YEAR, 1960, -1)]
    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Car
        exclude = ['seller', 'views_count', 'created_at', 'updated_at', 'is_active', 'is_featured']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control', 'id': 'id_brand'}),
            'model': forms.Select(attrs={'class': 'form-control', 'id': 'id_model'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'engine_volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'drive': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }