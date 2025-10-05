import requests
import random
from datetime import timedelta
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from django.db import IntegrityError
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.timezone import now

from rest_framework import serializers

from core.models import UserProfile
from core.adapters.custom_social_auth import user_signal

auth_verify_signal = Signal()

@receiver(user_signal)
def create_profile(sender, **kwargs):
    data = kwargs.get('data', {})
    user = data.get('user')

    name = data.get("name", "")
    picture = data.get("picture", "")

    image = None

    if picture:
        try:
            response = requests.get(picture)

            if response.status_code == 200:
                file_name = urlparse(picture).path.split("/")[-1]
                image = ContentFile(response.content, name=file_name)
        except Exception as e:
            print(f"An error occured while downloading an image {e}")


    try:
        profile, created = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "name": name,
                "image": image
            }
        )


    except IntegrityError as e:
        print(f"IntegrityError while creating/updating profile: {e}")
    except Exception as e:
        print(f"Unexpected error in create_profile signal: {e}")


@receiver(auth_verify_signal)
def handle_login_signal(sender, user, **kwargs):
    verification_code = "1234"
    verification_code_expiry = now() + timedelta(minutes=10)

    user.verification_code = verification_code
    user.verification_code_expiry = verification_code_expiry
    user.save() 

    # send_mail(
    #     subject="Your verification code",
    #     message=f"Here is your verification code {verification_code}. Don't share with anyone else.",
    #     from_email="no-reply@example.com",
    #     recipient_list=[user.email]
    # )

@receiver(reset_password_token_created)
def password_reset_token(sender, instance, reset_password_token, *args, **kwargs):
     email_message = f"Please click on the link and reset your password : http://127.0.0.1:8000/api/password_reset?token={reset_password_token.key} "
    #  send_mail(
    #       subject="Password Reset Request",
    #       message=email_message,
    #       from_email="noreply@example.com",
    #       recipient_list=[reset_password_token.user.email]
    #  )