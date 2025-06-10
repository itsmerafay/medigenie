from dj_rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer 
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from core.models import User

class CustomLoginSerializer(RestAuthLoginSerializer):
    username = None
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise ValidationError("Email and password are required.")

        user = authenticate(email=email, password=password)

        if user is None:
            if not User.objects.filter(email=email).exists():
                raise ValidationError({
                    "email":"Invalid Email"
                    })
            else:
                raise ValidationError({
                    "password":"Invalid password"
                    })

        if not user.is_active:
            raise ValidationError("This account is inactive. Please contact support.")

        attrs["user"] = user
        return attrs
    
    def to_representation(self, instance):
        return {'status': 'ok'}


class VerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verification_code = serializers.CharField(max_length=4 ,required=True)

    def validate(self, attrs):

        email = attrs.get("email").lower()
        verification_code = attrs.get("verification_code")

        try:
            if email and verification_code:
                user = User.objects.get(email=email)

                if not user.is_verification_code_valid():
                    raise serializers.ValidationError({
                        "verification_code":"The verification code has been expired"
                    })
                
                if user.verification_code  != verification_code:
                    raise serializers.ValidationError({
                        "verification_code":"Invalid verification code"
                        })
            else:
                raise serializers.ValidationError({
                    "field_error":"Email And Verification code are required"
                    })
        
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "user":"User with this email address does not exist"
                })

        return attrs

class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.JSONField()
