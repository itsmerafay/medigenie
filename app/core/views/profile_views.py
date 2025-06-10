from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from core.serializers import UserProfileSerializer
from core.models import UserProfile


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        if profile:
            return profile
        return None

class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        if profile:
            return profile
        return None


class ProfileDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        if profile:
            return profile
        return None
