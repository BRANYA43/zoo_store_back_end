from accounts.managers import UserManager
from base.mixins import UUIDMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class User(AbstractBaseUser, PermissionsMixin, UUIDMixin):
    email = models.EmailField(max_length=255, unique=True)
    joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        ordering = ['-joined']

    def __str__(self):
        return self.email

    def __repr__(self):
        return f'<User({self.email})>'
