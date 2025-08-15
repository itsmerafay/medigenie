from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from dj_rest_auth.views import LoginView as RestAuthLoginView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from core.signals import auth_verify_signal
from core.utility import *
from core.serializers import CustomLoginSerializer, VerificationCodeSerializer, UserDetailsSerializer, TokenResponseSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

@extend_schema(
    request=CustomLoginSerializer,
    responses={
        200: TokenResponseSerializer,
    },
)
class CustomLoginView(RestAuthLoginView):
    serializer_class = CustomLoginSerializer    

    def get_response_data(self, user, token, *args, **kwargs):
        return {'status': 'ok',
                'message':'Please check your email for the verification code.'}
  
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email").lower()
        password = serializer.validated_data.get("password")

        try:
            user = get_object_or_404(User, email=email)
            tokens = CustomJWTToken.for_user(user)
            user_data = UserDetailsSerializer(user).data

            response_data = {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "user": user_data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"detail": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )



@extend_schema(
    request=VerificationCodeSerializer,
    responses={
        200: TokenResponseSerializer,
    },
)
class VerificicationCodeAPIView(generics.GenericAPIView):
    serializer_class = VerificationCodeSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email").lower()
        verification_code = serializer.validated_data.get("verification_code")

        try:
            user = get_object_or_404(User, email=email)
            
            if not user.is_verification_code_valid():
                return Response({
                    "details": "Invalid verification code Or the verification code has been expired"
                }, status=status.HTTP_400_BAD_REQUEST)

            if user.verification_code != verification_code:
                return Response({
                    "detail": "Invalid verification code"
                }, status=status.HTTP_400_BAD_REQUEST)

            tokens = CustomJWTToken.for_user(user)
            user_data = UserDetailsSerializer(user).data

            response_data = {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "user": user_data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"detail": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )




