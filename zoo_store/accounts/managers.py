from accounts.errors import EmptyEmailError
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        return self._create_user(email, password, **extra_field)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password=None, **extra_field):
        if not email:
            raise EmptyEmailError
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self.db)
        return user

