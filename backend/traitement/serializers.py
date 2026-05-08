from rest_framework import serializers
from .models import Traitement
from rappel.serializers import RappelSerializer
from medicament.serializers import MedicamentSerializer


class TraitementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traitement
        fields = (
            "id",
            "dateDebut",
            "dateFin",
            "frequence",
            "instructionRepas",
        )
        read_only_fields = ("id",)


class TraitementDetailSerializer(serializers.ModelSerializer):
    """Serializer for Traitement with nested Medicament and Rappel details"""
    medecament = MedicamentSerializer(read_only=True)
    rappels = RappelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Traitement
        fields = (
            "id",
            "dateDebut",
            "dateFin",
            "frequence",
            "instructionRepas",
            "medecament",
            "rappels",
            "paitent_id",
        )
        read_only_fields = ("id", "paitent_id")