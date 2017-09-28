from django import forms
from django.forms.models import inlineformset_factory

from .models import Apart, Comment, University, ContactMe, ApartImage

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Field,Div,ButtonHolder,HTML

from phonenumber_field.widgets import PhoneNumberPrefixWidget
from mapwidgets.widgets import GooglePointFieldWidget 

from .widgets import extendMultiInputCheckboxWidget

from django.utils.translation import ugettext_lazy as _




class ApartForm(forms.ModelForm):
	class Meta:
		model = Apart
		fields = ['title','description','address', 'location2',
		'mainphonenumber','email','officalweblink','facebooklink',
		'gender','numberofrooms','numberofstudents','roomtype',
		'apartfeatures']
		# exclude = ['title']
		widgets = {
		'location2': GooglePointFieldWidget,
		'mainphonenumber': PhoneNumberPrefixWidget,
		'apartfeatures': forms.CheckboxSelectMultiple,
		'roomtype': extendMultiInputCheckboxWidget,
		}
		labels = {
		'location2': _('Location'),
		'officalweblink': _('<i class="fa fa-globe"></i> Web address'),
		'facebooklink': _('<i class="fa fa-facebook"></i> Facebook Link'),
		'email': _('<i class="fa fa-envelope-o"></i> Email'),
		'mainphonenumber': _('<i class="fa fa-phone"></i> Phone Number'),
		'title': _('Property Name'),
		'description': _('Description'),
		'address': _('Address'),
		'gender': _('Gender'),
		'numberofrooms': _('Number of Rooms'),
		'numberofstudents': _('Number of Students'),
		'roomtype': _('Type of room'),
		'apartfeatures': _('Amenities'),
		}

	def __init__(self,*args, **kwargs):
		super(ApartForm,self).__init__(*args,**kwargs)

		self.helper = FormHelper()
		self.helper.form_tag = False # don't add form tags

		self.helper.form_class = 'container'

		self.helper.layout = Layout(
			Div(
				Div(Field("title",css_class='form-control'),
				css_class="form-group col-sm-12",),
				Div(Field("description",css_class='form-control'),
				css_class='form-group col-sm-12'),
				Div(Field('address', css_class='form-control'),
				css_class='form-group col-sm-12'),
				Div(Field('location2', css_class='form-control'),
					css_class='form-group col-sm-12'),
				Div(Field("mainphonenumber",css_class='form-control'),
				css_class='form-group col-sm-12 col-md-6'),
				Div(Field("email",css_class='form-control'),
				css_class='form-group col-sm-12 col-md-6'),
				Div(Field("officalweblink",css_class='form-control'),
				css_class='form-group col-sm-12 col-md-6'),
				Div(Field("facebooklink",css_class='form-control'),
				css_class='form-group col-sm-12 col-md-6'),
				Div(Field("gender",css_class='form-control'),
				css_class='form-group col-sm-12 col-md-6'),
				Div(Field("numberofrooms",css_class='form-control'),
				css_class='form-group col-sm-12 col-md-6'),
				Div(Field("numberofstudents",css_class='form-control'),
				css_class='form-group col-sm-12 col-md-6'),
			css_class='row',
			),
			Div(Field("roomtype"),
				Field("apartfeatures"),
				css_class='row'),
		)

class ImageFormHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(ImageFormHelper, self).__init__(*args, **kwargs)
		self.form_tag = False
		self.layout = Layout(
			Field('image',),
			)


ImageFormSet = inlineformset_factory(
	Apart,
	ApartImage,
	fields=('image',),
	extra=1,
	can_delete=True,)


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
