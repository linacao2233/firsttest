from django import forms

from .models import CommentGeneral, ContactMe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Field,Div,ButtonHolder,HTML

from django.utils.translation import ugettext_lazy as _


class CommentForm(forms.ModelForm):
	class Meta:
		model = CommentGeneral
		fields = [
		'starlevel', 
		'body',
		]


class ContactForm(forms.ModelForm):
	class Meta:
		model = ContactMe
		fields = [
		    "subject",
		    "sender",
		    "body",
		]
		labels = {
		"subject" : _("Subject"),
		"sender": _("Email"),
		"body": _("Questions"),
		}




	#def __init__(self):
	def __init__(self,*args, **kwargs):
		super(ContactForm,self).__init__(*args,**kwargs)

		self.helper = FormHelper()
		self.helper.formtag = False # don't add form tags

		self.helper.form_class = 'container'

		self.helper.layout = Layout(
			HTML(_("""
				<p>Fill this form to send me messages. </p>
				""")),
			Div(Div(Field("subject",css_class='form-control', placeholder=_("Subject")),
				css_class="form-group col-sm-12",),
			css_class = 'row',
			),
			Div(Div(Field("sender",css_class='form-control', placeholder=_("Your email or phone number for us to contact you.")),
				css_class='form-group col-sm-12'),
			css_class = 'row'
				),
			Div(Div(Field('body', css_class='form-control', placeholder=_("Your questions?")),
				css_class='form-group col-sm-12',
				),
			css_class='row',
			),
			ButtonHolder(
				Submit('send',_('Send'), css_class='btn btn-secondary'),
				),
			HTML(_("""<p> You can also email me directly at: Email: <email>info@kalias.club</email> </p>
					<p> <address>Address: Electrical and Electronic department,
					 Karadeniz Technical University, Trabzon, Turkey</address> </p>
				""")),
		)

class ContactFormClaim(ContactForm):
	def __init__(self, *args, **kwargs):
		super(ContactFormClaim, self).__init__(*args, **kwargs)

		self.fields['subject'].initial = 'Claim'
		
class ContactApartOwnerForm(forms.ModelForm):
	class Meta:
		model = ContactMe
		fields = [
			"body",
		    "sender",		
		    ]
		labels = {
		"sender": "Email or phone number",
		"body": "question to owner",
		}
		widgets = {
		"body": forms.Textarea(attrs={'rows': 3})
		}

	#def __init__(self):
	def __init__(self,*args, **kwargs):
		super(ContactApartOwnerForm,self).__init__(*args,**kwargs)

		self.helper = FormHelper()
		self.helper.formtag = False # don't add form tags

		self.helper.form_class = 'container'

		self.helper.layout = Layout(
			Div(Div(Field('body', css_class='form-control', placeholder="Your questions?"),
				css_class='form-group col-sm-12',
				),
				Div(Field("sender",css_class='form-control', placeholder=
					"eg: ***@gmail.com"),
				css_class='form-group col-sm-12'),
				css_class = 'row'
				),

			ButtonHolder(
				Submit('send','Send', css_class='btn btn-secondary'),
				),
		)
