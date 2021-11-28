from django import forms
from django.forms import ModelForm, fields
from app.models import Company
from django.utils.translation import ugettext_lazy as _

class CompanyForm(ModelForm):
    class Meta:
        model = Company
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
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }