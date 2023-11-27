from accounts.models import Profile
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']
        extra_kwargs = {
            'key': {
                'label': 'token',
                'read_only': True,
            },
        }


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['url', 'uuid', 'user', 'first_name', 'last_name']
        extra_kwargs = {
            'uuid': {'read_only': True},
            'user': {'read_only': True},
            'first_name': {'style': {'placeholder': 'Rick'}},
            'last_name': {'style': {'placeholder': 'Sanchez'}},
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'uuid', 'profile', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login',
                  'joined']
        extra_kwargs = {
            'uuid': {'read_only': True},
            'email': {'style': {'placeholder': 'email@example.com'}},
            'password': {
                'write_only': True,
                'trim_whitespace': True,
                'style': {'input_type': 'password'}
            },
            'last_login': {'read_only': True},
            'joined': {'read_only': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserCreateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['url', 'uuid', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
