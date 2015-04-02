from django.shortcuts import render, redirect

# Create your views here.
from .forms import SignupForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.core import serializers


import base64

def base64_encoder(uname):
  a = base64.urlsafe_b64encode(uname.encode('utf-8'))
  return a.decode('utf-8')

def base64_decoder(encoded):
  a = encoded.encode('utf-8')
  return base64.urlsafe_b64decode(a).decode('utf-8')

def send_activation_email(uname, mail, first_name):
  activation_key = base64_encoder(uname)
  send_mail(
    'Account Activation Link - Portal', 
    get_template('myLogin/email_template.html').render(
      Context({
        'username': uname, 
        'activation_key': activation_key, 
        'first_name': first_name
        })
      ), 
    settings.EMAIL_HOST_USER, 
    [mail], 
    fail_silently=False)

def signup_template(request):
  return HttpResponse("Hello World !")

def signup_template2(request):
  registered = False
  if(not request.user.is_authenticated()):
    if (request.method == 'GET'):
      form = SignupForm
      return render(request, 'myLogin/signup.html', {'form': form})

    if (request.method == 'POST'):
      form = SignupForm(request.POST)
      if(form.is_valid()):
        uname = form.cleaned_data['username']
        fname = form.cleaned_data['first_name']
        lname = form.cleaned_data['last_name']
        mail = form.cleaned_data['email']
        passwd = form.cleaned_data['password']
        user = User.objects.create_user(
          username = uname,
          first_name = fname,
          last_name = lname,
          email = mail,
          password = passwd,
        )
        user.is_active = False
        user.is_staff = False
        user.save()
        
        user = authenticate(username = uname, password = passwd)
        if (user is not None):
          registered = True
          send_activation_email(user.username, user.email, user.first_name)
          return render(request, 'myLogin/signup.html', {'registered': registered, 'new_user': user})
    return render(request, 'myLogin/signup.html', {'form': form})
  else:
    return redirect('/mylogin/logged_in/')


def activate_user(request):
  activation_key = request.GET.get('activation_key')
  print(activation_key)
  new_user = base64_decoder(activation_key)

  uname = request.GET.get('username')

  already_activated = False
  user_exists = False
  if (uname == new_user):
    try:
      User.objects.get(username=uname)
      user = User.objects.get(username=uname)
      user_exists = True
    except User.DoesNotExist:
      return render(request, 'myLogin/confirm_activation.html', {'user': user, 'is_active': already_activated, 'user_exists': user_exists})

    if(user.is_active and user.is_staff):
      already_activated = True
    else:
      user.is_active = True
      user.is_staff = True
      user.save()
    return render(request, 'myLogin/confirm_activation.html', {'user': user, 'is_active': already_activated, 'user_exists': user_exists})

  else:
    user_exists = False
    return render(request, 'myLogin/confirm_activation.html', {'is_active': already_activated, 'user_exists': user_exists})


def login_template(request):
  if(request.user.is_authenticated()):
    return redirect('/myLogin/logged_in/')
  if(request.method == 'GET'):
    form = LoginForm()
    next_url = request.GET.get('next', '')
    return render(request, 'myLogin/login.html', {'form': form, 'next': next_url})

  if(request.method == 'POST'):
    next_url = request.POST['next']
    form = LoginForm(request.POST)
    if(form.is_valid()):
      uname = form.cleaned_data['username']
      passwd = form.cleaned_data['password']
      user = authenticate(username = uname, password = passwd)
      if(user is not None):
        login(request, user)
        if next_url:
          return redirect(next_url)
        else:
          return redirect('/myLogin/logged_in/')
  return render(request, 'myLogin/login.html', {'form': form})


@login_required (login_url = '/myLogin/')
def logged_in_template(request):
  return render(request, 'myLogin/logged_in.html')


def get_all_users_json(request):
  all_users = User.objects.all()
  data = serializers.serialize("json", all_users, fields=('username'))
  return HttpResponse(data, content_type="application/json")


@login_required (login_url = '/myLogin/')
def logout_view(request):
  logout(request)
  return redirect('/myLogin/')


def send_forgot_password_email(user):
  activation_key = base64_encoder(user.last_name)
  send_mail(
    'Reset Password - Portal', 
    get_template('myLogin/activation_email_template.html').render(
      Context({
        'user': user, 
        'activation_key': activation_key, 
        })
      ), 
    settings.EMAIL_HOST_USER, 
    [user.email], 
    fail_silently=False)



def forgot_password_view(request):
  if(request.user.is_authenticated()):
    return redirect('/myLogin/logged_in/')

  error = False
  mail_sent = False

  if(request.method == 'GET'):
    form = ForgotPasswordForm()
    return render(request, 'myLogin/forgot_password.html', {'form': form, 'error': error, 'mail_sent': mail_sent})

  if(request.method == 'POST'):
    form = ForgotPasswordForm(request.POST)
    if(form.is_valid()):
      mail = form.cleaned_data['email']
      try:
        User.objects.get(email=mail)
        user = User.objects.get(email = mail)
      except User.DoesNotExist:
        error = True
        return render(request, 'myLogin/forgot_password.html', {'error': error, 'mail_sent': mail_sent})
      
      if(user is not None):
        send_forgot_password_email(user)
        mail_sent = True
        return render(request, 'myLogin/forgot_password.html', {'error': error, 'mail_sent': mail_sent})
  return render(request, 'myLogin/login.html', {'form': form})


def reset_password_view(request):
  if(request.user.is_authenticated()):
    return redirect('/myLogin/logged_in/')

  user_exists = True  
  password_reset = False

  if(request.method == 'GET'):
    form = ResetPasswordForm()
    return render(request, 'myLogin/reset_password_template.html', {'form': form, 'password_reset': password_reset, 'user_exists': user_exists})

  if(request.method == 'POST'):
    form = ResetPasswordForm(request.POST)
    uname = request.GET.get('username')
    activation_key = request.GET.get('activation_key')
    print(uname)
    print(activation_key)
    url_last_name = base64_decoder(activation_key)

    if(form.is_valid()):
      new_password = form.cleaned_data['password']
      try:
        User.objects.get(username = uname)
        user = User.objects.get(username = uname)
      except user.DoesNotExist:
        user_exists = False
        return render(request, 'myLogin/reset_password_template.html', {'form': form, 'password_reset': password_reset, 'user_exists': user_exists})
        
      
      if(user is not None):
        if(user.last_name == url_last_name):
          user.set_password(new_password)
          user.save()
          password_reset = True
          return render(request, 'myLogin/reset_password_template.html', {'form': form, 'password_reset': password_reset, 'user_exists': user_exists})
        
  return render(request, 'myLogin/reset_password_template.html', {'form': form, 'password_reset': password_reset, 'user_exists': user_exists})
  