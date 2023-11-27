from accounts.models import Profile
from accounts.serializers import ProfileSerializer, UserCreateSerializer, UserSerializer
from accounts.tests import create_test_user
from base.test_cases import ModelTestCase, SerializerTestCase
from django.contrib.auth import get_user_model

User = get_user_model()
get_model_fields = ModelTestCase.get_fields


class ProfileSerializerTest(SerializerTestCase):
    def test_serializer_has_necessary_model_fields(self):
        necessary_fields = ['url'] + get_model_fields(Profile, only_names=True)
        serializer_fields = self.get_field_names(ProfileSerializer)

        self.assertFieldNamesEqual(serializer_fields, necessary_fields)

    def test_uuid_is_read_only(self):
        uuid = self.get_field(ProfileSerializer, 'uuid')
        self.assertTrue(uuid.read_only)

    def test_user_is_read_only(self):
        user = self.get_field(ProfileSerializer, 'user')
        self.assertTrue(user.read_only)


class UserCreateSerializerTest(SerializerTestCase):
    def serializer_inherit_UserSerializer(self):
        self.assertTrue(issubclass(UserCreateSerializer, UserSerializer))

    def test_serializer_has_necessary_model_fields(self):
        necessary_fields = ['url', 'uuid', 'email', 'password']
        serializer_fields = self.get_field_names(UserCreateSerializer)

        self.assertFieldNamesEqual(serializer_fields, necessary_fields)

    def test_uuid_is_read_only(self):
        uuid = self.get_field(UserCreateSerializer, 'uuid')
        self.assertTrue(uuid.read_only)

    def test_password_is_write_only(self):
        password = self.get_field(UserCreateSerializer, 'password')
        self.assertTrue(password.write_only)

    def test_create_creates_user_as_in_registration(self):
        data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
        }
        serializer = UserCreateSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))


class UserSerializerTest(SerializerTestCase):
    def test_serializer_has_necessary_model_fields(self):
        necessary_fields = ['url', 'profile'] + get_model_fields(User, only_names=True)
        serializer_fields = self.get_field_names(UserSerializer)

        self.assertFieldNamesEqual(serializer_fields, necessary_fields)

    def test_uuid_is_read_only(self):
        uuid = self.get_field(UserSerializer, 'uuid')
        self.assertTrue(uuid.read_only)

    def test_password_is_write_only(self):
        password = self.get_field(UserSerializer, 'password')
        self.assertTrue(password.write_only)

    def test_password_doesnt_trim_whitespace(self):
        password = self.get_field(UserSerializer, 'password')
        self.assertTrue(password.trim_whitespace)

    def test_last_login_is_read_only(self):
        last_login = self.get_field(UserSerializer, 'last_login')
        self.assertTrue(last_login.read_only)

    def test_joined_is_read_only(self):
        joined = self.get_field(UserSerializer, 'joined')
        self.assertTrue(joined.read_only)

    def test_update_updates_password(self):
        old_password = 'old_password123!@#'
        new_password = 'new_password123!@#'
        user = create_test_user(password=old_password)

        serializer = UserSerializer(user, data={'password': new_password}, partial=True)
        serializer.is_valid()
        serializer.save()

        user.refresh_from_db()

        self.assertFalse(user.check_password(old_password))
        self.assertTrue(user.check_password(new_password))
