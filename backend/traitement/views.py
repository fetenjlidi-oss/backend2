from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response    
from .serializers import TraitementSerializer
from .models import Traitement  
from rest_framework import status
class TraitementCreateView(APIView):
    def post(self, request):
        serializer = TraitementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        traitement = serializer.save()
        return Response(TraitementSerializer(traitement).data, status=status.HTTP_201_CREATED) 
class TraitementListView(APIView):
    def get(self, request):
        traitements = Traitement.objects.all().order_by("-id")
        serializer = TraitementSerializer(traitements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
class TraitementDetailView(APIView):    
    def get(self, request, pk):
        try:
            traitement = Traitement.objects.get(pk=pk)
        except Traitement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TraitementSerializer(traitement)
        return Response(serializer.data, status=status.HTTP_200_OK)  
class TraitementUpdateView(APIView):
    def put(self, request, pk):
        try:
            traitement = Traitement.objects.get(pk=pk)
        except Traitement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TraitementSerializer(traitement, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)  
    def patch(self, request, id: int):
        patient = get_object_or_404(Patient, id=id)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TraitementDeleteView(APIView):
    def delete(self, request, pk):
        try:
            traitement = Traitement.objects.get(pk=pk)
        except Traitement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        traitement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


# Create your views here.
