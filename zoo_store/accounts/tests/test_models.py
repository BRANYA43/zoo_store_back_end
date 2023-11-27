from accounts.models import User
from base.test_cases import ModelTestCase
from django.contrib.auth import get_user_model


def create_test_user(email='rick.sanchez@test.com', password='qwe123!@#', **extra_fields):
    return get_user_model().objects.create_user(email=email, password=password, **extra_fields)


class UserModelTest(ModelTestCase):

    def test_model_has_necessary_fields(self):
        necessary_fields = ['uuid', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'joined',
                            'last_login']
        model_fields = self.get_fields(User, only_names=True)

        self.assertFieldNamesEqual(model_fields, necessary_fields)

    def test_uuid_is_primary_key(self):
        uuid = self.get_field(User, 'uuid')
        self.assertTrue(uuid.primary_key)

    def test_email_is_unique(self):
        email = self.get_field(User, 'email')
        self.assertTrue(email.unique)

    def test_email_is_USERNAME_FIELD(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_is_active_is_true_by_default(self):
        is_active = self.get_field(User, 'is_active')
        self.assertTrue(is_active.default)

    def test_is_staff_is_false_by_default(self):
        is_staff = self.get_field(User, 'is_staff')
        self.assertFalse(is_staff.default)

    def test_is_superuser_is_false_by_default(self):
        is_superuser = self.get_field(User, 'is_superuser')
        self.assertFalse(is_superuser.default)

    def test_get_user_model_returns_correct_model(self):
        user = get_user_model()
        self.assertIs(user, User)

    def test_users_are_sorted_by_joined_in_descending_order(self):
        ordering = self.get_meta_attr(User, 'ordering')
        self.assertIn('-joined', ordering)
