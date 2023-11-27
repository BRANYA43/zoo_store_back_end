from accounts.managers import UserManager
from base.mixins import UUIDMixin
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Profile(UUIDMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, null=True, default=None)
    last_name = models.CharField(max_length=50, null=True, default=None)

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return f'<Profile({self.user.email} {self.full_name})>'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'


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
