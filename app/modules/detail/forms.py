from django import forms
from django.forms import ModelForm, fields
from app.models import Detail
from django.utils.translation import ugettext_lazy as _

class DetailForm(ModelForm):
    class Meta:
        model = Detail
        fields = '__all__'
        # fields = ['name','description','status','image']
        # labels = {
        #     'name': _('Nama'),
        #     'description': _('Deskripsi'),
        #     'status': _('Aktif'),
        #     'image': _('Gambar')
        # }
        widgets = {
            'transaction': forms.HiddenInput(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sell Price'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Buy Price'}),
            'price_sell': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sell Price'}),
        }