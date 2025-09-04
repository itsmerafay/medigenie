from rest_framework import serializers 

from django_countries.serializer_fields import CountryField
from core.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    city = serializers.CharField(allow_null=True, required=False)
    role = serializers.CharField(source='user.role', read_only=True)  
    email = serializers.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = (
            "id", "email", "role", "name", "age", "date_of_birth", "image", "gender",
            "city", "chronic_conditions", "current_medications", "known_allergies",
            "family_medical_history", "symptom_pattern", "sleep_quality", "diet_type",
            "lifestyle_type", "occupation", "smoking", "alcohol", 
            )
        read_only = ("user", )

    def create(self, validated_data):
        city_name = validated_data.pop("city", None)
        instance = super().create(validated_data)
        if city_name:
            city = city_name
            instance.city = city
            instance.save()
        return instance


    def update(self, instance, validated_data):
        city_name = validated_data.pop("city", None)
        email = validated_data.get("email", None)

        instance = super().update(instance, validated_data)

        if email:
            instance.user.email = email
            instance.user.save()

        if city_name:
            city = city_name
            instance.city = city
            instance.save()

        return instance
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation["email"] = instance.user.email
    #     return representation