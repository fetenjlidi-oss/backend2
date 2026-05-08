from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__" 
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):
        patient = Patient.objects.create_user(
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name',''),
            age=validated_data.get('age',0),
            weight=validated_data.get('weight',0.0),
            height=validated_data.get('height',0.0),
            chronic_diseases=validated_data.get('chronic_diseases',''),
        )
        return patient


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Patient
        fields = ("password", "email", "first_name", "last_name", "age", "weight", "height", "chronic_diseases")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.setdefault("password", validated_data.get("email"))
        user = Patient(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PatientSearchSerializer(serializers.ModelSerializer):
    """Serializer for patient search with complete treatment and medication details"""
    from traitement.serializers import TraitementDetailSerializer
    
    traitement_set = TraitementDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "age",
            "weight",
            "height",
            "chronic_diseases",
            "traitement_set",
        )
        read_only_fields = ("id",)

