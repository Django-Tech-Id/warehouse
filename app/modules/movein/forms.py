from django import forms
from django.forms import ModelForm, fields
from app.models import Transaction
from django.utils.translation import ugettext_lazy as _

class MoveinForm(ModelForm):
    class Meta:
        model = Transaction
        # fields = '__all__'
        fields = ['date','pending_date','accepted_date','warehousein','warehouseout','code','description']
        labels = {
            'warehousein': _('Warehouse Destination'),
            'warehouseout': _('Warehouse Source'),
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date', 'required': 'required', 'readonly': 'readonly'}),
            'pending_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date'}),
            'accepted_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date'}),
            'warehousein': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gudang Tujuan', 'required': 'required', 'readonly': 'readonly'}),
            'warehouseout': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gudang Source', 'required': 'required', 'readonly': 'readonly'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code', 'readonly': 'readonly'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }