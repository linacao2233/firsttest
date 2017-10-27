from django.shortcuts import render, redirect
from django.db.models import Q

from .models import *
from dormrent.models import Apart
from .forms import *

from onlinelearning.models import Subjects

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

	subjects = Subjects.objects.all()[:3]


	#ulist = University.objects.all()
	# patterlist = []
	# for university in ulist:
	# 	patterlist.append(university.title + ', '+university.city)

	# pattern = '|'.join(patterlist)

	context = {
	'subjects': subjects,
	# 'universitylist': ulist,
	# 'matchingpattern': pattern,
	}

	return render(request, template, context)



def ContactPage(request, slug):
	template='main/contact.html'

	title = _('contact me')
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
			if 'subject' in request.GET:
				if request.GET.get('subject') == 'Claim':
					subject = 'Claim ownership: '+ apart.title
				elif request.GET.get('subject') == 'Report':
					subject = 'Report Problem: '+ apart.title
				else:
					subject = request.GET.get('subject') +': ' + apart.title

				recipients = ['lncao6@gmail.com']

			else:					
				subject = 'email from yurtkayisla '
				recipients = [apart.email]

			confirm_message = 'thanks for the message'
			sender = form.cleaned_data['sender']
			message = 'from:'+ form.cleaned_data['sender'] + '\n' + form.cleaned_data['body']
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






