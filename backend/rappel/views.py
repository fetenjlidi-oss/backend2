from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView

from rest_framework.response import Response

from .serializers import RappelSerializer    
from .serializers import RappelSerializer
from .models import Rappel 
from rest_framework import status
class RappelCreateView(APIView):
    def post(self, request):
        serializer = RappelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rappel = serializer.save()
        return Response(RappelSerializer(rappel).data, status=status.HTTP_201_CREATED) 
class RappelListView(APIView):
    def get(self, request):
        rappels = Rappel.objects.all().order_by("-id")
        serializer = RappelSerializer(rappels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class RappelDetailView(APIView):    
    def get(self, request, pk):
        try:
            rappel = Rappel.objects.get(id=pk)
        except Rappel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RappelSerializer(rappel)
        return Response(serializer.data, status=status.HTTP_200_OK)
class RappelUpdateView(APIView):
    def put(self, request, pk):
        try:
            rappel = Rappel.objects.get(id=pk)
        except Rappel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RappelSerializer(rappel, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)  
    def patch(self, request,pk: int):
        rappel = get_object_or_404(Rappel, id=pk)
        serializer = RappelSerializer(rappel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
class RappelDeleteView(APIView):    
    def delete(self, request, pk):
        try:
            rappel = Rappel.objects.get(id=pk)
        except Rappel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        rappel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RappelSnoozeView(APIView):
    def post(self, request, pk):
        try:
            rappel = Rappel.objects.get(id=pk)
        except Rappel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        delai_snooze = request.data.get('delaiSnooze')
        if delai_snooze is not None:
            rappel.delaiSnooze = delai_snooze
            rappel.isSnoozed = True
            rappel.save()
            return Response(RappelSerializer(rappel).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "delaiSnooze is required"}, status=status.HTTP_400_BAD_REQUEST)
    

class RappelConfirmView(APIView):
    def post(self, request, pk):
        try:
            rappel = Rappel.objects.get(id=pk)
        except Rappel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        rappel.estConfirme = True
        rappel.save()
        return Response(RappelSerializer(rappel).data, status=status.HTTP_200_OK)
class RappelCancelSnoozeView(APIView):
    def post(self, request, pk):
        try:
            rappel = Rappel.objects.get(id=pk)
        except Rappel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        rappel.isSnoozed = False
        rappel.delaiSnooze = None
        rappel.save()
        return Response(RappelSerializer(rappel).data, status=status.HTTP_200_OK)
class GetNumbreOfRappelsIsSnoozedView(APIView):
    def get(self, request):
        count = Rappel.objects.filter(isSnoozed=False).count()
        return Response({"count": count}, status=status.HTTP_200_OK)

