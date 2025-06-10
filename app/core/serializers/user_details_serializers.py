from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer as SocialAuthUserDetailSerializer 
from core.serializers import UserProfileSerializer
from core.models import UserProfile

class UserDetailsSerializer(SocialAuthUserDetailSerializer):
    email = serializers.EmailField() 
    profile = UserProfileSerializer(source='userprofile', read_only=True)

    class Meta(SocialAuthUserDetailSerializer.Meta):
        fields = SocialAuthUserDetailSerializer.Meta.fields + ('role', 'profile')
