from django.conf.urls import patterns, include, url
from django.contrib import admin
from home.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GamingPortal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^',home_view,name="home_view"),
    url(r'^about/$',about_view,name="about_view"),
    url(r'^users/$',users_view,name="users_view"),
)
