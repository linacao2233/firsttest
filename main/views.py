from django.shortcuts import render

from .models import Apart, Comment
from .forms import ApartForm, CommentForm

from django.conf import settings
# Create your views here.

def home(request):
	template = 'main/list.html'

	apartlist = Apart.objects.all()

	context = {
	'apartlist': apartlist,
	}

	return render(request, template, context)


def CreateApart(request):
	template = 'main/apartform.html'

	if request.POST:
		form = ApartForm(request.POST)
	else:
		form = ApartForm(None)

	context = {
	'form': form,
	}
	return render(request, template, context)


def ApartDetail(request, slug):
	template='main/apartdetail.html'

	apart = Apart.objects.get(slug=slug)

	comments = Comment.objects.filter(apart=apart).order_by('modifiedTime')

	form = CommentForm(None)

	context = {
	'apart': apart,
	'comments': comments,
	'form': form,
	'apikey': settings.GOOGLE_MAPS_API_KEY,
	}

	return render(request, template, context)





