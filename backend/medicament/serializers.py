from rest_framework import serializers

from .models import Medicament


class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = (
            "id",
            "name",
            "dosage_ref",
            "description",
            "unity",
            "time",
            "time_takes",
            "quantity_total",
            "quantity_limit",
            "date_start",
            "date_end",
            "image",
        )
        read_only_fields = ("id",)