from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignupForm(forms.ModelForm):

  confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password*'}), label='')
  confirm_email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Confirm Email*'}), label='')

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'confirm_email', 'password', 'confirm_password']
    widgets = {
      'username': forms.TextInput(attrs={'placeholder': 'Username*'}),
      'email': forms.TextInput(attrs={'placeholder': 'Email*'}),
      'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
      'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
      'password': forms.PasswordInput(attrs={'placeholder': 'Password*'}),
    }

    labels = {
      'username': '',
      'email': '',
      'password':'',
      'first_name': '',
      'last_name': '',
    }

    help_texts = {
      'username': '',
    }

  def clean(self):
    cleaned_data = super(SignupForm, self).clean()

    email = cleaned_data.get('email')
    cemail = cleaned_data.get('confirm_email')

    if (email != cemail):
      raise forms.ValidationError('The email fields do not match.')
    else:
      try:
        user = User.objects.get(email = email)
        if(user is not None):
          raise forms.ValidationError('An account with this email id already exists.')
      except User.DoesNotExist:
        print('User model not found')

    password = cleaned_data.get('password')
    cpassword = cleaned_data.get('confirm_password')

    if (password != '' and password != cpassword):
      raise forms.ValidationError('The password fields do not match.')


class LoginForm(forms.Form):
  username = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'username'}))
  password = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
  
  def clean(self):
    cleaned_data = super(LoginForm, self).clean()

    uname = cleaned_data.get('username')
    passwd = cleaned_data.get('password')

    print(passwd)
    print(uname)
    try:
      User.objects.get(username = uname)
      user = User.objects.get(username = uname)
    except User.DoesNotExist:
      raise forms.ValidationError('*Invalid username or password')

    user = authenticate(username=uname, password=passwd)
    if (user is None):
      raise forms.ValidationError('*Invalid username or password')   


#continue here............................................................
    # if (uname == ''):
    #   raise forms.ValidationError('*Fill in the username')

    # if (passwd == ''):
    #   raise forms.ValidationError('*Password missing')

class ForgotPasswordForm(forms.Form):
  email = forms.CharField(label='', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
  



class ResetPasswordForm(forms.Form):
  password = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
  confirm_password = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))

  def clean(self):
    cleaned_data = super(ResetPasswordForm, self).clean()

    password = cleaned_data.get('password')
    cpassword = cleaned_data.get('confirm_password')

    if (password != '' and password != cpassword):
      raise forms.ValidationError('The password fields do not match.')
