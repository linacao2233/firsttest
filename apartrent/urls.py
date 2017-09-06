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
from main import ajaxviews as ajaxviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', mainviews.index, name='home'),
    url(r'^list/$', mainviews.list, name='list'),
    # testing views
    url(r'^list2/$', mainviews.list2, name='list2'),

    url(r'^contact/$', mainviews.ContactPage, name='contact'),
    url(r'^accounts/', include('allauth.urls')),


    url(r'^newpart/$', mainviews.CreateApart, name='create'),
    url(r'^comparison/$', mainviews.ComparisonApart, name='comparison'),

    url(r'^ajax/commentsave/$', mainviews.commentsSave, name='commentsave'),
    url(r'^(?P<slug>[-\w]+)/$', mainviews.ApartDetail, name='detail'),

    url(r'^ajax/apartlist/$', ajaxviews.apartlist.as_view(), name='ajaxlist'),
    url(r'^ajax/apart/(?P<pk>[0-9]+)/$', ajaxviews.ApartDetail.as_view()),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


