from django.contrib import admin

# Register your models here.
from .models import Apart, Comment
from mapwidgets.widgets import GooglePointFieldWidget 
#from django.contrib.gis.db import models
#from djgeojson.fields import PointField
from django.contrib.gis.db.models import PointField



#from django_google_maps import widgets as map_widgets
#from django_google_maps import fields as map_fields

# class ApartAdminForm(forms.ModelForm):
# 	class Meta:
# 		model= Apart
# 		widgets = {
# 		'location': GeopositionWidget,
# 		}

class ApartAdmin(admin.ModelAdmin):
	list_display = ('title', 
	'description',
	'iconpic',
	'address',
	'location_map',)

	formfield_overrides = {
	PointField: {"widget": GooglePointFieldWidget}
	}

	def location_map(self, instance):
		if instance.location2 is not None:
		    return '<img src="http://maps.googleapis.com/maps/api/staticmap?center=%(latitude)s,%(longitude)s&zoom=%(zoom)s&size=%(width)sx%(height)s&maptype=roadmap&markers=%(latitude)s,%(longitude)s&sensor=false&visual_refresh=true&scale=%(scale)s" width="%(width)s" height="%(height)s">' % {
		        'latitude': instance.location2.y,
		        'longitude': instance.location2.x,
		        'zoom': 15,
		        'width': 100,
		        'height': 100,
		        'scale': 2
		    }
	location_map.allow_tags = True

admin.site.register(Apart,ApartAdmin)
admin.site.register(Comment)