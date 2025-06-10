import re
from django.contrib.auth import get_user_model 
from rest_framework import serializers 
from dj_rest_auth.registration.serializers import RegisterSerializer as RestAuthRegisterSerializer 
from core.signals import user_signal, auth_verify_signal

class RegisterUserSerializer(RestAuthRegisterSerializer):
    username = None

    class Meta :
        model = get_user_model()        
        fields = ('email', 'password1', 'password2')

    def save(self,request, **kwargs):
        user = super().save(request)
        role = self.context.get('role') if hasattr(self, 'context') and isinstance(self.context, dict) else None
        if role:
            user.role = role
            user.save()
        
        data = {"user":user}
        print(data)
        user_signal.send(sender=get_user_model(), data=data)
        auth_verify_signal.send(sender=self.__class__, user=user)
        return user

    
    def validate_email(self, value):
        lower_email = value.lower()
        if get_user_model().objects.filter(email=lower_email).exists():
            raise serializers.ValidationError("User with this email address already exists")
        return lower_email

    def validate(self, attrs):
        email = attrs.get("email")
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if email and password1:
            if password1 != password2:
                raise serializers.ValidationError({
                    "password":"The two passwords does not match"
                })
            email_username = email.split('@')[0]

            email_chars = [char for char in email_username.lower() if char.isalpha()]
            password_chars = [char for char in password1.lower() if char.isalpha()]

            matching_chars = sum(1 for char in email_chars if char in password_chars)

            match_percentage = (matching_chars / len(email_chars)) * 100 if email_chars else 0

            if match_percentage > 80:
                raise serializers.ValidationError(
                    {"password": "The password is too similar to the email address."}
                )

        return super().validate(attrs)