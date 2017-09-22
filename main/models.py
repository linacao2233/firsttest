from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
from django.contrib.gis.db.models import PointField

from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from django.core.files.storage import default_storage as storage

from django.urls import reverse_lazy
from django.utils.translation import ugettext as _


#from django_google_maps import fields as map_fields
#from djgeojson.fields import PointField


class ApartFeatures(models.Model):
	name = models.CharField(max_length=50)
	priority = models.PositiveSmallIntegerField(choices=[(1,1),(2,2),(3,3)],
		help_text=_("1 is the highest (most important)"), default=1)
	note = models.CharField(max_length=50, null=True, blank=True)
	category = models.CharField(max_length=10,
		choices=[('room','oda'),('floor','kat'),('building','bina')],
		default='building')

	def __str__(self):
		return self.name


class RoomType(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()

	numberOfPeoplePerRoom = models.PositiveSmallIntegerField(default=2)
	restroomnumber = models.PositiveIntegerField(default=2)
	restroomtype = models.CharField(max_length=20,
		choices=[('1',_('In room')),('2',_('2 rooms share')),('3',_('3 rooms share')),
		('4', _('> 3 rooms share'))], default='3')
	showernumber = models.PositiveSmallIntegerField(default=1)
	showertype = models.CharField(max_length=20,
		choices=[('1',_('In room')),('2',_('2 rooms share')),('3',_('3 rooms share')),
		('4', _('3 to 6 rooms share')), ('5', _('>6 rooms share'))], 
		default='3')
	kitchen = models.CharField(max_length=20,
		choices=[('0', _('no kitchen')),('1',_('In room')),('2',_('2 rooms share')),('3',_('3 rooms share')),
		('4', _('> 3 rooms share'))], 
		default='3')
	livingroom = models.CharField(max_length=2,
		choices=[('0', _('no livingroom')),('1',_('In room')),('2',_('2 rooms share')),('3',_('3 rooms share')),
		('4', _('> 3 rooms share'))],
		default='3')

	def __str__(self):
		return self.name


def icon_image_url(instance,filename):
	fileurl = instance.title
	filenameextension = filename.split('.')[-1]

	savefilename = 'iconpic.'+filenameextension

	return 'apartimage/{0}/{1}'.format(fileurl,savefilename)

class Apart(models.Model):
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=300, editable=False)

	description = models.TextField(blank=True)

	iconpic = models.ImageField(upload_to=icon_image_url, blank=True,null=True)

	address=models.CharField(max_length=255, default='KTU')

	#location = GeopositionField(max_length=100, null=True, blank=True)
	location2 = PointField(null=True,blank=True)
	mainphonenumber = PhoneNumberField(blank=True,null=True,default='+90')
	phonenumber = models.CharField(max_length=100,null=True, blank=True)
	email = models.EmailField(max_length=254,null=True, blank=True)
	facebooklink = models.URLField(null=True, blank=True)
	officalweblink = models.URLField(null=True, blank=True)

	pricelow = models.FloatField(blank=True,null=True)
	pricehigh = models.FloatField(blank=True,null=True)

	# favorite session like or not
	#--------------------------------

	starlevel = models.FloatField(default=0)
	thumbsup = models.PositiveIntegerField(default=0)
	thumbsdown = models.PositiveIntegerField(default=0)
	sharenumbers = models.PositiveIntegerField(default=0)
	#---------------------------------

	likedby = models.ManyToManyField(User, related_name='likedaparts',
		blank=True, editable=False)
	dislikedby = models.ManyToManyField(User, 
		related_name='dislikedaparts',blank=True, editable=False)
	visitedby = models.ManyToManyField(User, 
		related_name='visitedaparts',blank=True, editable=False)
	sharedby = models.ManyToManyField(User, 
		related_name='sharedaparts', blank=True, editable=False)
	ownedby = models.ForeignKey(User, related_name='apart', blank=True, null=True)

	#--------------------------------------

	#features 
	# male or female
	gender = models.CharField(max_length=2,
		choices=[('m',_('Boy')),('f',_('Girl')), ('mf', _('Both Girl and Boy')),
		('n', _('Not Sure'))],
		default='n',
		)
	numberOfPeoplePerRoom = models.CharField(max_length=50,null=True,
		blank=True, help_text=_("enter in this format: 1,2,3"))

	#StudyDesk = models.BooleanField(help_text='study desk for each person?')

	roomsperbath = models.FloatField(null=True, blank=True,
		editable=False)


	numberofrooms = models.PositiveSmallIntegerField(null=True, blank=True, 
		help_text=_('how many rooms do you have in total?'))

	roomtype = models.ManyToManyField(RoomType, blank=True, null=True)

	numberofstudents = models.PositiveSmallIntegerField(null=True, blank=True,
		help_text=_('how many students can you host in total?'))


	apartfeatures = models.ManyToManyField(ApartFeatures, 
		blank=True)


	allowcomments = models.BooleanField(default=True, 
		help_text=_('allow to be commented or not?'))

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
	    if self.slug is None or self.slug == '':
	        self.slug = slugify(self.title)

	    i = 1
	    while True:
	        created_slug = self.create_slug(self.slug, i)
	        slug_count = Apart.objects.filter(slug__exact=
	                created_slug).exclude(pk=self.pk)
	        if not slug_count:
	                break
	                i+1

	    self.slug = created_slug
	    #self.modified_on = datetime.now()

	    # add description default to be title
	    if self.description is None or self.description == '':
	    	self.description = self.title


	    super(Apart, self).save(*args, **kwargs)

	def create_slug(self, initial_slug, i = 1):
	    if not i==1:
	            initial_slug += "-%s" % (i, )
	    return initial_slug

	def get_absolute_url(self):
		return reverse_lazy('detail',kwargs={'slug': self.slug})


