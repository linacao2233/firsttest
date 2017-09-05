from django import forms
from .models import Apart, Comment, University, ContactMe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Field,Div,ButtonHolder,HTML


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


class ContactForm(forms.ModelForm):
	class Meta:
		model = ContactMe
		fields = [
		    "subject",
		    "sender",
		    "body",
		]
		labels = {
		"subject" : "Subject",
		"sender": "Email",
		"body": "Questions",

		}

	#def __init__(self):
	def __init__(self,*args, **kwargs):
		super(ContactForm,self).__init__(*args,**kwargs)

		self.helper = FormHelper()
		self.helper.formtag = False # don't add form tags

		self.helper.form_class = 'container'

		self.helper.layout = Layout(
			HTML("""
				<p> Fill this form to send me messages. </p>
				"""),
			Div(Div(Field("subject",css_class='form-control', placeholder="Subject"),
				css_class="form-group col-sm-12",),
			css_class = 'row',
			),
			Div(Div(Field("sender",css_class='form-control', placeholder="Your email or phone number for us to contact you."),
				css_class='form-group col-sm-12'),
			css_class = 'row'
				),
			Div(Div(Field('body', css_class='form-control', placeholder="Your questions?"),
				css_class='form-group col-sm-12',
				),
			css_class='row',
			),
			ButtonHolder(
				Submit('send','Send', css_class='btn btn-secondary'),
				),
			HTML("""<p> You can also email me directly at: Email: <email>info@kalias.club</email> </p>
					<p> <address>Address: Electrical and Electronic department,
					 Karadeniz Technical University, Trabzon, Turkey</address> </p>
				"""),
		)

		
class ContactApartOwnerForm(forms.ModelForm):
	class Meta:
		model = ContactMe
		fields = [
		    "subject",
		    "sender",
		    "body",
		]
		labels = {
		"subject" : "Subject",
		"sender": "Email",
		"body": "Questions",
		}

	#def __init__(self):
	def __init__(self,*args, **kwargs):
		super(ContactApartOwnerForm,self).__init__(*args,**kwargs)

		self.helper = FormHelper()
		self.helper.formtag = False # don't add form tags

		self.helper.form_class = 'container'

		self.helper.layout = Layout(
			HTML("""
				<p> questions about this apartment? email the owner. </p>
				"""),
			Div(Div(Field("subject",css_class='form-control', placeholder="Subject"),
				css_class="form-group col-sm-12",),
			css_class = 'row',
			),
			Div(Div(Field("sender",css_class='form-control', placeholder="Your email or phone number for us to contact you."),
				css_class='form-group col-sm-12'),
			css_class = 'row'
				),
			Div(Div(Field('body', css_class='form-control', placeholder="Your questions?"),
				css_class='form-group col-sm-12',
				),
			css_class='row',
			),
			ButtonHolder(
				Submit('send','Send', css_class='btn btn-secondary'),
				),
		)
