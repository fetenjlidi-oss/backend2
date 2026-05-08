from rest_framework import serializers

from .models import Rappel


class RappelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rappel
        fields = (
            "id",
            "heure",
            "heurePrevue",
            "estConfirme",
            "delaiSnooze",  
        )
        read_only_fields = ("id",)