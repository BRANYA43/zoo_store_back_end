from accounts.models import Profile, User
from base.test_cases import ModelTestCase
from django.contrib.auth import get_user_model


def create_test_user(email='rick.sanchez@test.com', password='qwe123!@#', **extra_fields):
    return get_user_model().objects.create_user(email=email, password=password, **extra_fields)


class ProfileModelTest(ModelTestCase):

    def test_model_has_necessary_fields(self):
        necessary_fields = ['uuid', 'user', 'first_name', 'last_name']
        model_fields = self.get_fields(Profile, only_names=True)
        self.assertFieldNamesEqual(model_fields, necessary_fields)

    def test_uuid_is_primary_key(self):
        uuid = self.get_field(User, 'uuid')
        self.assertTrue(uuid.primary_key)

    def test_first_name_is_null_by_default(self):
        first_name = self.get_field(Profile, 'first_name')
        self.assertTrue(first_name.null)
        self.assertIsNone(first_name.default)

    def test_last_name_is_null_by_default(self):
        last_name = self.get_field(Profile, 'last_name')
        self.assertTrue(last_name.null)
        self.assertIsNone(last_name.default)

    def test_profile_has_one_to_one_relation_with_user(self):
        user = self.get_field(Profile, 'user')
        self.assertTrue(user.one_to_one)
        self.assertIs(user.related_model, User)

    def test_profile_is_deleted_after_deleting_user(self):
        user = create_test_user()

        self.assertEqual(Profile.objects.count(), 1)

        user.delete()

        self.assertEqual(Profile.objects.count(), 0)

    def test_profile_gets_full_name(self):
        data = {'first_name': 'Rick', 'last_name': 'Sanchez'}
        profile = Profile(**data)
        expected_full_name = f"{data['first_name']} {data['last_name']}"

        self.assertEqual(profile.full_name, expected_full_name)

    def test_profile_is_created_after_creating_user(self):
        user = create_test_user()
        self.assertEqual(Profile.objects.count(), 1)

        profile = Profile.objects.first()
        self.assertEqual(profile.user.uuid, user.uuid)


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
