from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response    
from .serializers import MedicamentSerializer
from .models import Medicament  
from rest_framework import status
class MedicamentCreateView(APIView):
    def post(self, request):
        serializer = MedicamentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        medicament = serializer.save()
        return Response(MedicamentSerializer(medicament).data, status=status.HTTP_201_CREATED) 
class MedicamentListView(APIView):
    def get(self, request):
        medicaments = Medicament.objects.all().order_by("-id")
        serializer = MedicamentSerializer(medicaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
class MedicamentDetailView(APIView):    
    def get(self, request, pk):
        try:
            medicament = Medicament.objects.get(pk=pk)
        except Medicament.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MedicamentSerializer(medicament)
        return Response(serializer.data, status=status.HTTP_200_OK)  
class MedicamentUpdateView(APIView):
    def put(self, request, pk):
        try:
            medicament = Medicament.objects.get(pk=pk)
        except Medicament.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MedicamentSerializer(medicament, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)  
    def patch(self, request, id: int):
        patient = get_object_or_404(Patient, id=id)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MedicamentDeleteView(APIView):
    def delete(self, request, pk):
        try:
            medicament = Medicament.objects.get(pk=pk)
        except Medicament.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        medicament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


