from django import forms
from django.forms import ModelForm, fields
from app.models import Transaction
from django.utils.translation import ugettext_lazy as _

class SellForm(ModelForm):
    class Meta:
        model = Transaction
        # fields = '__all__'
        fields = ['date','customer','warehousein','code','description']
        # labels = {
        #     'name': _('Nama'),
        #     'description': _('Deskripsi'),
        #     'status': _('Aktif'),
        #     'image': _('Gambar')
        # }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date', 'required': 'required'}),
            'customer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Supplier'}),
            'warehousein': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Warehouse'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }