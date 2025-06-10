from django.contrib.auth import get_user_model
from django.dispatch import Signal

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount


user_signal = Signal("data")
User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        This is called when the user is created for the first time.
        """
        user = super().save_user(request, sociallogin, form)
        role = getattr(request, 'role', None)
        if role:
            user.role = role
            user.save()
        first_name = sociallogin.account.extra_data.get("given_name", "")
        last_name = sociallogin.account.extra_data.get("family_name", "")
        name = f"{first_name} {last_name}".strip()
        picture = sociallogin.account.extra_data.get(
            'picture', '')
        if role:
            user.role = role
        user.save()

        data = {
            "user": user,
            "name": name,
            "picture": picture
        }
        user_signal.send(sender=user.__class__, data=data)
        return user

    def pre_social_login(self, request, sociallogin):
        if 'email' in sociallogin.account.extra_data:
            email = sociallogin.account.extra_data['email']

            try:
                user = User.objects.get(email=email)
                role = getattr(request, 'role', None)
                if role:
                    user.role = role
                    user.save()

                existing_account = SocialAccount.objects.filter(
                    user=user, provider=sociallogin.account.provider)
                if not existing_account.exists():
                    sociallogin.connect(request, user)

                first_name = sociallogin.account.extra_data.get(
                    'given_name', '')
                last_name = sociallogin.account.extra_data.get(
                    'family_name', '')
                name = f"{first_name} {last_name}"
                picture = sociallogin.account.extra_data.get(
                    'picture', '')
                data = {
                    'user': user,
                    'name': name,
                    'picture': picture
                }
                user_signal.send(sender=user.__class__, data=data)
                    

            except User.DoesNotExist:
                pass
