from django import forms
from django.forms import ModelForm, fields
from app.models import Supplier
from django.utils.translation import ugettext_lazy as _

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
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
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-control col-sm-1'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }