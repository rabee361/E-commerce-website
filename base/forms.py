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
        



class NewUserApi(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = MyUser
        fields = ("username","email","password1","password2")




PAYMENT_CHOICES = (
    ('paypal', 'PayPal'),
    ('payoneer', 'Payoneer'),
    ('check', 'Check Payment'),
    ('bank', 'Direct Bank Transfer'),
    ('cash', 'Cash on Delivery'),
)
class BillingForm(forms.ModelForm):
    payment = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ('first_name','last_name','address','mobile','country','city','state','payment')



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text','rating')