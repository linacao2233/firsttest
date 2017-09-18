from django import forms

class extendMultiInputCheckboxWidget(forms.CheckboxSelectMultiple):
	class Media: 
		css = {
		'all': ('css/forms.css',),
		}

	