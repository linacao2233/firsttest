from django.db import models
from django.template.defaultfilters import slugify

from urllib.parse import urlparse, parse_qs

# Create your models here.


class Subjects(models.Model):
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 300)
	slug = models.SlugField(max_length = 100, editable=False)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if self.slug is None or self.slug == '':
			self.slug = slugify(self.name)

		i = 0
		while True:
			slug_count = Subjects.objects.filter(
				slug__exact=self.slug).exclude(pk=self.pk)
			if not slug_count:
				break
			else:
				i += 1
				self.slug = self.slug + str(i)

		super(Subjects, self).save(*args, **kwargs)


class Chapters(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=100, editable=False, unique=True)
	subject = models.ForeignKey('Subjects', on_delete=models.CASCADE, 
		related_name="chapters")

	def __str__(self):
		return self.subject.name +":"+self.name

	def save(self, *args, **kwargs):
		if self.slug is None or self.slug == '':
			self.slug = slugify(self.name)

		i = 0
		while True:
			slug_count = Chapters.objects.filter(
				slug__exact=self.slug).exclude(pk=self.pk)
			if not slug_count:
				break
			else:
				i += 1
				self.slug = self.slug + str(i)

		super(Chapters, self).save(*args, **kwargs)


class Videos(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=300, editable=False, null=True)
	description = models.TextField(blank=True, null=True)
	youtubeurl = models.URLField()
	youtubevid = models.CharField(max_length=16, editable=False, null=True)
	chapter = models.ForeignKey('Chapters', on_delete = models.CASCADE)

	def __str__(self):
		return self.chapter.subject.name+":"+\
		self.chapter.name + ":" +self.name

	def save(self, *args, **kwargs):
		if self.youtubevid is None or self.youtubevid == '':
			if self.youtubeurl:
				parsed = urlparse(self.youtubeurl)
				try:
					self.youtubevid = parse_qs(parsed.query)['v'][0]
				except:
					pass


		if self.slug is None or self.slug == '':
			self.slug = slugify(self.name)

		i = 0
		while True:
			slug_count = Videos.objects.filter(chapter=self.chapter).filter(
				slug__exact=self.slug).exclude(pk=self.pk)
			if not slug_count:
				break
			else:
				i += 1
				self.slug = self.slug + str(i)

		super(Videos, self).save(*args, **kwargs)


