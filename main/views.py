from django.shortcuts import render

from .models import *
from .forms import ApartForm, CommentForm, MainSearchForm,ContactForm,ContactApartOwnerForm

from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse

from django.core.mail import send_mail


# Create your views here.

def index(request):
	template='main/index.html'

	ulist = University.objects.all()
	patterlist = []
	for university in ulist:
		patterlist.append(university.title + ', '+university.city)

	pattern = '|'.join(patterlist)

	context = {
	'universitylist': ulist,
	'matchingpattern': pattern,

	}

	return render(request, template, context)


def list(request):
	template = 'main/list.html'

	if request.GET:
		universityname = request.GET.get('university').split(',')[0]
		university = University.objects.get(title=universityname)

		gatelist = university.universitygate_set.all()

		universitygate = gatelist[0]

		#gender = request.GET.get('gender')

		if 'Kiz' in request.GET:
			genders = ['f','mf', 'n']
		else:
			genders = ['m', 'mf', 'n']

		apartlist = Apart.objects.filter(location2__distance_lte=
			(universitygate.location, 5000)).filter(
			gender__in=genders)
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

def list2(request):
	template = 'main/listajax.html'

	if request.GET:
		universityname = request.GET.get('university').split(',')[0]
		university = University.objects.get(title=universityname)

		gatelist = university.universitygate_set.all()

		universitygate = gatelist[0]

		location = universitygate.location
		print(location)

		#gender = request.GET.get('gender')

		if 'Kiz' in request.GET:
			genders = ['f','mf', 'n']
		else:
			genders = ['m', 'mf', 'n']

		apartlist = Apart.objects.filter(location2__distance_lte=
			(universitygate.location, 5000)).filter(
			gender__in=genders)
	else:
		apartlist = Apart.objects.all()
		gatelist = UniversityGate.objects.all()
		location = gatelist[0].location

	apikey = settings.GOOGLE_MAPS_API_KEY

	context = {
	'apartlist': apartlist,
	'gatelist': gatelist,
	'googleapikey': apikey,
	'location': location,
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
	gatelist = UniversityGate.objects.filter(location__distance_lte=(apart.location2,5000))

	form = CommentForm(None)
	contactform = ContactApartOwnerForm(None)

	featureToCompare = ApartFeatures.objects.filter(priority=1).order_by('note')

	criticalfeatures = []

	for num in range(10):
		features = featureToCompare.filter(note__icontains=num)
		if features:
			note = features[0].note.split('_')[1]
			criticalfeatures.append({
				'category': note,
				'features': features,
				})

	otherfeatures = ApartFeatures.objects.exclude(priority=1)

	# add to visited history
	if request.user.is_authenticated: 
		pass

	try:
		request.session['visited'].append(apart.slug)
	except:
		request.session['visited'] = [apart.slug]
		

	context = {
	'apart': apart,
	'comments': comments,
	'form': form,
	'contactform': contactform,
	'apikey': settings.GOOGLE_MAPS_API_KEY,
	'criticalfeatures': criticalfeatures,
	'otherfeatures': otherfeatures,
	'gatelist': gatelist,
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
		apartlist = request.GET.get('apartlist').split(',')
	else:
		apartlist = ''

	apartToCompare = Apart.objects.filter(title__in=apartlist)
	if apartToCompare:
		gatelist = UniversityGate.objects.filter(location__distance_lte=(
			apartToCompare[0].location2,10000))
	else:
		gatelist = ''

	apikey = settings.GOOGLE_MAPS_API_KEY

	featureToCompare = ApartFeatures.objects.filter(priority=1).order_by('note')

	featurestosend = []

	for num in range(10):
		features = featureToCompare.filter(note__icontains=num)
		if features:
			note = features[0].note.split('_')[1]
			featurestosend.append({
				'category': note,
				'features': features,
				})


	context={
	'apartlist': apartToCompare,
	'googleapikey': apikey,
	'featureslist': featurestosend,
	'gatelist': gatelist,
	}

	return render(request,template, context)


def ContactPage(request):
	template='main/contact.html'

	title = 'contact me'
	form = ContactForm(request.POST or None)
	confirm_message = None

	if form.is_valid():
		subject = 'email from mysite:' + form.cleaned_data['subject']
		message = 'from: ' + form.cleaned_data['sender'] +'\n'+form.cleaned_data['body']

		confirm_message = 'thanks for the message'
		sender = form.cleaned_data['sender']
		recipients = ['lina.cao.ktu@gmail.com']


		send_mail(subject, message, sender, recipients)
		send_mail('site message received', '',sender, ['lncao6@gmail.com'])
		
		contactme = ContactMe(
			subject=subject,
			sender=form.cleaned_data['sender'],
			body=form.cleaned_data['body'],
			receiver=recipients[0])

		contactme.save()

	context = {
	'contactform': form,
	'title': title,
	'message': confirm_message,
	}

	return render(request, template, context)	





