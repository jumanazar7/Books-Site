from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from .managers import CustomUserManager
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    username = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDERS, default=GENDERS[2])
    address = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
