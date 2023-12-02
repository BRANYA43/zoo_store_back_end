from accounts.models import Profile
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['url', 'uuid', 'user', 'first_name', 'last_name']
        read_only_fields = ['uuid', 'user']
        extra_kwargs = {
            'first_name': {'style': {'placeholder': 'Rick'}},
            'last_name': {'style': {'placeholder': 'Sanchez'}},
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'uuid', 'profile', 'email', 'password', 'last_login',
                  'joined']
        read_only_fields = ['uuid', 'profile', 'last_login', 'joined']
        extra_kwargs = {
            'email': {
                'required': False,
                'style': {'placeholder': 'email@example.com'},
            },
            'password': {
                'write_only': True,
                'trim_whitespace': False,
                'required': False,
                'style': {'input_type': 'password'},
            },
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'uuid', 'email', 'password']
        read_only_fields = ['uuid']
        extra_kwargs = {
            'email': {
                'style': {'placeholder': 'email@example.com'},
            },
            'password': {
                'write_only': True,
                'trim_whitespace': False,
                'style': {'input_type': 'password'}
            },
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
