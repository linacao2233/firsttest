from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
from django.contrib.gis.db.models import PointField

from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from django.urls import reverse_lazy

#from django_google_maps import fields as map_fields
#from djgeojson.fields import PointField


class ApartFeatures(models.Model):
	name = models.CharField(max_length=50)
	priority = models.PositiveSmallIntegerField(choices=[(1,1),(2,2),(3,3)],
		help_text="1 is the highest (most important)", default=1)
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
		choices=[('1','In room'),('2','2 rooms share'),('3','3 rooms share'),
		('4', '> 3 rooms share')], default='3')
	showernumber = models.PositiveSmallIntegerField(default=1)
	showertype = models.CharField(max_length=20,
		choices=[('1','In room'),('2','2 rooms share'),('3','3 rooms share'),
		('4', '3 to 6 rooms share'), ('5', '>6 rooms share')], 
		default='3')
	kitchen = models.CharField(max_length=20,
		choices=[('0', 'no kitchen'),('1','In room'),('2','2 rooms share'),('3','3 rooms share'),
		('4', '> 3 rooms share')], 
		default='3')
	livingroom = models.CharField(max_length=2,
		choices=[('0', 'no livingroom'),('1','In room'),('2','2 rooms share'),('3','3 rooms share'),
		('4', '> 3 rooms share')],
		default='3')

	def __str__(self):
		return self.name


class Apart(models.Model):
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=300, editable=False)

	description = models.TextField(blank=True)
	iconpic = models.ImageField(null=True, blank=True)

	address=models.CharField(max_length=255, default='KTU')

	#location = GeopositionField(max_length=100, null=True, blank=True)
	location2 = PointField(null=True,blank=True)
	mainphonenumber = PhoneNumberField(blank=True,null=True)
	phonenumber = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=254,null=True, blank=True)
	facebooklink = models.URLField(null=True, blank=True)
	officalweblink = models.URLField(null=True, blank=True)

	pricelow = models.FloatField(blank=True,null=True)
	pricehigh = models.FloatField(blank=True,null=True)

	starlevel = models.FloatField(default=0)

	#features 
	# male or female
	gender = models.CharField(max_length=2,
		choices=[('m','Erkek'),('f','Kiz'), ('mf', 'Erkek and Kiz'),
		('n', 'Not Sure')],
		default='n',
		)
	numberOfPeoplePerRoom = models.CharField(max_length=50,null=True,
		blank=True, help_text="enter in this format: 1,2,3")

	#StudyDesk = models.BooleanField(help_text='study desk for each person?')

	roomsperbath = models.FloatField(null=True, blank=True,
		editable=False)


	numberofrooms = models.PositiveSmallIntegerField(null=True, blank=True, 
		help_text='how many rooms do you have in total?')

	roomtype = models.ManyToManyField(RoomType, blank=True, null=True)

	numberofstudents = models.PositiveSmallIntegerField(null=True, blank=True,
		help_text='how many students can you host in total?')


	apartfeatures = models.ManyToManyField(ApartFeatures, 
		blank=True)




	allowcomments = models.BooleanField(default=True, 
		help_text='allow to be commented or not?')

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

def apartimagepath(instance, filename):
	apartid = instance

class ApartImage(models.Model):
	apart = models.ForeignKey(Apart)
	image = models.ImageField(upload_to=apartimagepath)
	thumbnail = models.ImageField(upload_to='apartimage/%Y/%m/%d', null=True,
		blank=True, editable=False)

	def __str__(self):
		return self.apart.title


class University(models.Model):
	title = models.CharField(max_length=200)
	city = models.CharField(max_length = 200)

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











