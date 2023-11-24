from django.contrib.auth.models import PermissionsMixin
from django.test import TestCase

from ..models import User


class UserModelTest(TestCase):

    @staticmethod
    def get_field(model, field_name: str):
        return model._meta.get_field(field_name)

    @staticmethod
    def get_meta_attr(model, attr_name: str):
        return getattr(model._meta, attr_name)

    def test_user_inherit_necessary_mixins(self):
        self.assertTrue(issubclass(User, PermissionsMixin))

    def test_user_has_necessary_fields(self):
        necessary_fields = ['uuid', 'email', 'password', 'last_login', 'joined']
        fields = [field.name for field in User._meta.fields]

        for necessary_field in necessary_fields:
            self.assertIn(necessary_field, fields)

    def test_user_dont_have_username_from_django(self):
        fields = [field.name for field in User._meta.fields]

        self.assertNotIn('username', fields)

    def test_uuid_is_primary_key_for_user(self):
        uuid = self.get_field(User, 'uuid')
        self.assertTrue(uuid.primary_key)

    def test_email_is_unique_for_user(self):
        email = self.get_field(User, 'email')
        self.assertTrue(email.unique)

    def test_email_is_identifier_for_user(self):
        """
        USERNAME_FIELD is identifier for AbstractBaseUser in django
        """
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_email_is_email_field_for_user(self):
        self.assertEqual(User.EMAIL_FIELD, 'email')

    def test_user_is_sorted_by_decreasing_joined_date(self):
        self.assertIn('-joined', self.get_meta_attr(User, 'ordering'))
