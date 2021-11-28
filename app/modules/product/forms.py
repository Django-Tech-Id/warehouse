from django import forms
from django.forms import ModelForm, fields
from app.models import Product
from django.utils.translation import ugettext_lazy as _

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['name','description','status','image']
        # labels = {
        #     'name': _('Nama'),
        #     'description': _('Deskripsi'),
        #     'status': _('Aktif'),
        #     'image': _('Gambar')
        # }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Supplier'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'sell_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sell Price'}),
            'buy_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Buy Price'}),
            'spesification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Spesification'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-control col-sm-1'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }