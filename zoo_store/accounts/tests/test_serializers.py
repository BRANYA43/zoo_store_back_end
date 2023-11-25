from accounts.models import Profile
from accounts.serializers import ProfileSerializer, UserSerializer
from base import ModelTest, SerializerTest
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileTestSerializer(SerializerTest):
    def test_serializer_contain_all_profile_fields(self):
        model_fields = ModelTest.get_fields(Profile, only_name=True)
        serializer_fields = self.get_fields(ProfileSerializer, only_names=True)

        self.assert_field_lists_equal(serializer_fields, model_fields)

    def test_uuid_is_read_only(self):
        uuid = self.get_field(ProfileSerializer, 'uuid')
        self.assertTrue(uuid.read_only)


class UserTestSerializer(SerializerTest):

    def test_serializer_contain_necessary_user_fields(self):
        model_fields = ModelTest.get_fields(User, only_name=True)
        model_fields.remove('password')
        serializer_fields = self.get_fields(UserSerializer, only_names=True)

        self.assert_field_lists_equal(serializer_fields, model_fields)

    def test_uuid_is_read_only(self):
        uuid = self.get_field(UserSerializer, 'uuid')
        self.assertTrue(uuid.read_only)

    def test_joined_is_read_only(self):
        joined = self.get_field(UserSerializer, 'joined')
        self.assertTrue(joined.read_only)

    def test_last_login_is_read_only(self):
        last_login = self.get_field(UserSerializer, 'last_login')
        self.assertTrue(last_login.read_only)
