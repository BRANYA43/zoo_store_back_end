from base.mixins import UUIDMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, UUIDMixin):
    email = models.EmailField(unique=True, max_length=255)
    joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    class Meta:
        ordering = ['-joined']

    def __str__(self):
        return self.email


class Profile(UUIDMixin):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, null=True, default=None)
    last_name = models.CharField(max_length=100, null=True, default=None)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
