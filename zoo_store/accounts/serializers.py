from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Profile
        fields = ['uuid', 'user', 'first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['uuid', 'email', 'last_login', 'joined']
