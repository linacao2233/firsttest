from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
from django.contrib.gis.db.models import PointField

from django.utils import timezone

#from django_google_maps import fields as map_fields
#from djgeojson.fields import PointField

class Apart(models.Model):
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=300)

	description = models.TextField()
	iconpic = models.ImageField(null=True, blank=True)

	address=models.CharField(max_length=255, default='KTU')

	#location = GeopositionField(max_length=100, null=True, blank=True)
	location2 = PointField(null=True,blank=True)
	phonenumber = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=254,null=True, blank=True)

	numberofrooms = models.PositiveSmallIntegerField(null=True, blank=True, 
		help_text='how many rooms do you have in total?')
	numberofstudents = models.PositiveSmallIntegerField(null=True, blank=True,
		help_text='how many students can you host in total?')
	roomsperbath = models.PositiveSmallIntegerField(default=3, 
		help_text='how many rooms share on bathroom?')

	facebooklink = models.URLField(null=True, blank=True)
	officalweblink = models.URLField(null=True, blank=True)

	starlevel = models.FloatField()

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

	    super(Apart, self).save(*args, **kwargs)

	def create_slug(self, initial_slug, i = 1):
	    if not i==1:
	            initial_slug += "-%s" % (i, )
	    return initial_slug


class Comment(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	ipaddress = models.CharField(max_length=100, null=True, blank=True)
	starlevel = models.PositiveSmallIntegerField(
		choices=[(1,1),(2,2),(3,3),(4,4),(5,5)],
		default=1,
		)
	body = models.TextField(null=True,blank=True)

	createdTime = models.DateTimeField(auto_now_add=True)
	modifiedTime = models.DateTimeField(auto_now_add=True)

	apart = models.ForeignKey(Apart)

	def __str__(self):
		return self.owner.username+'-'+self.apartment.title

	def save(self, *args, **kwargs):
		self.modifiedTime = timezone.now()

		super(Comment,self).save(*args, **kwargs)