class Comment(models.Model):
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

	apart = models.ForeignKey(Apart)

	def __str__(self):
		return self.owner.username+'-'+self.apartment.title

	def save(self, *args, **kwargs):
		self.modifiedTime = timezone.now()

		super(Comment,self).save(*args, **kwargs)


def apart_image_path(instance,filename):
	apartname = instance.apart.title
	return 'apartimage/{0}/{1}'.format(
		apartname, filename)


class ApartImage(models.Model):
	apart = models.ForeignKey(Apart)
	image = models.ImageField(upload_to=apart_image_path)
	thumbnail = models.ImageField(upload_to=apart_image_path, null=True,
		blank=True, editable=False)

	def __str__(self):
		return self.apart.title

	def save(self, *args, **kwargs):
		if not self.thumbnail:
			self.create_thumbnail()
		super(ApartImage, self).save(*args, **kwargs)

	def create_thumbnail(self):
		"""
		Create and save the thumbnail for images

		"""
		from PIL import Image
		import os
		from io import BytesIO
		from django.core.files.base import ContentFile


		DJANGO_TYPE = self.image.file.content_type

		if DJANGO_TYPE == 'image/jpeg':
		    PIL_TYPE = 'jpeg'
		    FILE_EXTENSION = 'jpg'
		elif DJANGO_TYPE == 'image/png':
		    PIL_TYPE = 'png'
		FILE_EXTENSION = 'png'

		image = Image.open(self.image)


		image.thumbnail((128,128), Image.ANTIALIAS)

		thumbname, thumb_extension = os.path.splitext(self.image.name)
		thumb_filename = thumbname+'_thumb' + thumb_extension

		temp_thumb = BytesIO()
		image.save(temp_thumb, PIL_TYPE)
		temp_thumb.seek(0)

		self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)

		temp_thumb.close()






class University(models.Model):
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=300, editable=False, null=True)

	city = models.CharField(max_length = 200)

	def save(self, *args, **kwargs):
		if self.slug is None or self.slug == '':
			self.slug = slugify(self.title)

	    # check whether there is duplicate slugs
		slug_count = University.objects.filter(slug__exact=
	                self.slug).exclude(pk=self.pk)

		if slug_count:
			self.slug += self.pk
		
		super(University, self).save(*args, **kwargs)



	def __str__(self):
		return self.title

		

class UniversityGate(models.Model):
	title = models.CharField(max_length=200)
	location = PointField()
	university = models.ForeignKey(University)

	def __str__(self):
		return self.title


class ContactMe(models.Model):
	subject = models.CharField(max_length=200)
	sender = models.CharField(max_length=200)
	receiver = models.CharField(max_length=300)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)


class FrequentlyAskedQuestions(models.Model):
	question = models.CharField(max_length=200)
	answer = models.TextField()

	def __str__(self):
		return self.question











