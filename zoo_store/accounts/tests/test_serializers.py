
from accounts.serializers import UserSerializer
from base import SerializerTest


class UserTestSerializer(SerializerTest):

    def test_serializer_contain_necessary_user_fields(self):
        necessary_fields = ['url', 'uuid', 'email', 'last_login', 'joined']
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
