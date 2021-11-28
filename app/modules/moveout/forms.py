from django import forms
from django.forms import ModelForm, fields
from app.models import Transaction
from django.utils.translation import ugettext_lazy as _

class MoveoutForm(ModelForm):
    class Meta:
        model = Transaction
        # fields = '__all__'
        fields = ['date','warehousein','warehouseout','code','description']
        labels = {
            'warehousein': _('Warehouse Source'),
            'warehouseout': _('Warehouse Destination'),
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date', 'required': 'required'}),
            'warehousein': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gudang Tujuan', 'required': 'required'}),
            'warehouseout': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gudang Source', 'required': 'required'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }