from django.shortcuts import render

from .models import Apart, Comment, University, UniversityGate
from .forms import ApartForm, CommentForm, MainSearchForm

from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse

# Create your views here.

def index(request):
	template='main/index.html'

	ulist = University.objects.all()

	context = {
	'universitylist': ulist,

	}

	return render(request, template, context)

def list(request):
	template = 'main/list.html'

	if request.GET:
		universityname = request.GET.get('university').split(',')[0]
		university = University.objects.get(title=universityname)

		gatelist = university.universitygate_set.all()

		universitygate = gatelist[0]

		gender = request.GET.get('gender')

		if gender=='Kiz':
			genders = ['f','mf', 'n']
		else:
			genders = ['m', 'mf', 'n']

		apartlist = Apart.objects.filter(location2__distance_lte=
			(universitygate.location, 5000)).filter(
			gender__in=genders)
		print('here I am')
	else:
		apartlist = Apart.objects.all()
		gatelist = UniversityGate.objects.all()

	apikey = settings.GOOGLE_MAPS_API_KEY

	context = {
	'apartlist': apartlist,
	'gatelist': gatelist,
	'googleapikey': apikey,
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def commentsSave(request):
	if request.method == 'POST':
		body = request.POST['body']
		rating = request.POST['rating']
		print(body)
		if body:
			apart = Apart.objects.get(slug=request.POST['postid'])

			if request.user.is_authenticated:
				comment = Comment(
					body=body, 
					apart=apart,
					created_by = request.user,
					modifiedTime = timezone.now(),
					starlevel=rating,
					)
			else:
				ipaddress = get_client_ip(request)
				comment = Comment(
					body=body, 
					apart=apart,
					ipaddress = request.user,
					modifiedTime = timezone.now(),
					starlevel=rating,
					)


			comment.save()

			returncomment = {
			'body': body,
			'created_by': request.user.username,
			'created_on': 'now',
			}

			return JsonResponse(returncomment)
	else:
		return HttpResponse('no comments input')


def ComparisonApart(request):
	#template='main/apartdetail.html'

	template = 'main/comparison.html'

	if request.GET:
		apartlist = request.GET['apartlist']
	else:
		apartlist = ''

	apartToCompare = Apart.objects.filter(slug__in=apartlist)
	apikey = settings.GOOGLE_MAPS_API_KEY

	context={
	'apartlist': apartToCompare,
	'googleapikey': apikey,
	}

	return render(request,template, context)




