from .models import Apart, University
from .serializers import ApartSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics


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

	def get_queryset(self):
		if 'university' in self.request.GET:
			print('university inside')
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
			gender__in=genders)
		else:
			apartlist = Apart.objects.all()

		return apartlist

class visitedApart(generics.ListAPIView):
	serializer_class = ApartSerializer

	def get_queryset(self):
		try:
			visited = self.request.session['visited']
			apartlist = Apart.objects.filter(slug__in=visited)
		except:
			apartlist = []

		return apartlist




class ApartDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Apart.objects.all()
	serializer_class = ApartSerializer
