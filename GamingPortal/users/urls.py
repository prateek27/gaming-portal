from django.conf.urls import patterns, include, url
from django.contrib import admin
from users.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GamingPortal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^',user_profile_view,name="user_profile_view"),
 	url(r'^all/',all_users_view,name="all_users_view"),
       
)
