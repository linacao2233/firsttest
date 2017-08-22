from django import forms
from .models import Apart, Comment, University

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Field,Div

class ApartForm(forms.ModelForm):
	class Meta:
		model = Apart
		fields = [
		'title',
		'description',
		'location2',
		'phonenumber',
		'email',
		'numberofrooms',
		'numberofstudents',
		'roomsperbath',
		'facebooklink',
		'officalweblink',
		'allowcomments',
		]


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = [
		'starlevel', 
		'body',
		]


class MainSearchForm(forms.Form):
	q = forms.ModelChoiceField(queryset=University.objects.all())


		

