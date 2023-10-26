from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from captcha.fields import ReCaptchaField
from captcha import fields , widgets
from captcha.widgets import ReCaptchaV2Invisible ,ReCaptchaV2Checkbox

class NewUser(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' , 'type' : 'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' , 'type' : 'password'}))

    captcha = fields.ReCaptchaField(
        widget=widgets.ReCaptchaV2Checkbox()
    )
        
    class Meta:
        model = MyUser
        fields = ("username","email","password1","password2")
        
