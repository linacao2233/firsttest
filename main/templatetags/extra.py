from django import template

register = template.Library()

@register.filter(name='has_feature')
def has_feature(apart,feature):
	pk = feature.pk
	return apart.apartfeatures.filter(pk=pk).exists()