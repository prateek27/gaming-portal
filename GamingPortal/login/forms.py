from django import forms
from login.models import UserProfile
from django.contrib.auth.models import User



class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('first_name','last_name','username','email','password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('profile_url','profile_image')

class LoginForm(forms.ModelForm):
	#password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username','password')



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
