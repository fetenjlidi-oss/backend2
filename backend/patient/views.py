from urllib.parse import urljoin

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Q
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Patient
from .serializers import PatientSerializer, RegisterSerializer, PatientSearchSerializer

from rest_framework import serializers
from django.contrib.auth import authenticate

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter 
from allauth.socialaccount.providers.oauth2.client import OAuth2Client 
from dj_rest_auth.registration.views import AllowAny, SocialLoginView 
from django.conf import settings 

from rest_framework import status
from django.utils import timezone
from django.db.models import Count, Q
from datetime import date

from patient.models import Patient
from traitement.models import Traitement
class PatientCreateView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientListView(APIView):
    def get(self, request):
        patients = Patient.objects.all().order_by("-id")
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientDetailView(APIView):
    def get(self, request, id: int):
        patient = get_object_or_404(Patient, id=id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientUpdateView(APIView):
    def put(self, request, id: int):
        patient = get_object_or_404(Patient, id=id)
        serializer = PatientSerializer(patient, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id: int):
        patient = get_object_or_404(Patient, id=id)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientDeleteView(APIView):
    def delete(self, request, id: int):
        patient = get_object_or_404(Patient, id=id)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class PatientLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        patient = serializer.validated_data["patient"]

        refresh = RefreshToken.for_user(patient)  # type: ignore

        return Response(
            {
                "patient": PatientSerializer(patient).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class PatientCountView(APIView):
    def get(self, request):
        count = Patient.objects.count()
        return Response({"count": count})
# views.py



class PatientStatisticsView(APIView):

    def get(self, request, patient_id):
        # --- Get Patient ---
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()

        # --- Traitements ---
        traitements = Traitement.objects.filter(paitent_id=patient).select_related('medecament')

        total_traitements        = traitements.count()
        active_traitements       = traitements.filter(dateDebut__lte=today, dateFin__gte=today).count()
        completed_traitements    = traitements.filter(dateFin__lt=today).count()
        upcoming_traitements     = traitements.filter(dateDebut__gt=today).count()

        # --- Medicaments ---
        medicaments_qs = traitements.exclude(medecament=None)
        total_medicaments  = medicaments_qs.count()
        unique_medicaments = medicaments_qs.values('medecament').distinct().count()

        # --- Instruction Repas breakdown ---
        repas_breakdown = (
            traitements.values('instructionRepas')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # --- Frequence breakdown ---
        frequence_breakdown = (
            traitements.values('frequence')
            .annotate(count=Count('id'))
            .order_by('frequence')
        )

        # --- Medicament details ---
        medicaments_detail = []
        for t in medicaments_qs.select_related('medecament'):
            m = t.medecament
            duration_days = None
            if t.dateDebut and t.dateFin:
                duration_days = (t.dateFin - t.dateDebut).days

            # Status
            if t.dateDebut and t.dateFin:
                if t.dateDebut <= today <= t.dateFin:
                    traitement_status = "active"
                elif t.dateFin < today:
                    traitement_status = "completed"
                else:
                    traitement_status = "upcoming"
            else:
                traitement_status = "unknown"

            medicaments_detail.append({
                "traitement_id"     : t.id,
                "status"            : traitement_status,
                "date_debut"        : t.dateDebut,
                "date_fin"          : t.dateFin,
                "frequence_per_day" : t.frequence,
                "instruction_repas" : t.instructionRepas,
                "duration_days"     : duration_days,
                "medicament": {
                    "id"             : m.id,
                    "name"           : m.name,
                    "dosage_ref"     : m.dosage_ref,
                    "description"    : m.description,
                    "unity"          : m.unity,
                    "quantity_total" : m.quantity_total,
                    "quantity_limit" : m.quantity_limit,
                    "date_start"     : m.date_start,
                    "date_end"       : m.date_end,
                    "image"          : m.image,
                }
            })

        # --- Final Response ---
        data = {
            "patient": {
                "id"              : patient.id,
                "email"           : patient.email,
                "first_name"      : patient.first_name,
                "last_name"       : patient.last_name,
                "age"             : patient.age,
                "weight_kg"       : patient.weight,
                "height_cm"       : patient.height,
                "chronic_diseases": patient.chronic_diseases,
            },
            "statistics": {
                "total_traitements"    : total_traitements,
                "active_traitements"   : active_traitements,
                "completed_traitements": completed_traitements,
                "upcoming_traitements" : upcoming_traitements,
                "total_medicaments"    : total_medicaments,
                "unique_medicaments"   : unique_medicaments,
                "repas_breakdown"      : list(repas_breakdown),
                "frequence_breakdown"  : list(frequence_breakdown),
            },
            "traitements": medicaments_detail,
        }

        return Response(data, status=status.HTTP_200_OK)
from django.db.models import Q, Value
from django.db.models.functions import Concat
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PatientSearchView(APIView):
    """
    Search patients by first name (partial match, case-insensitive)
    """
    # permission_classes = [AllowAny]

    def get(self, request):
        """
        Query parameters:
        - first_name: Search by first_name (required)
        """
        first_name = request.query_params.get('first_name', '').strip()

        # Require first_name param
        if not first_name:
            return Response(
                {"message": "Please provide 'first_name' parameter", "data": []},
                status=status.HTTP_400_BAD_REQUEST
            )

        patients = Patient.objects.filter(
            first_name__icontains=first_name
        ).order_by('first_name', 'last_name')

        if not patients.exists():
            return Response(
                {"message": f"No patients found with first name '{first_name}'", "data": []},
                status=status.HTTP_200_OK
            )

        serializer = PatientSearchSerializer(patients, many=True)
        return Response(
            {"message": f"Found {patients.count()} patient(s)", "data": serializer.data},
            status=status.HTTP_200_OK
        )