from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput
from .models import city
from users.models import Profile
from pyuploadcare.dj.forms import ImageField


class CityForm(ModelForm):
    class Meta:
        model = city
        fields = ['name']
        widgets = {
            'name':TextInput(attrs={'class' : 'input','placholder' : 'City Name'})
        }

class UserProfileForm(forms.ModelForm):
    profile_photo = ImageField(label='')
    class Meta:
        model = Profile
        exclude = ['user']  