from django.shortcuts import render
from .models import Subjects, Videos, Chapters

# Create your views here.

def index(request):
	template = 'onlinelearning/index.html'

	subjects = Subjects.objects.all()


	context = {
	'subjects': subjects,
	}

	return render(request, template, context)


def VideoPerSubject(request,subjectslug,chapterslug,videoslug):
	template = 'onlinelearning/videolist.html'

	subject = Subjects.objects.get(slug=subjectslug)
	chapter = subject.chapters.get(slug=chapterslug)
	video = chapter.videos_set.get(slug=videoslug)

	context = {
	'subject': subject,
	'video': video,
	}

	return render(request, template, context)

def Videolist(request,subjectslug):
	template = 'onlinelearning/videolist.html'

	subject = Subjects.objects.get(slug=subjectslug)
	chapter = subject.chapters.all()[:1].get()
	video = chapter.videos_set.all()[:1]

	context = {
	'subject': subject,
	'video': video,
	}

	return render(request, template, context)

