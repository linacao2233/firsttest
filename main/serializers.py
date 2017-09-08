from rest_framework import serializers
from .models import * 
from django.urls import reverse_lazy

class ApartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Apart
		fields = ('id','url','title','description','iconpic', 
			'location')

	location = serializers.ReadOnlyField(source='location2.tuple')
	url = serializers.ReadOnlyField(source="get_absolute_url")
