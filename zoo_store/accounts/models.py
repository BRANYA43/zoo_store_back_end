from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid4, unique=True, max_length=20, primary_key=True)
    email = models.EmailField(unique=True, max_length=255)
    joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    class Meta:
        ordering = ['-joined']

    def __str__(self):
        return self.email
