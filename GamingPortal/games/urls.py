from django.conf.urls import patterns, include, url
from django.contrib import admin
from games.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GamingPortal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',games_view,name="games_view"),
    url(r'(?P<game_name>[a-z,0-9,A-Z,-]+)/$',launch_game_view,name="launch_game_view"),
  )
