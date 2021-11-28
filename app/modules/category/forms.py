from django import forms
from django.forms import ModelForm, fields
from app.models import Category
from django.utils.translation import ugettext_lazy as _

class CategoryForm(ModelForm):
    class Meta:
        model = Category
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
            'status': forms.CheckboxInput(attrs={'class': 'form-control col-sm-1'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }