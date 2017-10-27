from django.conf.urls import url

from .views import * 

urlpatterns = [
	url(r'^$', index, name='index'),
    url(r'^(?P<subjectslug>[-\w]+)/$', Videolist, name='videolist'),
    url(r'^(?P<subjectslug>[-\w]+)/(?P<chapterslug>[-\w]+)/(?P<videoslug>[-\w]+)/$', VideoPerSubject, name='videodetail'),
]
