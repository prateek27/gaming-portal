from django.conf.urls import patterns, include, url
from myLogin.views import signup_template, activate_user, login_template, logged_in_template, get_all_users_json, logout_view, forgot_password_view, reset_password_view



urlpatterns = patterns('',
  url(r'^signup/$', signup_template),
  url(r'^user_graph/$', get_all_users_json),
  url(r'^confirm/', activate_user),
  url(r'^$',login_template),
  url(r'^logged_in/$', logged_in_template),
  url(r'^logout/$', logout_view),
  url(r'^forgot_password/$', forgot_password_view),
  url(r'^reset_password/', reset_password_view)
)