from .models import Apart
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
	queryset = Apart.objects.all()
	serializer_class = ApartSerializer

class ApartDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Apart.objects.all()
	serializer_class = ApartSerializer
