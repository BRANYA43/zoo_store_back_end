from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['url', 'uuid', 'email', 'last_login', 'joined']
