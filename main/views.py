from django.shortcuts import render, redirect

from .models import *
from .forms import ApartForm,ImageFormHelper, CommentForm, MainSearchForm,ContactForm, ContactApartOwnerForm, ImageFormSet

from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.utils.translation import ugettext as _

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
		if 'apart' in request.GET:
			apartname = request.GET.get('apart')

			apartlist = Apart.objects.filter(title__icontains=apartname)

			if apartlist.count() == 1 :
				url = reverse_lazy('detail', kwargs={'slug':apartlist[0].slug})
				return redirect(url)

	else:
		apartlist = Apart.objects.all()

	apikey = settings.GOOGLE_MAPS_API_KEY

	context = {
	'apartlist': apartlist,
	'googleapikey': apikey,
	}

	return render(request, template, context)

def list2(request):
	template = 'main/listajax.html'

	if request.GET:
		if 'university' in request.GET: 
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

	else:
		gatelist = UniversityGate.objects.all()
		location = gatelist[0].location

	apikey = settings.GOOGLE_MAPS_API_KEY

	context = {
	'gatelist': gatelist,
	'googleapikey': apikey,
	'location': location,
	}

	return render(request, template, context)


# list of aparts by clicking tree
def apartlist(request, city=None, university=None):
	"""
	get the list of properties by the name of city and universities
	input:
	'city': name of city, string
	'university': University slug, string
	"""

	template = 'main/apartlist.html'

	apartlist = None
	cities = None
	universities = None
	universityobject = None

	#if request.GET:
	if 'sortby' in request.GET:
		sortpara = request.GET.get('sortby')
	else:
		sortpara = '-starlevel'

	if university:
		universityobject = University.objects.get(slug=university)
		gate = universityobject.universitygate_set.all()[:1].get()
		apartlist = Apart.objects.filter(location2__distance_lte=
				(gate.location,5000)).order_by(sortpara)
		city = universityobject.city
	else:
		if city:
			universities = University.objects.filter(city__icontains=city).order_by('title')
		else:
			cities = University.objects.values_list('city', 
					flat=True).distinct().order_by('city')

	context = {
	'apartlist': apartlist,
	'cities': cities,
	'universities': universities,
	'city': city,
	'universityobject': universityobject,
	}


	return render(request, template, context)


def propertylist(request):
	template = 'main/propertylist.html'

	cities = University.objects.values_list('city', flat=True).distinct().order_by('city')

	context = {
	'cities': cities,
	}

	return render(request, template, context)
# apart create, update, detail, delete pages

def CreateApart(request):
	template = 'main/apartform.html'

	if request.POST:
		form = ApartForm(request.POST)
		imageform = ImageFormSet(request.POST)

		if form.is_valid() and imageform.is_valid():
			form.save()
			imageform.save()
			print('saved')
	else:
		form = ApartForm(None)
		imageform = ImageFormSet(None)
	
	imageformhelper = ImageFormHelper

	context = {
	'form': form,
	'imageform': imageform,
	'imageformhelper': imageformhelper,
	}
	return render(request, template, context)


class ApartCreateView(CreateView):
	model = Apart
	form_class = ApartForm
	template_name = 'main/apartform.html'



class ApartUpdateView(UpdateView):
	model = Apart
	form_class = ApartForm
	template_name = 'main/apartform.html'


def uploadapartpic(request,slug):
	apart = Apart.objects.get(slug=slug)

	if request.POST:
		form = ImageFormSet(request.POST, request.FILES, instance=apart)
		if form.is_valid():
			form.save()
			#return HttpResponseRedirect(apart.get_absolute_url())
	
	form = ImageFormSet(instance = apart)

	template='main/uploadpic.html'
	context = {
	'form':form,
	'apart': apart,
	}

	return render(request, template, context)




def ApartDetail(request, slug):
	template='main/apartdetail.html'

	apart = Apart.objects.get(slug=slug)

	rating =' ' *round(apart.starlevel)
	norating = ' ' * (5-round(apart.starlevel))
	

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
		request.user.visitedaparts.add(apart)

	try:
		sessionvisitedlist = request.session['visited']
		sessionvisitedlist.append(apart.slug)
	except:
		sessionvisitedlist = [apart.slug]
		#request.session['visited'] = apart.pk

	request.session['visited'] = sessionvisitedlist
	print(request.session['visited'])

		

	context = {
	'apart': apart,
	'rating': rating,
	'norating': norating,
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
		apartlist = request.GET.get('apartlist').split(',')[0:-1]
		print(apartlist)
	else:
		apartlist = ''

	apartToCompare = Apart.objects.filter(pk__in=apartlist)
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


def ContactPage(request, slug):
	template='main/contact.html'

	title = 'contact me'
	confirm_message = None
	
	if slug=='me':
		form = ContactForm(request.POST or None)


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

	else:
		form = ContactApartOwnerForm(request.POST or None)
		apart = Apart.objects.get(slug=slug)

		if form.is_valid():
			subject = 'email from yurtkayisla '
			confirm_message = 'thanks for the message'
			sender = form.cleaned_data['sender']
			recipients = [apart.email]
			send_mail(subject, message, sender, recipients)

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


def roomtypedetail(request, pk):
	template = 'main/roomtypedetail.html'
	roomtype = RoomType.objects.get(pk=pk)
	print(roomtype)

	context = {
	'roomtype': roomtype,
	}

	return render(request, template, context)



def helppage(request):
	template = 'main/helppage.html'
	questions = FrequentlyAskedQuestions.objects.all()

	context = {
	'questions': questions,
	}

	return render(request, template, context)


@login_required
def userProfile(request):
	user = request.user

	template = 'main/userprofile.html'

	context = {
	'user': user,
	}

	return render(request, template, context)






