from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
from django.contrib.gis.db.models import PointField

from django.utils import timezone

#from django_google_maps import fields as map_fields
#from djgeojson.fields import PointField

class ApartFeatures(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Apart(models.Model):
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=300, editable=False)

	description = models.TextField()
	iconpic = models.ImageField(null=True, blank=True)

	address=models.CharField(max_length=255, default='KTU')

	#location = GeopositionField(max_length=100, null=True, blank=True)
	location2 = PointField(null=True,blank=True)
	phonenumber = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=254,null=True, blank=True)
	facebooklink = models.URLField(null=True, blank=True)
	officalweblink = models.URLField(null=True, blank=True)

	starlevel = models.FloatField()

	#features 
	# male or female
	gender = models.CharField(max_length=2,
		choices=[('m','Erkek'),('f','Kiz'), ('mf', 'Erkek and Kiz'),
		('n', 'Not Sure')],
		default='n',
		)
	numberOfPeoplePerRoom = models.PositiveSmallIntegerField(null=True,blank=True)
	#StudyDesk = models.BooleanField(help_text='study desk for each person?')


	numberofrooms = models.PositiveSmallIntegerField(null=True, blank=True, 
		help_text='how many rooms do you have in total?')
	numberofstudents = models.PositiveSmallIntegerField(null=True, blank=True,
		help_text='how many students can you host in total?')
	roomsperbath = models.PositiveSmallIntegerField(default=3, 
		help_text='how many rooms share on bathroom?')
	apartfeatures = models.ManyToManyField(ApartFeatures)




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

class ApartImage(models.Model):
	apart = models.ForeignKey(Apart)
	image = models.ImageField(upload_to='apartimage/%Y/%m/%d')
	thumbnail = models.ImageField(upload_to='apartimage/%Y/%m/%d', null=True,
		blank=True)

	def create_thumbnail(self):
	    # original code for this method came from
	    # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

	    # If there is no image associated with this.
	    # do not create thumbnail
	    if not self.image:
	        return

	    from PIL import Image
	    from cStringIO import StringIO
	    from django.core.files.uploadedfile import SimpleUploadedFile
	    import os

	    # Set our max thumbnail size in a tuple (max width, max height)
	    THUMBNAIL_SIZE = (99, 66)

	    DJANGO_TYPE = self.image.file.content_type

	    if DJANGO_TYPE == 'image/jpeg':
	        PIL_TYPE = 'jpeg'
	        FILE_EXTENSION = 'jpg'
	    elif DJANGO_TYPE == 'image/png':
	        PIL_TYPE = 'png'
	        FILE_EXTENSION = 'png'

	    # Open original photo which we want to thumbnail using PIL's Image
	    image = Image.open(StringIO(self.image.read()))

	    # We use our PIL Image object to create the thumbnail, which already
	    # has a thumbnail() convenience method that contrains proportions.
	    # Additionally, we use Image.ANTIALIAS to make the image look better.
	    # Without antialiasing the image pattern artifacts may result.
	    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

	    # Save the thumbnail
	    temp_handle = StringIO()
	    image.save(temp_handle, PIL_TYPE)
	    temp_handle.seek(0)

	    # Save image to a SimpleUploadedFile which can be saved into
	    # ImageField
	    suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
	            temp_handle.read(), content_type=DJANGO_TYPE)
	    # Save SimpleUploadedFile into image field
	    self.thumbnail.save(
	        '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
	        suf,
	        save=False
	    )

	def save(self, *args, **kwargs):

		self.create_thumbnail()

		force_update = False

		# If the instance already has been saved, it has an id and we set 
		# force_update to True
		if self.id:
		    force_update = True

		# Force an UPDATE SQL query if we're editing the image to avoid integrity exception
		super(ApartImage, self).save(force_update=force_update)

	def __str__(self):
		return self.apart.title+self.pk


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











