from django import forms
from django.forms import ModelForm, fields
from app.models import Customer
from django.utils.translation import ugettext_lazy as _

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        # fields = ['name','description','status','image']
        # labels = {
        #     'name': _('Nama'),
        #     'description': _('Deskripsi'),
        #     'status': _('Aktif'),
        #     'image': _('Gambar')
        # }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-control col-sm-1'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }