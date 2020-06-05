from django import forms
from .models import Camera, Organization
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.forms.models import model_to_dict

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


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
