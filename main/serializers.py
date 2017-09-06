from rest_framework import serializers
from .models import * 

class ApartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Apart
		fields = ('id','slug','title','description','iconpic', 
			'location')

	location = serializers.ReadOnlyField(source='location2.tuple')
