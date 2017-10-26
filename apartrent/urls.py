"""apartrent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from main import views as mainviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),  # admin view

# views from main app
    url(r'^$', mainviews.index, name='home'), # home view
    url(r'^help/$', mainviews.helppage, name='helppage'),
    url(r'^contact/(?P<slug>[-\w]+)/$', mainviews.ContactPage, name='contact'),
    url(r'^profile/$', mainviews.userProfile, name='userprofile'),


# dorm app urls
    url(r'^dorm-living/$', include('dormrent.urls'), namespace='dormrent'),

# onlinelearning urls  
    url(r'^learn/$', include('onlinelearning.urls'), namespace='learning'),

# accounts info
    url(r'^accounts/', include('allauth.urls')),

# language setting
    url(r'^i18n/', include('django.conf.urls.i18n')),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


