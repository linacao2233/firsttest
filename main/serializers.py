from rest_framework import serializers
from .models import * 
from django.urls import reverse_lazy


class ApartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Apart
		fields = ('id','url','title','description','iconpic', 
			'location','rating','numberofcomments')

	location = serializers.ReadOnlyField(source='location2.tuple')
	url = serializers.ReadOnlyField(source="get_absolute_url")
	rating = serializers.ReadOnlyField(source="starlevel")
	numberofcomments=serializers.ReadOnlyField(source="comment_set.count")


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment

		fields = ('id','createdname', 'created_by','rating','starlevel', 'body', 'modifiedtimesince', 
			'likenumber', 'apart')

	rating = serializers.ReadOnlyField(source='starrating')
	createdname = serializers.ReadOnlyField(source='created_by.username')



			
