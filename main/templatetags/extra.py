from django import template
from main.models import University

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