from curses import noecho
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now
from django_countries.fields import CountryField


from django.db import models

from core.model_mixins import UUIDBase
from docmind.utilities import pdf_upload_path

from core.model_mixins import UUIDBase

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    class RoleChoices(models.TextChoices):
        ADMIN = "Admin", ("Admin")
        USER = "User", ("User")

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )

    is_acive = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=RoleChoices.choices)
    verification_code = models.CharField(max_length=4, null=True, blank=True)
    verification_code_expiry = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def is_verification_code_valid(self):
        if not self.verification_code_expiry:
            return False
        return self.verification_code_expiry > now()

class UserProfile(UUIDBase):

    class GENDERCHOICES(models.TextChoices):
        MALE = "Male", ("Male")
        FEMALE = "Female", ("Female")
        OTHER = "Other", ("Other")

    class SLEEPQUALITYCHOICES(models.TextChoices):
        GOOD = "Good", ("Good")
        AVERAGE = "Average", ("Average")
        POOR = "Poor", ("Poor")


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    image = models.ImageField(upload_to="image/", null=True, blank=True)

    gender = models.CharField(max_length=50, choices=GENDERCHOICES.choices, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    chronic_conditions = models.TextField(null=True, blank=True)
    current_medications = models.TextField(null=True, blank=True)
    known_allergies = models.TextField(null=True, blank=True)
    family_medical_history = models.TextField(null=True, blank=True)

    symptom_pattern = models.TextField(null=True, blank=True)
    sleep_quality = models.CharField(max_length=255, choices=SLEEPQUALITYCHOICES.choices, null=True, blank=True)
    diet_type = models.TextField(null=True, blank=True)

    lifestyle_type = models.TextField(null=True, blank=True)
    occupation = models.TextField(null=True, blank=True)
    smoking = models.BooleanField(default=False)
    alcohol = models.BooleanField(default=False)


    def clean(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                (today.month - today.day) - (self.date_of_birth.month - self.date_of_birth.day)
            )
            if age < 0:
                raise ValidationError("Age can't be less than 0")
    
    def __str__(self):
        return self.name if self.name else self.user.email



class Session(UUIDBase):

    class SessionType(models.TextChoices):
        RAG  = "RAG", ("RAG")
        RESEARCH = "RESEARCH", ("RESEARCH")
        DERMAI = "DERMAI", ("DERMAI")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="New Rag Session")
    session_type = models.CharField(
        max_length=25, choices=SessionType.choices, default=SessionType.RAG
    )
    file = models.FileField(upload_to=pdf_upload_path, null=True, blank=True)
    index_dir = models.CharField(max_length=1024, blank=True)
    embedding_model = models.CharField(
            max_length=200, default="thenlper/gte-small"
        )

    def __str__(self):
        return f"{self.id} - {self.title if self.title else None}"


class Message(UUIDBase):

    class ROLECHOICES(models.TextChoices):
        USER = "User", ("User")
        ASSISTANT = "Assistant", ("Assistant")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=25, choices=ROLECHOICES.choices, default=ROLECHOICES.USER)
    content = models.TextField()
    image = models.ImageField(upload_to="message/images/", null=True, blank=True)
    audio = models.FileField(upload_to="message/audio/", null=True, blank=True)

    
    def __str__(self):
        return f"{self.role}: {self.content}"   
    
