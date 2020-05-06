from django import forms
from .models import Camera
from .models import Organization

class CameraForm(forms.ModelForm):

    class Meta:
        model = Camera
        fields = '__all__'

class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = '__all__'
