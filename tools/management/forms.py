from django import forms
from .models import Camera
from .models import Organization

class CameraForm(forms.ModelForm):

    class Meta:
        model = Camera
        fields = '__all__'

        widgets = {

            'camera_title' : forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Camera Title',
            }),

            'area' : forms.TextInput(
                attrs={
                'class':'form-control',
                'placeholder': 'Admin',
                }
            ),

            'organization_name' : forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Organization Name'
            }),

            'IP_camera' : forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Camera IP',
            }),

            'status' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder': 'Status'
            }),

        }


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = '__all__'
        widgets = {

            'id' : forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'organization_name',
                'readonly': 'readonly'
            }),

            'admin' : forms.TextInput(
                attrs={
                'class':'form-control',
                'placeholder': 'Admin',
                }
            ),

            'organization_name' : forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Organization Name'
            }),

            'location' : forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Location',
            }),

            'tel' : forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Telephone'
            }),

        }
