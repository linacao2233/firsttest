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

from django.conf.urls.static import static
from django.conf import settings

from . import views as mainviews
from . import ajaxviews as ajaxviews

urlpatterns = [
    url(r'^$', mainviews.index, name='home'),
    url(r'^list/$', mainviews.list2, name='list'),
    url(r'^filterapart/$', mainviews.list, name='filterapart'),
    url(r'^help/$', mainviews.helppage, name='helppage'),

    # testing views
    #url(r'^list2/$', mainviews.list2, name='list2'),

    url(r'^contact/(?P<slug>[-\w]+)/$', mainviews.ContactPage, name='contact'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/$', mainviews.userProfile, name='userprofile'),

# apart create, update, detail, delete views
    url(r'^newapart/$', mainviews.CreateApart, name='create'),
    url(r'^createapart/$', mainviews.ApartCreateView.as_view(), 
        name='createapart'),    
    url(r'^updateapart/(?P<slug>[-\w]+)/$', mainviews.ApartUpdateView.as_view(), 
        name='updateview'),
    url(r'^uploadimage/(?P<slug>[-\w]+)/$', mainviews.uploadapartpic, 
        name='uploadpic'),

    # list views for searching perpose 
    #url(r'^propertylist/$', mainviews.propertylist, name='propertylist'),

    url(r'^propertylist(?:/(?P<city>[-\w]+))?(?:/(?P<university>[-\w]+))?/$',
        mainviews.apartlist, name='apartlist'),


    url(r'^comparison/$', mainviews.ComparisonApart, name='comparison'),

 #   url(r'^ajax/commentsave/$', mainviews.commentsSave, name='commentsave'),
    url(r'^(?P<slug>[-\w]+)/$', mainviews.ApartDetail, name='detail'),

    url(r'^ajax/apartlist/$', ajaxviews.apartlist.as_view(), name='ajaxlist'),
    url(r'^ajax/commentslist/$', ajaxviews.CommentList.as_view(), name='commentlist'),
    url(r'^ajax/visitedapartlist/$', ajaxviews.visitedApart.as_view(), name='ajaxvisitedlist'),

    url(r'^ajax/apart/(?P<pk>[0-9]+)/$', ajaxviews.ApartDetail.as_view()),
    url(r'^roomtypes/(?P<pk>[0-9]+)/$', mainviews.roomtypedetail, name="roomtypedetail"),

    # ajax thumbs up down share views
    url(r'^ajax/thumbsup/(?P<pk>[0-9]+)/$', ajaxviews.thumbsup, name="thumbsup"),
    url(r'^ajax/thumbsdown/(?P<pk>[0-9]+)/$', ajaxviews.thumbsdown, name="thumbsdown"),
    url(r'^ajax/shareaparts/(?P<pk>[0-9]+)/$', ajaxviews.shareaparts, name="shareaparts"),
    url(r'^ajax/likeup(?:/(?P<pk>[0-9]+))?/$', ajaxviews.commentLikeUp, name="likeup"),
    url(r'^ajax/commentdetail/(?P<pk>[0-9]+)/$', ajaxviews.commentDetail.as_view(), 
        name="commentupdate"),

# language setting
]


