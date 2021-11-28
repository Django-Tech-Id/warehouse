from django import forms
from django.forms import ModelForm, fields
from app.models import Status
from django.utils.translation import ugettext_lazy as _

class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = '__all__'