from accounts.models import Profile
from accounts.serializers import ProfileSerializer, UserSerializer
from base import ModelTest, SerializerTest


class ProfileTestSerializer(SerializerTest):
    def test_serializer_contain_all_profile_fields(self):
        fields = ModelTest.get_fields(Profile, only_name=True)
        self.assertSequenceEqual(self.get_fields(ProfileSerializer, only_names=True), fields)

    def test_uuid_is_read_only(self):
        uuid = self.get_field(ProfileSerializer, 'uuid')
        self.assertTrue(uuid.read_only)


class UserTestSerializer(SerializerTest):

    def test_serializer_contain_necessary_user_fields(self):
        necessary_fields = ['uuid', 'email', 'last_login', 'joined']
        self.assertSequenceEqual(self.get_fields(UserSerializer, only_names=True), necessary_fields)

    def test_uuid_is_read_only(self):
        uuid = self.get_field(UserSerializer, 'uuid')
        self.assertTrue(uuid.read_only)

    def test_joined_is_read_only(self):
        joined = self.get_field(UserSerializer, 'joined')
        self.assertTrue(joined.read_only)

    def test_last_login_is_read_only(self):
        last_login = self.get_field(UserSerializer, 'last_login')
        self.assertTrue(last_login.read_only)
