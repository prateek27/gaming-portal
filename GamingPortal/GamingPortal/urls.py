from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GamingPortal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^',include('login.urls')),
    url(r'^',include('home.urls')),
    url(r'^games/',include('games.urls')),
    url(r'^users',include('users.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
