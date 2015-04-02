from django.conf.urls import patterns, include, url
from django.contrib import admin
from login.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GamingPortal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$',login_view,name="login_view"),
    url(r'^logout/$',logout_view,name="logout_view"),
)
