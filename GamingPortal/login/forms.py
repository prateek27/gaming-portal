from django import forms
from login.models import UserProfile
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password')

class UserProfileForm(forms.ModelForm):
    captcha = CaptchaField()
    
    class Meta:
        model = UserProfile
        fields = ('profile_url','profile_image')

class LoginForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','password')


