from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
from django.contrib.gis.db.models import PointField

from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from django.core.files.storage import default_storage as storage

from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import timesince

#from django_google_maps import fields as map_fields
#from djgeojson.fields import PointField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
	"""
	a general comment model which can be used for different models
	"""
	created_by = models.ForeignKey(User, null=True, blank=True)
	ipaddress = models.CharField(max_length=100, null=True, blank=True)
	starlevel = models.PositiveSmallIntegerField(
		choices=[(1,1),(2,2),(3,3),(4,4),(5,5)],
		default=1,
		)
	body = models.TextField(null=True,blank=True)

	createdTime = models.DateTimeField(auto_now_add=True)
	modifiedTime = models.DateTimeField(auto_now_add=True)

	likenumber = models.PositiveIntegerField(default=0)

	# use contenttype genericrelation for multiple models

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	cotent_object = GenericForeignKey('content_type', 'object_id')

	#apart = models.ForeignKey(Apart)

	def __str__(self):
		return self.created_by.username

	def modifiedtimesince(self):
		return timesince(self.modifiedTime)


	def save(self, *args, **kwargs):
		self.modifiedTime = timezone.now()

		super(Comment,self).save(*args, **kwargs)


class ContactMe(models.Model):
	subject = models.CharField(max_length=200)
	sender = models.CharField(max_length=200)
	receiver = models.CharField(max_length=300)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)


class FrequentlyAskedQuestions(models.Model):
	question = models.CharField(max_length=200)
	answer = models.TextField()
	category = models.CharField(max_length=100)

	def __str__(self):
		return self.question











