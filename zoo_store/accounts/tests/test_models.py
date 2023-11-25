from base import ModelTest
from django.contrib.auth import get_user_model

from ..models import Profile, User


def create_test_user(email='user@example.com', **kwargs) -> User:
    return get_user_model().objects.create_user(email=email, **kwargs)


class ProfileModelTest(ModelTest):
    def test_profile_has_necessary_fields(self):
        necessary_fields = ['uuid', 'first_name', 'last_name', 'user']
        fields = self.get_fields(Profile, only_name=True)

        for necessary_field in necessary_fields:
            self.assertIn(necessary_field, fields)

    def test_uuid_is_primary_key_for_profile(self):
        uuid = self.get_field(User, 'uuid')
        self.assertTrue(uuid.primary_key)

    def test_profile_has_one_to_one_relation_with_user(self):
        user = self.get_field(Profile, 'user')
        self.assertTrue(user.one_to_one)
        self.assertIs(user.related_model, User)

    def test_profile_is_created_after_created_user(self):
        User.objects.create(email='user@example.com')
        self.assertEqual(Profile.objects.count(), 1)

    def test_profile_gets_full_name(self):
        profile = Profile(first_name='Rick', last_name='Sanchez')
        self.assertEqual(profile.full_name, 'Rick Sanchez')


class UserModelTest(ModelTest):

    def test_user_has_necessary_fields(self):
        necessary_fields = ['uuid', 'email', 'password', 'last_login', 'joined']
        fields = self.get_fields(User, only_name=True)

        for necessary_field in necessary_fields:
            self.assertIn(necessary_field, fields)

    def test_user_dont_have_username_from_django(self):
        fields = self.get_fields(User, only_name=True)

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

    def test_get_user_model_returns_user_of_accounts_app(self):
        self.assertIs(get_user_model(), User)
