from django import template
from dormrent.models import University

register = template.Library()

@register.filter(name='has_feature')
def has_feature(apart,feature):
	pk = feature.pk
	return apart.apartfeatures.filter(pk=pk).exists()


@register.inclusion_tag('searchnavbar.html', name='universitysearchform')
def universitylist():
	ulist = University.objects.all()
	patterlist = []
	for university in ulist:
		patterlist.append(university.title + ', '+university.city)

	pattern = '|'.join(patterlist)

	return {
	'universitylist': ulist,
	'matchingpattern': pattern,
	}

@register.filter(name='index')
def index(apartlist, i):
	return apartlist[int(i)]

@register.filter(name="ratingstar")
def ratingstar(rating):
	ratingnumber = round(rating)
	filledstar = '<i class="fa fa-star" style="color:orange;"></i>'
	emptystar = '<i class="fa fa-star-o" style="color:orange;"></i>'

	display = filledstar*ratingnumber + emptystar*(5-ratingnumber)

	return display
