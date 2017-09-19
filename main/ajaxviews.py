from .models import Apart, University
from .serializers import ApartSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.http import JsonResponse

from django.utils.translation import ugettext as _



# @csrf_exempt
# def apartlist(request):
# 	if request.method == 'GET':
# 		apartlist = Apart.objects.all()
# 		serializer = ApartSerializer(apartlist, many = True)
# 		return JsonResponse(serializer.data, safe=False)

# 	elif request.method == 'POST':
# 		data = JSONParser().parse(request)
# 		serializer = ApartSerializer(data=data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return JsonResponse(serializer.data, status = 201)

# 		return JsonResponse(serializer.errors, status=400)


# @api_view(['GET', 'POST'])
# def apartlist(request):
# 	if request.method == 'GET':
# 		apartlist = Apart.objects.all()
# 		serializer = ApartSerializer(apartlist, many = True)
# 		return Response(serializer.data)

# 	elif request.method == 'POST':
# 		serializer = ApartSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status = status.HTTP_201_CREATED)

# 		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class apartlist(generics.ListCreateAPIView):
	serializer_class = ApartSerializer

	#lookup_url_kwarg= "university"
	
	#ordering = ('-rating',)

	def get_queryset(self):
		if 'university' in self.request.GET:
			#print('university inside')
			universityname = self.request.GET.get('university').split(',')[0]
			university = University.objects.get(title=universityname)

			gatelist = university.universitygate_set.all()

			universitygate = gatelist[0]

		#gender = request.GET.get('gender')

			if 'Kiz' in self.request.GET:
				genders = ['f','mf', 'n']
			else:
				genders = ['m', 'mf', 'n']

			apartlist = Apart.objects.filter(location2__distance_lte=
			(universitygate.location, 5000)).filter(
			gender__in=genders).order_by('-starlevel')
		else:
			apartlist = Apart.objects.all()

		return apartlist

class visitedApart(generics.ListAPIView):
	serializer_class = ApartSerializer

	def get_queryset(self):
		try:
			visited = self.request.session['visited']
			print(visited)
			apartlist = Apart.objects.filter(slug__in=visited)
		except:
			apartlist = []

		return apartlist


class ApartDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Apart.objects.all()
	serializer_class = ApartSerializer


def thumbsup(request, pk):
	apart = Apart.objects.get(pk=pk)

	if request.user.is_authenticated:
		if request.user not in apart.likedby.all():
			apart.likedby.add(request.user)
			apart.thumbsup += 1
			apart.save()
			return JsonResponse({'content':_('you liked this'), 'data': apart.thumbsup})

		else:
			return JsonResponse({'content':_('this is already on your like list'),
				'data': apart.thumbsup})

	else:
		if request.session.get('thumbsup'+pk, False):
			return JsonResponse({'content':_('you have alreadly liked this'), 
				'data': apart.thumbsup})
		else:
			apart.thumbsup += 1
			apart.save()
			request.session['thumbsup'+pk] = True
			return JsonResponse({'content':_('thanks for liking this'), 
				'data': apart.thumbsup})


def thumbsdown(request, pk):
	apart = Apart.objects.get(pk=pk)

	if request.user.is_authenticated:
		if request.user not in apart.dislikedby.all():
			apart.dislikedby.add(request.user)
			apart.thumbsdown += 1
			apart.save()
			return JsonResponse({'content':_('you disliked this'), 'data': apart.thumbsdown})

		else:
			return JsonResponse({'content':_('this is already on your dislike list'), 
				'data': apart.thumbsdown})

	else:
		if request.session.get('thumbsdown'+pk, False):
			return JsonResponse({'content':_('you have alreadly disliked this'), 
				'data': apart.thumbsdown})
		else:
			apart.thumbsdown += 1
			apart.save()
			request.session['thumbsdown'+pk] = True
			return JsonResponse({'content':_('you disliked this'), 
				'data': apart.thumbsdown})

def shareaparts(request, pk):
	apart = Apart.objects.get(pk=pk)

	if request.user.is_authenticated:
		apart.sharedby.add(request.user)

	apart.sharenumbers += 1
	apart.save()
	return JsonResponse({'content':_('Thanks for sharing this'), 'data': apart.sharenumbers})

	# else:
	# 	if 'thumbsup' in request.session:
	# 		return JsonResponse({'content':'you have already clicked this', 
	# 			'data': apart.thumbsup})
	# 	else:
	# 		apart.thumbsup += 1
	# 		request.session['thumbsup'] = True

	# 		return JsonResponse({'content':'you liked this', 
	# 				'data': apart.thumbsup})






